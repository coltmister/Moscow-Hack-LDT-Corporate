const items = {
    comments: {
        popular: [
            {
                id: 0,
                user: {
                    id: 1,
                    fullName: 'Вася Пупкин',
                    avatarUrl: 'https://leonardo.osnova.io/598fc957-a3f6-598c-b6f9-a033c3941d12/-/scale_crop/64x64/-/format/webp/',
                },
                text: 'Теперь, каждое рабочее утро, после кровати, я перекладываюсь туда спать ещё на часок. Ну и…',
                post: {
                    id: 1,
                    title: 'Какая у вас дома ванна?',
                },
                createdAt: new Date().toString(),
            },
            {
                id: 1,
                user: {
                    id: 1,
                    fullName: 'Маша Пупкина',
                    avatarUrl: 'https://www.kindpng.com/picc/m/163-1636340_user-avatar-icon-avatar-transparent-user-icon-png.png',
                },
                text:
                    'Теперь, каждое рабочее утро, после кровати, я перекладываюсь туда спать ещё на часок. Ну и…б' +
                    'Теперь, каждое рабочее утро, после кровати, я перекладываюсь туда спать ещё на часок. Ну и…',
                post: {
                    id: 1,
                    title: 'Какая у вас дома ванна?',
                },
                createdAt: new Date().toString(),
            },
            {
                id: 2,
                user: {
                    id: 1,
                    fullName: 'Вася Пупкин',
                    avatarUrl: 'https://www.freelancejob.ru/upload/131/5092087670389.png',
                },
                text: 'Теперь, каждое рабочее утро, после кровати, я перекладываюсь туда спать ещё на часок. Ну и…',
                post: {
                    id: 1,
                    title: 'Какая у вас дома ванна?',
                },
                createdAt: new Date().toString(),
            },
        ],
        latest: [
            {
                id: 2,
                user: {
                    id: 1,
                    fullName: 'Вася Пупкин',
                    avatarUrl: 'https://www.freelancejob.ru/upload/131/5092087670389.png',
                },
                text: 'Теперь, каждое рабочее утро, после кровати, я перекладываюсь туда спать ещё на часок. Ну и…',
                post: {
                    id: 1,
                    title: 'Какая у вас дома ванна?',
                },
                createdAt: new Date().toString(),
            },
        ],
    },
};

export default items;
