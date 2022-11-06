import { ProfileEdit } from './ProfileEdit';
import { ProfileView } from './ProfileView';
import { useGetUserProfileQuery } from '@/services';
import { useUserInfo } from '../../../../../hooks/useUserInfo';
import { useState } from 'react';
import { useAppropriateUserData } from '../../../../../hooks/useAppropriateUserData';

const ProfileTab = () => {
    const { data } = useAppropriateUserData();
    const [isEditing, setIsEditing] = useState(false);
    return (
        <>
            {data && isEditing && <ProfileEdit data={data} setIsEditing={setIsEditing} />}
            {data && !isEditing && <ProfileView data={data} setIsEditing={setIsEditing} />}
        </>
    );
};

export default ProfileTab;
