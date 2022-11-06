export const enum ProfileTabsTypes {
    PROFILE = 'profile',
    FORM = 'form',
    IDEAS = 'ideas',
    SETTINGS = 'settings',
}

interface TabsListModel {
    id: number;
    label: string;
    value: ProfileTabsTypes;
}

export const tabsList: TabsListModel[] = [
    { id: 0, label: 'Профиль', value: ProfileTabsTypes.PROFILE },
    { id: 1, label: 'Анкета', value: ProfileTabsTypes.FORM },
    { id: 2, label: 'Идеи', value: ProfileTabsTypes.IDEAS },
];
