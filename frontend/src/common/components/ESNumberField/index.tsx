import {Box, TextField} from "@mui/material";
import {memo, useState} from "react";

import {ChangeEvent} from 'react';


type TESNumberFieldProps = {
    label: string,
    value: string,
    setValue: (val: string) => void
}

export const ESNumberFieldRaw = ({label, value, setValue}: TESNumberFieldProps) => {


    const [error, setError] = useState<boolean>(false)

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (!Number.isNaN(+event.target.value)) {
            setValue(event.target.value)
            setError(false)
        } else {
            setError(true)
        }
    }


    return (
        <Box sx={{width: '100%'}}>
            <TextField
                value={value}
                onChange={handleChange}
                label={label}
                variant="outlined"
                error={error}
                helperText={error && 'Надо вводить число'}
            />
        </Box>
    );
}


export const ESNumberField = memo(ESNumberFieldRaw, (prevProps, nextProps) => prevProps.value === nextProps.value)
