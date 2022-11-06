import { useUserInfo } from '../useUserInfo';
import { useParams } from 'react-router-dom';
import { useGetMyUserSettingsQuery, useGetUserSettingsQuery } from '@/services';

export const useAppropriateUserSettings = () => {
    const { isUserOwnProfile, isAdmin } = useUserInfo();
    const { id } = useParams();

    const otherUserData = useGetUserSettingsQuery(id ?? '', { skip: !id || isUserOwnProfile || !isAdmin });

    const myUserData = useGetMyUserSettingsQuery(null, { skip: !isUserOwnProfile });

    return isUserOwnProfile ? myUserData : otherUserData;
};
