import { useForm, FormProvider, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import { LoginValidation } from '@/utils';

import { Button } from '@mui/material';
import { FormField } from '@/components';

import { FormsInterface } from './common';

import s from '../AuthDialog.module.scss';

export const Login = ({ onClick }: FormsInterface) => {
    const form = useForm({
        mode: 'onChange',
        resolver: yupResolver(LoginValidation),
    });

    // TODO: DTO для Логина
    const onSubmit: SubmitHandler<any> = (data) => console.log(data);

    return (
        <FormProvider {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)}>
                <div className={s.items}>
                    <FormField name='email' type='email' label='Почта' />
                    <FormField name='password' type='password' label='Пароль' />
                </div>
                <div className={s.controls}>
                    <Button disabled={!form.formState.isValid} type='submit' color='primary' variant='contained'>
                        Войти
                    </Button>
                    <Button type='button' color='primary' variant='text' onClick={onClick}>
                        Регистрация
                    </Button>
                </div>
            </form>
        </FormProvider>
    );
};
