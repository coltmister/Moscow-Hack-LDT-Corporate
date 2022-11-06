import { Button, Checkbox, Divider, FormControlLabel, Grid, TextField } from '@mui/material';
import s from './styles.module.scss';
import { UserFormResponseDTO } from '@/dto';
import { CustomAutocomplete } from '../../../../ui/Autocomplete';
import { Controller, useForm } from 'react-hook-form';
import classNames from 'classnames';
import React, { Dispatch, SetStateAction, useContext } from 'react';
import { EDUCATION_LEVEL, EMPLOYMENT_TYPES, preprocessDataToSend } from '@/utils';
import { useUpdateUserFormMutation } from '@/services';
import { useUserInfo } from '../../../../../hooks/useUserInfo';
import { SnackbarContext } from '../../../../../context/SnackbarContext';

interface FormEditProps {
    data: UserFormResponseDTO;
    setIsEditing: Dispatch<SetStateAction<boolean>>;
}

const FormEdit = ({ data, setIsEditing }: FormEditProps) => {
    const { control, getValues, watch, handleSubmit } = useForm({ mode: 'onChange', defaultValues: data });
    const { isUserOwnProfile } = useUserInfo();
    const { setSnack } = useContext(SnackbarContext);

    const [request] = useUpdateUserFormMutation();

    const onSubmit = (data: any) => {
        const { id, user, ...dataToPreprocess } = data;
        const dataToSend = preprocessDataToSend(dataToPreprocess);

        request({ id: isUserOwnProfile ? 'me' : user.id, body: dataToSend }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Данные обновлены' });
                setIsEditing(false);
            }
        });
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Divider className={classNames(s.dividerTop, s.divider)} textAlign='left'>
                Общая информация
            </Divider>
            <Grid container direction={'column'} spacing={2}>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => <CustomAutocomplete {...field} hookName={'useGetCountriesQuery'} label={'Гражданство'} />}
                        name={'citizenship'}
                    />
                </Grid>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <FormControlLabel {...field} control={<Checkbox checked={field.value} />} label='Есть ИП или юр.лицо' />
                        )}
                        name={'has_own_company'}
                    />
                </Grid>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <FormControlLabel {...field} control={<Checkbox checked={field.value} />} label='Есть зарегистированные РИД' />
                        )}
                        name={'has_iar'}
                    />
                </Grid>
            </Grid>
            <Divider className={s.divider} textAlign='left'>
                Образование
            </Divider>
            <Grid container direction={'row'} spacing={4}>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <CustomAutocomplete {...field} hookName={'useGetUniversitiesQuery'} label={'Учебное заведение'} />
                        )}
                        name={'education_university'}
                    />
                </Grid>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => <CustomAutocomplete {...field} options={EDUCATION_LEVEL} label={'Уровень образования'} />}
                        name={'education_level'}
                    />
                </Grid>

                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <TextField
                                {...field}
                                sx={{ width: 300 }}
                                type={'number'}
                                min={1900}
                                max={2040}
                                size={'small'}
                                label={'Год окончания'}
                            />
                        )}
                        name={'education_end_year'}
                    />
                </Grid>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => <TextField {...field} sx={{ width: 300 }} size={'small'} label={'Направление обучения'} />}
                        name={'education_speciality'}
                    />
                </Grid>
            </Grid>
            <Divider className={s.divider} textAlign='left'>
                Работа
            </Divider>
            <Grid container direction={'row'} spacing={4}>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => <CustomAutocomplete {...field} options={EMPLOYMENT_TYPES} label={'Тип трудоустройства'} />}
                        name={'employment'}
                    />
                </Grid>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <TextField
                                rows={3}
                                {...field}
                                sx={{ width: '300px' }}
                                type={'number'}
                                min={0}
                                max={90}
                                size={'small'}
                                label={'Опыт работы (лет)'}
                            />
                        )}
                        name={'work_experience'}
                    />
                </Grid>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <TextField rows={3} multiline={true} sx={{ width: '300px' }} {...field} label={'Ваши обязанности'} />
                        )}
                        name={'professional_experience'}
                    />
                </Grid>
            </Grid>
            <Divider className={s.divider} textAlign='left'>
                Командная работа
            </Divider>
            <Grid container direction={'row'} spacing={4}>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <CustomAutocomplete
                                {...field}
                                hookName={'useGetTeamRolesQuery'}
                                multiple={true}
                                label={'Ваша роль в команде'}
                            />
                        )}
                        name={'team_role'}
                    />
                </Grid>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <TextField
                                rows={3}
                                {...field}
                                sx={{ width: '300px' }}
                                type={'number'}
                                min={0}
                                max={90}
                                size={'small'}
                                label={'Опыт участия в хакатонах (лет)'}
                            />
                        )}
                        name={'hack_experience'}
                    />
                </Grid>
            </Grid>
            <Grid className={s.divider} container spacing={2}>
                <Grid item>
                    <Button size={'large'} type={'submit'}>
                        Сохранить
                    </Button>
                </Grid>
                <Grid item>
                    <Button size={'large'} type={'button'} onClick={() => setIsEditing(false)}>
                        Отменить
                    </Button>
                </Grid>
            </Grid>
        </form>
    );
};

export default FormEdit;
