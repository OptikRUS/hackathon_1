import {createSlice, PayloadAction} from '@reduxjs/toolkit'
import {TCoords} from "src/common/types";


type TEstateState = {
    currentCoords: TCoords | null
    currentAddress: string | null
}


const initialState: TEstateState = {
    currentCoords: null,
    currentAddress: null
}

const estateSlice = createSlice({
    name: 'estate',
    initialState,
    reducers: {
        setCoordsToRedux(state, action: PayloadAction<TCoords>) {
            state.currentCoords = action.payload
        },
        setAddressToRedux(state, action: PayloadAction<string>) {
            state.currentAddress = action.payload
        }
    }
})

export const {setCoordsToRedux, setAddressToRedux} = estateSlice.actions
export const estateReducer = estateSlice.reducer

