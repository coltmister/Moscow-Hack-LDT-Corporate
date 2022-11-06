import { useFormContext } from 'react-hook-form';
import { DatePicker } from '@mui/x-date-pickers';

import { TextField } from '@mui/material';

const dateFormat = 'dd/MM/yyyy';

interface DatepickerProps {
    name: string;
    label: string;
    type: string;
    disableFuture: boolean;
}

export const Datepicker = ({ name, label, type, disableFuture = false }: DatepickerProps) => {
    const {
        register,
        formState: { errors },
        watch,
        setValue,
    } = useFormContext();

    const errorMessage = errors[name]?.message;

    return (
        <DatePicker
            label={label}
            inputFormat={dateFormat}
            disableFuture={disableFuture}
            renderInput={(props) => (
                <TextField type={type} size='small' {...props} helperText={errorMessage?.toString()} error={!!errorMessage} />
            )}
            {...register(name)}
            value={watch(name)}
            onChange={(value) => setValue(name, value)}
        />
    );
};
