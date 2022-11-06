import { useUserInfo } from '../useUserInfo';
import { useParams } from 'react-router-dom';
import { useGetMyProfileQuery, useGetUserProfileQuery } from '@/services';

export const useAppropriateUserData = () => {
    const { isUserOwnProfile } = useUserInfo();
    const { id } = useParams();

    const otherUserData = useGetUserProfileQuery(id ?? '', { skip: !id || isUserOwnProfile });

    const myUserData = useGetMyProfileQuery(null, { skip: !isUserOwnProfile });

    return isUserOwnProfile ? myUserData : otherUserData;
};
