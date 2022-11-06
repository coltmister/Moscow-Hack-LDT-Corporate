import { IconButton } from '@mui/material';

import { PostActionsData, PostActionsDataInterface } from './PostActions.data';

import s from './PostActions.module.scss';

export const PostActions = () => {
    return (
        <ul className={s.list}>
            {PostActionsData.map(({ key, item }: PostActionsDataInterface) => (
                <li key={key}>
                    <IconButton>{item}</IconButton>
                </li>
            ))}
        </ul>
    );
};
