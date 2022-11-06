import { useForm, FormProvider, SubmitHandler, FieldValues } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import { RegisterValidation } from '@/utils';

import { Button } from '@mui/material';
import { FormField, Datepicker } from '@/components';

import { UserCreateDto } from '@/dto';
import { FormsInterface } from './common';

import s from '../AuthDialog.module.scss';

export const Register = ({ onClick }: FormsInterface) => {
    const form = useForm<UserCreateDto>({
        mode: 'onChange',
        resolver: yupResolver(RegisterValidation),
    });

    const isValid =
        Object.keys(form.getValues()).length === Object.values(form.getValues()).filter((el) => el.length).length &&
        !Object.keys(form.formState.errors).length;

    // TODO: ==CHECK FOR APPROVE== DTO usercreate
    const onSubmit: SubmitHandler<FieldValues> = (data) => console.log(data);

    return (
        <FormProvider {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)}>
                <div className={s.items}>
                    <FormField name='surname' type='text' label='Фамилия' />
                    <FormField name='name' type='text' label='Имя' />
                    <FormField name='lastname' type='text' label='Отчество' />
                    <Datepicker name='birth' type='date' label='Дата рождения' disableFuture />
                    <FormField name='email' type='text' label='Почта' />
                    <FormField name='password' type='password' label='Пароль' />
                    <div className={s.controls}>
                        <Button disabled={!isValid} type='submit' color='primary' variant='contained'>
                            Регистрация
                        </Button>
                        <Button onClick={onClick} color='primary' variant='text' type='button'>
                            Войти
                        </Button>
                    </div>
                </div>
            </form>
        </FormProvider>
    );
};
