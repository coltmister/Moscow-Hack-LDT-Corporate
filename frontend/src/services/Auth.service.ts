import { API } from '@/api';
import { STORAGE } from '@/utils';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';
import { fetchBaseQueryWithReauth } from '../utils/fetchBaseQueryWithReauth';

const invalidateTags = ['AUTH'];

export const authService = createApi({
    reducerPath: 'AuthAPI',
    tagTypes: invalidateTags,
    baseQuery: fetchBaseQueryWithReauth,
    endpoints: (build) => ({
        getNewTokenByRefresh: build.mutation<string, any>({
            query: () => ({
                url: '/api/v1/iam/auth/refresh-token/',
                method: 'POST',
                body: {
                    refresh_token: localStorage.getItem('refresh_token'),
                },
            }),
        }),
        getAuthenticationRoute: build.query<string, any>({
            query: (redirect_uri) => {
                const details = {
                    client_id: 'corp',
                    response_type: 'code',
                    scope: 'openid profile',
                    redirect_uri,
                };
                return {
                    url: 'auth/realms/dpir/protocol/openid-connect/auth',
                    mode: 'no-cors',
                    params: details,
                    method: 'GET',
                };
            },
        }),
    }),
});

export const { useGetAuthenticationRouteQuery } = authService;
