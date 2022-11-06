import { isEmpty } from 'lodash';
import { useParams } from 'react-router-dom';
import { ChangeEvent, FormEvent, useState } from 'react';

import { CreateIdeaDto, IdeaModel } from '@/dto';
import { useCreateIdeaMutation, useUpdateIdeaMutation } from '@/services';

export const useCreateIdea = (data: CreateIdeaDto) => {
    const { id } = useParams();

    const [title, setTitle] = useState(data?.title || '');
    const [isLoading, setIsLoading] = useState(false);
    const [blocks, setBlocks] = useState(data?.idea_json || '');
    const [createIdea] = useCreateIdeaMutation();
    const [updateIdea] = useUpdateIdeaMutation();

    const onTitleChange = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.currentTarget.value);

    const onCreatePostHandler = async (e: FormEvent) => {
        e.preventDefault();

        try {
            setIsLoading(true);
            const dataToSend: CreateIdeaDto | IdeaModel = {
                title,
                description: Array.isArray(blocks) && blocks.filter((el) => el.type === 'paragraph')[0].data.text,
                idea_json: blocks,
            };
            if (isEmpty(data)) {
                const idea = await createIdea(dataToSend);
                window.location.assign('/ideas/' + idea.data.id);
            } else {
                await updateIdea({ ...dataToSend, id });
                window.location.assign('/ideas/' + id);
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
