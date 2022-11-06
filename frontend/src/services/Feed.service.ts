import { API } from '@/api';
import { STORAGE } from '@/utils';
import { CommentItemDto } from '@/dto';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';

const invalidateTags = ['FEED'];

export const feedService = createApi({
    reducerPath: 'FeedAPI',
    tagTypes: invalidateTags,
    baseQuery: fetchBaseQuery({
        baseUrl: API.url,
        prepareHeaders: (headers) => {
            const token = STORAGE.getToken();

            if (token) {
                headers.set('authorization', `Bearer ${token}`);
            }

            return headers;
        },
    }),
    endpoints: (build) => ({
        getAllPosts: build.query<CommentItemDto[], { page: number; itemsPerPage?: number; sortDesc: boolean }>({
            query: ({ page, itemsPerPage = 10, sortDesc }) => ({
                url: '/ideas/posts/',
                params: {
                    page,
                    itemsPerPage,
                    sortDesc,
                },
            }),
            providesTags: ['FEED'],
        }),
    }),
});

export const { useGetAllPostsQuery } = feedService;
