import { Profile } from '@/components';
import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { useUserInfo } from '../../hooks/useUserInfo';

const ProfilePage = () => {
    const { hash, pathname } = useLocation();
    const navigate = useNavigate();
    const { user } = useUserInfo();

    useEffect(() => {
        //TODO: Пофиксить костыль с ссылкой из меню
        if (pathname.includes('/profile/me')) {
            navigate(`/profile/${user?.id}${hash}`, { replace: true });
        }
    }, [pathname]);

    return <Profile />;
};

export default ProfilePage;
