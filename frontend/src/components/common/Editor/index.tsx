import { useEffect, useId } from 'react';
import EditorJS, { OutputData } from '@editorjs/editorjs';
import { i18nConfig } from './i18n';
import { EDITOR_JS_TOOLS } from './tools';

interface EditorProps {
    onChange(blocks: OutputData['blocks']): void;
    initialBlocks: OutputData['blocks'];
    placeholder?: string;
}

export const Editor = ({ onChange, initialBlocks, placeholder = 'Введите текст вашей статьи' }: EditorProps) => {
    const id = useId();
    let editor: { isReady: boolean } | EditorJS = { isReady: false };

    useEffect(() => {
        if (!editor.isReady) {
            editor = new EditorJS({
                holder: id,
                data: {
                    blocks: initialBlocks,
                },
                i18n: i18nConfig,
                placeholder: placeholder,
                onChange: async () => {
                    if ('save' in editor) {
                        const { blocks } = await editor.save();
                        onChange(blocks);
                    }
                },
                // @ts-ignore
                tools: EDITOR_JS_TOOLS,
            });
        }
    }, []);

    return <div id={id} />;
};
