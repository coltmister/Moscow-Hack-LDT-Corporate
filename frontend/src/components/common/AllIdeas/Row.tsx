import { Avatar, Box, Chip, Collapse, Divider, Grid, IconButton, Table, TableCell, TableHead, TableRow, Typography } from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { useContext, useState } from 'react';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { Link } from 'react-router-dom';
import { CustomAutocomplete } from '../../ui/Autocomplete';
import {
    useGetAllIdeaCategoriesQuery,
    useGetIdeaSuggestedCategoriesQuery,
    useUpdateIdeaCategoriesMutation,
    useUpdateIdeaStatusMutation,
} from '../../../services/Admin.service';
import { SnackbarContext } from '../../../context/SnackbarContext';
import { isEqual } from 'lodash';

export const AllIdeasRow = ({ row }) => {
    const [open, setOpen] = useState(false);
    const { data: categories, isLoading: isCategoriesLoading } = useGetAllIdeaCategoriesQuery(null);
    const { data: suggestedCategories, isLoading: isSuggestedCategoriesLoading } = useGetIdeaSuggestedCategoriesQuery(row.id, {
        skip: !open,
    });

    const { setSnack } = useContext(SnackbarContext);

    const [updateCategory] = useUpdateIdeaCategoriesMutation();

    const [updateIdeaStatus] = useUpdateIdeaStatusMutation();

    const handleUpdateCategory = (categories) => {
        if (!isEqual(categories, row.category)) {
            updateCategory({ ideaId: row.id, categories: categories.map(({ id }) => id) }).then((res) => {
                if ('data' in res) {
                    setSnack({ message: 'Категории обновлены' });
                }
            });
        }
    };

    const handleUpdateIdeaStatus = (status) => {
        if (!isEqual(status, row.status)) {
            updateIdeaStatus({ ideaId: row.id, status: status.status }).then((res) => {
                if ('data' in res) {
                    setSnack({ message: 'Категории обновлены' });
                }
            });
        }
    };

    return (
        <>
            {' '}
            <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
                <TableCell>
                    <IconButton aria-label='expand row' size='small' onClick={() => setOpen(!open)}>
                        {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell component='th' scope='row'>
                    {row.title}
                </TableCell>
                <TableCell component='th' scope='row'>
                    {row.status.name}
                </TableCell>
                <TableCell component='th' scope='row'>
                    <Grid container spacing={1}>
                        {row.category.map((item: any) => (
                            <Grid key={item.id} item>
                                <Chip size={'small'} key={item.id} label={item.name}></Chip>
                            </Grid>
                        ))}
                    </Grid>
                </TableCell>
                <TableCell align='right'>
                    {' '}
                    <Link style={{ display: 'flex', alignItems: 'center', gap: 8 }} to={`/profile/${row.author.id}`}>
                        <Avatar style={{ width: 24, height: 24 }} src={row.author.avatar_thumbnail} /> {row.author.snp}
                    </Link>
                </TableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0, backgroundColor: '#FAFAFA' }} colSpan={6}>
                    <Collapse in={open} timeout='auto' unmountOnExit>
                        <Box sx={{ margin: 1 }}>
                            <Typography variant='h6' gutterBottom component='div'>
                                Управление идеей
                            </Typography>
                            <br />
                            <CustomAutocomplete
                                label='Изменить статус'
                                hookName={'useGetStatusesQuery'}
                                value={row.status}
                                onChange={handleUpdateIdeaStatus}
                            />
                            <br />
                            <Divider>Работа с категориями</Divider>
                            <br />
                            <Grid container spacing={2}>
                                <Grid item>
                                    <CustomAutocomplete
                                        label='Категории идеи'
                                        options={categories}
                                        value={row.category}
                                        multiple={true}
                                        onChange={handleUpdateCategory}
                                    />
                                </Grid>

                                <Grid item>
                                    {!isSuggestedCategoriesLoading && (
                                        <Grid container>
                                            {suggestedCategories && suggestedCategories?.length ? (
                                                suggestedCategories?.map((item) => (
                                                    <Grid key={item.id} item>
                                                        <Chip size={'small'} key={item.id} label={item.name}></Chip>
                                                    </Grid>
                                                ))
                                            ) : (
                                                <Typography sx={{ padding: 1, alignText: 'center' }} variant={'caption'}>
                                                    Пока что рекомендаций нет
                                                </Typography>
                                            )}
                                        </Grid>
                                    )}
                                </Grid>
                            </Grid>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </>
    );
};
