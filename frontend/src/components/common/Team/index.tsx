import { useGetIdeaByIdQuery } from '@/services';
import { useParams } from 'react-router-dom';
import { ViewTeam } from './ViewTeam';
import { CreateTeamForm } from '@/components';
import { Typography } from '@mui/material';

interface TeamTabProps {
    isUserIdeaOwner: boolean;
}

export const TeamTab = ({ isUserIdeaOwner }: TeamTabProps) => {
    const id = useParams().id;
    const { data, isLoading } = useGetIdeaByIdQuery(id);

    return (
        <div>
            {data.team && !isLoading && <ViewTeam />}
            {!data.team && !isLoading && (
                <> {isUserIdeaOwner ? <CreateTeamForm /> : <Typography sx={{ padding: 24 }}>Команда еще не создана</Typography>}</>
            )}
        </div>
    );
};
