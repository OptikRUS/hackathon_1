import { combineReducers, configureStore } from '@reduxjs/toolkit'
import {estateReducer} from "./estation";

const rootReducer = combineReducers({
    estate: estateReducer
})

export const store = configureStore({
  reducer: rootReducer
})


export type TRootState = ReturnType<typeof store.getState>
