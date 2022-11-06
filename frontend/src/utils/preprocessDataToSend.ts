import { isObject } from 'lodash';

export const preprocessDataToSend = (data: any) => {
    const newObj: Record<string, string | number> = {};
    Object.keys(data).forEach((key) => {
        if (Array.isArray(data[key])) {
            newObj[key] = data[key].map(({ id }: { id: string }) => id);
        } else if (isObject(data[key])) {
            if ('getDate' in data[key]) {
                newObj[key] = new Date(data[key])
                    .toLocaleDateString({ year: 'numeric', month: 'numeric', day: '2-digit' })
                    .split('.')
                    .reverse()
                    .join('-');
            } else {
                newObj[key] = data[key].id;
            }
        } else {
            newObj[key] = data[key];
        }
    });
    return newObj;
};
