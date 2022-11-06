import { ProfileHeader } from './ProfileHeader';
import { ProfileTitle } from './ProfileTitle';
import { ProfileTabs } from './ProfileTabs';

import { MainLayout } from '@/layouts';

export const Profile = () => {
    return (
        <MainLayout contentFullWidth hideFilters>
            <ProfileHeader />
            <ProfileTitle />
            <ProfileTabs />
        </MainLayout>
    );
};
