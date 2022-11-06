import * as React from 'react';
import { styled } from '@mui/material/styles';
import Rating, { IconContainerProps, RatingProps } from '@mui/material/Rating';

const StyledRating = styled(Rating)(({ theme }) => ({
    '& .MuiRating-iconEmpty .MuiSvgIcon-root': {
        color: theme.palette.action.disabled,
    },
    '.MuiRating-root': {
        display: 'flex',
        gap: 5,
    },
    '.MuiRating-icon': {},
}));

export const customIcons: {
    [index: number]: {
        id: string;
        icon: any;
        label: string;
    };
} = {
    1: {
        id: 'super_dislikes',
        icon: '🤨',
        label: 'Ужасно',
    },
    2: {
        id: 'dislikes',
        icon: '💔',
        label: 'Не нравится',
    },
    3: {
        id: 'neutrals',
        icon: '😐',
        label: 'Нейтрально',
    },
    4: {
        id: 'likes',
        icon: '❤️',
        label: 'Нравится',
    },
    5: {
        id: 'super_likes',
        icon: '🥰',
        label: 'Очень круто',
    },
};

function IconContainer(props: IconContainerProps, my_reaction: any, reactions: Reactions) {
    const { value, ...other } = props;
    return (
        <span
            {...other}
            style={{ display: 'flex', alignItems: 'center', backgroundColor: 'rgba(0, 0, 0, 0.02)', borderRadius: 6, padding: '0 4px' }}
        >
            {customIcons[value].icon}{' '}
            <span style={{ fontSize: 16, marginLeft: 4 }}>{reactions && reactions[customIcons[value].id]?.count}</span>
        </span>
    );
}
interface ReactionStat {
    users: Array<any>;
    count: number;
}

export interface ReactionProps {
    dislikes: ReactionStat;
    likes: ReactionStat;
    neutrals: ReactionStat;
    super_dislikes: ReactionStat;
    super_likes: ReactionStat;
}

export interface MyReaction {
    value: string;
    id: string;
    created_at: string;
}

interface ReactionsProps extends RatingProps {
    reactions: ReactionProps;
    my_reaction: MyReaction;
}

export default function Reactions({ reactions, my_reaction, ...props }: ReactionsProps) {
    const defaultValue = my_reaction?.value && Object.keys(customIcons).filter((id) => customIcons[+id].id === my_reaction.value + 's')[0];
    return (
        <StyledRating
            style={{ gap: 5 }}
            name='highlight-selected-only'
            max={5}
            IconContainerComponent={(props) => IconContainer(props, my_reaction, reactions)}
            getLabelText={(value: number) => {
                return customIcons[value].label;
            }}
            highlightSelectedOnly
            {...(defaultValue && { defaultValue })}
            {...props}
        />
    );
}
