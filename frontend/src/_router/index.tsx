import { ReactNode } from 'react';
import { Error404Page, IndexPage, AuthPage, CreateIdeaPage, ProfilePage, IdeasPage, IdeaPage, PostPage } from '../_pages/pages-list';
import VacanciesPage from '../_pages/vacancies';
import AllIdeasPage from '../_pages/all-ideas';
import AllUsersPage from '../_pages/all-users';

interface RouterModel {
    path: string;
    component: ReactNode;
}

export const router: RouterModel[] = [
    {
        path: '*',
        component: <Error404Page />,
    },
    {
        path: '/',
        component: <IndexPage />,
    },
    {
        path: '/auth',
        component: <AuthPage />,
    },
    {
        path: '/create-idea',
        component: <CreateIdeaPage />,
    },
    {
        path: '/profile/me',
        component: <ProfilePage />,
    },
    {
        path: '/profile/:id',
        component: <ProfilePage />,
    },
    {
        path: '/ideas',
        component: <IdeasPage />,
    },
    {
        path: '/vacancies',
        component: <VacanciesPage />,
    },
    {
        path: '/ideas/:id',
        component: <IdeaPage />,
    },
    {
        path: '/admin/ideas',
        component: <AllIdeasPage />,
    },
    {
        path: '/admin/users',
        component: <AllUsersPage />,
    },
    {
        path: '/posts/:id',
        component: <PostPage />,
    },
];
