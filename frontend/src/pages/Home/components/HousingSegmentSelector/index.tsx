import {Box, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import {useState} from "react";
import {TSegment} from "src/common/types";


export const HousingSegmentSelector = () => {
    const [segment, setSegment] = useState<TSegment | ''>('');

    const handleChange = (event: SelectChangeEvent<TSegment>) => {
        setSegment(event.target.value as TSegment);
    };

    return (
        <Box sx={{width: '100%'}}>
            <FormControl required fullWidth size={'medium'}>
                <InputLabel id="Housing-Segment-Selector">Сегмент</InputLabel>
                <Select
                    labelId="Housing-Segment-Selector"
                    id="demo-simple-select-segment"
                    value={segment}
                    label="Сегмент"
                    onChange={handleChange}
                >
                    <MenuItem value={'new'}>Новостройка</MenuItem>
                    <MenuItem value={'current'}>Cовременное жилье</MenuItem>
                    <MenuItem value={'old'}>Cтарый жилой фонд</MenuItem>
                </Select>
            </FormControl>
        </Box>
    );
}
