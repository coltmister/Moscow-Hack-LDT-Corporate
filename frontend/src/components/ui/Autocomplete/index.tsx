import { Autocomplete, Box, Grid, TextField, Typography } from '@mui/material';
import React, { useEffect } from 'react';
import { useDebounce } from '../../../hooks/useDebounce/useDebounce';
import { ConstantResponse, constantsService, useGetCountriesQuery } from '../../../services/Constants.service';
import { isEqual } from 'lodash';
import usePrevious from '../../../hooks/usePrevious';

interface CustomAutocompleteProps {
    hookName?:
        | 'useGetStatusesQuery'
        | 'useGetCountriesQuery'
        | 'useGetInterestsQuery'
        | 'useGetSkillsQuery'
        | 'useGetTeamRolesQuery'
        | 'useGetUniversitiesQuery';
    label: string;
    value: ConstantResponse | any;
    onChange: (value: ConstantResponse | null) => void;
    name: string;
    options?: ConstantResponse[];
    multiple: boolean;
    key: any;
}

export const CustomAutocomplete = ({
    hookName,
    value: initialValue,
    onChange,

    name,
    label,
    options: initialOptions = [],
    multiple = false,
}: CustomAutocompleteProps) => {
    const [value, setValue] = React.useState<ConstantResponse | null>(initialValue ?? null);
    const [inputValue, setInputValue] = React.useState('');
    const [options, setOptions] = React.useState<ConstantResponse[]>(initialOptions);

    const debouncedValue = useDebounce(inputValue, 500);

    const { data } = constantsService[hookName ?? 'useGetCountriesQuery'](debouncedValue, { skip: !hookName });

    const previous = usePrevious(value);

    useEffect(() => {
        if (hookName && data) {
            setOptions(data);
        }
    }, [data]);

    useEffect(() => {
        if (!isEqual(previous, value)) {
            onChange(value);
        }
    }, [value, initialValue]);

    return (
        <Autocomplete
            sx={{ width: 300 }}
            getOptionLabel={(option) => (typeof option === 'string' ? option : option.name)}
            filterOptions={(x) => x}
            options={Array.isArray(options) ? options : options.payload}
            autoComplete
            includeInputInList
            size={'small'}
            multiple={multiple}
            placeholder={'Введите текс'}
            filterSelectedOptions
            value={value}
            isOptionEqualToValue={(option, value) => isEqual(option, value)}
            noOptionsText={'Нет вариантов'}
            onChange={(event: any, newValue: any | null) => {
                // setOptions(newValue ? [newValue, ...options] : options);
                setValue(newValue);
            }}
            onInputChange={(event, newInputValue) => {
                setInputValue(newInputValue);
            }}
            renderInput={(params) => <TextField {...params} size={'small'} label={label} fullWidth />}
            renderOption={(props, option) => {
                return (
                    <li {...props}>
                        <Grid container alignItems='center'>
                            <Typography variant='body2' color='text.secondary'>
                                {option.name}
                            </Typography>
                        </Grid>
                    </li>
                );
            }}
        />
    );
};
