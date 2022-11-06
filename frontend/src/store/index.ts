import { combineReducers, configureStore } from '@reduxjs/toolkit';

import { commentsService, postsService, authService, userService, constantsService, ideasService } from '../services';
import { teamsService } from '../services/Teams.service';
import { adminService } from '../services/Admin.service';
import { feedService } from '../services/Feed.service';

const rootReducer = combineReducers({
    [postsService.reducerPath]: postsService.reducer,
    [commentsService.reducerPath]: commentsService.reducer,
    [authService.reducerPath]: authService.reducer,
    [userService.reducerPath]: userService.reducer,
    [constantsService.reducerPath]: constantsService.reducer,
    [ideasService.reducerPath]: ideasService.reducer,
    [teamsService.reducerPath]: teamsService.reducer,
    [adminService.reducerPath]: adminService.reducer,
    [feedService.reducerPath]: feedService.reducer,
});

export const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat([
            postsService.middleware,
            commentsService.middleware,
            authService.middleware,
            userService.middleware,
            constantsService.middleware,
            ideasService.middleware,
            teamsService.middleware,
            adminService.middleware,
            feedService.middleware,
        ]),
});

export type RootState = ReturnType<typeof rootReducer>;
export type AppStore = typeof store;
export type AppDispatch = AppStore['dispatch'];
