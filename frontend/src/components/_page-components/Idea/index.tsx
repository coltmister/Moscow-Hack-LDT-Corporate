import { FullPost } from '../../common/FullPost';
import {
    useGetAllCommentsQuery,
    useGetIdeaByIdQuery,
    useGetIdeaSettingsByIdQuery,
    useGetPostsByIdQuery,
    useLazyGetIncomingRequestsQuery,
} from '@/services';
import { useNavigate, useParams } from 'react-router-dom';
import { MainLayout } from '@/layouts';
import { TabContext, TabList, TabPanel } from '@mui/lab';
import { Box, Button, Tab, Typography } from '@mui/material';
import { IdeasTabsTypes, tabs } from './tabs';
import { SyntheticEvent, useEffect, useState } from 'react';
import { useUserInfo } from '../../../hooks/useUserInfo';
import { TeamTab } from '../../common/Team';
import { SettingsTab } from '../../common/IdeaTabs/Settings';
import { formatDistance } from 'date-fns';
import ru from 'date-fns/locale/ru';
import { TeamRequest } from '../../common/TeamRequest';
import { AddCommentForm, CommentItem, WriteForm } from '@/components';
import { getDeclension } from '../../../utils/getDeclanations';
import s from './Idea.module.scss';

export const Idea = () => {
    const id = useParams().id;
    const { data } = useGetIdeaByIdQuery(id);
    const { user } = useUserInfo();
    const isUserIdeaOwner = user?.id === data?.author.id;
    const { data: ideaSettings } = useGetIdeaSettingsByIdQuery(id, { skip: !isUserIdeaOwner });
    const [getIncomingRequests, currentRequests] = useLazyGetIncomingRequestsQuery();
    const postCreatedAt = formatDistance(new Date(data?.created_at ?? '1900-01-01'), new Date(), { addSuffix: true, locale: ru });
    const { data: allPosts } = useGetPostsByIdQuery({ idea_id: id, limit: 10, desc: true, page: 1, search: '', items: 20 });

    const navigate = useNavigate();

    const [activeTab, setActiveTab] = useState(IdeasTabsTypes.CREATE_IDEA);
    const [isCreateMode, setIsCreateMode] = useState(false);
    const { data: allComments } = useGetAllCommentsQuery(id);

    const handleChange = (event: SyntheticEvent<Element, Event>, value: any) => {
        navigate('#' + value);
        setActiveTab(value);
    };

    useEffect(() => {
        if (data?.team?.id !== 'undefined') {
            getIncomingRequests(data?.team?.id);
        }
    }, [data?.id]);

    return (
        <MainLayout hideFilters contentFullWidth>
            <div className={s.tabs}>
                {data && (
                    <TabContext value={activeTab}>
                        <Box>
                            {!isCreateMode && (
                                <header className={s.header}>
                                    <div>
                                        <Typography variant='h4' className={s.title}>
                                            {data?.title}
                                        </Typography>
                                        {isUserIdeaOwner && (
                                            <Button sx={{ padding: '10px 15px' }} onClick={() => setIsCreateMode(!isCreateMode)}>
                                                Редактировать
                                            </Button>
                                        )}
                                    </div>
                                    <Typography>{postCreatedAt}</Typography>
                                </header>
                            )}
                            <TabList variant='scrollable' scrollButtons={true} onChange={handleChange}>
                                {tabs.map((tab) => (
                                    <Tab
                                        hidden={
                                            (!isUserIdeaOwner && tab.value === IdeasTabsTypes.SETTINGS) ||
                                            (!isUserIdeaOwner && tab.value === IdeasTabsTypes.MANAGE_TEAM) ||
                                            (!currentRequests?.data?.length && tab.value === IdeasTabsTypes.MANAGE_TEAM)
                                        }
                                        key={tab.id}
                                        label={tab.label}
                                        value={tab.value}
                                    />
                                ))}
                            </TabList>
                        </Box>
                        <TabPanel value={IdeasTabsTypes.CREATE_IDEA}>
                            {isCreateMode && <WriteForm mode={'update'} data={data} />}
                            {!isCreateMode && <FullPost data={data} blocks={data?.idea_json} />}
                            {!isCreateMode &&
                                allPosts?.payload?.map((post) => <FullPost data={post.idea} blocks={post.post_json} mode='post' />)[0]}
                            {!isCreateMode && data?.settings.is_commentable && <AddCommentForm />}
                            {!isCreateMode && allComments?.payload && (
                                <>
                                    <Typography sx={{ marginBottom: 3 }}>
                                        {getDeclension({
                                            count: allComments.payload.length,
                                            one: 'Комментарий',
                                            many: 'Комментариев',
                                            few: 'Комментария',
                                        })}
                                    </Typography>
                                    {allComments?.payload.map((comment) => (
                                        <CommentItem
                                            id={comment.id}
                                            created_at={comment.created_at}
                                            text={comment.text}
                                            user={comment.user}
                                        />
                                    ))}
                                </>
                            )}
                        </TabPanel>
                        <TabPanel value={IdeasTabsTypes.CREATE_TEAM}>
                            <TeamTab isUserIdeaOwner={isUserIdeaOwner} />
                        </TabPanel>
                        {isUserIdeaOwner && (
                            <TabPanel value={IdeasTabsTypes.SETTINGS}>
                                {ideaSettings && <SettingsTab data={ideaSettings} isUserIdeaOwner={isUserIdeaOwner} />}
                            </TabPanel>
                        )}
                        <TabPanel value={IdeasTabsTypes.MANAGE_TEAM}>
                            <TeamRequest requests={currentRequests.data} />
                        </TabPanel>
                    </TabContext>
                )}
            </div>
        </MainLayout>
    );
};
