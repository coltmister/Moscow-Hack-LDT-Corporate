import { useEffect } from 'react';
import { FetchBaseQueryError } from '@reduxjs/toolkit/query';
import { SerializedError } from '@reduxjs/toolkit';

import { STORAGE } from '@/utils';

export const useErrorHandling = (error: FetchBaseQueryError | SerializedError | undefined) => {
    useEffect(() => {
        if (error && 'status' in error) {
            switch (error.status) {
                case 468:
                    return STORAGE.clear();
            }
        }
    }, [error]);
};
