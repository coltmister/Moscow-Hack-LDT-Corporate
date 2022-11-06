import { MainLayout } from '@/layouts';
import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import { useGetAllIdeaCategoriesQuery, useGetAllIdeasQuery } from '../../../services/Admin.service';
import { AllIdeasRow } from '../../common/AllIdeas/Row';
import TablePagination from '@mui/material/TablePagination';
import { IdeaDTO } from '@/dto';

export const AllIdeas = () => {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    const { data: ideas, isLoading: isIdeasLoading } = useGetAllIdeasQuery({ page: page + 1, itemsPerPage: rowsPerPage });

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    return (
        <MainLayout hideFilters contentFullWidth>
            <TableContainer component={Paper}>
                <Table aria-label='collapsible table'>
                    <TableHead>
                        <TableRow>
                            <TableCell />
                            <TableCell>Название</TableCell>
                            <TableCell>Статус</TableCell>

                            <TableCell>Категории</TableCell>
                            <TableCell align='right'>Автор</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {!isIdeasLoading && ideas && ideas?.payload?.map((row: IdeaDTO) => <AllIdeasRow key={row.name} row={row} />)}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                onRowsPerPageChange={handleChangeRowsPerPage}
                component='div'
                count={ideas?.total_count}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
            />{' '}
        </MainLayout>
    );
};

export default AllIdeas;
