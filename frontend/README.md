# Boilerplate edition

## Components
### UI
<b>ATOM:</b> UI это кастомные / кастомизированные UI-элементы, которые можно переиспользовать в любом месте приложения.
Как правило, не имеют своей логики. 
Пример - контейнеры, кнопки, инпуты итп

### common
<b>MOLECULE:</b> Common или Общие компоненты - собранные в группу полноценные элементы интерфейса. Могут иметь какое-то внутреннее состояние.
<br>Могут переиспользоваться везде. <br>
Пример - карточка товара, модальные окна, Hero-секции

### page-components (views)
<b>ORGANISM:</b> Полноценный готовый компонент, который можно встроить на страницу. Наполнен своей полноценной логикой. <br>
<br>Как правило, используется в конкретном месте или на конкретной странице.

___

## Services

RTK предоставляет мощный механизм управления данными, где бэкенд это единственный источник правды.
[RTK Query](https://redux-toolkit.js.org/tutorials/rtk-query) вдохновлен [React-Query](https://tanstack.com/query/v4) и имеет все те же механизмы работы - кеширование данных, рефетчинг итд.

Из сервиса экспортируются сгенерированные хуки, где окончание:
- "Query" - это запрос на получение (например GET для получения всех постов);
- "Mutation" - запрос на изменение (например PUT для редактирования поста);

`export const { useGetAllPostsQuery, useSearchPostsQuery, useCreatePostMutation, useUpdatePostMutation, useDeletePostMutation } =`<br>
`postsService;`<br>

Внутри себя хуки имеют набор полей: <br>
`const {data: posts, error, isLoading, refetch} = useGetAllPostsQuery(limit);`

_________

### Required

- [NodeJS](https://nodejs.org/en/)

### Install

1. Clone or Download this repository;
2. Open the terminal and install deps with `yarn` or `npm i`;
3. `yarn dev` or `npm run dev` for start dev-server;
4. Open `127.0.0.1` in your browser;

### Stack

- [MaterialUI](https://mui.com/)
- [TypeScript](https://www.typescriptlang.org/)
- [SCSS](https://sass-lang.com/)
- [CSS Modules](https://github.com/css-modules/css-modules)
- [ClassNames](https://github.com/JedWatson/classnames)
- [React Hook Form](https://react-hook-form.com/)

### Linters

- [Stylelint]()
- [ESLint]()
- [Prettier]()
- [EditorConfig]()

## 🐣 Порядок импортов
- Библиотеки
- Контекст
- HOC
- UI-компоненты
- Компоненты
- Изображения
- Хуки
- Роуты
- Сервисы
- Утилиты
- Константы
- Стили
