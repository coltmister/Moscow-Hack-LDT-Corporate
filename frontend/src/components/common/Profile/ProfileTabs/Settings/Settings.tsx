import { Checkbox, FormControlLabel, FormGroup, Typography } from '@mui/material';
import React, { useContext, useEffect } from 'react';
import { useGetUserSettingsQuery, useUpdateUserSettingsMutation } from '@/services';
import { useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { UserSettingsDto } from '@/dto';
import { SnackbarContext } from '../../../../../context/SnackbarContext';
import { useAppropriateUserSettings } from '../../../../../hooks/useAppropriateUserSettings';

const Settings = () => {
    const { setSnack } = useContext(SnackbarContext);
    const { isLoading: isSettingsLoading, data } = useAppropriateUserSettings();

    const [updateSettings] = useUpdateUserSettingsMutation();

    const { setValue, register, watch, getValues } = useForm({
        mode: 'onChange',
    });

    useEffect(() => {
        if (data) {
            Object.keys(data as UserSettingsDto).forEach(
                (key) =>
                    key !== 'id' &&
                    setValue(key, data[key], {
                        shouldValidate: true,
                    })
            );
        }
    }, [data]);

    //Без этого не работает
    useEffect(() => {}, [watch()]);

    const checkboxRegister = (name: string) => {
        const data = register(name);
        return { ...data, checked: watch(name) };
    };

    const handleChange = (_e) => {
        updateSettings(getValues()).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Обновлено' });
            }
        });
    };

    return (
        <>
            {!!Object.keys(getValues()).length && !isSettingsLoading && (
                <form onChange={handleChange}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                        <FormGroup className={'my-2'}>
                            <Typography>Приватность:</Typography>
                            <FormControlLabel
                                control={<Checkbox {...checkboxRegister('can_be_invite')} />}
                                label='Разрешить приглашать меня в команды'
                            />
                        </FormGroup>
                        <FormGroup>
                            <Typography>Показывать пользователям:</Typography>
                            <FormControlLabel control={<Checkbox {...checkboxRegister('show_birthdate')} />} label='День рождения' />
                            <FormControlLabel control={<Checkbox {...checkboxRegister('show_biography')} />} label='О себе' />
                            <FormControlLabel control={<Checkbox {...checkboxRegister('show_email')} />} label='Электронная почта' />
                            <FormControlLabel control={<Checkbox {...checkboxRegister('show_interests')} />} label='Интересы' />
                            <FormControlLabel control={<Checkbox {...checkboxRegister('show_phone')} />} label='Телефон' />
                            <FormControlLabel control={<Checkbox {...checkboxRegister('show_sex')} />} label='Пол' />
                            <FormControlLabel control={<Checkbox {...checkboxRegister('show_skills')} />} label='Навыки' />
                            <FormControlLabel
                                control={<Checkbox {...checkboxRegister('show_social_networks')} />}
                                label='Социальные сети'
                            />
                        </FormGroup>
                    </div>
                </form>
            )}
        </>
    );
};

export default Settings;
