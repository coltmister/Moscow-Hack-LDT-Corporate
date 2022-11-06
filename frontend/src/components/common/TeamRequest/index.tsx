import { PostAuthorDTO } from '@/dto';
import { Avatar, Button, Typography } from '@mui/material';
import s from './TeamRequest.module.scss';
import { useAcceptIncomingRequestMutation, useLazyGetIncomingRequestsQuery } from '@/services';

interface TeamRequestProps {
    requests: {
        cover_letter: string;
        id: string;
        request_status: {
            id: number;
            name: string;
        };
        role: {
            id: string;
            name: string;
        };
        team: {
            id: string;
        };
        user: PostAuthorDTO;
    }[];
}

export const TeamRequest = ({ requests }: TeamRequestProps) => {
    const [acceptUserRequest] = useAcceptIncomingRequestMutation();
    const [getIncoming] = useLazyGetIncomingRequestsQuery();

    return (
        <ul>
            {requests?.map((request) => (
                <li className={s.item} key={request.id}>
                    <div className={s.info}>
                        <Avatar src={request.user.avatar_thumbnail ?? ''} />
                        <div>
                            <Typography variant='body1'>{request.user.snp}</Typography>
                            <Typography variant='body2'>{request.role.name}</Typography>
                        </div>
                    </div>
                    <div className={s.controls}>
                        <Button
                            onClick={() => {
                                acceptUserRequest({ team_id: request.team.id, request_id: request.id, decision: true });
                                getIncoming(request.team.id);
                            }}
                        >
                            Принять
                        </Button>
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                acceptUserRequest({ team_id: request.team.id, request_id: request.id, decision: false });
                                getIncoming(request.team.id);
                            }}
                        >
                            Отклонить
                        </Button>
                    </div>
                </li>
            ))}
        </ul>
    );
};
