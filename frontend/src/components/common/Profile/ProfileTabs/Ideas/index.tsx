import Paper from '@mui/material/Paper';
import { useAppropriateUserIdea } from '../../../../../hooks/useAppropriateUserIdea';
import { Button, Chip, Divider, Grid, Typography } from '@mui/material';
import { Link, useLocation, useParams } from 'react-router-dom';
import { useUserInfo } from '../../../../../hooks/useUserInfo';
import { useGetUserIncomingRequestsQuery, userService, useSendUserRequestApprovalMutation } from '@/services';
import { SnackbarContext } from '../../../../../context/SnackbarContext';
import { useContext } from 'react';
import { StarBorderOutlined } from '@mui/icons-material';

export const Ideas = () => {
    const { id } = useParams();
    const { isUserOwnProfile } = useUserInfo();
    const { data, isLoading } = useAppropriateUserIdea();
    const { setSnack } = useContext(SnackbarContext);
    const { data: incomingRequests, isLoading: isIncomingRequestsLoading } = useGetUserIncomingRequestsQuery(null, {
        skip: !isUserOwnProfile,
    });
    const [approve] = useSendUserRequestApprovalMutation();

    const handleApproval = (flag: boolean, requestId: string) => {
        approve({ decision: flag, requestId }).then((res) => {
            if ('data' in res) {
                setSnack({ message: flag ? 'Приглашение принято' : 'Приглашение отклонено' });
                userService.useGetMyIdeasQuery(null);
            }
        });
    };

    return (
        <>
            <Grid container spacing={2}>
                {data &&
                    !isLoading &&
                    data.map((item) => (
                        <Grid item key={item.id} xs={12}>
                            <Link to={`/ideas/${item.id}`}>
                                <Paper sx={{ padding: 2, width: '100%' }} variant='outlined'>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                        <Typography variant={'h5'}>{item.title}</Typography>
                                        {id === item.author.id && (
                                            <StarBorderOutlined style={{ height: 20, width: 20 }} color={'primary'} />
                                        )}
                                    </div>
                                    <Typography>{item.description}</Typography>
                                    <br />
                                    Статус: <Chip size={'small'} label={item.status.name} />
                                </Paper>
                            </Link>
                        </Grid>
                    ))}
                {!data?.length && !isLoading && (
                    <Grid sx={{ margin: 16 }} container alignItems={'center'} justifyContent={'center'}>
                        <Grid item>Идей еще нет. {isUserOwnProfile && <Link to={'/create-idea'}> Создать?</Link>}</Grid>
                    </Grid>
                )}
            </Grid>
            {incomingRequests && !!incomingRequests.length && !isIncomingRequestsLoading && (
                <>
                    <Divider sx={{ margin: '16px 0' }}>Приглашения в команду</Divider>
                    {incomingRequests.map((request) => (
                        <Grid item key={request.id} xs={12}>
                            <Paper sx={{ padding: 2, width: '100%', borderColor: 'orange' }} variant='outlined'>
                                <Link to={`/ideas/${request.team.idea.id}`}>
                                    <Typography variant={'h5'}>{request.team.name}</Typography>
                                    <Typography variant={'body2'}>{request.team.idea.title}</Typography>
                                    <br />
                                    <Typography>Приглашение: {request.cover_letter}</Typography>
                                    <br />
                                    Предлагаемая роль: <Chip size={'small'} label={request.role.name} />
                                </Link>
                                <Grid sx={{ marginTop: 1 }} container spacing={2}>
                                    <Grid item>
                                        <Button onClick={() => handleApproval(true, request.id)}>Принять</Button>
                                    </Grid>
                                    <Grid item>
                                        <Button onClick={() => handleApproval(false, request.id)}>Отклонить</Button>
                                    </Grid>
                                </Grid>
                            </Paper>
                        </Grid>
                    ))}
                </>
            )}
        </>
    );
};
