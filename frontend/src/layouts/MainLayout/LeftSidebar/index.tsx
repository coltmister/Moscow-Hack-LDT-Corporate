import { useIsLarge, useOnClickOutside, useRouter } from '@/hooks';

import { Link } from 'react-router-dom';

import { Button, Divider, IconButton, Typography } from '@mui/material';

import { actionsMenu, adminMenu, menu, MenuModel } from './common';
import s from './LeftSidebar.module.scss';
import { DetailedHTMLProps, HTMLAttributes, useRef } from 'react';
import clsx from 'clsx';
import { Close } from '@mui/icons-material';
import { useUserInfo } from '../../../hooks/useUserInfo';

interface LeftSidebarProps extends DetailedHTMLProps<HTMLAttributes<HTMLElement>, HTMLElement> {
    isOpen: boolean;

    setOpen(b: boolean): void;
}

export const LeftSidebar = ({ className, isOpen, setOpen, ...props }: LeftSidebarProps) => {
    const { location } = useRouter();
    const isLarge = useIsLarge();
    const { isAdmin } = useUserInfo();
    const getButtonStyleByPath = (path: string) => (location?.pathname?.toString() === path ? 'contained' : 'text');

    const ref = useRef<HTMLElement>(null);

    useOnClickOutside(ref, () => !isLarge && setOpen(false));

    return (
        <aside
            className={clsx(s.menu, className, {
                [s.open]: isOpen,
            })}
            ref={ref}
            {...props}
        >
            <IconButton className={s.close} onClick={() => setOpen(false)}>
                <Close />
            </IconButton>
            <ul>
                {menu.map(({ path, icon, text }: MenuModel) => (
                    <li key={path}>
                        <Button component={Link} to={path} variant={getButtonStyleByPath(path)} color='secondary'>
                            <>
                                {icon}
                                {text}
                            </>
                        </Button>
                    </li>
                ))}
            </ul>
            <Divider sx={{ margin: '12px 0 12px' }} />
            <ul>
                {actionsMenu.map(({ path, icon, text, subtext }: MenuModel) => (
                    <li key={path}>
                        <Button component={Link} to={path} color='primary'>
                            <>
                                {icon}
                                <div>
                                    {text} &nbsp;{' '}
                                    <Typography variant='caption' display='block' gutterBottom>
                                        {subtext}
                                    </Typography>
                                </div>
                            </>
                        </Button>
                    </li>
                ))}
            </ul>
            {isAdmin && (
                <>
                    {' '}
                    <Divider sx={{ margin: '12px 0 12px' }} />
                    <ul>
                        {adminMenu.map(({ path, icon, text, subtext }: MenuModel) => (
                            <li key={path}>
                                {path.includes('https://') ? (
                                    <Button href={path} target={'_blank'} color='primary'>
                                        <>
                                            {icon}
                                            <div>
                                                {text} &nbsp;{' '}
                                                <Typography variant='caption' display='block' gutterBottom>
                                                    {subtext}
                                                </Typography>
                                            </div>
                                        </>
                                    </Button>
                                ) : (
                                    <Button component={Link} to={path} color='primary'>
                                        <>
                                            {icon}
                                            <div>
                                                {text} &nbsp;{' '}
                                                <Typography variant='caption' display='block' gutterBottom>
                                                    {subtext}
                                                </Typography>
                                            </div>
                                        </>
                                    </Button>
                                )}
                            </li>
                        ))}
                    </ul>
                </>
            )}
        </aside>
    );
};
