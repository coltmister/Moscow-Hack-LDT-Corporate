import { Paper, Typography } from '@mui/material';

interface TeamInvitationsProps {
    data: any;
}

export const TeamInvitations = ({ data }: TeamInvitationsProps) => {
    return <div>{!!data.length ? <Paper sx={{ padding: 2 }}></Paper> : <Typography sx={{ padding: 24 }}>Приглашений нет</Typography>}</div>;
};
