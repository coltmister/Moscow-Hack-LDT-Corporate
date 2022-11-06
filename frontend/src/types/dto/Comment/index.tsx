import { PostDto, UserResponseDto } from '@/dto';

export interface CommentItemDto {
    id: number;
    text: string;
    post: PostDto;
    user: UserResponseDto;
    createdAt: string;
    updatedAt: string;
}
