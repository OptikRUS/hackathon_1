import {Box, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import {useState} from "react";
import {TBalconyPresence} from "src/common/types";

export const BalconyPresenceSelector = () => {
    const [balconyIsPresence, setBalconyIsPresence] = useState<TBalconyPresence>('');

    const handleChange = (event: SelectChangeEvent) => {
        setBalconyIsPresence(event.target.value as TBalconyPresence);
    };

    return (
        <Box sx={{width: '100%'}}>
            <FormControl fullWidth size={'medium'}>
                <InputLabel id="demo-select-balcony">Наличие балкона / лоджии</InputLabel>
                <Select
                    labelId="demo-select-balcony"
                    value={balconyIsPresence}
                    label="Наличие балкона / лоджии"
                    onChange={handleChange}
                >
                    <MenuItem value={'yes'}>Да</MenuItem>
                    <MenuItem value={'no'}>Нет</MenuItem>
                </Select>
            </FormControl>
        </Box>
    );
}
