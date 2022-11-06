import { nothingToNull } from './nothingToNull';

class StorageAdapter {
    public readonly VERSION = '1.0.0-SNAPSHOT';

    private storage = new Map<string, any>();

    private readonly getFromStore = <T>(key: string) => {
        const storedObjectWrapperJson = nothingToNull(window.localStorage.getItem(key));

        if (storedObjectWrapperJson) {
            try {
                const storedObjectWrapper = JSON.parse(storedObjectWrapperJson) as {
                    version: string;
                    object: T;
                };

                if (storedObjectWrapper.version != this.VERSION) {
                    window.localStorage.removeItem(key);
                    return null;
                } else {
                    return storedObjectWrapper.object;
                }
            } catch (error) {
                return null;
            }
        } else {
            return null;
        }
    };

    private readonly store = <T>(key: string, object: T) =>
        window.localStorage.setItem(key, JSON.stringify(this.createVersionWrapper(object)));

    private createVersionWrapper = <T>(object: T) => ({
        version: this.VERSION,
        object: object,
    });

    public setToken = (token: string): void => {
        window.localStorage.setItem('token', token);
    };

    public deleteToken = (): void => {
        window.localStorage.removeItem('token');
    };

    public getToken = (): string | null => {
        if (typeof window !== 'undefined') {
            return window.localStorage.getItem('token');
        }
        return null;
    };

    public clear = (): void => {
        window.localStorage.clear();
        window.location.assign('/');
    };
}

export const STORAGE = new StorageAdapter();
