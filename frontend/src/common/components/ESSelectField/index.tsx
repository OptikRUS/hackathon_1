import {Box, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import {memo} from 'react'

export type TOption = {
    key: string,
    label: string
}

type TEsSelectFieldProps = {
    value: string
    setValue: (val: string) => void
    label: string
    options: TOption[]
    required?: boolean
}

const ESSelectFieldRaw = ({value, setValue, label, options, required}: TEsSelectFieldProps) => {


    const handleChange = (event: SelectChangeEvent) => {
        setValue(event.target.value);
    };

    return (
        <Box sx={{width: '100%'}}>
            <FormControl required={required} fullWidth size={'medium'}>
                <InputLabel id={`select-${label.replace(/\s/g, '')}`}>{label}</InputLabel>
                <Select
                    labelId={`select-${label.replace(/\s/g, '')}`}
                    value={value}
                    label={label}
                    onChange={handleChange}
                >
                    {options.map(({key, label}) => <MenuItem key={key} value={key}>{label}</MenuItem>)}
                </Select>
            </FormControl>
        </Box>
    );
}


export const ESSelectField = memo(ESSelectFieldRaw, (prevProps, nextProps) => prevProps.value === nextProps.value)

