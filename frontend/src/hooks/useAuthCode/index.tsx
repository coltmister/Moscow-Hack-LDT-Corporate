import { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { debounce } from '../../utils/debounce';
import { STORAGE } from '../../utils/StorageAdapter';

export const useAuthCode = () => {
    const [params, setParams] = useSearchParams();
    const [wasSent, setWasSent] = useState(false);

    useEffect(() => {
        const code = params.get('code');

        const fn = async () => {
            if (code && !wasSent) {
                setWasSent(true);
                try {
                    fetch(`https://api.dpir.moscow/api/v1/iam/auth/obtain-tokens/?code=${code}&redirect_uri=${window.location.origin}`, {})
                        .then((r) => {
                            return r.json();
                        })
                        .then((data) => {
                            document.write(JSON.stringify(data, null, 4));
                        });
                    // STORAGE.setToken(data.token);
                    // localStorage.setItem('refresh_token', data.token);
                } catch {
                    localStorage.setItem('token', 's');
                }
            }
        };
        if (code) {
            params.delete('code');
            setParams(params);
        }
    }, [params.get('code'), wasSent]);
};
