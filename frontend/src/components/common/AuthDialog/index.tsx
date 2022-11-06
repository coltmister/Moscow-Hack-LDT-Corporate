import clsx from 'clsx';
import { useState } from 'react';

import { ArrowBack } from '@mui/icons-material';
import { Dialog, DialogContent, DialogContentText, Typography } from '@mui/material';

import { Login } from './forms/Login';
import { Main } from './forms/Main';
import { Register } from './forms/Register';

import s from './AuthDialog.module.scss';

export type FormType = 'main' | 'register' | 'login';

export interface AuthDialogInterface {
    onClose?(): void;
    open: boolean;
}

export const AuthDialog = ({ onClose, open }: AuthDialogInterface) => {
    const [formType, setFormType] = useState<FormType>('login');

    const renderComponentMap: Record<FormType, JSX.Element> = {
        main: <Main onClick={() => setFormType('login')} />,
        login: <Login onClick={() => setFormType('register')} />,
        register: <Register onClick={() => setFormType('login')} />,
    };

    const renderTitleMap: Record<FormType, string> = {
        main: 'Вход в TJ',
        login: 'Войти через почту',
        register: 'Зарегистрироваться',
    };

    const onCloseHandler = () => {
        if (onClose) {
            onClose();
        }
    };

    return (
        <Dialog className={clsx(s.dialog)} fullWidth open={open} maxWidth='xs' onClose={onCloseHandler}>
            <DialogContent className={s.root}>
                <DialogContentText className={s.content}>
                    <Typography className={s.title}>
                        <>
                            {renderTitleMap[formType]}
                            {formType !== 'login' && (
                                <button type='button' className={s.back} onClick={() => setFormType('login')}>
                                    <ArrowBack />
                                    Назад
                                </button>
                            )}
                        </>
                    </Typography>

                    {renderComponentMap[formType]}
                </DialogContentText>
            </DialogContent>
        </Dialog>
    );
};
