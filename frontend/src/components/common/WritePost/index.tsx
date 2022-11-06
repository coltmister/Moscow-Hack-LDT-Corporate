import s from '../WriteForm/WriteForm.module.scss';
import { Button, Input } from '@mui/material';
import { Editor } from '@/components';
import { OutputBlockData } from '@editorjs/editorjs';
import { isEmpty } from 'lodash';
import { useCreatePost } from '@/hooks';
import { CreatePostDTO } from '@/dto';

interface WritePostProps {
    data: CreatePostDTO;
}

export const WritePost = ({ data }: WritePostProps) => {
    const { onCreatePost, title, onTitleChange, blocks, setBlocks, isLoading } = useCreatePost(data);

    return (
        <form className={s.form} onSubmit={onCreatePost}>
            <Input
                value={title}
                onChange={onTitleChange}
                placeholder='Заголовок'
                defaultValue={data.title}
                classes={{ root: s.titleField }}
            />
            <div className={s.editor}>
                <Editor initialBlocks={data.post_json as OutputBlockData[]} onChange={(arr) => setBlocks(arr)} />
            </div>
            <Button
                type='submit'
                disabled={isLoading || (Array.isArray(blocks) && !blocks.length) || !title}
                variant='contained'
                color='primary'
            >
                {data && !isEmpty(data) ? 'Сохранить' : 'Опубликовать'}
            </Button>
        </form>
    );
};
