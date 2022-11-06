import clsx from 'clsx';
import { DetailedHTMLProps, HTMLAttributes } from 'react';

import { ProfileAvatar } from '../ProfileAvatar';

import s from './ProfileHeader.module.scss';

interface ProfileHeaderProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {}

export const ProfileHeader = ({ className, ...props }: ProfileHeaderProps) => {
    return (
        <div className={clsx(s.header, className)} {...props}>
            <ProfileAvatar />
        </div>
    );
};
