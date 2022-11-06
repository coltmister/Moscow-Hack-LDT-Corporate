import { STORAGE } from './StorageAdapter';

export const prepareHeaders = (headers: Headers) => {
    const token = STORAGE.getToken();

    if (token) {
        headers.set('authorization', `Bearer ${token}`);
    }

    return headers;
};
