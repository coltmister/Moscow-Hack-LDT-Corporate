import clsx from 'clsx';
import { Checkbox, FormControlLabel, FormGroup, Paper } from '@mui/material';

import s from './SidebarFilters.module.scss';

interface SidebarFiltersProps {
    sortDesc: boolean;
    setDesc(b: boolean): void;
    setLimit?(b: boolean): void;
    limit?: boolean;
}

export const SidebarFilters = ({ sortDesc = true, setDesc, setLimit, limit }: SidebarFiltersProps) => {
    return (
        <Paper elevation={0} className={clsx(s.filters)}>
            <FormGroup>
                <FormControlLabel control={<Checkbox checked={sortDesc} onChange={() => setDesc(!sortDesc)} />} label='Сначала новые' />
                {setLimit && (
                    <FormControlLabel control={<Checkbox checked={limit} onChange={() => setLimit(!limit)} />} label='Больше записей' />
                )}
            </FormGroup>
        </Paper>
    );
};
