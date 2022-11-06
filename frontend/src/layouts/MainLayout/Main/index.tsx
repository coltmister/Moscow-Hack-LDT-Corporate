import clsx from 'clsx';
import { DetailedHTMLProps, HTMLAttributes } from 'react';

interface MainProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {}

export const Main = ({ children, className }: MainProps) => <main className={clsx('content', className)}>{children}</main>;
