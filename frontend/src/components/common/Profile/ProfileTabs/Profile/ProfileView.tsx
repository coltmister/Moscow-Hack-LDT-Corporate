import { UserProfileResponseDTO } from '@/dto';
import { Button, Chip, Divider, Grid } from '@mui/material';
import { IconWithText } from '../../../../ui/Container/IconWithText/IconWithText';
import {
    CalendarMonth,
    ChatBubbleOutline,
    EmailRounded,
    InsertLink,
    ListAlt,
    PanToolRounded,
    PeopleAlt,
    Person,
    Phone,
    Settings,
} from '@mui/icons-material';
import s from './styles.module.scss';
import { Dispatch, SetStateAction } from 'react';
import { NavLink } from 'react-router-dom';

interface ProfileViewProps {
    data: UserProfileResponseDTO;
    setIsEditing: Dispatch<SetStateAction<boolean>>;
}

export const ProfileView = ({ setIsEditing, data }: ProfileViewProps) => {
    const parseDate = (data: string) => {
        return new Date(data).toLocaleDateString('ru-RU', { month: 'long', year: 'numeric', day: 'numeric' });
    };
    return (
        <>
            <div>
                <IconWithText icon={<Person />} text={'Пол'}>
                    {data.sex ? data.sex.name : 'не указан'}
                </IconWithText>
                <IconWithText icon={<CalendarMonth />} text={'День рождения'}>
                    {data.birthdate ? parseDate(data.birthdate) : 'не указан'}
                </IconWithText>
                <IconWithText icon={<ListAlt />} text={'О себе'}>
                    {data.biography ? data.biography : 'не указано'}
                </IconWithText>
                <IconWithText icon={<Settings />} text={'Навыки'}>
                    {Array.isArray(data.skills) && data.skills.length ? (
                        <Grid container={true} spacing={1}>
                            {data.skills.map((item) => (
                                <Grid key={item.id} item>
                                    <Chip size={'small'} label={item.name} />
                                </Grid>
                            ))}
                        </Grid>
                    ) : (
                        'не указаны'
                    )}
                </IconWithText>
                <IconWithText icon={<PanToolRounded />} text={'Интересы'}>
                    {Array.isArray(data.interests) && data.interests.length ? (
                        <Grid container={true} spacing={1}>
                            {data.interests.map((item) => (
                                <Grid key={item.id} item>
                                    <a href={item?.chat?.chat_link} target={'_blank'}>
                                        <Chip
                                            style={item?.chat?.chat_link && { backgroundColor: '#ADD8E6', cursor: 'pointer' }}
                                            icon={item?.chat?.chat_link && <InsertLink />}
                                            size={'small'}
                                            label={item.name}
                                        />
                                    </a>
                                </Grid>
                            ))}
                        </Grid>
                    ) : (
                        'не указаны'
                    )}
                </IconWithText>
                <Divider className={s.divider}>Контакты</Divider>
                <IconWithText icon={<EmailRounded />} text={'Email'}>
                    {data.email ?? 'не указан'}
                </IconWithText>
                <IconWithText icon={<Phone />} text={'Телефон'}>
                    {data.phone ?? 'не указан'}
                </IconWithText>
                <IconWithText icon={<PeopleAlt />} text={'Социальные сети'}>
                    {Array.isArray(data.social_networks) && data.social_networks.length ? (
                        <Grid container={true} spacing={1}>
                            {data.social_networks.map((item) => (
                                <Grid key={item.id} item>
                                    {item.nickname.includes('https://') ? (
                                        <a href={item.nickname} target={'_blank'}>
                                            <Chip size={'small'} label={`${item.network_type}`} />
                                        </a>
                                    ) : (
                                        <Chip size={'small'} label={`${item.network_type}: ${item.nickname}`} />
                                    )}
                                </Grid>
                            ))}
                        </Grid>
                    ) : (
                        'не указаны'
                    )}
                </IconWithText>
            </div>
            <Button className={s.divider} onClick={() => setIsEditing(true)} size='medium'>
                Редактировать
            </Button>
        </>
    );
};
