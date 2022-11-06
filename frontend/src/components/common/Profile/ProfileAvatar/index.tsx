import clsx from 'clsx';
import { ChangeEvent } from 'react';

import { Avatar } from '@mui/material';
import { useUpdateUserAvatarMutation } from '@/services';
import { useUserInfo } from '../../../../hooks/useUserInfo';
import { useAppropriateUserData } from '../../../../hooks/useAppropriateUserData';

import s from './ProfileAvatar.module.scss';

export const ProfileAvatar = () => {
    const { data } = useAppropriateUserData();
    const { isUserOwnProfile } = useUserInfo();
    const [request] = useUpdateUserAvatarMutation();

    const onChangeAvatarHandler = (e: ChangeEvent<HTMLInputElement>) => {
        if (isUserOwnProfile && e.target.files) {
            const formData = new FormData();
            formData.append('file', e.target.files[0]);
            request({ id: isUserOwnProfile ? 'me' : 'id', formData });
        }
    };

    return (
        <label className={s.label}>
            <Avatar sx={{ width: 96, height: 96 }} sizes='m' className={s.avatar} src={data?.avatar} />
            <input onChange={onChangeAvatarHandler} className={clsx('absolute w-full h-full', s.input)} type='file' accept='image/*' />
        </label>
    );
};
