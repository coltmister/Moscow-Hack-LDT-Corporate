import { useState } from 'react';
import { Divider, Paper, Tab, Tabs, Typography } from '@mui/material';
import { AddCommentForm, Comment } from '@/components';
import { useCreateCommentMutation, useDeleteCommentMutation, useGetAllCommentsQuery } from '@/services';
import { CommentItemDto } from '@/dto';
import { Container } from '@/ui';
import { getDeclension } from '../../../utils/getDeclanations';

interface PostCommentsProps {
    postId: number | string;
}

export const PostComments = ({ postId }: PostCommentsProps) => {
    const { data: comments } = useGetAllCommentsQuery(postId);
    const [deleteComment] = useDeleteCommentMutation();
    const [createComment] = useCreateCommentMutation();
    // const userData = useAppSelector(selectUserData);
    const [activeTab, setActiveTab] = useState(0);

    const onAddComment = (comment: CommentItemDto) => createComment(comment);
    const onRemoveComment = (id: number) => deleteComment(id);

    return (
        <Paper elevation={0} className='mt-40 p-30'>
            <Container>
                <Typography variant='h6' className='mb-20'>
                    {getDeclension({ count: comments?.length ?? 0, one: 'комментарий', few: 'комментария', many: 'комментариев' })}
                </Typography>
                <Tabs
                    onChange={(_, newValue) => setActiveTab(newValue)}
                    className='mt-20'
                    value={activeTab}
                    indicatorColor='primary'
                    textColor='primary'
                >
                    <Tab label='Популярные' />
                    <Tab label='По порядку' />
                </Tabs>
                <Divider />
                {/*{userData && <AddCommentForm addComment={onAddComment} postId={postId} />}*/}
                <div className='mb-20' />
                {comments?.map((obj) => (
                    <Comment
                        key={obj.id}
                        id={obj.id}
                        //TODO
                        comment={obj}
                        // currentUserId={userData?.id}
                        currentUserId={0}
                        onRemove={onRemoveComment}
                    />
                ))}
            </Container>
        </Paper>
    );
};
