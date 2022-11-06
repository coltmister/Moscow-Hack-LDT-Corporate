import ArticleIcon from '@mui/icons-material/Article';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import GroupsIcon from '@mui/icons-material/Groups';
import ControlPointIcon from '@mui/icons-material/ControlPoint';
import GroupAddIcon from '@mui/icons-material/GroupAdd';
import { ReactNode } from 'react';
import { Dashboard, LightbulbOutlined, PeopleAltRounded } from '@mui/icons-material';
import AllIdeasPage from '../../../_pages/all-ideas';

export interface MenuModel {
    text: string;
    path: string;
    icon: ReactNode;
    subtext?: string;
}

export const menu: MenuModel[] = [
    {
        text: 'Лента',
        icon: <ArticleIcon />,
        path: '/',
    },
    { text: 'Идеи', icon: <LightbulbIcon />, path: '/ideas' },
    { text: 'Вакансии', icon: <GroupsIcon />, path: '/vacancies' },
];

export const actionsMenu: MenuModel[] = [
    {
        text: 'Создать Идею',
        subtext: 'и найти команду',
        icon: <ControlPointIcon />,
        path: '/create-idea',
    },
    { text: 'Заполнить анкету', subtext: 'и присоединиться к идее', icon: <GroupAddIcon />, path: '/profile/me#form' },
];

export const adminMenu: MenuModel[] = [
    {
        text: 'Все пользователи',
        icon: <PeopleAltRounded />,
        path: '/admin/users',
    },
    {
        text: 'Все идеи',
        icon: <LightbulbOutlined />,
        path: '/admin/ideas',
    },
    { text: 'Дашборд', icon: <Dashboard />, path: 'https://dashboard.dpir.moscow/d/M1dqwMvVk/statistika-platformy?orgId=1' },
];
