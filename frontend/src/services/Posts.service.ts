import { API } from '@/api';
import { CreatePostDTO, PostDTO, PostQueryParams } from '@/dto';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';
import { prepareHeaders } from '@/utils';

const invalidateTags = ['POST'];

export const postsService = createApi({
    reducerPath: 'PostsAPI',
    tagTypes: invalidateTags,
    baseQuery: fetchBaseQuery({ baseUrl: API.url, prepareHeaders: prepareHeaders }),
    endpoints: (build) => ({
        getAllPosts: build.query<PostDTO, PostQueryParams>({
            query: ({ limit = 5, page = 1, search = '', desc = true }) => ({
                url: `/ideas/posts/?page=${page}&sortBy=id&sortDesc=${desc}&itemsPerPage=${limit}&search=${search}`,
            }),
            providesTags: (result) => invalidateTags,
        }),
        getPostsById: build.query({
            query: ({ idea_id, page = 1, desc = true, items = 10, search = '' }) => ({
                url: `/ideas/${idea_id}/posts/?page=${page}&sortBy=id&sortDesc=${desc}&itemsPerPage=${items}&search=${search}`,
            }),
        }),
        createPost: build.mutation<CreatePostDTO, { idea_id: string; post: CreatePostDTO }>({
            query: ({ idea_id, post }) => ({
                url: `/ideas/${idea_id}/posts/`,
                method: 'POST',
                body: post,
            }),
        }),
        updatePost: build.mutation<CreatePostDTO, { idea_id: string; post_id: string; post: CreatePostDTO }>({
            query: ({ idea_id, post_id, post }) => ({
                url: `/ideas/${idea_id}/posts/${post_id}/`,
                method: 'PUT',
                body: post,
            }),
        }),
        getPost: build.query({
            query: ({ idea_id, post_id }) => ({
                url: `/ideas/${idea_id}/posts/${post_id}`,
            }),
        }),
    }),
});

export const { useGetAllPostsQuery, useCreatePostMutation, useUpdatePostMutation, useGetPostsByIdQuery, useGetPostQuery } = postsService;
