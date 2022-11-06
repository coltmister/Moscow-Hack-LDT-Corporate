import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';
import { API } from '@/api';
import { prepareHeaders } from '@/utils';
import { TeamVacancy, UserVacancy, VacanciesQueryParams } from '../types/dto/Teams';

const invalidateTags = ['TEAMS', 'TEAM_VACANCIES', 'USER_PROFIELS', 'USER_INVITATIONS', 'VACANCIES'];

export const teamsService = createApi({
    reducerPath: 'TeamsAPI',
    tagTypes: invalidateTags,
    baseQuery: fetchBaseQuery({ baseUrl: API.url, prepareHeaders: prepareHeaders }),
    endpoints: (build) => ({
        createTeam: build.mutation({
            query: (team) => ({
                url: `/teams/`,
                method: 'POST',
                body: team,
            }),
            invalidatesTags: ['IDEAS'],
        }),
        getVacancies: build.query<
            { payload: UserVacancy[] | TeamVacancy[]; total_pages: number; has_next_page: boolean; total_count: number },
            VacanciesQueryParams
        >({
            query: ({ page = 1, itemsPerPage = 10, mode, team }) => ({
                url: `/teams/${mode === 'people' ? team + '/' : ''}${mode === 'ideas' ? 'team-vacancy' : 'user-vacancy'}`,
                params: {
                    page,
                    itemsPerPage,
                },
            }),
            providesTags: ['VACANCIES'],
        }),
        getTeamVacancies: build.query<
            { payload: UserVacancy[] | TeamVacancy[]; total_pages: number; has_next_page: boolean; total_count: number },
            VacanciesQueryParams
        >({
            query: ({ page = 1, itemsPerPage = 10, mode, team }) => ({
                url: `/teams/team-vacancy`,
                params: {
                    page,
                    itemsPerPage,
                },
            }),
            providesTags: ['TEAM_VACANCIES'],
        }),
        getUserProfiles: build.query<
            { payload: UserVacancy[] | TeamVacancy[]; total_pages: number; has_next_page: boolean; total_count: number },
            VacanciesQueryParams
        >({
            query: ({ page = 1, itemsPerPage = 10, mode, team }) => ({
                url: `/teams/${team + '/'}user-vacancy`,
                params: {
                    page,
                    itemsPerPage,
                },
            }),
            providesTags: ['USER_PROFILES'],
        }),
        sendInvitation: build.mutation({
            query: ({ userId, role, cover_letter, teamId }) => ({
                url: `/teams/${teamId + '/'}outgoing-request`,
                body: {
                    user: userId,
                    role,
                    cover_letter,
                },
                method: 'POST',
            }),
            invalidatesTags: ['USER_PROFILES'],
        }),
        sendJoinRequestInvitation: build.mutation({
            query: ({ role, cover_letter, teamId }) => ({
                url: `/teams/outgoing-request`,
                body: {
                    team: teamId,
                    role,
                    cover_letter,
                },
                method: 'POST',
            }),
            invalidatesTags: ['TEAM_VACANCIES'],
        }),
        getUserIncomingRequests: build.query<any, void>({
            query: () => ({
                url: `teams/incoming-request?request_status=0`,
            }),
            providesTags: ['USER_INVITATIONS'],
        }),
        sendUserRequestApproval: build.mutation({
            query: ({ decision, requestId }) => ({
                url: `/teams/incoming-request/${requestId}`,
                body: {
                    decision,
                },
                method: 'PUT',
            }),
            invalidatesTags: ['USER_INVITATIONS'],
        }),
        getIncomingRequests: build.query<any[], string>({
            query: (team_id) => ({
                url: `/teams/${team_id}/incoming-request?request_status=0`,
            }),
        }),
        acceptIncomingRequest: build.mutation<void, { [K: string]: any; decision: boolean }>({
            query: ({ team_id, request_id, decision }) => ({
                url: `/teams/${team_id}/incoming-request/${request_id}`,
                method: 'PUT',
                body: { decision },
            }),
        }),
        getTeamChat: build.query({
            query: ({ team_id }) => ({
                url: `chats/teams/${team_id}/vk-chat`,
                method: 'GET',
            }),
        }),
    }),
});

export const {
    useGetVacanciesQuery,
    useCreateTeamMutation,
    useGetTeamVacanciesQuery,
    useGetUserProfilesQuery,
    useSendInvitationMutation,
    useSendJoinRequestInvitationMutation,
    useGetUserIncomingRequestsQuery,
    useSendUserRequestApprovalMutation,
    useLazyGetIncomingRequestsQuery,
    useAcceptIncomingRequestMutation,
    useGetTeamChatQuery,
} = teamsService;
