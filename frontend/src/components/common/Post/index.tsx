import ru from 'date-fns/locale/ru';
import { formatDistance } from 'date-fns';

import { Link } from 'react-router-dom';

import { Avatar, Grid, Paper, Typography } from '@mui/material';
import s from './Post.module.scss';
import Reactions, { customIcons, MyReaction, ReactionProps } from '../../ui/Reactions';
import { useLikeIdeaMutation, useLikePostMutation } from '@/services';

interface PostProps {
    id: number | string;
    title: string;
    description: string;
    imageUrl?: string;
    author: string;
    avatar?: string;
    authorId: string;
    mode?: 'posts' | 'ideas';
    created_at: string | Date;
    reactions?: ReactionProps;
    onLike?: () => void;
    my_reaction?: MyReaction;
    ideaId?: string;
}

export const Post = ({
    id,
    authorId,
    title,
    description,
    imageUrl,
    author,
    avatar,
    created_at,
    mode = 'posts',
    reactions,
    my_reaction,
    onLike,
    ideaId,
}: PostProps) => {
    const postCreatedAt = formatDistance(new Date(created_at ?? '1900-01-01'), new Date(), { addSuffix: true, locale: ru });

    const [likeIdea] = useLikeIdeaMutation();

    const [likePost] = useLikePostMutation();

    const reactionHandler = (value) => {
        if (value) {
            if (mode === 'ideas') {
                likeIdea({
                    ideaId: id,
                    body: { value: customIcons[value].id.slice(0, customIcons[value].id.length - 1) },
                }).then((res) => {
                    if ('data' in res) {
                        onLike();
                    }
                });
            }
            if (mode === 'posts') {
                likePost({
                    ideaId,
                    postId: id,
                    body: { value: customIcons[value].id.slice(0, customIcons[value].id.length - 1) },
                }).then((res) => {
                    if ('data' in res) {
                        onLike();
                    }
                });
            }
        }
    };

    return (
        <Paper component='article' elevation={0} classes={{ root: s.paper }}>
            <Link className={s.top} to={`/profile/${authorId}`}>
                <Grid container alignItems={'center'} justifyContent={'space-between'}>
                    <Grid item style={{ display: 'flex', gap: 8 }}>
                        <Avatar style={{ width: 24, height: 24 }} src={avatar} />
                        <Typography>{author}</Typography>
                    </Grid>
                    <Typography style={{ opacity: 0.7 }} variant={'body2'}>
                        {postCreatedAt}
                    </Typography>
                </Grid>
            </Link>
            <Link to={`/${mode}/${id}`}>
                <Typography variant='h5' className={s.title}>
                    {title}
                </Typography>
                <Typography className={s.descr}>{`${description}`}</Typography>
                {imageUrl && <img src={imageUrl} height={500} width={600} alt={title} />}
            </Link>
            {reactions && (
                <div style={{ marginTop: 12 }}>
                    <Reactions onClick={(e) => reactionHandler(e.target.value)} reactions={reactions} my_reaction={my_reaction} />
                </div>
            )}
        </Paper>
    );
};
