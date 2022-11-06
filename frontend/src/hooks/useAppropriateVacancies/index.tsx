import { useGetTeamVacanciesQuery, useGetUserProfilesQuery } from '@/services';

export interface useAppropriateVacanciesProps {
    mode: string;
    team: string;
    page: number;
    itemsPerPage: number;
}

export const useAppropriateVacancies = ({ mode, team, page, itemsPerPage }: useAppropriateVacanciesProps) => {
    const userProfiles = useGetUserProfilesQuery({ page, itemsPerPage, team }, { skip: mode === 'ideas' && !team });
    const teamVacancies = useGetTeamVacanciesQuery({ page, itemsPerPage }, { skip: mode === 'people' });

    return mode === 'ideas' ? teamVacancies : userProfiles;
};
