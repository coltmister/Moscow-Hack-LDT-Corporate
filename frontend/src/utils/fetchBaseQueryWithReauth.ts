import { fetchBaseQuery } from '@reduxjs/toolkit/query';
import type { BaseQueryFn, FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query';
import { Mutex } from 'async-mutex';
import { STORAGE } from './StorageAdapter';
import { API } from '@/api';

// create a new mutex
const mutex = new Mutex();
const baseQuery = fetchBaseQuery({
    baseUrl: API.auth,
    prepareHeaders: (headers) => {
        const token = STORAGE.getToken();

        if (token) {
            headers.set('Authorization', `Bearer ${token}`);
        }

        return headers;
    },
});
const logout = () => {
    window.localStorage.removeItem('token');
    window.localStorage.removeItem('refresh_token');
    window.location.href = '/';
};
export const fetchBaseQueryWithReauth: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (args, api, extraOptions) => {
    // wait until the mutex is available without locking it
    await mutex.waitForUnlock();
    let result = await baseQuery(args, api, extraOptions);
    if (result.error && result.error.status === 468) {
        // checking whether the mutex is locked
        if (!mutex.isLocked()) {
            const release = await mutex.acquire();
            try {
                const refreshResult = await baseQuery('/refreshToken', api, extraOptions);
                if (refreshResult.data) {
                    STORAGE.setToken(refreshResult.data.access_token);
                    window.localStorage.setItem('refresh_token', refreshResult.data.refresh_token);
                    // retry the initial query
                    result = await baseQuery(args, api, extraOptions);
                } else {
                    logout();
                }
            } finally {
                // release must be called once the mutex should be released again.
                release();
            }
        } else {
            // wait until the mutex is available without locking it
            await mutex.waitForUnlock();
            result = await baseQuery(args, api, extraOptions);
        }
    }
    if (result.error && result.error.status === 401) {
        logout();
    }
    return result;
};
