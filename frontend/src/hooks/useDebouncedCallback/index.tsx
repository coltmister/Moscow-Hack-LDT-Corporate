import { useCallback, useRef } from 'react';

export const useDebouncedCallback = <T,>(callback: Function, delay: number, dependencies?: unknown[]) => {
    const timeout = useRef<NodeJS.Timeout>();

    const comboDeps = dependencies ? [callback, delay, ...dependencies] : [callback, delay];

    return useCallback((...args: T[]) => {
        if (timeout.current != null) {
            clearTimeout(timeout.current);
        }

        timeout.current = setTimeout(() => {
            callback(...args);
        }, delay);
    }, comboDeps);
};
