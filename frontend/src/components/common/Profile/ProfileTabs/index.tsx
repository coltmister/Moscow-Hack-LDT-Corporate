import { useLocation, useNavigate } from 'react-router-dom';

import { Box, Tab } from '@mui/material';
import React, { useEffect, useState, SyntheticEvent } from 'react';
import s from './ProfileTabs.module.scss';
import { useUserInfo } from '../../../../hooks/useUserInfo';
import Form from './Form';
import { TabContext, TabList, TabPanel } from '@mui/lab';
import { Settings } from './Settings';
import { ProfileTabsTypes, tabsList } from './tabs';
import ProfileTab from './Profile/index';
import { Ideas } from './Ideas';

const ProfileTabs = () => {
    const { isUserOwnProfile } = useUserInfo();
    const location = useLocation();
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState(ProfileTabsTypes.PROFILE);

    const handleChange = (event: React.SyntheticEvent<Element, Event>, value: any) => {
        navigate('#' + value);
        setActiveTab(value);
    };

    useEffect(() => {
        if (location.hash) {
            setActiveTab(location.hash.slice(1) as ProfileTabsTypes);
        }
    }, []);

    return (
        <div className={s.tabs}>
            <TabContext value={activeTab}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                    <TabList onChange={handleChange}>
                        {tabsList.map((el) => (
                            <Tab key={el.id} label={el.label} value={el.value} />
                        ))}
                        {isUserOwnProfile && <Tab label='Настройки' value={ProfileTabsTypes.SETTINGS} />}
                    </TabList>
                </Box>
                <TabPanel value='profile'>
                    <ProfileTab />
                </TabPanel>
                <TabPanel value='form'>
                    <Form />
                </TabPanel>
                <TabPanel value='ideas'>
                    <Ideas />
                </TabPanel>
                <TabPanel value='settings'>
                    <Settings />
                </TabPanel>
            </TabContext>
        </div>
    );
};
export { ProfileTabs };
export default ProfileTabs;
