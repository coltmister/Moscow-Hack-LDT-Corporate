import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export const useRedirect = (reason: boolean, route: string) => {
    const navigate = useNavigate();
    useEffect(() => {
        if (reason) {
            navigate(route, { replace: true });
        }
    }, [reason]);
};
