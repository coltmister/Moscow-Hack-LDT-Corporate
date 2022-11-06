export interface VacanciesQueryParams {
    page: number;
    itemsPerPage: number;
    team?: string;
}

export interface UserVacancy {
    id: string;
    username: string;
    name: string;
    surname: string;
    patronymic: null;
    is_active: boolean;
    is_admin: boolean;
    is_verified: boolean;
    snp: string;
    avatar: string;
    avatar_thumbnail: string;
}

export interface TeamVacancy {
    id: string;
    name: string;
    description: string;
    idea: Idea;
    members: Member[];
    team_leader: TeamLeader;
    is_looking_for_members: boolean;
}

export interface Idea {
    id: string;
    title: string;
    description: string;
    idea_json: null;
    author: TeamLeader;
    status: Status;
    category: Category[];
    tags: any[];
    rating: number;
    created_at: Date;
    updated_at: Date;
    subscribers_count: number;
    comments_count: number;
    likes_count: number;
    reactions_count: number;
}

export interface TeamLeader {
    id: string;
    username: string;
    name: string;
    surname: string;
    patronymic: null | string;
    is_active: boolean;
    is_admin: boolean;
    is_verified: boolean;
    snp: string;
    avatar: null;
    avatar_thumbnail: null;
}

export interface Category {
    id: string;
    name: string;
    description: string;
    idea_count: number;
}

export interface Status {
    id: number;
    name: string;
}

export interface Member {
    user: TeamLeader;
    role: Role;
    date_joined: Date;
    membership_requester: Status;
}

export interface Role {
    id: string;
    name: string;
}
