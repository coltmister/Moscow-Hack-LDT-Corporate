import { API } from '@/api';
import { STORAGE } from '@/utils';
import { UserFormResponseDTO, UserProfileResponseDTO, UserSettingsDto } from '@/dto';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react';
import { prepareHeaders } from '../utils/prepareHeaders';

const invalidateTags = ['CONSTANTS'];

export interface ConstantResponse {
    id: string;
    name: string;
}

export const constantsService = createApi({
    reducerPath: 'ConstantsApi',
    tagTypes: invalidateTags,
    baseQuery: fetchBaseQuery({
        baseUrl: API.url,
        prepareHeaders: prepareHeaders,
    }),
    endpoints: (build) => ({
        getSkills: build.query<ConstantResponse[], string>({
            query: (string) => {
                return {
                    url: '/users/skills',
                    method: 'GET',
                    params: {
                        search: string,
                    },
                };
            },
        }),
        getCountries: build.query<ConstantResponse[], string>({
            query: (string) => {
                return {
                    url: '/users/country',
                    method: 'GET',
                    params: {
                        search: string,
                    },
                };
            },
        }),
        getUniversities: build.query<ConstantResponse[], null>({
            query: (string) => {
                return {
                    url: '/users/university',
                    method: 'GET',
                    params: {
                        search: string,
                    },
                };
            },
        }),
        getTeamRoles: build.query<ConstantResponse[], void>({
            query: (string) => {
                return {
                    url: '/users/team-roles',
                    method: 'GET',
                    params: {
                        search: string,
                    },
                };
            },
        }),
        getInterests: build.query<ConstantResponse[], null>({
            query: (string) => {
                return {
                    url: '/users/interests',
                    method: 'GET',
                    params: {
                        search: string,
                    },
                };
            },
        }),
        getStatuses: build.query<ConstantResponse[], null>({
            query: () => {
                return {
                    url: '/ideas/status/',
                    method: 'GET',
                };
            },
        }),
    }),
});

export const {
    useGetCountriesQuery,
    useGetInterestsQuery,
    useGetSkillsQuery,
    useGetTeamRolesQuery,
    useGetUniversitiesQuery,
    useGetStatusesQuery,
} = constantsService;
