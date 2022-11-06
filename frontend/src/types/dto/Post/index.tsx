import { OutputData } from '@editorjs/editorjs';

export interface PostQueryParams {
    limit: number;
    page: number;
    search: string;
    desc: boolean;
}

export interface PostAuthorDTO {
    id: string;
    username: string;
    name: string;
    surname: string;
    patronymic: null;
    is_active: boolean;
    is_admin: boolean;
    is_verified: boolean;
    snp: string;
    avatar: null;
    avatar_thumbnail: string | null;
}

export interface PostDTO {
    total_pages: number;
    total_count: number;
    has_next_page: boolean;
    payload: [
        {
            id: string;
            title: string;
            // IDEA DTO
            idea: {
                id: string;
                title: string;
                description: string;
                idea_json: null;
                author: {
                    id: string;
                    username: string;
                    name: string;
                    surname: string;
                    patronymic: null;
                    is_active: boolean;
                    is_admin: boolean;
                    is_verified: boolean;
                    snp: string;
                    avatar: string | null;
                    avatar_thumbnail: string | null;
                };
                status: {
                    id: 5;
                    name: string;
                };
                category: [
                    {
                        id: string;
                        name: string;
                        description: string;
                        idea_count: number;
                    },
                    {
                        id: string;
                        name: string;
                        description: string;
                        idea_count: number;
                    }
                ];
                tags: any[];
                rating: number;
                created_at: string | Date;
                updated_at: string | Date;
                subscribers_count: number;
                comments_count: number;
                likes_count: number;
                reactions_count: number;
            };
            description: string;
            post_json: null;
            author: PostAuthorDTO;
            rating: number;
        }
    ];
}

export interface CreatePostDTO {
    title: string;
    description: string;
    idea?: string;
    post_json: OutputData['blocks'];
}
