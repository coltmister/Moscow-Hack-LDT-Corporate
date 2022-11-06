import { useUserInfo } from '../useUserInfo';
import { useParams } from 'react-router-dom';
import {
    useDeleteAllMySessionExceptCurrentMutation,
    useDeleteUserSessionsMutation,
    useGetMyUserSettingsQuery,
    useGetUserSettingsQuery,
    useUpdateMySettingsMutation,
    useUpdateUserSettingsMutation,
} from '@/services';

export const useAppropriateSecuritySettingsMutation = () => {
    const { isUserOwnProfile, isAdmin } = useUserInfo();
    const { id } = useParams();

    const othersRequest = useDeleteUserSessionsMutation();

    const myRequest = useDeleteAllMySessionExceptCurrentMutation();

    return isUserOwnProfile ? myRequest : othersRequest;
};
