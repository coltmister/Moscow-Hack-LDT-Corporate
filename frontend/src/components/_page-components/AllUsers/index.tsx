import { MainLayout } from '@/layouts';
import React from 'react';
import { useGetAllIdeasQuery, useGetAllUsersQuery } from '../../../services/Admin.service';
import TableContainer from '@mui/material/TableContainer';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';
import TableBody from '@mui/material/TableBody';
import { IdeaDTO } from '@/dto';
import { AllIdeasRow } from '../../common/AllIdeas/Row';
import TablePagination from '@mui/material/TablePagination';
import { AllUsersRow } from '../../common/AllUsers/Row';

export const AllUsers = () => {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    const { data: users, isLoading: isUsersLoading } = useGetAllUsersQuery({ page: page + 1, itemsPerPage: rowsPerPage });

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
                            <TableCell>Пользователь</TableCell>
                            <TableCell>Статус</TableCell>
                            <TableCell>Подтвержден</TableCell>
                            <TableCell>Администратор</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {!isUsersLoading && users && users?.payload?.map((row: IdeaDTO) => <AllUsersRow key={row.name} row={row} />)}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                onRowsPerPageChange={handleChangeRowsPerPage}
                component='div'
                count={users?.total_count}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
            />
        </MainLayout>
    );
};

export default AllUsers;
