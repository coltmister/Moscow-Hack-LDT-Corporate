export const enum IdeasTabsTypes {
    CREATE_IDEA = 'idea',
    CREATE_TEAM = 'team',
    SETTINGS = 'settings',
    MANAGE_TEAM = 'manage_team',
}

interface IdeasTabsModel {
    id: number;
    value: IdeasTabsTypes;
    label: string;
}

export const tabs: IdeasTabsModel[] = [
    {
        id: 0,
        value: IdeasTabsTypes.CREATE_IDEA,
        label: 'Описание',
    },
    { id: 1, value: IdeasTabsTypes.CREATE_TEAM, label: 'Команда' },
    { id: 2, value: IdeasTabsTypes.SETTINGS, label: 'Настройки' },
    { id: 3, value: IdeasTabsTypes.MANAGE_TEAM, label: 'Заявки на вступление' },
];
