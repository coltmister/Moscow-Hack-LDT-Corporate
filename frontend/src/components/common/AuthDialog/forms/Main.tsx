import { Button } from '@mui/material';
import { MailOutline } from '@mui/icons-material';

import { VKicon, TWITTERicon, FBicon, GOOGLEicon, APPLEicon } from '../img';

import s from '../AuthDialog.module.scss';
import { FormsInterface } from './common';

export const Main = ({ onClick }: FormsInterface): JSX.Element => {
    return (
        <div className={s.items}>
            <Button onClick={onClick} variant='contained' fullWidth className='mb-15'>
                <MailOutline />
                <span>Почта</span>
            </Button>
            <Button variant='contained' fullWidth className='mb-15'>
                <VKicon width={24} height={24} />
                <span>ВКонтакте</span>
            </Button>
            <Button variant='contained' fullWidth className='mb-15'>
                <GOOGLEicon width={24} height={24} />
                <span>Google</span>
            </Button>
            <div className={s.icons}>
                <Button variant='contained' className='mb-15'>
                    <FBicon width={24} height={24} />
                </Button>
                <Button variant='contained' className='mb-15'>
                    <TWITTERicon width={24} height={24} />
                </Button>
                <Button variant='contained' className='mb-15'>
                    <APPLEicon width={24} height={24} />
                </Button>
            </div>
        </div>
    );
};
