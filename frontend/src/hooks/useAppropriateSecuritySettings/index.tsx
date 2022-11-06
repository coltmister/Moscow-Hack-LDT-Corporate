import { useUserInfo } from '../useUserInfo';
import { useParams } from 'react-router-dom';
import {
    useGetMySecuritySettingsQuery,
    useGetMyUserSettingsQuery,
    useGetUserSecuritySettingsQuery,
    useGetUserSettingsQuery,
} from '@/services';

export const useAppropriateSecuritySettings = () => {
    const { isUserOwnProfile, isAdmin } = useUserInfo();
    const { id } = useParams();

    const otherUserData = useGetUserSecuritySettingsQuery(id ?? '', { skip: !id || isUserOwnProfile || !isAdmin });

    const myUserData = useGetMySecuritySettingsQuery(null, { skip: !isUserOwnProfile });

    return isUserOwnProfile ? myUserData : otherUserData;
};
