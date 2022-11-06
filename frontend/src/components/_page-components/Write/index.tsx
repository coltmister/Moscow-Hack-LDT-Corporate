import { MainLayout } from '@/layouts';
import { WriteForm } from '@/components';
import { CreateIdeaDto } from '@/dto';

export const Write = () => {
    return (
        <MainLayout contentFullWidth className='main-layout-white' hideFilters hideMenu>
            <WriteForm data={{} as CreateIdeaDto} />
        </MainLayout>
    );
};
