import { MainLayout } from '@/layouts';
import { Post } from '@/components';
import { teamsService, useGetAllIdeasQuery, useSendInvitationMutation, useSendJoinRequestInvitationMutation } from '@/services';
import { VacanciesFilters } from '../../common/Vacancies/VacanciesFilters';
import { useForm, FormProvider } from 'react-hook-form';
import { useGetVacanciesQuery } from '../../../services/Teams.service';
import { TeamCard } from '../../common/VacancyCards/TeamCard';
import { PersonCard } from '../../common/VacancyCards/PersonCard';

import { TeamVacancy, UserVacancy } from '../../../types/dto/Teams';
import { useContext, useEffect, useState } from 'react';
import { Pagination } from '@mui/lab';
import { useAppropriateVacancies } from '../../../hooks/useAppropriateVacancies';
import { SnackbarContext } from '../../../context/SnackbarContext';
export const Vacancies = () => {
    const methods = useForm({ mode: 'onChange', defaultValues: { mode: 'ideas', team: null } });
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [page, setPage] = useState(1);
    const { setSnack } = useContext(SnackbarContext);

    const required_roles = methods.watch('team')?.required_members;

    const teamId = methods.watch('team')?.id;

    const [invite] = useSendInvitationMutation();

    const [joinRequest] = useSendJoinRequestInvitationMutation();

    const { data } = useAppropriateVacancies({ page, itemsPerPage, mode: methods.watch('mode'), team: methods.watch('team')?.id });

    const onSubmit = (data) => console.log(data);

    const onUserInvitation = (userId: any, favoriteRole: any, cover_letter: any) => {
        invite({ userId, cover_letter, role: favoriteRole.id, teamId }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Приглашение отправлено' });
            } else {
                setSnack({ message: res.error.data.message ?? 'Ошибка ' });
            }
        });
    };

    const onJoinRequest = (teamId: any, favoriteRole: any, cover_letter: any) => {
        joinRequest({ teamId, cover_letter, role: favoriteRole.id }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Запрос отправлен' });
            } else {
                setSnack({ message: res.error.data.message ?? 'Ошибка ' });
            }
        });
    };

    return (
        <MainLayout
            sidebarTitle='Фильтр вакансий'
            sidebarNode={
                <FormProvider {...methods}>
                    <form onSubmit={methods.handleSubmit(onSubmit)}>
                        <VacanciesFilters />
                    </form>
                </FormProvider>
            }
        >
            {methods.watch('mode') === 'ideas' &&
                (data?.payload as TeamVacancy[])?.map((team) => (
                    <TeamCard
                        id={team.id}
                        title={team.name}
                        idea={team.idea}
                        members={team.members}
                        description={team.description}
                        author={team.team_leader}
                        authorId={team.team_leader.id}
                        isLookingForMembers={team.is_looking_for_members}
                        onJoinRequest={onJoinRequest}
                    />
                ))}
            {methods.watch('mode') === 'people' &&
                (data?.payload as UserVacancy[])?.map((person) => (
                    <PersonCard
                        key={person.id}
                        avatar={person.avatar_thumbnail}
                        biography={person?.profile?.biography}
                        personName={person.snp}
                        personId={person.id}
                        requiredRoles={required_roles}
                        id={person.id}
                        skills={person?.profile?.skills}
                        onInvitation={onUserInvitation}
                    />
                ))}
            {/*{data?.payload.map((idea) => (*/}
            {/*    <Post*/}
            {/*        key={idea.id}*/}
            {/*        mode='ideas'*/}
            {/*        description={idea.description}*/}
            {/*        title={idea.title}*/}
            {/*        author={idea.team_leader.snp}*/}
            {/*        authorId={idea.team_leader.id}*/}
            {/*        id={idea.id}*/}
            {/*        avatar={undefined}*/}
            {/*    />*/}
            {/*))}*/}
            {!!data?.payload?.length && (
                <Pagination className='mb-15' count={data?.total_pages} onChange={(event, page) => setPage(page)} />
            )}
        </MainLayout>
    );
};
