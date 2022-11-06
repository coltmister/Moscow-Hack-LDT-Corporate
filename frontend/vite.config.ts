import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from '@svgr/rollup';

const generateScopedName = '[name]__[local]___[hash:base64:5]';

export default defineConfig({
    plugins: [svgr(), react()],

    css: {
        modules: {
            generateScopedName,
        },
        preprocessorOptions: {
            scss: {
                additionalData: '@import "./src/assets/styles/general/_mixins.scss";',
            },
        },
        devSourcemap: true,
    },

    resolve: {
        alias: [
            { find: '@/ui', replacement: path.resolve(__dirname, './src/components/ui/index.tsx') },
            { find: '@/api', replacement: path.resolve(__dirname, './src/_api/index.ts') },
            { find: '@/layouts', replacement: path.resolve(__dirname, './src/layouts/index.tsx') },
            { find: '@/components', replacement: path.resolve(__dirname, './src/components/common/index.tsx') },
            { find: '@/page-components', replacement: path.resolve(__dirname, './src/components/_page-components/index.tsx') },
            { find: '@/utils', replacement: path.resolve(__dirname, './src/utils/index.tsx') },
            { find: '@/hooks', replacement: path.resolve(__dirname, './src/hooks/index.tsx') },
            { find: '@/dto', replacement: path.resolve(__dirname, './src/types/dto/index.tsx') },
            { find: '@/models', replacement: path.resolve(__dirname, './src/types/models/index.tsx') },
            { find: '@/services', replacement: path.resolve(__dirname, './src/services/index.ts') },
        ],
    },
});
