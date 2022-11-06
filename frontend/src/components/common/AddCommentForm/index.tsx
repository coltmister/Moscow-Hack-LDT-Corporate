import { ChangeEvent, FormEvent, useState } from 'react';

import s from './AddCommentForm.module.scss';
import { Button, Input } from '@mui/material';
import { FormProvider, useForm } from 'react-hook-form';
import { FormField } from '../FormField';
import { useCreateCommentMutation, useGetAllCommentsQuery } from '@/services';
import { useParams } from 'react-router-dom';

interface AddCommentFormProps {}

export const AddCommentForm = ({}: AddCommentFormProps) => {
    const id = useParams().id;
    const form = useForm();
    const { handleSubmit } = form;
    const [isClicked, setClicked] = useState<boolean>(false);
    const clickedHandler = () => setClicked(true);
    const [createComment] = useCreateCommentMutation();

    const onSubmitHandler = (data) => {
        createComment({ idea_id: id, comment: { text: data.text, parent: null } });
        form.reset();
        setClicked(false);
    };

    return (
        <FormProvider {...form}>
            <form className={s.textfield} onSubmit={handleSubmit(onSubmitHandler)}>
                <FormField
                    classes={{
                        root: s.fieldRoot,
                    }}
                    placeholder='Написать комментарий...'
                    fullWidth
                    multiline
                    minRows={isClicked ? 5 : 1}
                    onFocus={clickedHandler}
                    label={''}
                    name='text'
                    type='text'
                />
                {isClicked && (
                    <Button type='submit' color='primary' variant='contained' classes={{ root: s.btn }}>
                        Отправить
                    </Button>
                )}
            </form>
        </FormProvider>
    );
};
