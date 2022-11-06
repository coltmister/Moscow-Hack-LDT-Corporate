interface FormControlsLabelsModel {
    id: number;
    name: string;
    label: string;
}

export const formControlsLabels: FormControlsLabelsModel[] = [
    { id: 0, name: 'is_public', label: 'Идея видна всем' },
    { id: 1, name: 'is_commentable', label: 'Можно комментировать идею' },
    // { id: 2, name: 'is_joinable', label: 'Можно подать заявку в команду' },
];
