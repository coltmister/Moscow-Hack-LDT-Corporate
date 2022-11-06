import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';
import { API } from '@/api';
import { prepareHeaders } from '@/utils';
import { TeamVacancy, UserVacancy, VacanciesQueryParams } from '../types/dto/Teams';

const invalidateTags = ['IDEAS', 'USERS'];

export const adminService = createApi({
    reducerPath: 'AdminApi',
    tagTypes: invalidateTags,
    baseQuery: fetchBaseQuery({ baseUrl: API.url, prepareHeaders: prepareHeaders }),
    endpoints: (build) => ({
        getAllUsers: build.query({
            query: ({ page, itemsPerPage, search }) => ({
                url: `/users`,
                method: 'GET',
                params: {
                    page,
                    itemsPerPage,
                    search,
                },
            }),
            providesTags: ['USERS'],
        }),
        getAllIdeas: build.query({
            query: ({ page = 1, itemsPerPage = 10, search }) => ({
                url: `/ideas/`,
                params: {
                    page,
                    itemsPerPage,
                    search,
                },
            }),
            providesTags: ['IDEAS'],
        }),
        getAllIdeaCategories: build.query({
            query: () => ({
                url: `/ideas/category`,
            }),
            providesTags: ['CATEGORIES'],
        }),
        getIdeaSuggestedCategories: build.query({
            query: (ideaId) => ({
                url: `/ideas/${ideaId}/category`,
            }),
            providesTags: ['CATEGORIES'],
        }),
        updateIdeaCategories: build.mutation({
            query: ({ ideaId, categories }) => ({
                url: `/ideas/${ideaId}/category/`,
                method: 'PUT',
                body: { categories },
            }),
            invalidatesTags: ['IDEAS'],
        }),
        updateIdeaStatus: build.mutation({
            query: ({ ideaId, status }) => ({
                url: `/ideas/${ideaId}/status/`,
                method: 'PUT',
                body: { status, comment: 'Модерация пройдена' },
            }),
            invalidatesTags: ['IDEAS'],
        }),
        updateUserVerification: build.mutation({
            query: ({ userId, is_verified }) => ({
                url: `/users/${userId}/verify`,
                method: 'PUT',
                body: { is_verified },
            }),
            invalidatesTags: ['USERS'],
        }),
        updateUserAdmin: build.mutation({
            query: ({ userId, is_admin }) => ({
                url: `/users/${userId}/admin`,
                method: 'PUT',
                body: { is_admin },
            }),
            invalidatesTags: ['USERS'],
        }),
        updateUserActivity: build.mutation({
            query: ({ userId, enabled }) => ({
                url: `iam/users/${userId}/activity-status/`,
                method: 'PUT',
                body: { enabled },
            }),
            invalidatesTags: ['USERS'],
        }),
    }),
});

export const {
    useGetAllIdeaCategoriesQuery,
    useGetAllIdeasQuery,
    useGetAllUsersQuery,
    useGetIdeaSuggestedCategoriesQuery,
    useUpdateIdeaCategoriesMutation,
    useUpdateIdeaStatusMutation,
    useUpdateUserActivityMutation,
    useUpdateUserAdminMutation,
    useUpdateUserVerificationMutation,
} = adminService;
