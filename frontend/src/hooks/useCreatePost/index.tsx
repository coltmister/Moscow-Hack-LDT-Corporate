import { useParams } from 'react-router-dom';
import { ChangeEvent, FormEvent, useState } from 'react';
import { useCreatePostMutation, useUpdatePostMutation } from '@/services';
import { CreatePostDTO } from '@/dto';
import { isEmpty } from 'lodash';

export const useCreatePost = (data: CreatePostDTO) => {
    const { id } = useParams();

    const [title, setTitle] = useState(data?.title || '');
    const [isLoading, setIsLoading] = useState(false);
    const [blocks, setBlocks] = useState(data?.post_json || '');
    const [createPost] = useCreatePostMutation();
    const [updatePost] = useUpdatePostMutation();

    const onTitleChange = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.currentTarget.value);

    const onCreatePostHandler = async (e: FormEvent) => {
        e.preventDefault();

        try {
            setIsLoading(true);
            const dataToSend: CreatePostDTO = {
                title,
                idea: id,
                description: Array.isArray(blocks) && blocks.filter((el) => el.type === 'paragraph')[0].data.text,
                post_json: blocks,
            };
            if (isEmpty(data)) {
                await createPost({ idea_id: id ?? '', post: dataToSend });
                window.location.reload();
            } else {
                // TODO надо прокинуть {idea_id, post_id, post}
                await updatePost(dataToSend);
            }
        } catch (err) {
            console.warn('Create posts', err);
            alert(err);
        } finally {
            setIsLoading(false);
        }
    };

    return {
        onCreatePost: onCreatePostHandler,
        isLoading,
        title,
        onTitleChange,
        blocks,
        setBlocks,
    };
};
