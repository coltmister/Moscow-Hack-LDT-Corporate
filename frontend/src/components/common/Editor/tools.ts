import Image from '@editorjs/image';
import Attaches from '@editorjs/attaches';
import { API } from '@/api';
import { STORAGE } from '@/utils';

const token = STORAGE.getToken();

export const EDITOR_JS_TOOLS = {
    image: {
        class: Image,
        config: {
            endpoints: {
                byFile: API.url + `ideas/files/`,
            },
            additionalRequestHeaders: {
                Authorization: `Bearer ${token}`,
            },
        },
    },
    attaches: {
        class: Attaches,
        config: {
            endpoint: API.url + `ideas/files/`,

            additionalRequestHeaders: {
                Authorization: `Bearer ${token}`,
            },
        },
    },
};
