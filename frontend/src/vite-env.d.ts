// <reference types="vite/client" />
declare module '*.scss' {
    const content: Record<string, string>;
    export default content;
}

declare module '*.svg' {
    import React from 'react';
    export const ReactComponent: React.FC<React.SVGProps<SVGSVGElement>>;
    const src: string;
    export default src;
}

declare module '@editorjs/image' {}
declare module '@editorjs/attaches' {}
