import { STORAGE } from '@/utils';
import { useRedirect } from '@/hooks';
import { useEffect, useState } from 'react';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { useAuthCode } from '../useAuthCode';
import { goToAuthPage } from '../../utils/goToAuthPage';
import { useGetMyProfileQuery, useGetUserProfileQuery } from '../../services/User.service';

export const useAuth = () => {
    // index();
    const [params, setParams] = useSearchParams();

    const [isAuth, setIsAuth] = useState(false);
    const [isValidated, setIsValidated] = useState(false);

    const keycloakCode = params.get('code');
    const isRedirectedFromKeycloak = !!keycloakCode;

    const { data: _data } = useGetMyProfileQuery(null, { skip: !isValidated });

    useEffect(() => {
        if (isRedirectedFromKeycloak) {
            try {
                fetch(`https://api.dpir.moscow/api/v1/iam/auth/obtain-tokens/?code=${keycloakCode}&redirect_uri=${window.location.origin}/`)
                    .then((r) => {
                        return r.json();
                    })
                    .then((data) => {
                        params.delete('session_state');
                        params.delete('code');
                        setParams(params);
                        if (data.access_token) {
                            STORAGE.setToken(data.access_token);
                            localStorage.setItem('refresh_token', data.refresh_token);
                        }
                    });
            } catch {
                // localStorage.setItem('token', 's');
            }
            setIsAuth(true);
            setIsValidated(true);
        } else {
            let isAuth = false;

            try {
                isAuth = !!STORAGE.getToken();
                setIsAuth(isAuth);
            } catch (_e) {
                setIsAuth(false);
            }

            setIsValidated(true);

            if (!isAuth) {
                goToAuthPage();
            }
        }
    }, [isRedirectedFromKeycloak, keycloakCode]);

    return { isAuth, isValidated };
};
