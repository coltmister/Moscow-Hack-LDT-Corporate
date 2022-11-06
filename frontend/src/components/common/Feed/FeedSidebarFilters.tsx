import clsx from 'clsx';
import { Button, ButtonGroup, Checkbox, FormControlLabel, FormGroup, Paper } from '@mui/material';

import s from './SidebarFilters.module.scss';
import { Dispatch, SetStateAction } from 'react';

interface FeedSidebarFiltersProps {
    setCategory: Dispatch<SetStateAction<any>>;
}

const categories: Array<{ id: 'new' | 'smart' | 'popular' | 'my_tags' | 'people_choice'; name: string }> = [
    { id: 'new', name: 'Новые' },
    { id: 'smart', name: 'Могут заинтересовать вас' },
    { id: 'popular', name: 'Популярные' },
    { id: 'my_tags', name: 'По моим интересам' },
    { id: 'people_choice', name: 'Выбор людей' },
];

export const FeedSidebarFilters = ({ setCategory }: FeedSidebarFiltersProps) => {
    return (
        <Paper elevation={0} className={clsx(s.filters)}>
            <ButtonGroup fullWidth={true} orientation='vertical' aria-label='vertical contained button group' variant='text'>
                {categories.map((item) => (
                    <Button onClick={() => setCategory(item.id)} key={item.id}>
                        {item.name}
                    </Button>
                ))}
            </ButtonGroup>
        </Paper>
    );
};
