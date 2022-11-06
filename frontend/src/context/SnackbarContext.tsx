import { createContext, FC, useState } from 'react';
import { Snackbar, SnackbarCloseReason, SnackbarProps } from '@mui/material';

export interface SnackbarContextInterface {
    setSnack: (props: SnackbarProps) => void;
}

export const SnackbarContext = createContext<SnackbarContextInterface>({} as SnackbarContextInterface);

export const SnackbarProvider: FC<SnackbarProps> = ({ children }) => {
    const [snack, setSnack] = useState<SnackbarProps>({
        message: '',
        color: '',
        open: false,
    });

    const handleSetSnack = ({
        anchorOrigin = { horizontal: 'right', vertical: 'top' },
        open = true,
        onClose = handleClose,
        autoHideDuration = 2000,
        ...rest
    }: SnackbarProps) => {
        setSnack({ anchorOrigin, autoHideDuration, open, onClose, ...rest });
    };

    const handleClose = (event: React.SyntheticEvent<any> | Event, reason: SnackbarCloseReason) => {
        if (snack.onClose) {
            snack.onClose(event, reason);
        } else {
            setSnack((prev) => ({ ...prev, open: false }));
        }
    };

    return (
        <SnackbarContext.Provider value={{ setSnack: handleSetSnack }}>
            <Snackbar {...snack} />
            {children}
        </SnackbarContext.Provider>
    );
};
