import { MouseEvent, useState } from 'react';

import { Avatar, IconButton, Menu, MenuItem, Typography } from '@mui/material';
import MoreIcon from '@mui/icons-material/MoreHorizOutlined';

import s from './Comment.module.scss';
import { UserResponseDto } from '@/dto';

export interface CommentPostProps {
    id: number;
    // TODO: CommentDto?
    comment: any;
    currentUserId: number;
    onRemove(id: number): void;
}

export const Comment = ({ id, comment, currentUserId, onRemove }: CommentPostProps) => {
    const [anchorEl, setAnchorEl] = useState<Element | null>(null);

    const handleClick = (event: MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget);
    const handleClose = () => setAnchorEl(null);

    return (
        <div className={s.comment}>
            <div className={s.userInfo}>
                {/*<Avatar style={{ marginRight: 10 }}>{user.fullName[0]}</Avatar>*/}
                <b>{comment.name}</b>
                {/*<span>{createdAt}</span>*/}
            </div>
            <Typography className={s.text}>{comment.body}</Typography>
            {/*{user.id === currentUserId && (*/}
            {/*    <>*/}
            {/*        <span className={s.replyBtn}>Ответить</span>*/}
            {/*        <IconButton onClick={handleClick}>*/}
            {/*            <MoreIcon />*/}
            {/*        </IconButton>*/}
            {/*        <Menu anchorEl={anchorEl} elevation={2} open={Boolean(anchorEl)} onClose={handleClose} keepMounted>*/}
            {/*            <MenuItem onClick={() => onRemove(id)}>Удалить</MenuItem>*/}
            {/*            <MenuItem onClick={handleClose}>Редактировать</MenuItem>*/}
            {/*        </Menu>*/}
            {/*    </>*/}
            {/*)}*/}
        </div>
    );
};
