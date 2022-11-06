import { API } from '@/api';
import { STORAGE } from '@/utils';
import { Devices, UserFormResponseDTO, UserIdea, UserProfileResponseDTO, UserSettingsDto } from '@/dto';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';

const invalidateTags = ['USER', 'FORM', 'ME', 'SECURITY', 'IDEAS'];

export const userService = createApi({
    reducerPath: 'UserApi',
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
        getMyProfile: build.query<UserProfileResponseDTO, void | null>({
            query: () => {
                return {
                    url: '/users/me/profile',
                    method: 'GET',
                };
            },
            providesTags: invalidateTags,
        }),
        getUserProfile: build.query<UserProfileResponseDTO, string | null>({
            query: (id) => {
                return {
                    url: `/users/${id}/profile`,
                    method: 'GET',
                };
            },
            providesTags: ['USER'],
        }),
        updateUserProfile: build.mutation<
            UserProfileResponseDTO,
            {
                id: string;
                body: UserProfileResponseDTO;
            }
        >({
            query: ({ id, body }) => {
                return {
                    url: id === 'me' ? '/users/me/profile' : `/users/${id}/profile`,
                    method: 'PUT',
                    body,
                };
            },
            invalidatesTags: ['USER'],
        }),
        updateUserAvatar: build.mutation<
            any,
            {
                id: string;
                formData: any;
            }
        >({
            query: ({ id, formData }) => {
                return {
                    url: id === 'me' ? '/users/me/avatar' : `/users/${id}/avatar`,
                    method: 'PUT',
                    body: formData,
                };
            },
            invalidatesTags: ['USER'],
        }),
        getUserForm: build.query<UserFormResponseDTO, string>({
            query: (id) => {
                return {
                    url: `/users/${id}/add-info`,
                    method: 'GET',
                };
            },
            providesTags: ['FORM'],
        }),
        getMyForm: build.query<UserFormResponseDTO, null>({
            query: () => {
                return {
                    url: '/users/add-info',
                    method: 'GET',
                };
            },
            providesTags: ['FORM'],
        }),
        updateUserForm: build.mutation<UserFormResponseDTO, { id: string; body: any }>({
            query: ({ id, body }) => {
                return {
                    url: id === 'me' ? '/users/add-info' : `/users/${id}/add-info`,
                    method: 'PUT',
                    body,
                };
            },
            invalidatesTags: ['FORM'],
        }),
        getUserSettings: build.query<UserSettingsDto, string | null>({
            query: (id) => {
                return {
                    url: `users/${id}/profile-settings`,
                    method: 'GET',
                };
            },
        }),
        getMyUserSettings: build.query<UserSettingsDto, string | null>({
            query: (id) => {
                return {
                    url: `users/me/profile-settings`,
                    method: 'GET',
                };
            },
        }),
        updateMySettings: build.mutation<UserSettingsDto, any>({
            query: ({ body }) => {
                return {
                    url: 'users/me/profile-settings',
                    body,
                    method: 'PUT',
                };
            },
        }),
        updateUserSettings: build.mutation<UserSettingsDto, any>({
            query: ({ id, body }) => {
                return {
                    url: `users/${id}/profile-settings`,
                    body,
                    method: 'PUT',
                };
            },
        }),
        //SECURITY
        getMySecuritySettings: build.query<Devices[], string | null>({
            query: (id) => {
                return {
                    url: `iam/users/devices`,
                    method: 'GET',
                };
            },
            providesTags: ['SECURITY'],
        }),
        getUserSecuritySettings: build.query<Devices[], string | null>({
            query: (id) => {
                return {
                    url: `iam/users/${id}/devices`,
                    method: 'GET',
                };
            },
            providesTags: ['SECURITY'],
        }),
        deleteUserSessions: build.mutation<string, any>({
            query: ({ id }) => {
                return {
                    url: `iam/users/${id}/logout-user/`,
                    method: 'DELETE',
                };
            },
            invalidatesTags: ['SECURITY'],
        }),
        deleteAllMySessionExceptCurrent: build.mutation<UserSettingsDto, any>({
            query: () => {
                return {
                    url: 'iam/users/logout-user',
                    method: 'DELETE',
                };
            },
            invalidatesTags: ['SECURITY'],
        }),
        //USER-IDEAS
        getMyIdeas: build.query<UserIdea[], string | null>({
            query: (id) => {
                return {
                    url: `users/ideas`,
                    method: 'GET',
                };
            },
            providesTags: ['IDEAS'],
        }),
        getUserIdeas: build.query<UserIdea[], string | null>({
            query: (id) => {
                return {
                    url: `users/${id}/ideas`,
                    method: 'GET',
                };
            },
            providesTags: ['IDEAS'],
        }),
        //USER-TEAMS
        getMyTeams: build.query<{ id: string; name: string }[], boolean | null>({
            query: (boolean) => {
                return {
                    url: `users/me/teams`,
                    method: 'GET',
                    params: { is_team_leader: boolean },
                };
            },
            providesTags: ['IDEAS'],
        }),
    }),
});

export const {
    useGetUserProfileQuery,
    useGetUserSettingsQuery,
    useUpdateUserSettingsMutation,
    useGetUserFormQuery,
    useUpdateUserFormMutation,
    useUpdateUserProfileMutation,
    useUpdateUserAvatarMutation,
    useGetMyProfileQuery,
    useGetMyUserSettingsQuery,
    useUpdateMySettingsMutation,
    useGetMySecuritySettingsQuery,
    useGetUserSecuritySettingsQuery,
    useDeleteUserSessionsMutation,
    useDeleteAllMySessionExceptCurrentMutation,
    useGetMyFormQuery,
    useGetMyIdeasQuery,
    useGetUserIdeasQuery,
    useGetMyTeamsQuery,
} = userService;
