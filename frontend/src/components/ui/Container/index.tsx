import clsx from 'clsx';
import { DetailedHTMLProps, HTMLAttributes } from 'react';

import s from './Container.module.scss';

interface ContainerProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {}

export const Container = ({ children, className, ...props }: ContainerProps) => (
    <div className={clsx(s.container, className)} {...props}>
        {children}
    </div>
);
