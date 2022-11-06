import { useUserInfo } from '../useUserInfo';
import { useParams } from 'react-router-dom';
import { useGetMyUserSettingsQuery, useGetUserSettingsQuery, useUpdateMySettingsMutation, useUpdateUserSettingsMutation } from '@/services';

export const useAppropriateUserSettingsMutation = () => {
    const { isUserOwnProfile, isAdmin } = useUserInfo();
    const { id } = useParams();

    const othersRequest = useUpdateUserSettingsMutation();

    const myRequest = useUpdateMySettingsMutation();

    return isUserOwnProfile ? myRequest : othersRequest;
};
