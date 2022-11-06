import { API } from '@/api';
import { STORAGE } from '@/utils';
import { CommentItemDto } from '@/dto';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';

const invalidateTags = ['COMMENTS'];

export const commentsService = createApi({
    reducerPath: 'CommentsAPI',
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
        getAllComments: build.query<CommentItemDto[], string>({
            query: (postId) => ({
                url: `/ideas/${postId}/comments/`,
            }),
            providesTags: (result) => invalidateTags,
        }),
        createComment: build.mutation<CommentItemDto, { comment: { text: string; parent: null }; idea_id?: string }>({
            query: ({ comment, idea_id }) => ({
                url: `/ideas/${idea_id}/comments/`,
                method: 'POST',
                body: comment,
            }),
            invalidatesTags: invalidateTags,
        }),
        deleteComment: build.mutation<CommentItemDto[], number>({
            query: (commentId) => ({
                url: `/comments/${commentId}`,
                method: 'DELETE',
            }),
        }),
    }),
});

export const { useGetAllCommentsQuery, useDeleteCommentMutation, useCreateCommentMutation } = commentsService;
