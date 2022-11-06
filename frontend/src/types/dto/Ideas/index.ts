import { OutputData } from '@editorjs/editorjs';
import { UserProfile, UserProfileResponseDTO } from '../User';
import { bool } from 'yup';

export interface CreateIdeaDto {
    title: string;
    description: string;
    idea_json: OutputData['blocks'] | null | {};
    tags?: [
        {
            id: string;
            name: string;
            description: string;
            premium: boolean;
        }
    ];
    links?: string[];
}

export interface IdeaModel {
    id: string;
    updated_at: Date | string;
    created_at: string | Date;
    title: string;
    description: string;
    tags: any[];
    rating: number;
    likes_count: number;
    comments_count: number;
    reactions_count: number;
    subscribers_count: number;
    idea_json: null | {};
    status: { id: number; name: string };
    category: {
        description: string;
        id: string;
        idea_count: number;
        name: string;
    }[];
    author: {
        avatar: null | string;
        avatar_thumbnail: string | null;
        id: string;
        is_active: boolean;
        is_admin: boolean;
        is_verified: boolean;
        name: string;
        patronymic: boolean;
        snp: string;
        surname: string;
        username: string;
    };
}

export interface IdeaDTO {
    has_next_page: boolean;
    total_count: number;
    total_pages: number;
    payload: IdeaModel[];
}
