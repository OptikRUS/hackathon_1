import {Box, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import {useState} from "react";
import {TWallMaterial} from "src/common/types";


export const WallMaterialSelector = () => {
    const [material, setMaterial] = useState<TWallMaterial | ''>('');

    const handleChange = (event: SelectChangeEvent) => {
        setMaterial(event.target.value as TWallMaterial);
    };

    return (
        <Box sx={{width: '100%'}}>
            <FormControl required fullWidth size={'medium'}>
                <InputLabel id="housing-material">Материал стен дома</InputLabel>
                <Select
                    labelId="housing-material"
                    value={material}
                    label="Материал стен дома"
                    onChange={handleChange}
                >
                    <MenuItem value={'brick'}>Кирпич</MenuItem>
                    <MenuItem value={'panel'}>Панель</MenuItem>
                    <MenuItem value={'monolith'}>Монолит</MenuItem>
                </Select>
            </FormControl>
        </Box>
    );
}
