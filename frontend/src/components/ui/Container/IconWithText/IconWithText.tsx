import { Grid, Typography } from '@mui/material';
import PublicIcon from '@mui/icons-material/Public';
import { FC, ReactNode } from 'react';
import s from './style.module.scss';

interface IconWithTextProps {
    icon?: ReactNode;
    text: string;
    children: ReactNode;
}

export const IconWithText: FC<IconWithTextProps> = (props) => {
    return (
        <>
            {props.icon ? (
                <Grid className={s.iconWithText} container direction='row' alignItems='center'>
                    <Grid className={s.icon} item>
                        {props.icon}
                    </Grid>
                    <Grid item>
                        <Typography className={s.text}>{props.text}</Typography>
                    </Grid>
                </Grid>
            ) : (
                <Grid className={s.iconWithText} container direction='row' alignItems='center'>
                    <Grid item>
                        <Typography className={s.text}>{props.text}</Typography>
                    </Grid>
                </Grid>
            )}
            {props.children}
        </>
    );
};
