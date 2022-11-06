import clsx from 'clsx';
import { useState } from 'react';
import { Link } from 'react-router-dom';

import { useAuth } from '@/hooks';

import { Avatar, Button, IconButton, Paper } from '@mui/material';
import {
    SearchOutlined as SearchIcon,
    SmsOutlined as MessageIcon,
    Menu as MenuIcon,
    NotificationsNoneOutlined as NotificationIcon,
    AccountCircleOutlined,
    ArrowUpward,
    Add,
    Logout,
} from '@mui/icons-material';

import { AuthDialog } from '@/components';

import { ReactComponent as Logo } from './img/logotype.svg';
import s from './Header.module.scss';
import { useUserInfo } from '../../../hooks/useUserInfo';
import { useGetMyProfileQuery } from '@/services';

interface HeaderProps {
    setMenu(b: boolean): void;

    isOpenMenu: boolean;
}

export const Header = ({ setMenu, isOpenMenu }: HeaderProps) => {
    const [isOpenAuthDialog, setOpenAuthDialog] = useState<boolean>(false);
    const isAuth = useAuth();

    const data = useUserInfo();

    const openAuthDialog = () => setOpenAuthDialog(true);
    const closeAuthDialog = () => setOpenAuthDialog(false);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
    };

    return (
        <Paper component='header' classes={{ root: s.root }} className={s.header} elevation={0}>
            <div className={clsx(s.left)}>
                <IconButton onClick={() => setMenu(!isOpenMenu)}>
                    <MenuIcon />
                </IconButton>
                <Link to='/' className={s.logo}>
                    <Logo width={100} height={35} />
                </Link>
                {/*<div className={s.searchBlock}>*/}
                {/*    <SearchIcon />*/}
                {/*    <input type='text' placeholder='Поиск' />*/}
                {/*</div>*/}
                {/*<Button component={Link} to='/create-idea' variant='outlined' color='secondary' className={s.penButton}>*/}
                {/*    <Add />*/}
                {/*    Новая запись*/}
                {/*</Button>*/}
            </div>
            <div className={clsx('d-flex', 'align-center')}>
                {/*<div className={s.controls}>*/}
                {/*    <IconButton>*/}
                {/*        <MessageIcon />*/}
                {/*    </IconButton>*/}
                {/*    <IconButton>*/}
                {/*        <NotificationIcon />*/}
                {/*    </IconButton>*/}
                {/*</div>*/}
                {isAuth && (
                    <Link className='d-flex align-center' to={`/profile/${data?.user?.id}`}>
                        <Avatar
                            className={s.avatar}
                            alt={'Аватар пользователя ' + data?.user?.snp ?? 'Аватар пользователя'}
                            src={data?.avatar_thumbnail}
                            title='Перейти в раздел профиль'
                        />
                        <IconButton onClick={handleLogout}>
                            <Logout />
                        </IconButton>
                    </Link>
                )}

                {!isAuth && (
                    <button className={s.login} onClick={openAuthDialog}>
                        <AccountCircleOutlined />
                        Войти
                    </button>
                )}
            </div>
            <AuthDialog onClose={closeAuthDialog} open={isOpenAuthDialog} />
        </Paper>
    );
};
