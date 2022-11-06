import { Button, Divider, Input, Slider, TextField, Typography } from '@mui/material';
import { Editor } from '@/components';

import s from './WriteForm.module.scss';

import { CreateIdeaDto, IdeaModel } from '@/dto';
import { useCreateIdea } from '@/hooks';
import { OutputBlockData } from '@editorjs/editorjs';
import { isEmpty } from 'lodash';
import { useState } from 'react';
import { useUpdateInfoMutation } from '@/services';
import { useParams } from 'react-router-dom';

interface WriteFormProps {
    data: CreateIdeaDto | IdeaModel;
    mode: 'update' | 'create';
}

export const WriteForm = ({ data, mode = 'create' }: WriteFormProps) => {
    const params = useParams();
    const { onCreatePost, title, onTitleChange, blocks, isLoading, setBlocks } = useCreateIdea(data as CreateIdeaDto);

    const [budget, setBudget] = useState('');
    const [progress, setProgress] = useState(0);

    const [updateInfo] = useUpdateInfoMutation();

    const handleSubmit = (e: React.FormEvent<Element>) => {
        if (mode === 'update' && params?.id) {
            updateInfo({ ideaId: params.id, body: { budget, progress } });
        }
        onCreatePost(e);
    };

    return (
        <form className={s.form} onSubmit={handleSubmit}>
            <Input
                value={title}
                onChange={onTitleChange}
                placeholder='Заголовок'
                defaultValue={data.title}
                classes={{ root: s.titleField }}
            />
            <div className={s.editor}>
                <Editor initialBlocks={data.idea_json as OutputBlockData[]} onChange={(arr) => setBlocks(arr)} />
            </div>
            {mode === 'update' && (
                <>
                    <br />

                    <Divider>Дополнительно</Divider>
                    <br />
                    <div>
                        <TextField
                            type={'number'}
                            onChange={(e) => setBudget(e.target.value)}
                            size={'small'}
                            fullWidth={true}
                            label={'Размер инвестиций (в руб.)'}
                        />
                    </div>
                    <br />
                    <div>
                        <Typography variant={'body2'}>Оцените готовность идеи</Typography>
                        <Slider defaultValue={progress} value={progress} onChange={(_e, v) => setProgress(v)} />
                    </div>
                    <br />
                    <Button
                        type='submit'
                        disabled={isLoading || (Array.isArray(blocks) && !blocks.length) || !title}
                        variant='contained'
                        color='primary'
                    >
                        {data && !isEmpty(data) ? 'Сохранить' : 'Опубликовать'}
                    </Button>
                </>
            )}
        </form>
    );
};
