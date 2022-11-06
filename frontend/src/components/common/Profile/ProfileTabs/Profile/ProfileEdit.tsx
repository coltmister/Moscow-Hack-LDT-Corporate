import { UserProfileResponseDTO } from '@/dto';
import { Controller, useFieldArray, useForm } from 'react-hook-form';
import { useUserInfo } from '../../../../../hooks/useUserInfo';
import React, { Dispatch, SetStateAction, useContext, useMemo } from 'react';
import { SnackbarContext } from '../../../../../context/SnackbarContext';
import { useUpdateUserProfileMutation } from '@/services';
import { preprocessDataToSend, SEX, SOCIAL_NETWORKS, SocialNetworkType } from '@/utils';
import { Button, Divider, Grid, IconButton, TextField } from '@mui/material';
import { CustomAutocomplete } from '../../../../ui/Autocomplete';
import { DatePicker } from '@mui/x-date-pickers';
import s from '../Form/styles.module.scss';
import { AddCircleOutlineRounded, AddCircleRounded, AddRounded, PlusOneRounded, RemoveCircleOutlineRounded } from '@mui/icons-material';

interface ProfileEditProps {
    data: UserProfileResponseDTO;
    setIsEditing: Dispatch<SetStateAction<boolean>>;
}

export const ProfileEdit = ({ setIsEditing, data }: ProfileEditProps) => {
    const { control, getValues, watch, handleSubmit, register } = useForm({ mode: 'onChange', defaultValues: data });

    const { fields, append, prepend, remove, swap, move, insert } = useFieldArray({
        control,
        name: 'social_networks',
    });

    const { isUserOwnProfile } = useUserInfo();
    const { setSnack } = useContext(SnackbarContext);

    const [request] = useUpdateUserProfileMutation();

    const onSubmit = (data: any) => {
        const { id, social_networks, user, ...dataToPreprocess } = data;
        const dataToSend = preprocessDataToSend(dataToPreprocess);
        const dataToSendWithAdditional = { ...dataToSend, user, social_networks };

        request({ id: isUserOwnProfile ? 'me' : user.id, body: dataToSendWithAdditional }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Данные обновлены' });
                setIsEditing(false);
            }
        });
    };

    const getSocialNetworkName = (network_id: SocialNetworkType) => {
        return SOCIAL_NETWORKS.filter(({ name }) => name === network_id)[0].name;
    };

    const SocialNetworkOptions = useMemo(() => {
        return SOCIAL_NETWORKS.filter(
            ({ id }) =>
                !getValues('social_networks')
                    .map(({ network_type }) => network_type)
                    .includes(id as SocialNetworkType)
        );
    }, [watch('social_networks')]);

    return (
        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
            <div>
                <Grid item>
                    <Controller
                        control={control}
                        render={({ field }) => <TextField label={'Статус'} {...field} size={'small'} sx={{ width: 300 }} />}
                        name={'status'}
                    />
                </Grid>
            </div>
            <Divider>Профиль</Divider>
            {/*<div>*/}
            {/*    <Grid container direction={'row'} spacing={4}>*/}
            {/*        <Grid item>*/}
            {/*            <Controller*/}
            {/*                control={control}*/}
            {/*                render={({ field }) => <TextField {...field} sx={{ width: 300 }} size={'small'} label={'Имя'} />}*/}
            {/*                name={'user.name'}*/}
            {/*            />*/}
            {/*        </Grid>*/}
            {/*        <Grid item>*/}
            {/*            <Controller*/}
            {/*                control={control}*/}
            {/*                render={({ field }) => <TextField {...field} sx={{ width: 300 }} size={'small'} label={'Фамилия'} />}*/}
            {/*                name={'user.surname'}*/}
            {/*            />*/}
            {/*        </Grid>*/}
            {/*        <Grid item>*/}
            {/*            <Controller*/}
            {/*                control={control}*/}
            {/*                render={({ field }) => <TextField {...field} sx={{ width: 300 }} size={'small'} label={'Отчество'} />}*/}
            {/*                name={'user.patronymic'}*/}
            {/*            />*/}
            {/*        </Grid>*/}
            {/*    </Grid>*/}
            {/*</div>*/}
            <div>
                <Grid container direction={'row'} spacing={4}>
                    <Grid item>
                        <Controller
                            control={control}
                            render={({ field }) => <CustomAutocomplete {...field} value={field.value} options={SEX} label={'Пол'} />}
                            name={'sex'}
                        />
                    </Grid>
                    <Grid item>
                        <Controller
                            control={control}
                            render={({ field }) => (
                                <DatePicker
                                    label={'День рождения'}
                                    inputFormat={'dd/MM/yyyy'}
                                    disableFuture={true}
                                    renderInput={(props) => <TextField sx={{ width: 300 }} type={'date'} size='small' {...props} />}
                                    {...field}
                                />
                            )}
                            name={'birthdate'}
                        />
                    </Grid>
                </Grid>
            </div>
            <div>
                <Grid container spacing={4}>
                    <Grid item>
                        <Controller
                            control={control}
                            render={({ field }) => (
                                <CustomAutocomplete {...field} hookName={'useGetSkillsQuery'} multiple={true} label={'Навыки'} />
                            )}
                            name={'skills'}
                        />
                    </Grid>
                    <Grid item>
                        <Controller
                            control={control}
                            render={({ field }) => (
                                <CustomAutocomplete {...field} hookName={'useGetInterestsQuery'} multiple={true} label={'Интересы'} />
                            )}
                            name={'interests'}
                        />
                    </Grid>
                </Grid>
            </div>
            <div>
                <Grid container>
                    <Grid item>
                        <Controller
                            control={control}
                            render={({ field }) => <TextField label={'О себе'} {...field} sx={{ width: 300 }} multiline={true} rows={3} />}
                            name={'biography'}
                        />
                    </Grid>
                </Grid>
            </div>
            <Divider>Контакты</Divider>
            <div>
                <Grid container spacing={4}>
                    <Grid item>
                        <Controller
                            control={control}
                            render={({ field }) => <TextField label={'Телефон'} {...field} size={'small'} sx={{ width: 300 }} />}
                            name={'phone'}
                        />
                    </Grid>
                    <Grid item>
                        <Controller
                            control={control}
                            render={({ field }) => <TextField label={'Электронная почта'} {...field} size={'small'} sx={{ width: 300 }} />}
                            name={'email'}
                        />
                    </Grid>
                </Grid>
            </div>
            <Divider>Социальные сети</Divider>
            <div>
                <Grid container spacing={4}>
                    {fields?.map((field, index) => (
                        <Grid key={field.id} item spacing={4}>
                            <Grid container spacing={4} alignItems={'center'}>
                                <Grid item xs={1}>
                                    <IconButton onClick={() => remove(index)} color={'error'}>
                                        <RemoveCircleOutlineRounded sx={{ opacity: 0.7 }} />
                                    </IconButton>
                                </Grid>
                                <Grid item xs={2}>
                                    {getSocialNetworkName(field.network_type)}
                                </Grid>
                                <Grid item>
                                    <TextField
                                        label={'Ссылка или никнейм'}
                                        {...register(`social_networks.${index}.nickname`)}
                                        size={'small'}
                                        sx={{ width: 300 }}
                                    />
                                </Grid>
                            </Grid>
                        </Grid>
                    ))}
                </Grid>
            </div>
            <Grid container alignItems={'center'} spacing={1}>
                <Grid item>
                    <AddCircleOutlineRounded sx={{ marginTop: 1, opacity: 0.7 }} />
                </Grid>
                <Grid item>
                    <CustomAutocomplete
                        label={'Выберите соц.сеть'}
                        options={SocialNetworkOptions}
                        key={watch('social_networks')}
                        onChange={(val) => {
                            return val?.id && append({ network_type: val.id as SocialNetworkType, nickname: '' });
                        }}
                        multiple={false}
                        name={'custom'}
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
