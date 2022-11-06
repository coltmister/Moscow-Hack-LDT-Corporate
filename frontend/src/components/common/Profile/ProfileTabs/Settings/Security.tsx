import React, { useState } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useAppropriateSecuritySettingsMutation } from '../../../../../hooks/useAppropriateSecuritySettingsMutation';
import { Devices } from '@/dto';
import { DesktopMac, DesktopMacOutlined, PhoneEnabled, Smartphone, SmartphoneOutlined } from '@mui/icons-material';
import { Grid } from '@mui/material';

interface SecurityProps {
    data: Devices[];
}

const Security = ({ data }: SecurityProps) => {
    const [expanded, setExpanded] = useState<number | false>(false);

    const handleChange = (panel: number) => (event: React.SyntheticEvent, isExpanded: boolean) => {
        setExpanded(isExpanded ? panel : false);
    };

    return (
        <div>
            {data.map((item) => (
                <Accordion expanded={expanded === item.lastAccess} onChange={handleChange(item.lastAccess)}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls='panel1bh-content' id='panel1bh-header'>
                        <Grid container alignItems={'center'}>
                            <Grid item xs={6}>
                                <Typography sx={{ flexShrink: 0, display: 'flex', alignItems: 'center', gap: 1 }}>
                                    {item.mobile ? <SmartphoneOutlined /> : <DesktopMacOutlined />} {item.os + ' ' + item?.osVersion}
                                </Typography>
                            </Grid>
                            <Grid xs={6} item>
                                <Typography sx={{ color: 'text.secondary' }}>
                                    {new Date(item.lastAccess * 1000).toLocaleString()} {item.current && ' | текущий'}
                                </Typography>
                            </Grid>
                        </Grid>
                    </AccordionSummary>
                    <AccordionDetails>
                        {item.sessions.map(({ browser, ipAddress, lastAccess, current }) => (
                            <Grid container justifyContent={'space-between'}>
                                <Grid item>{browser}</Grid>
                                <Grid item>{ipAddress}</Grid>
                                <Grid item>
                                    {new Date(lastAccess * 1000).toLocaleString()} {item.current && ' | текущий'}
                                </Grid>
                            </Grid>
                        ))}
                    </AccordionDetails>
                </Accordion>
            ))}
        </div>
    );
};

export default Security;
