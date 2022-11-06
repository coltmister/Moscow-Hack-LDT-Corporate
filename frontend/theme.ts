import { createTheme, experimental_sx as sx } from '@mui/material';
import { ruRU } from '@mui/material/locale';

export const theme = createTheme(
    {
        breakpoints: {
            values: {
                xs: 320,
                sm: 576,
                md: 768,
                lg: 992,
                xl: 1398,
            },
        },

        palette: {
            primary: {
                main: '#8ac795',
            },
            background: {
                default: '#f2f2f2',
            },
        },
        typography: {
            fontFamily: 'Russia, Roboto, Arial, sans-serif',
        },
        components: {
            MuiFormLabel: {
                styleOverrides: {
                    root: {
                        '&.Mui-focused': {
                            color: '#8ac795',
                        },
                    },
                },
            },
            MuiInputBase: {
                styleOverrides: {
                    root: {
                        '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                            borderColor: '#8ac795 !important',
                        },
                    },
                },
            },
            MuiButtonBase: {
                defaultProps: {
                    disableRipple: true,
                },
            },
            MuiButton: {
                styleOverrides: {
                    root: {
                        borderRadius: '8px',
                        textTransform: 'inherit',
                        fontSize: 16,
                        transition: 'none',
                        color: '#377e44',

                        '&:focus': {
                            backgroundColor: 'rgba(156, 39, 176, 0.04);',
                        },
                    },
                    contained: {
                        backgroundColor: 'white',
                        boxShadow:
                            '0 1px 1px rgb(0 0 0 / 15%), 0 4px 7px rgb(0 0 0 / 5%), 0 -1px 0 rgb(0 0 0 / 5%), -1px 0 0 rgb(0 0 0 / 5%), 1px 0 0 rgb(0 0 0 / 5%)',
                        '&:hover, &:focus': {
                            backgroundColor: 'white',
                            boxShadow: 'none',
                        },
                    },
                    containedPrimary: {
                        backgroundColor: 'white',
                        '&:hover, &:focus': {
                            backgroundColor: 'white',
                            boxShadow: '0 0px 0px 1px rgb(0 0 0 / 15%)',
                        },
                    },
                    containedSecondary: {
                        backgroundColor: '#8ac795',
                        color: '#fff',
                        '&:hover, &:focus': {
                            backgroundColor: '#8ac795',
                        },
                    },
                    outlinedSecondary: {
                        backgroundColor: '#fff',
                        borderColor: '#fff',
                        '&:hover, &:focus': {
                            color: '#fff',
                            borderColor: '#8ac795',
                            backgroundColor: '#8ac795',
                        },
                    },
                    textError: {
                        color: 'red',
                    },
                },
            },
            MuiPaper: {
                defaultProps: {
                    square: true,
                },
            },
            MuiDialog: {
                styleOverrides: {
                    paper: {
                        boxShadow: 'none',
                    },
                },
            },
            MuiTab: {
                styleOverrides: {},
            },
            MuiTypography: {
                styleOverrides: {
                    body1: {
                        fontSize: 17,
                    },
                },
            },
        },
    },
    ruRU
);
