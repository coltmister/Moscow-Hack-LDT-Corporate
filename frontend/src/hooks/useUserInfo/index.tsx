import { useParams } from 'react-router-dom';
import { useGetMyProfileQuery } from '@/services';
import { useErrorHandling } from '@/hooks';

export const useUserInfo = () => {
    const { id } = useParams();

    const { data, error } = useGetMyProfileQuery();
    useErrorHandling(error);

    const isUserOwnProfile = data?.user.id === id;

    return { isUserOwnProfile, isAdmin: data?.user.is_admin, isVerified: data?.user.is_verified, avatar: data?.avatar, ...data };
};
