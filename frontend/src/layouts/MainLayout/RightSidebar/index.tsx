import clsx from 'clsx';
import { DetailedHTMLProps, HTMLAttributes, useState } from 'react';

import { NavigateNextOutlined as ArrowRightIcon } from '@mui/icons-material';

//TODO: Backend items
import items from '../../../data';

import { CommentItem } from '@/components';

import s from './RightSidebar.module.scss';

interface RightSidebarProps extends DetailedHTMLProps<HTMLAttributes<HTMLElement>, HTMLElement> {
    title: string;
}

export const RightSidebar = ({ className, title = 'Фильтр', children, ...props }: RightSidebarProps) => {
    const [isVisibleComments, setVisibleComments] = useState<boolean>(true);

    const onToggleVisibleHandler = () => setVisibleComments(!isVisibleComments);

    return (
        <aside className={clsx(s.root, !isVisibleComments && s.rotated, className)} {...props}>
            <button type='button' className={s.buttonText} onClick={onToggleVisibleHandler}>
                <b>
                    {title} <ArrowRightIcon />
                </b>
            </button>
            {/* @ts-ignore DTO Model */}
            <div className={s.filters}>{children}</div>
        </aside>
    );
};
