import { FormProvider, useFieldArray, useForm } from 'react-hook-form';
import { FormField } from '../../FormField';
import { useParams } from 'react-router-dom';
import { Button, Chip, Grid, IconButton, SelectChangeEvent, TextField } from '@mui/material';
import s from './CreateTeamForm.module.scss';
import { ideasService, useCreateTeamMutation, useGetIdeaByIdQuery } from '@/services';
import React, { useContext, useState } from 'react';
import { SnackbarContext } from '../../../../context/SnackbarContext';
import { AddCircleOutlineRounded, RemoveCircleOutlineRounded } from '@mui/icons-material';
import { CustomAutocomplete } from '../../../ui/Autocomplete';

export const CreateTeamForm = () => {
    const { id } = useParams();
    const form = useForm({ mode: 'onChange' });
    const { control, watch, handleSubmit, register } = form;

    const { fields, append, remove } = useFieldArray({
        control,
        name: 'required_members',
    });

    const { data, isLoading, refetch } = useGetIdeaByIdQuery(id);

    const [createTeam] = useCreateTeamMutation();

    const { setSnack } = useContext(SnackbarContext);

    const onSubmit = (data) => {
        createTeam(data).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Команда успешно создана' });
                refetch();
            }
        });
    };

    return (
        <FormProvider {...form}>
            <form className={s.form} onSubmit={handleSubmit(onSubmit)}>
                <FormField hidden name='idea' label='id идеи' type='hidden' value={id} />
                <FormField name='name' label='Название команды' type='text' />
                <FormField name='description' label='Краткое описание' rows={3} multiline type='text' />

                <div>
                    <Grid container spacing={4}>
                        {fields?.map((field, index) => (
                            <Grid key={field.id} item spacing={4}>
                                <Grid container spacing={4} alignItems={'center'}>
                                    <Grid item xs={6}>
                                        <TextField
                                            label={'Необходимое количество'}
                                            {...register(`required_members.${index}.amount`)}
                                            size={'small'}
                                            type={'number'}
                                            min={1}
                                            sx={{ width: 'auto' }}
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Chip size={'small'} onDelete={() => remove(index)} label={field.name}></Chip>
                                    </Grid>
                                </Grid>
                            </Grid>
                        ))}
                    </Grid>
                </div>
                <Grid container alignItems={'center'} spacing={1}>
                    <Grid item>
                        <CustomAutocomplete
                            label={'Выберите роль'}
                            onChange={(val) => {
                                return (
                                    val?.id &&
                                    !fields.filter((field) => field.name === val.name).length &&
                                    append({ ...val, amount: 0, role: val.id })
                                );
                            }}
                            hookName={'useGetTeamRolesQuery'}
                            multiple={false}
                            name={'custom'}
                            key={watch('required_members')}
                        />
                    </Grid>
                </Grid>

                <Button type='submit' variant='contained' color='secondary'>
                    Создать команду
                </Button>
            </form>
        </FormProvider>
    );
};
