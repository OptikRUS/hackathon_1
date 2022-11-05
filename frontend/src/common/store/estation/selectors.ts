import { TRootState } from '../index'


export const getCurrentAddress = (state: TRootState) => state.estate.currentAddress
export const getCurrentCoords = (state: TRootState) => state.estate.currentCoords

