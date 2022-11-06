import { useState } from 'react';
import { Button } from '@mui/material';
import { AddOutlined as AddIcon, CheckOutlined as CheckIcon } from '@mui/icons-material';

export const FollowButton = () => {
    const [followed, setFollowed] = useState(false);

    const followedHandler = () => setFollowed(!followed);

    return (
        <Button onClick={followedHandler} variant='contained' style={{ minWidth: 30, width: 35, height: 30 }}>
            {!followed ? <AddIcon /> : <CheckIcon style={{ fontSize: 20, color: '#2ea83a' }} />}
        </Button>
    );
};
