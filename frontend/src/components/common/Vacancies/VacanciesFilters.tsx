import { Alert, Box, FormControlLabel, Paper, Radio, RadioGroup, ToggleButton, ToggleButtonGroup, Typography } from '@mui/material';
import clsx from 'clsx';
import React, { useEffect } from 'react';

import s from './style.module.scss';
import { LightbulbOutlined, PeopleOutlined } from '@mui/icons-material';
import { Controller, useFormContext } from 'react-hook-form';
import { useGetMyTeamsQuery } from '@/services';
import { CustomAutocomplete } from '../../ui/Autocomplete';
import { AlertTitle } from '@mui/lab';

interface VacanciesFiltersProps {}

export const VacanciesFilters = ({}: VacanciesFiltersProps) => {
    const { watch } = useFormContext();

    const { data } = useGetMyTeamsQuery(true, { skip: watch('mode') !== 'ideas' });

    return (
        <Paper elevation={0} sx={{ padding: 2 }} className={clsx(s.filter)}>
            <div>
                <Alert severity='info'>
                    <AlertTitle>Интеллектуальный поиск</AlertTitle>
                    Подберем идеальную команду и сокомандников с помощью <strong>алгоритмов!</strong>
                </Alert>
                <br />
                <Typography sx={{ marginBottom: 1 }} variant={'h6'}>
                    Что вы хотите найти?
                </Typography>
                <Controller
                    name={'mode'}
                    render={({ field }) => (
                        <RadioGroup color='primary' {...field}>
                            <FormControlLabel value='ideas' control={<Radio />} label='Команду' />
                            <FormControlLabel value='people' control={<Radio />} label='Людей в команду' />
                        </RadioGroup>
                    )}
                />

                {watch('mode') === 'people' && (
                    <>
                        <Box sx={{ marginTop: 2 }}>
                            {!data?.length && <Typography color={'error'}>Чтобы отркыть анкеты людей, создайте идею</Typography>}
                            {!!data?.length && (
                                <>
                                    <Typography sx={{ marginBottom: 1 }} variant={'h6'}>
                                        Выберите команду:
                                    </Typography>
                                    <Controller name={'team'} render={({ field }) => <CustomAutocomplete {...field} options={data} />} />
                                </>
                            )}
                        </Box>
                    </>
                )}
            </div>
        </Paper>
    );
};
