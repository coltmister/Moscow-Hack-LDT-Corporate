import { useFormContext } from 'react-hook-form';
import { InputProps, TextField, TextFieldProps } from '@mui/material';

type FormFieldProps = {
    name: string;
    label: string;
    type: string;
} & TextFieldProps;

export const FormField = ({ name, label, type, ...props }: FormFieldProps) => {
    const {
        register,
        formState: { errors },
    } = useFormContext();

    const errorMessage = errors[name]?.message;

    return (
        <TextField
            className='mb-20'
            size='small'
            label={label}
            variant='outlined'
            fullWidth
            required
            type={type}
            error={!!errorMessage}
            helperText={errorMessage?.toString()}
            {...register(name)}
            {...props}
        />
    );
};
