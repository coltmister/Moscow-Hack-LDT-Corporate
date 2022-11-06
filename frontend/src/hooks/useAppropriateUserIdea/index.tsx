import { useUserInfo } from '../useUserInfo';
import { useParams } from 'react-router-dom';
import { useGetMyIdeasQuery, useGetUserIdeasQuery } from '@/services';

export const useAppropriateUserIdea = () => {
    const { isUserOwnProfile, isAdmin } = useUserInfo();
    const { id } = useParams();

    const otherUserData = useGetUserIdeasQuery(id ?? '', { skip: !id || isUserOwnProfile || !isAdmin });

    const myUserData = useGetMyIdeasQuery(null, { skip: !isUserOwnProfile });

    return isUserOwnProfile ? myUserData : otherUserData;
};
