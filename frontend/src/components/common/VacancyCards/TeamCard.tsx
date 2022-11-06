import { Link } from 'react-router-dom';

import { Avatar, Button, Chip, Dialog, DialogActions, DialogContent, DialogTitle, Grid, Paper, TextField, Typography } from '@mui/material';

import s from './Post.module.scss';
import Reactions from '../../ui/Reactions';
import { TeamVacancy } from '../../../types/dto/Teams';
import { LightbulbOutlined, PeopleAltOutlined } from '@mui/icons-material';
import { useState } from 'react';
import { CustomAutocomplete } from '../../ui/Autocomplete';
import { useGetTeamRolesQuery } from '@/services';

interface TeamCardProps {
    id: number | string;
    title: string;
    idea: TeamVacancy['idea'];
    members: TeamVacancy['members'];
    description: string;
    author: TeamVacancy['team_leader'];
    authorId: string;
    isLookingForMembers: boolean;
    onJoinRequest: (teamId: any, favoriteRole: any, cover_letter: any) => void;
}

export const TeamCard = ({
    id,
    authorId,
    title,
    description,
    author,
    isLookingForMembers,
    idea,
    members,
    onJoinRequest,
}: TeamCardProps) => {
    const [isOpenModal, setIsOpenModal] = useState(false);
    const [favoriteRole, setFavoriteRole] = useState(null);
    const [coverLetter, setCoverLetter] = useState('');

    return (
        <Paper component='article' elevation={0} classes={{ root: s.paper }}>
            <Link to={`/ideas/${idea.id}`} style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                <Typography variant='h5' className={s.title}>
                    {title}
                </Typography>
                <Typography className={s.descr} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <LightbulbOutlined sx={{ width: 20 }} /> {` ${idea.title}`}
                </Typography>
                {!!members.filter((member) => member?.role?.name).length && (
                    <Typography className={s.descr} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <PeopleAltOutlined sx={{ width: 20 }} /> В команде:
                        {members
                            .filter((member) => member?.role?.name)
                            .map((member) => (
                                <Chip size={'small'} key={member.user.id} label={member?.role?.name} />
                            ))}
                    </Typography>
                )}
            </Link>

            <div className={s.emotions}>
                <Link className={s.profile} to={`/profile/${authorId}`}>
                    <Avatar style={{ width: 20, height: 20 }} src={author.avatar_thumbnail} />
                    <Typography variant={'body2'}>{author.snp}</Typography>
                </Link>
                {isLookingForMembers && (
                    <Button size={'small'} onClick={() => setIsOpenModal(true)}>
                        Присоединиться
                    </Button>
                )}
            </div>
            <Dialog open={isOpenModal} onClose={() => setIsOpenModal(false)}>
                <DialogTitle>Присоединиться к {title}</DialogTitle>
                <DialogContent>
                    <Grid container spacing={2} direction={'column'}>
                        <Grid item>
                            <br />
                            <CustomAutocomplete
                                label={'Выберите роль'}
                                hookName={'useGetTeamRolesQuery'}
                                value={favoriteRole}
                                onChange={(value) => setFavoriteRole(value)}
                                multiple={false}
                            />
                        </Grid>
                        <Grid item>
                            <TextField
                                value={coverLetter}
                                onChange={(e) => setCoverLetter(e.target.value)}
                                autoFocus
                                margin='dense'
                                label='Текст приглашения'
                                rows={3}
                                multiline
                                fullWidth
                                variant='outlined'
                            />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setIsOpenModal(false)}>Отменить</Button>
                    <Button
                        disabled={!coverLetter.length || !favoriteRole?.id}
                        onClick={() => {
                            setIsOpenModal(false);
                            onJoinRequest(id, favoriteRole, coverLetter);
                        }}
                    >
                        Отправить запрос
                    </Button>
                </DialogActions>
            </Dialog>
        </Paper>
    );
};
