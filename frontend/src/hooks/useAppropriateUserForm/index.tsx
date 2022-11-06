import { useUserInfo } from '../useUserInfo';
import { useParams } from 'react-router-dom';
import { useGetMyFormQuery, useGetUserFormQuery } from '@/services';

export const useAppropriateUserForm = () => {
    const { isUserOwnProfile, isAdmin } = useUserInfo();
    const { id } = useParams();

    const otherUserData = useGetUserFormQuery(id ?? '', { skip: !id || isUserOwnProfile || !isAdmin });

    const myUserData = useGetMyFormQuery(null, { skip: !isUserOwnProfile });

    return isUserOwnProfile ? myUserData : otherUserData;
};
