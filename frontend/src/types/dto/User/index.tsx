export interface LoginDto {
    email: string;
    password: string;
}

export interface UserCreateDto extends LoginDto {
    surname?: string;
    name: string;
    lastname?: string;
    birth: string;
}

export interface UserResponseDto {
    id: number;
    email: string;
    fullName: string;
    token: string;
    commentsCount?: number;
    createdAt: string;
    updatedAt: string;
}

export interface UserSettingsDto {
    show_birthdate: boolean;
    show_sex: boolean;
    show_biography: boolean;
    show_phone: boolean;
    show_email: boolean;
    show_social_networks: boolean;
    can_be_invited: boolean;
    id: string;
    show_skills: boolean;
    show_interests: boolean;
}

export interface UserProfileResponseDTO {
    id: string;
    user: UserProfile;
    status: '🤬👹👺👿💩🤡';
    avatar: string;
    avatar_thumbnail: string;
    biography: string;
    phone: string; //'79045508041';
    birthdate: string; //'1999-10-11';
    sex: Sex;
    skills: Skill[];
    interests: any[];
    social_networks: SocialNetwork[];
    email: string;
}

export interface UserFormResponseDTO {
    id: string;
    user: UserProfile;
    citizenship?: Citizenship;
    education_university?: University;
    education_level?: EducationLevel;
    education_speciality?: string;
    education_end_year?: number;
    employment?: Employment;
    work_experience?: number;
    professional_experience?: string;
    team_role?: Array<TeamRole>;
    has_iar?: boolean;
    has_own_company?: boolean;
    hack_experience?: number;
}

export interface University {
    id: string;
    name: string;
    rating: number;
}

export interface EducationLevel {
    id: number;
    name: string;
}

export interface Employment {
    id: number;
    name: string;
}

export interface TeamRole {
    id: string;
    name: string;
    weight: number;
}

export interface Citizenship {
    id: string;
    name: string;
}

export type Sex = 'male' | 'female';

export type SocialNetworkType = 'Вконтакте' | 'Telegram' | 'Instagram' | ' Facebook' | 'YouTube' | 'Twitter' | 'LinkedIn' | 'Google';

export interface UserProfile {
    id: string;
    username: string;
    name: string;
    surname: string;
    patronymic: string;
    is_active: boolean;
    is_admin: boolean;
    is_verified: boolean;
    snp: string;
}

export interface SocialNetwork {
    id: string;
    network_type: SocialNetworkType;
    nickname: string;
}

export interface Skill {
    id: string;
    name: string;
}

export interface Devices {
    os: string;
    osVersion: string;
    device: string;
    lastAccess: number;
    current: boolean;
    sessions: Session[];
    mobile: boolean;
}

export interface Session {
    id: string;
    ipAddress: string;
    started: number;
    lastAccess: number;
    expires: number;
    clients: Client[];
    browser: string;
    current: boolean;
}

export interface Client {
    clientId: string;
    clientName: string;
    userConsentRequired: boolean;
    inUse: boolean;
    offlineAccess: boolean;
}

export interface UserIdea {
    id: string;
    title: string;
    description: string;
    idea_json: any;
    author: Author;
    status: Status;
    category: any[];
    tags: any[];
    links: string[];
    rating: number;
    created_at: Date;
    updated_at: Date;
    subscribers: any[];
    subscribers_count: number;
    can_edit: boolean;
    settings: Settings;
    information: Information;
    reactions: Reactions;
    last_post: null;
}

export interface Author {
    id: string;
    username: string;
    name: string;
    surname: string;
    patronymic: string;
    is_active: boolean;
    is_admin: boolean;
    is_verified: boolean;
    snp: string;
    avatar: null;
    avatar_thumbnail: null;
}

export interface Information {
    id: string;
    progress: number;
    budget: number;
}

export interface Reactions {
    likes: Dislikes;
    super_likes: Dislikes;
    dislikes: Dislikes;
    neutrals: Dislikes;
    super_dislikes: Dislikes;
}

export interface Dislikes {
    users: any[];
    count: number;
}

export interface Settings {
    id: string;
    is_public: boolean;
    is_commentable: boolean;
}

export interface Status {
    id: number;
    name: string;
}
