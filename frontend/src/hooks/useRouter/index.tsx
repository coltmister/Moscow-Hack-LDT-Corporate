import { useLocation, useParams } from 'react-router-dom';
import { useMemo } from 'react';
import queryString from 'query-string';

export const useRouter = () => {
    const params = useParams();
    const location = useLocation();
    return useMemo(() => {
        return {
            pathname: location.pathname,
            query: {
                ...queryString.parse(location.search),
                ...params,
            },
            location,
        };
    }, [params, location, history]);
};
