import locale from 'date-fns/locale/ru';
import { Route, Routes } from 'react-router-dom';

import { router } from './_router';

import { useAuth } from '@/hooks';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { theme } from '../theme';
import { CircularProgress, ThemeProvider } from '@mui/material';
import { SnackbarProvider } from './context/SnackbarContext';

export const App = () => {
    const { isValidated, isAuth } = useAuth();

    return (
        <SnackbarProvider>
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={locale}>
                <ThemeProvider theme={theme}>
                    <form
                        id='login'
                        action='https://id.dpir.moscow/auth/realms/dpir/protocol/openid-connect/auth'
                        style={{ display: 'none' }}
                    >
                        <input type='hidden' name='client_id' />
                        <input type='hidden' name='response_type' />
                        <input type='hidden' name='scope' />
                        <input type='hidden' name='redirect_uri' />
                    </form>
                    {isValidated && isAuth && (
                        <Routes>
                            {router.map((route, idx) => (
                                <Route key={idx} path={route.path} element={route.component} />
                            ))}
                        </Routes>
                    )}
                    {!isValidated && <CircularProgress className='progress-center' />}
                </ThemeProvider>
            </LocalizationProvider>
        </SnackbarProvider>
    );
};
