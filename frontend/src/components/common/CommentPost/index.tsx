import { useState } from 'react';
import { IconButton, Menu, MenuItem, Paper, Typography } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';

import s from './CommentPost.module.scss';

interface CommentPostProps {
    user: {
        fullname: string;
    };
    text: string;
    post: {
        title: string;
    };
}

export const CommentPost = ({ user, post, text }: CommentPostProps) => {
    const [anchorEl, setAnchorEl] = useState<null>(null);

    const handleClick = (event: any) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <Paper elevation={0} className='p-20' classes={{ root: s.paper }}>
            <Typography variant='h6' className={s.title}>
                <a href='#'>{post.title}</a>
                <IconButton onClick={handleClick}>
                    <MoreVertIcon />
                </IconButton>
            </Typography>
            <Typography className='mt-10 mb-15'>{text}</Typography>

            <Menu id='simple-menu' anchorEl={anchorEl} elevation={3} keepMounted open={Boolean(anchorEl)} onClose={handleClose}>
                <MenuItem onClick={handleClose}>Удалить</MenuItem>
                <MenuItem onClick={handleClose}>Редактировать</MenuItem>
            </Menu>
        </Paper>
    );
};
