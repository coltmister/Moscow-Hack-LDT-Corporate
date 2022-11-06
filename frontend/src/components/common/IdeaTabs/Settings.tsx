import { Alert, Button, Checkbox, Chip, Divider, FormControlLabel, TextField, Typography } from '@mui/material';
import { useGetIdeaByIdQuery, useUpdateIdeaMutation, useUpdateIdeaSettingsByIdMutation } from '@/services';
import { useParams } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { formControlsLabels } from './labels';
import { useForm } from 'react-hook-form';
import { SnackbarContext } from '../../../context/SnackbarContext';

interface SettingsTabProps {
    isUserIdeaOwner: boolean;
    data: any;
}
export const SettingsTab = ({ isUserIdeaOwner, data }: SettingsTabProps) => {
    const id = useParams().id;

    const { setSnack } = useContext(SnackbarContext);

    const { setValue, register, watch, getValues } = useForm({
        mode: 'onChange',
    });

    const [updateSettings] = useUpdateIdeaSettingsByIdMutation();

    const { data: ideaData } = useGetIdeaByIdQuery(id);
    const [comment, setComment] = useState('');
    const onChange = (e, value) => {
        setComment(value);
    };
    const sendToModeration = () => {
        //Логика отправки на модерацию (можно не посылать status, а только коммент)
    };

    //Без этого не работает
    useEffect(() => {}, [watch()]);

    const handleChange = () => {
        updateSettings({ id: ideaData?.id, body: getValues() }).then((res) => {
            if ('data' in res) {
                setSnack({ message: 'Обновлено' });
            }
        });
    };

    useEffect(() => {
        if (data) {
            Object.keys(data).forEach(
                (key) =>
                    key !== 'id' &&
                    //@ts-ignore TODO FIX
                    setValue(key, data[key], {
                        shouldValidate: true,
                    })
            );
        }
    }, [data]);

    const checkboxRegister = (name: string) => {
        const data = register(name);
        return { ...data, checked: watch(name) };
    };

    return (
        <div>
            {[0, 1, 2, 3].includes(ideaData.status.id) && (
                <Alert severity='info'>Чтобы опубликовать идею публично, она должна быть в статусе "Одобрена"!</Alert>
            )}
            {[4, 5].includes(ideaData.status.id) && <Alert severity='success'>Ваша идея опубликована в каталоге!</Alert>}
            <br />
            <Typography sx={{ margin: '2px 0' }}>
                Статус идеи: <Chip size={'small'} label={ideaData?.status.name}></Chip>
            </Typography>

            <br />
            {[0, 2].includes(ideaData.status.id) && (
                <div>
                    <Divider>Модерация</Divider>

                    <TextField
                        label={'Комментарий для модераторов'}
                        sx={{ marginTop: 2 }}
                        multiline={true}
                        rows={3}
                        value={comment}
                        style={{ width: '100%' }}
                        onChange={onChange}
                    ></TextField>
                    <Button onClick={sendToModeration} sx={{ marginTop: 2 }}>
                        Отправить на модерацию
                    </Button>
                </div>
            )}
            <div>
                <Divider>Приватность</Divider>
                <form onChange={handleChange}>
                    {formControlsLabels.map((el) => (
                        <FormControlLabel key={el.id} control={<Checkbox {...checkboxRegister(el.name)} />} label={el.label} />
                    ))}
                </form>
                <br />
            </div>
            <div>
                <Divider>Опасная зона</Divider>
                <Button color={'error'}>Удалить идею</Button>
            </div>
        </div>
    );
};
