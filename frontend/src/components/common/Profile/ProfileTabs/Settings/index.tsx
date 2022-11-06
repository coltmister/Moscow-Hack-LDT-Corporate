import { Button, Checkbox, FormControlLabel, FormGroup, Grid, Typography } from '@mui/material';
import { useContext, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { SnackbarContext } from '../../../../../context/SnackbarContext';
import { formControlsLabels } from './labels';
import { useErrorHandling } from '@/hooks';
import { useAppropriateUserSettings } from '../../../../../hooks/useAppropriateUserSettings';
import { useAppropriateUserSettingsMutation } from '../../../../../hooks/useAppropriateUserSettingsMutation';
import { useAppropriateUserData } from '../../../../../hooks/useAppropriateUserData';
import { useAppropriateSecuritySettings } from '../../../../../hooks/useAppropriateSecuritySettings';
import { useAppropriateSecuritySettingsMutation } from '../../../../../hooks/useAppropriateSecuritySettingsMutation';
import Security from './Security';
import { useUserInfo } from '../../../../../hooks/useUserInfo';
import { useParams } from 'react-router-dom';

export const Settings = () => {
    const { setSnack } = useContext(SnackbarContext);

    const { data: userData } = useAppropriateUserData();

    const { id } = useParams();

    const { isUserOwnProfile } = useUserInfo();

    const { setValue, register, watch, getValues } = useForm({
        mode: 'onChange',
    });

    const { isLoading: isSettingsLoading, data, error } = useAppropriateUserSettings();

    const { data: securityData } = useAppropriateSecuritySettings();

    useErrorHandling(error);

    const isAvailableValues = Object.keys(getValues()).length && !isSettingsLoading;

    const [updateSettings] = useAppropriateUserSettingsMutation();

    const [updateSecuritySettings] = useAppropriateSecuritySettingsMutation();

    useEffect(() => {
        if (data) {
            Object.keys(data).forEach(
                (key) =>
                    key !== 'id' &&
                    //@ts-ignore TODO FIX
                    setValue(key, data[key], {
                        shouldValidate: true,
                    })
            );
        }
    }, [data]);

    const checkboxRegister = (name: string) => {
        const data = register(name);
        return { ...data, checked: watch(name) };
    };

    //Без этого не работает
    useEffect(() => {}, [watch()]);

    const handleChange = () => {
        updateSettings({ id: userData?.user.id, body: getValues() }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Обновлено' });
            }
        });
    };

    const handleEndSessions = () => {
        updateSecuritySettings(isUserOwnProfile ? null : id).then((res: any) => {
            if ('data' in res) {
                setSnack({ message: 'Сессии сброшены' });
            }
        });
    };

    if (isAvailableValues) {
        return (
            <form onChange={handleChange}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    <FormGroup className='my-2'>
                        <Grid sx={{ marginBottom: 1 }} container alignItems={'center'} justifyContent={'space-between'}>
                            <Grid item>
                                <Typography fontWeight={'bold'}>Сессии</Typography>
                            </Grid>
                            <Grid item>
                                <Button onClick={handleEndSessions} color={'error'}>
                                    {isUserOwnProfile ? 'Завершить сессии, кроме текущей' : 'Завершить все сессии пользователя'}
                                </Button>
                            </Grid>
                        </Grid>
                        {securityData && <Security data={securityData} />}
                    </FormGroup>
                    <FormGroup className='my-2'>
                        <Typography sx={{ marginBottom: 1 }} fontWeight={'bold'}>
                            Приватность:
                        </Typography>
                        <FormControlLabel
                            control={<Checkbox {...checkboxRegister('can_be_invite')} />}
                            label='Разрешить приглашать меня в команды'
                        />
                    </FormGroup>
                    <FormGroup>
                        <Typography sx={{ marginBottom: 1 }} fontWeight={'bold'}>
                            Показывать пользователям:
                        </Typography>
                        {formControlsLabels.map((el) => (
                            <FormControlLabel key={el.id} control={<Checkbox {...checkboxRegister(el.name)} />} label={el.label} />
                        ))}
                    </FormGroup>
                </div>
            </form>
        );
    }

    return <></>;
};
