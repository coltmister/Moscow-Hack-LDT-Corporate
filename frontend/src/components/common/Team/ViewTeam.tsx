import { Link, useParams } from 'react-router-dom';
import { useGetIdeaByIdQuery, useGetTeamChatQuery } from '@/services';
import { Chip, Typography } from '@mui/material';
import { TeamMember } from './TeamMember';
import s from './ViewTeam.module.scss';
import { useUserInfo } from '../../../hooks/useUserInfo';
import { VKicon } from '../AuthDialog/img';

export const ViewTeam = () => {
    const id = useParams().id;
    const { user } = useUserInfo();
    const { data } = useGetIdeaByIdQuery(id);

    const participantsIds = data?.team.members.map((member) => member.user.id);

    const {
        team: { members, name, is_looking_for_members, description, chat },
    } = data;

    return (
        <article className={s.team}>
            <header>
                <Typography variant='h5'>{name}</Typography>
                {is_looking_for_members && <Chip size='small' label='В активном поиске' />}
                <div className={s.description}>
                    <Typography variant='body1'>{description}</Typography>
                </div>
            </header>
            {chat && (
                <main>
                    <Typography sx={{ marginBottom: 1 }} variant='h5'>
                        Чат команды
                    </Typography>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }} className={s.team}>
                        <a target={'_blank'} href={chat?.chat_link}>
                            <VKicon width={36} />
                        </a>
                    </div>
                </main>
            )}
            <main>
                <Typography sx={{ marginBottom: 3 }} variant='h5'>
                    Состав команды:
                </Typography>
                <div className={s.team}>{members.map((member: any) => <TeamMember key={member.user.id} profile={member} />).reverse()}</div>
            </main>
        </article>
    );
};
