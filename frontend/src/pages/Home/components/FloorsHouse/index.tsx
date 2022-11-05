import {Box, styled, TextField} from "@mui/material";
import {useState} from "react";
import {TFloors} from "src/common/types";
import {ChangeEvent} from 'react';


const Legend = styled("legend")(() => ({
    color: 'text.primary'
}))
const Fieldset = styled("fieldset")(() => ({
    height: '90px',
}))

type TFloorsBool = { [M in keyof TFloors]: boolean }

export const FloorsHouse = () => {
    const [floors, setFloors] = useState<TFloors>({floorsFrom: '', floorsTo: ''});

    const [errors, setErrors] = useState<TFloorsBool>({floorsFrom: false, floorsTo: false})

    const handleChange = (val: keyof TFloors) => (event: ChangeEvent<HTMLInputElement>) => {
        if (!Number.isNaN(+event.target.value)) {
            setFloors((prevState) => ({
                ...prevState,
                [val]: event.target.value,
            }))
            setErrors((prevState) => ({
                ...prevState,
                [val]: false,
            }))
        } else {
            setErrors((prevState) => ({
                ...prevState,
                [val]: true,
            }))
        }
    }


    return (
        <Box sx={{width: '100%', mb: 3}}>
            <Fieldset>
                <Legend>Этажность дома</Legend>
                <Box sx={{display: 'flex', gap: '30px'}}>
                    <TextField
                        value={floors.floorsFrom || ''}
                        onChange={handleChange('floorsFrom')}
                        label="От"
                        variant="outlined"
                        error={errors.floorsFrom}
                        helperText={errors.floorsFrom && 'Введите число'}
                    />
                    <TextField
                        value={floors.floorsTo || ''}
                        onChange={handleChange('floorsTo')}
                        label="До"
                        variant="outlined"
                        error={errors.floorsTo}
                        helperText={errors.floorsTo && 'Введите число'}
                    />
                </Box>
            </Fieldset>

        </Box>
    );
}
