import {Box, TextField, Typography} from "@mui/material";
import {useMemo} from "react";
import {createStyle} from "./styles";
import {EstateMap} from "./components/EstateMap";
import {SelectedMapField} from "./components/SelectMapField";
import {TypeObjectSelector} from "./components/TypeObjectSelector";
import {RoomQuantitySelector} from "./components/RoomQuantitySelector";
import {HousingSegmentSelector} from "./components/HousingSegmentSelector";
import {FloorsHouse} from "./components/FloorsHouse";
import {WallMaterialSelector} from "./components/WallMaterialSelector";
import {StateOfFinishSelector} from "./components/StateOfFinishSelector";
import {BalconyPresenceSelector} from "./components/BalconyPresenceSelector";


export const Home = () => {

    const styles = useMemo(() => createStyle(), [])


    return (
        <Box sx={styles.root}>
            <Box sx={styles.requiredFields}>
                <Typography variant={'h2'}>Обязательные поля</Typography>
                <Box sx={styles.mapWrapper}>
                    <SelectedMapField/>
                    <Box>
                        <EstateMap/>
                    </Box>
                </Box>
                <TypeObjectSelector/>
                <RoomQuantitySelector/>
                <HousingSegmentSelector/>
                <FloorsHouse/>
                <WallMaterialSelector/>
            </Box>
            <Box sx={styles.optionalFields}>
                <Typography variant={'h2'}>Опциональные поля</Typography>
                <TextField label="Этаж расположения квартиры" variant="outlined"/>
                <TextField label="Площадь квартиры (кв.м)" variant="outlined"/>
                <TextField label="Площадь кухни (кв.м)" variant="outlined"/>
                <BalconyPresenceSelector/>
                <TextField label="Удаленность от станции метро (мин. пешком)" variant="outlined"/>
                <StateOfFinishSelector/>
            </Box>

        </Box>
    )
}
