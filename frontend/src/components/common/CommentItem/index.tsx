import s from './CommentItem.module.scss';
import { Link } from 'react-router-dom';
import { UserResponseDto } from '@/dto';
import { Avatar, Typography } from '@mui/material';
import { formatDistance } from 'date-fns';
import ru from 'date-fns/locale/ru';

interface CommentItemProps {
    user: {
        id: string;
        snp: string;
        avatar_thumbnail: string;
    };
    created_at: string;
    id: string;
    text: string;
}

export const CommentItem = ({ user, created_at, id, text }: CommentItemProps) => {
    return (
        <div className={s.commentItem}>
            <div className={s.userInfo}>
                <Avatar src={user.avatar_thumbnail ?? ''} alt={user.snp} />
                <Link style={{ display: 'grid' }} to={`/profile/${user.id}`}>
                    <b>{user.snp}</b>
                    <Typography style={{ opacity: 0.55 }} variant='caption'>
                        {formatDistance(new Date(created_at ?? '1900-01-01'), new Date(), { locale: ru, addSuffix: true })}
                    </Typography>
                </Link>
            </div>
            <p className={s.text}>{text}</p>
        </div>
    );
};
