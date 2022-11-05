import {Box, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import {useState} from "react";

export const RoomQuantitySelector = () => {
    const [roomCount, setRoomCount] = useState('');

    const handleChange = (event: SelectChangeEvent) => {
        setRoomCount(event.target.value as string);
    };

    return (
        <Box sx={{width: '100%'}}>
            <FormControl required fullWidth size={'medium'}>
                <InputLabel id="demo-select-label">Количество комнат</InputLabel>
                <Select
                    labelId="demo-select-label"
                    value={roomCount}
                    label="Количество комнат"
                    onChange={handleChange}
                >
                    <MenuItem value={1}>1</MenuItem>
                    <MenuItem value={2}>2</MenuItem>
                    <MenuItem value={3}>3</MenuItem>
                    <MenuItem value={4}>4</MenuItem>
                    <MenuItem value={5}>5</MenuItem>
                    <MenuItem value={6}>6</MenuItem>
                </Select>
            </FormControl>
        </Box>
    );
}
