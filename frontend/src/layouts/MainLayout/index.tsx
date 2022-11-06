import clsx from 'clsx';
import { DetailedHTMLProps, HTMLAttributes, useRef, useState, KeyboardEvent, useEffect, ReactNode } from 'react';

import { CssBaseline } from '@mui/material';
import { Header } from './Header';
import { Main } from './Main';
import { LeftSidebar } from './LeftSidebar';
import { RightSidebar } from './RightSidebar';

import s from './MainLayout.module.scss';
import { useIsLarge } from '@/hooks';

interface MainLayoutProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    hideFilters?: boolean;
    hideMenu?: boolean;
    contentFullWidth?: boolean;
    sidebarTitle?: string;
    sidebarNode?: ReactNode;
}

export const MainLayout = ({
    children,
    className,
    hideMenu,
    hideFilters,
    contentFullWidth,
    sidebarTitle,
    sidebarNode,
    ...props
}: MainLayoutProps) => {
    const isLarge = useIsLarge();
    const [isSkip, setSkip] = useState<boolean>(false);
    const [isOpenNavigation, setIsOpenNavigation] = useState(false);
    const bodyRef = useRef<HTMLDivElement>(null);

    const skipContentAction = (key: KeyboardEvent) => {
        if (key.code === 'Space' || key.code === 'Enter') {
            key.preventDefault();
            bodyRef.current?.focus();
        }

        setSkip(false);
    };

    useEffect(() => {
        setIsOpenNavigation(isLarge);
    }, [isLarge]);

    return (
        <>
            <Header isOpenMenu={isOpenNavigation} setMenu={setIsOpenNavigation} />
            <CssBaseline />
            <div className={clsx('wrapper', contentFullWidth && 'content--full', isOpenNavigation && s.menuOpen, className)} {...props}>
                <a
                    onFocus={() => setSkip(true)}
                    onBlur={() => setSkip(false)}
                    onKeyDown={skipContentAction}
                    tabIndex={0}
                    className={clsx(s.skip, isSkip && s.displayed)}
                >
                    Сразу к содержанию
                </a>
                <LeftSidebar isOpen={isOpenNavigation} setOpen={setIsOpenNavigation} />
                <Main>{children}</Main>
                <RightSidebar title={sidebarTitle ?? ''} className={clsx(hideFilters && s.hide)}>
                    {sidebarNode}
                </RightSidebar>
            </div>
        </>
    );
};
