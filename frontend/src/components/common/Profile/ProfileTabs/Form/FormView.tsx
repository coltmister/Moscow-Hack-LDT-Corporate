import { UserFormResponseDTO } from '@/dto';
import { Button, Chip, Divider, Grid } from '@mui/material';
import PublicIcon from '@mui/icons-material/Public';
import PsychologyIcon from '@mui/icons-material/Psychology';
import WorkOutlineIcon from '@mui/icons-material/WorkOutline';
import CorporateFareIcon from '@mui/icons-material/CorporateFare';
import { IconWithText } from '../../../../ui/Container/IconWithText/IconWithText';
import SchoolIcon from '@mui/icons-material/School';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import s from './styles.module.scss';
import classNames from 'classnames';
import { Dispatch, SetStateAction } from 'react';

interface FormViewProps {
    data: UserFormResponseDTO;
    setIsEditing: Dispatch<SetStateAction<boolean>>;
}

const FormView = ({ data, setIsEditing }: FormViewProps) => {
    return (
        <div>
            <Divider textAlign='left' className={classNames(s.dividerTop, s.divider)}>
                Общая информация
            </Divider>
            <Grid container>
                <IconWithText icon={<PublicIcon />} text={'Гражданство'}>
                    {data.citizenship?.name ?? 'не указано'}
                </IconWithText>
                <IconWithText icon={<WorkOutlineIcon />} text={'Есть ИП или юр.лицо'}>
                    {data.has_own_company ? 'Да' : 'Нет'}
                </IconWithText>
                <IconWithText icon={<PsychologyIcon />} text={'Есть зарегистированные РИД'}>
                    {data.has_iar ? 'Да' : 'Нет'}
                </IconWithText>
            </Grid>
            <Divider className={s.divider} textAlign='left'>
                Образование
            </Divider>
            <Grid container spacing={2}>
                <Grid item xs={0}>
                    <SchoolIcon sx={{ width: 64, height: 64, opacity: 0.7 }} />
                </Grid>
                <Grid item xs={10}>
                    <Grid>
                        <IconWithText text={'Университет'}>{data.education_university?.name ?? 'не указан'}</IconWithText>
                        <IconWithText text={'Уровень образования'}>{data.education_level?.name ?? 'не указан'}</IconWithText>
                        <IconWithText text={'Направление'}>{data.education_speciality ?? 'не указано'}</IconWithText>
                        <IconWithText text={'Год окончания'}>{data.education_end_year ?? 'не указан'}</IconWithText>
                    </Grid>
                </Grid>
            </Grid>
            <Divider className={s.divider} textAlign='left'>
                Работа
            </Divider>
            <Grid container spacing={2}>
                <Grid item xs={0}>
                    <CorporateFareIcon sx={{ width: 64, height: 64, opacity: 0.7 }} />
                </Grid>
                <Grid item xs={10}>
                    <Grid>
                        <IconWithText text={'Тип работы'}>{data.employment?.name ?? 'не указано'}</IconWithText>
                        <IconWithText text={'Опыт работы'}>
                            {Number.isFinite(data.work_experience) ? data.work_experience : 'не указан'}
                        </IconWithText>
                        <IconWithText text={'Обязанности'}>{data.professional_experience ?? 'не указаны'}</IconWithText>
                    </Grid>
                </Grid>
            </Grid>
            <Divider className={s.divider} textAlign='left'>
                Опыт командной работы
            </Divider>
            <Grid container spacing={2}>
                <Grid item xs={0}>
                    <EmojiEventsIcon sx={{ width: 64, height: 64, opacity: 0.7 }} />
                </Grid>
                <Grid item xs={10}>
                    <Grid>
                        <IconWithText text={'Роли в команде'}>
                            {Array.isArray(data.team_role) && data.team_role.length ? (
                                <Grid container={true} spacing={1}>
                                    {data.team_role.map((item) => (
                                        <Grid key={item.id} item>
                                            <Chip size={'small'} label={item.name} />
                                        </Grid>
                                    ))}
                                </Grid>
                            ) : (
                                'не указаны'
                            )}
                        </IconWithText>
                        <IconWithText text={'Опыт хакатонов'}>
                            {data.hack_experience ? `${data.hack_experience} лет` : 'не указан'}
                        </IconWithText>
                    </Grid>
                </Grid>
            </Grid>
            <Button className={s.divider} onClick={() => setIsEditing(true)} size='medium'>
                Редактировать
            </Button>
        </div>
    );
};

export default FormView;
