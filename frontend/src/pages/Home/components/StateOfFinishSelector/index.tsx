import {Box, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import {useState} from "react";
import {TFinishState} from "src/common/types";

export const StateOfFinishSelector = () => {
    const [finishState, setFinishState] = useState<TFinishState | ''>('');

    const handleChange = (event: SelectChangeEvent) => {
        setFinishState(event.target.value as TFinishState);
    };

    return (
        <Box sx={{width: '100%'}}>
            <FormControl fullWidth size={'medium'}>
                <InputLabel id="demo-select-finish">Состояние отделки</InputLabel>
                <Select
                    labelId="demo-select-finish"
                    value={finishState}
                    label="Состояние отделки"
                    onChange={handleChange}
                >
                    <MenuItem value={'without'}>Без отделки</MenuItem>
                    <MenuItem value={'municipal'}>Муниципальный ремонт</MenuItem>
                    <MenuItem value={'modern'}>Современный ремонт</MenuItem>
                </Select>
            </FormControl>
        </Box>
    );
}
