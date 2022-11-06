import { Grid, Typography } from '@mui/material';
import { useGetUserProfileQuery } from '@/services';
import s from './ProfileTitle.module.scss';
import { AdminPanelSettingsRounded, LockRounded, VerifiedRounded } from '@mui/icons-material';

import { useAppropriateUserData } from '../../../../hooks/useAppropriateUserData';

export const ProfileTitle = () => {
    const { data } = useAppropriateUserData();

    return (
        <div className={s.profile}>
            <Grid container spacing={1} alignItems={'center'}>
                <Grid item>
                    <Typography variant='h5' sx={{ fontWeight: 'bold' }}>
                        {data?.user.snp}
                    </Typography>
                </Grid>
                <Grid item>{data?.user.is_verified && <VerifiedRounded sx={{ paddingTop: 1 }} color={'primary'} />}</Grid>
                <Grid item>{data?.user.is_admin && <AdminPanelSettingsRounded sx={{ paddingTop: 1 }} color={'info'} />}</Grid>
                <Grid item>{!data?.user.is_active && <LockRounded sx={{ paddingTop: 1 }} color={'warning'} />}</Grid>
            </Grid>
            {data?.status && (
                <div>
                    <Typography variant='body2' sx={{ fontWeight: 'bold' }}>
                        {data.status}
                    </Typography>
                </div>
            )}
        </div>
    );
};
