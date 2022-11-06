import { Avatar, Button, Divider, Grid, Paper, Typography } from '@mui/material';

import s from './FullPost.module.scss';
import { OutputData } from '@editorjs/editorjs';
import { Container } from '@/ui';
import { CreatePostDTO, IdeaModel } from '@/dto';
import { useGetMyProfileQuery, useGetPostsByIdQuery } from '@/services';
import { useLikeIdeaMutation } from '@/services';
import { DetailedHTMLProps, Fragment, HTMLAttributes, useRef, useState } from 'react';
import Reactions, { customIcons } from '../../ui/Reactions';
import PostAddIcon from '@mui/icons-material/PostAdd';
import { WritePost } from '../WritePost';
import { useParams } from 'react-router-dom';
import { formatDistance } from 'date-fns';
import ru from 'date-fns/locale/ru';
import { IconWithText } from '../../ui/Container/IconWithText/IconWithText';
import { Construction, ConstructionOutlined, Money } from '@mui/icons-material';

interface FullPostProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    data: IdeaModel;
    blocks: OutputData['blocks'];
    title?: string;
    mode?: 'post' | 'idea';
}

export const FullPost = ({ data, blocks, title, mode = 'idea', ...props }: FullPostProps) => {
    const id = useParams().id;
    const { data: user } = useGetMyProfileQuery();
    const isOwnProfile = user?.user.id === data?.author.id;
    const [isCreateNewPost, setIsCreateNewPost] = useState(false);
    const newPostAnchor = useRef<HTMLDivElement>(null);
    const { data: allPosts } = useGetPostsByIdQuery({ idea_id: id, limit: 10, desc: true, page: 1, search: '', items: 20 });

    const [like] = useLikeIdeaMutation();
    const {
        author: { avatar_thumbnail, snp },
        subscribers_count,
        my_reaction,
        reactions,
    } = data;

    const reactionHandler = (value) => {
        if (value) {
            like({
                ideaId: mode === 'idea' ? id : data.id,
                body: { value: customIcons[value].id.slice(0, customIcons[value].id.length - 1) },
            });
        }
    };

    const totalSubscribers = subscribers_count > 0 ? `+${subscribers_count}` : subscribers_count;

    return (
        <>
            <div {...props}>
                <Paper elevation={0} className={s.paper}>
                    <Container>
                        {title && <Typography>{title}</Typography>}
                        {mode === 'idea' && (
                            <div className={s.text}>
                                {Array.isArray(blocks) &&
                                    blocks.length &&
                                    blocks?.map((obj) => (
                                        <Fragment key={obj.id}>
                                            {obj.type === 'image' && <img src={obj.data.file.url} width={500} height={600} alt={''} />}
                                            {obj.type === 'paragraph' && <Typography dangerouslySetInnerHTML={{ __html: obj.data.text }} />}
                                            {obj.type === 'attaches' && (
                                                <a download href={obj.data.file.url}>
                                                    {obj.data.title}
                                                </a>
                                            )}
                                        </Fragment>
                                    ))}
                                <Divider style={{ margin: '16px 0' }} />
                                {!!data?.information?.budget && (
                                    <div>
                                        <Grid container style={{ opacity: 0.7 }} spacing={0.5}>
                                            <Grid item alignItems={'center'}>
                                                <Money />
                                            </Grid>
                                            <Grid item>Привлечено инвестиций</Grid>
                                        </Grid>
                                        <Typography variant={'body1'} style={{ fontWeight: 700, marginTop: -8 }}>
                                            {data?.information?.budget}₽
                                        </Typography>
                                    </div>
                                )}

                                {!!data?.information?.progress && (
                                    <>
                                        <Grid container style={{ opacity: 0.7 }} spacing={0.5}>
                                            <Grid item alignItems={'center'}>
                                                <ConstructionOutlined />
                                            </Grid>
                                            <Grid item>Проработанность идеи и прототипа</Grid>
                                        </Grid>
                                        <Typography variant={'body1'} style={{ fontWeight: 700, marginTop: -8 }}>
                                            {data?.information?.progress}%
                                        </Typography>
                                    </>
                                )}

                                <div
                                    style={{
                                        width: '100%',
                                        marginLeft: -5,
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'center',
                                        marginTop: 16,
                                    }}
                                >
                                    {mode === 'idea' && data?.status.id === 4 && (
                                        <Reactions
                                            onClick={(e) => reactionHandler(e.target.value)}
                                            reactions={reactions}
                                            my_reaction={my_reaction}
                                        />
                                    )}
                                </div>
                                <div className='d-flex justify-between align-center mt-30 mb-30'>
                                    <div className={s.userInfo}>
                                        <Avatar src={avatar_thumbnail ?? ''} />
                                        <b>{snp}</b>
                                        <p hidden={!isOwnProfile}>(Это вы)</p>
                                        <span>{totalSubscribers}</span>
                                    </div>
                                    {isOwnProfile && (
                                        <div className={s.controls}>
                                            <Button
                                                disabled={isCreateNewPost}
                                                onClick={() => {
                                                    setIsCreateNewPost(true);
                                                    setTimeout(
                                                        () =>
                                                            newPostAnchor.current?.scrollIntoView({
                                                                behavior: 'smooth',
                                                                block: 'start',
                                                            }),
                                                        500
                                                    );
                                                }}
                                                variant='contained'
                                            >
                                                <PostAddIcon />
                                            </Button>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </Container>
                </Paper>

                <div ref={newPostAnchor}>{isCreateNewPost && <WritePost data={{} as CreatePostDTO} />}</div>
            </div>
            <div className={s.posts}>
                {mode === 'post' && (
                    <ul>
                        {allPosts?.payload?.map((el) => (
                            <li className={s.post}>
                                <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                                    <Avatar src={el.author.avatar_thumbnail} />
                                    <div style={{ display: 'grid' }}>
                                        <Typography style={{ margin: 0 }}>{el.author.snp}</Typography>
                                        <Typography style={{ margin: 0 }}>
                                            {formatDistance(new Date(el.created_at ?? '1970-01-01'), new Date(), {
                                                locale: ru,
                                                addSuffix: true,
                                            })}
                                        </Typography>
                                    </div>
                                </div>
                                <br />
                                <Typography variant='h5'>{el.title}</Typography>
                                {el.post_json?.map((obj) => (
                                    <Fragment key={el.id}>
                                        {obj.type === 'image' && <img src={obj.data.file.url} width={500} height={600} alt={''} />}
                                        {obj.type === 'paragraph' && <Typography dangerouslySetInnerHTML={{ __html: obj.data.text }} />}
                                        {obj.type === 'attaches' && (
                                            <a download href={obj.data.file.url}>
                                                {obj.data.title}
                                            </a>
                                        )}
                                    </Fragment>
                                ))}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </>
    );
};
