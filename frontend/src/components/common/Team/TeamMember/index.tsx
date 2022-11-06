import clsx from 'clsx';
import { Avatar, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import s from './TeamMember.module.scss';
import { PostAuthorDTO } from '@/dto';

export interface TeamMemberProps {
    profile: {
        date_joined: string | Date;
        membership_requester: {
            id: number;
            name: string;
        };
        role: {
            id: string;
            name: string;
        };
        user: PostAuthorDTO;
    };
}

export const TeamMember = ({ profile }: TeamMemberProps) => {
    const { role, user } = profile;

    return (
        <Link to={`/profile/${user.id}`} className={s.member}>
            <Avatar src={user.avatar_thumbnail ?? ''} />
            <div className={s.info}>
                <Typography className={s.name} variant='body1'>
                    {user.snp}
                    <CheckCircleIcon className={clsx(s.icon, user.is_verified && s.verify)} />
                </Typography>
                <Typography sx={{ color: '#7e7e7e' }} variant='body2'>
                    {role?.name}
                </Typography>
            </div>
        </Link>
    );
};
