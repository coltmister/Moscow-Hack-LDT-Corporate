import Grid from '@mui/material/Unstable_Grid2';
import { Avatar, Box, Button, Checkbox, Container, FormControlLabel, TextField, Typography } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { MainLayout } from '../../layouts';
import { Link } from 'react-router-dom';

const Error404Page = () => {
    return (
        <MainLayout>
            <div>Not Found</div>
        </MainLayout>
    );
};

export default Error404Page;
