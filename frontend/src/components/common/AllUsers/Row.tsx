import {
    Avatar,
    Box,
    Button,
    Chip,
    Collapse,
    Divider,
    Grid,
    IconButton,
    Table,
    TableCell,
    TableHead,
    TableRow,
    Typography,
} from '@mui/material';
import { useContext, useState } from 'react';
import { Link } from 'react-router-dom';
import {
    useUpdateIdeaCategoriesMutation,
    useUpdateIdeaStatusMutation,
    useUpdateUserActivityMutation,
    useUpdateUserAdminMutation,
    useUpdateUserVerificationMutation,
} from '../../../services/Admin.service';
import { SnackbarContext } from '../../../context/SnackbarContext';
import { isEqual } from 'lodash';
import {
    AccessibilityNewOutlined,
    AdminPanelSettingsOutlined,
    CheckCircleOutline,
    RemoveDone,
    ThumbDownAltOutlined,
} from '@mui/icons-material';
import BlockIcon from '@mui/icons-material/Block';
import { useUpdateUserSettingsMutation } from '@/services';

export const AllUsersRow = ({ row }) => {
    const { setSnack } = useContext(SnackbarContext);

    const [updateUserAdmin] = useUpdateUserAdminMutation();

    const [updateVerification] = useUpdateUserVerificationMutation();

    const [updateActivity] = useUpdateUserActivityMutation();

    const handleUpdateAdmin = (flag) => {
        updateUserAdmin({ userId: row.id, is_admin: flag }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Пользователь обновлен' });
            }
        });
    };

    const handleUpdateVerification = (flag) => {
        updateVerification({ userId: row.id, is_verified: flag }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Пользователь обновлен' });
            }
        });
    };

    const handleUpdateActivityStatus = (flag) => {
        updateActivity({ userId: row.id, enabled: flag }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Пользователь обновлен' });
            }
        });
    };

    return (
        <>
            {' '}
            <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
                <TableCell component='th' scope='row'>
                    <Link style={{ display: 'flex', alignItems: 'center', gap: 8 }} to={`/profile/${row.id}`}>
                        <Avatar style={{ width: 24, height: 24 }} src={row.avatar_thumbnail} /> {row.snp}
                    </Link>
                </TableCell>
                <TableCell component='th' scope='row'>
                    {row.is_active ? (
                        <Button
                            size={'small'}
                            variant='outlined'
                            onClick={() => handleUpdateActivityStatus(false)}
                            startIcon={<BlockIcon />}
                        >
                            Заблокировать
                        </Button>
                    ) : (
                        <Button
                            size={'small'}
                            variant='outlined'
                            onClick={() => handleUpdateActivityStatus(true)}
                            startIcon={<AccessibilityNewOutlined />}
                        >
                            Разблокировать
                        </Button>
                    )}
                </TableCell>
                <TableCell component='th' scope='row'>
                    {row.is_verified ? (
                        <Button
                            size={'small'}
                            variant='outlined'
                            onClick={() => handleUpdateVerification(false)}
                            startIcon={<RemoveDone />}
                        >
                            Снять верификацию
                        </Button>
                    ) : (
                        <Button
                            size={'small'}
                            variant='outlined'
                            onClick={() => handleUpdateVerification(true)}
                            startIcon={<CheckCircleOutline />}
                        >
                            Верифицировать
                        </Button>
                    )}
                </TableCell>
                <TableCell component='th' scope='row'>
                    {row.is_admin ? (
                        <Button
                            size={'small'}
                            variant='outlined'
                            onClick={() => handleUpdateAdmin(false)}
                            startIcon={<ThumbDownAltOutlined />}
                        >
                            Разжаловать{' '}
                        </Button>
                    ) : (
                        <Button
                            size={'small'}
                            onClick={() => handleUpdateAdmin(true)}
                            variant='outlined'
                            startIcon={<AdminPanelSettingsOutlined />}
                        >
                            Назначить администратором
                        </Button>
                    )}
                </TableCell>
            </TableRow>
        </>
    );
};
