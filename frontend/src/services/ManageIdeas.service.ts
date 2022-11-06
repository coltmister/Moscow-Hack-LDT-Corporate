import { API } from '@/api';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';
import { CreateIdeaDto, IdeaDTO, IdeaModel } from '@/dto';
import { prepareHeaders } from '@/utils';

const invalidateTags = ['IDEA'];

interface A {
    data: {
        id: string;
    };
}

export const ideasService = createApi({
    reducerPath: 'IdeasAPI',
    tagTypes: invalidateTags,
    baseQuery: fetchBaseQuery({ baseUrl: API.url, prepareHeaders: prepareHeaders }),
    endpoints: (build) => ({
        createIdea: build.mutation<{ id: string }, CreateIdeaDto>({
            query: (idea) => ({
                url: '/ideas/',
                method: 'POST',
                body: idea,
            }),
            invalidatesTags: ['IDEAS'],
        }),
        updateIdea: build.mutation<CreateIdeaDto, IdeaModel | CreateIdeaDto>({
            query: (idea) => ({
                url: 'id' in idea ? `/ideas/${idea.id}/` : '/ideas/',
                body: idea,
                method: 'PUT',
            }),
            invalidatesTags: ['IDEAS'],
        }),
        deleteIdea: build.mutation<void, string>({
            query: (id) => ({
                url: `/ideas/${id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['IDEAS'],
        }),
        getAllIdeas: build.query<
            IdeaDTO,
            { sortDesc: boolean; limit: number; page: number; feed_param: 'new' | 'popular' | 'my_tags' | 'people_choice' }
        >({
            query: ({ sortDesc, limit, page, feed_param }) => ({
                url: `/ideas/feed/?feed_param=people_choice&sortDesc=${sortDesc}&itemsPerPage=${limit}&page=${page}&feed_param=${feed_param}`,
            }),
        }),
        getIdeaById: build.query({
            query: (ideaId) => ({
                url: `/ideas/${ideaId}/`,
            }),
            providesTags: ['IDEAS'],
        }),
        getIdeaSettingsById: build.query({
            query: (ideaId) => ({
                url: `/ideas/${ideaId}/settings/`,
            }),
            providesTags: ['IDEAS'],
        }),
        updateIdeaSettingsById: build.mutation({
            query: ({ id, body }) => ({
                url: `/ideas/${id}/settings/`,
                body,
                method: 'PUT',
            }),
            invalidatesTags: ['IDEAS'],
        }),
        likePost: build.mutation({
            query: ({ ideaId, postId, body }) => ({
                url: `/ideas/${ideaId}/posts/${postId}/likes/`,
                body,
                method: 'POST',
            }),
            invalidatesTags: ['IDEAS'],
        }),
        likeIdea: build.mutation({
            query: ({ ideaId, body }) => ({
                url: `/ideas/${ideaId}/likes/`,
                body,
                method: 'POST',
            }),
            invalidatesTags: ['IDEAS'],
        }),
        updateInfo: build.mutation({
            query: ({ ideaId, body }) => ({
                url: `/ideas/${ideaId}/information/`,
                body,
                method: 'PUT',
            }),
            invalidatesTags: ['IDEAS'],
        }),
    }),
});

export const {
    useCreateIdeaMutation,
    useGetAllIdeasQuery,
    useGetIdeaByIdQuery,
    useUpdateIdeaMutation,
    useDeleteIdeaMutation,
    useGetIdeaSettingsByIdQuery,
    useUpdateIdeaSettingsByIdMutation,
    useLikePostMutation,
    useLikeIdeaMutation,
    useUpdateInfoMutation,
} = ideasService;
