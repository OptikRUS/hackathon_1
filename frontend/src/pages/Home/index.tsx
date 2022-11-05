import {Box, Typography} from "@mui/material";
import {useEffect, useMemo, useState} from "react";
import {createStyle} from "./styles";
import {
    EstateMap,
    SelectedMapField,
    TypeObjectSelector,
    InputFile,
} from "./components";
import {ESNumberField} from "src/common/components"
import {SendButton} from "./components/SendButton";
import {ESSelectField, TOption} from "../../common/components/ESSelectField";


const RoomOptions: TOption[] = [
    {
        key: '1',
        label: '1-комнатная'
    },
    {
        key: '2',
        label: '2-комнатная'
    },
    {
        key: '3',
        label: '3-комнатная'
    },
    {
        key: '4',
        label: '4-комнатная'
    },
    {
        key: '5',
        label: '5-комнатная'
    },
    {
        key: '6',
        label: '6-комнатная'
    },
    {
        key: '7',
        label: 'Студия'
    },
    {
        key: '9',
        label: 'Свободная планировка'
    },
]

const SegmentOptions: TOption[] = [
    {
        key: 'new',
        label: 'Новостройка'
    },
    {
        key: 'old',
        label: 'Старый жилой фонд'
    },
    {
        key: 'current',
        label: 'Современной жилье'
    },
]

const HouseMaterialOptions: TOption[] = [
    {key: 'brick', label: 'Кирпич'},
    {key: 'panel', label: 'Панель'},
    {key: 'monolith', label: 'Монолит'},
]

const BalconyOptions: TOption[] = [
    {key: 'yes', label: 'Да'},
    {key: 'no', label: 'Нет'},
]

const StateOfFinish: TOption[] = [
    {key: 'without', label: 'Без отделки'},
    {key: 'municipal', label: 'Муниципальный ремонт'},
    {key: 'modern', label: 'Современный ремонт'},
]


type TFormState = {
    room_type: string,
    segment: string,
    floor: string,
    house_material_type: string,
    pool: File | null,
    address: string,
    floor_cor: string,
    square_cor: string,
    metro_step_way_cor: string,
    repair_state: string,
    kitchen_square_cor: string,
    isBalcony: string
}


export const Home = () => {

    const styles = useMemo(() => createStyle(), [])
    const [state, setState] = useState<TFormState>({
        room_type: '',
        segment: '',
        floor: '',
        house_material_type: '',
        pool: null,
        address: '',
        square_cor: '',
        floor_cor: '',
        metro_step_way_cor: '',
        repair_state: '',
        kitchen_square_cor: '',
        isBalcony: ''
    })

    useEffect(() => {
        console.log(state)
    }, [state])

    const handleChange = <K extends keyof TFormState>(key: K) => (val: TFormState[K]) => {
        setState((pervState) => ({
            ...pervState,
            [key]: val
        }))
    }


    return (
        <Box sx={styles.root}>
            <Box sx={styles.fieldsWrapper}>
                <Box sx={styles.requiredFields}>
                    <Typography variant={'h2'}>Обязательные поля</Typography>
                    <Box sx={styles.mapWrapper}>
                        <SelectedMapField/>
                        <Box>
                            <EstateMap/>
                        </Box>
                    </Box>
                    <TypeObjectSelector/>
                    <ESSelectField
                        label={'Количество комнат'}
                        value={state.room_type}
                        setValue={handleChange('room_type')}
                        options={RoomOptions}
                    />
                    <ESSelectField
                        label={'Сегмент'}
                        value={state.segment}
                        setValue={handleChange('segment')}
                        options={SegmentOptions}
                    />
                    <ESNumberField
                        label="Этажность дома"
                        value={state.floor}
                        setValue={handleChange('floor')}
                    />
                    <ESSelectField
                        value={state.house_material_type}
                        setValue={handleChange('house_material_type')}
                        label={'Материал стен дома'}
                        options={HouseMaterialOptions}/>
                </Box>
                <Box sx={styles.optionalFields}>
                    <Typography variant={'h2'}>Опциональные поля</Typography>
                    <ESNumberField
                        label="Этаж расположения квартиры"
                        value={state.floor_cor}
                        setValue={handleChange('floor_cor')}
                    />
                    <ESNumberField
                        label="Площадь квартиры (кв.м)"
                        value={state.square_cor}
                        setValue={handleChange('square_cor')}
                    />
                    <ESNumberField
                        label="Площадь кухни (кв.м)"
                        value={state.kitchen_square_cor}
                        setValue={handleChange('kitchen_square_cor')}
                    />
                    <ESSelectField
                        label={'Наличие балкона / лоджии'}
                        value={state.isBalcony}
                        setValue={handleChange('isBalcony')}
                        options={BalconyOptions}
                    />
                    <ESNumberField
                        label="Удаленность от станции метро (мин. пешком)"
                        value={state.metro_step_way_cor}
                        setValue={handleChange('metro_step_way_cor')}
                    />
                    <ESSelectField
                        label={'Состояние отделки'}
                        value={state.repair_state}
                        setValue={handleChange('repair_state')}
                        options={StateOfFinish}
                    />
                </Box>
            </Box>
            <Box>
                <InputFile setFile={handleChange('pool')} file={state.pool}/>
            </Box>
            <SendButton/>

        </Box>
    )
}
