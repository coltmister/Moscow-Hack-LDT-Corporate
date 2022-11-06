import { Link } from 'react-router-dom';

import {
    Avatar,
    Box,
    Button,
    Chip,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    Paper,
    TextField,
    Typography,
} from '@mui/material';

import s from './Post.module.scss';
import { useState } from 'react';
import { CustomAutocomplete } from '../../ui/Autocomplete';

interface PersconCardProps {
    id: number | string;
    personName: string;
    biography: string;
    personId: string;
    avatar: string;
    skills: Array<any>;
    onInvitation: (userId: string, favoriteRole: any, coverLetter: any) => void;
    requiredRoles: Array<{ id: string; name: string; amount: number }>;
}

export const PersonCard = ({ id, personName, biography, personId, avatar, skills, onInvitation, requiredRoles }: PersconCardProps) => {
    const [isOpenModal, setIsOpenModal] = useState(false);
    const [favoriteRole, setFavoriteRole] = useState(null);
    const [coverLetter, setCoverLetter] = useState('');

    return (
        <>
            <Paper component='article' elevation={0} classes={{ root: s.paper }}>
                <Link className={s.top} to={`/profile/${personId}`}>
                    <Avatar src={avatar} />
                    <Typography>{personName}</Typography>
                </Link>
                <Link to={`/profile/${id}`}>
                    <Typography className={s.descr}>{`${biography}`}</Typography>
                    <Grid sx={{ marginTop: 1 }} container spacing={1}>
                        {skills &&
                            skills.map((skill) => (
                                <Grid item>
                                    <Chip size={'small'} label={skill.name} />
                                </Grid>
                            ))}
                    </Grid>
                </Link>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                    <Button onClick={() => setIsOpenModal(true)}>Пригласить</Button>
                </Box>
                <Dialog open={isOpenModal} onClose={() => setIsOpenModal(false)}>
                    <DialogTitle>Пригласить {personName}</DialogTitle>
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
                                    id='name'
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
                                onInvitation(personId, favoriteRole, coverLetter);
                            }}
                        >
                            Пригласить
                        </Button>
                    </DialogActions>
                </Dialog>
            </Paper>
        </>
    );
};
