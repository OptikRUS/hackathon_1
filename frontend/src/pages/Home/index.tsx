import {Box, Typography} from "@mui/material";
import {useMemo, useState} from "react";
import {createStyle} from "./styles";
import {
    EstateMap,
    SelectedMapField,
    TypeObjectSelector,
    InputFile,
} from "./components";
import {ESNumberField} from "src/common/components"
import {SendButton} from "./components/SendButton";
import {ESSelectField} from "src/common/components/ESSelectField";
import {useSelector} from "react-redux";
import {getCurrentCoords, getCurrentAddress} from "../../common/store/estation";
import axios from "axios";
import {log} from "util";
import {toast} from "react-toastify";


const RoomOptions = [
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

const SegmentOptions = [
    {
        key: 'newBuild',
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

const segmentYears = {
    old: {
        min_year: '1985',
        max_year: '2000',
    },
    newBuild: {
        min_year: '2019',
        max_year: '2030',
    },
    current: {
        min_year: '2000',
        max_year: '2019',
    },
}

const HouseMaterialOptions = [
    {key: '1', label: 'Кирпич'},
    {key: '4', label: 'Панель'},
    {key: '3', label: 'Монолит'},
]

const BalconyOptions = [
    {key: 'yes', label: 'Да'},
    {key: 'no', label: 'Нет'},
]

const AuctionOption = [
    {key: 'yes', label: 'Да'},
    {key: 'no', label: 'Нет'},
]

const StateOfFinish = [
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
    balcony_cor: string
    auction_cor: string
}

type TRequired = {
    bbox: string
    room_type: string
    house_material_type: string
    floor: number
    min_year: string
    max_year: string
    address: string
    segment: string
}

type TOptional = {
    auction_cor: boolean
    floor_cor: number
    square_cor: number
    kitchen_square_cor: number
    balcony_cor: boolean
    metro_stepway_cor: string
    repair_state: string
}


export const Home = () => {

    const styles = useMemo(() => createStyle(), [])
    const [loading, setLoading] = useState<boolean>(false)
    const center = useSelector(getCurrentCoords)
    const address = useSelector(getCurrentAddress)
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
        balcony_cor: '',
        auction_cor: ''
    })

    const handleSend = () => {
        const required: TRequired = {
            address: "",
            floor: 0,
            house_material_type: "",
            max_year: "",
            min_year: "",
            room_type: "",
            segment: "",
            bbox: ''
        }

        const optional: Partial<TOptional> = {}


        const roundSix = (val: number) => val.toFixed(6)

        if (center) {
            required.bbox = `${roundSix(center[0] + 0.015)}%2C${roundSix(center[1] + 0.015)}%2C${roundSix(center[0] - 0.015)}%2C${roundSix(center[1] - 0.015)}`
        }

        if (address) {
            required.address = address
        }

        if (state.floor) {
            required.floor = +state.floor
        }

        if (state.segment) {
            required.segment = SegmentOptions.find(el => el.key === state.segment)?.label.toLowerCase() || 'современное жилье'
            required.min_year = segmentYears[state.segment as keyof typeof segmentYears].min_year
            required.max_year = segmentYears[state.segment as keyof typeof segmentYears].max_year
        }

        if (state.room_type) {
            required.room_type = state.room_type
        }

        if (state.house_material_type) {
            required.house_material_type = state.house_material_type
        }

        if (state.floor_cor) {
            optional.floor_cor = +state.floor_cor
        }

        if (state.square_cor) {
            optional.square_cor = +state.square_cor
        }
        if (state.kitchen_square_cor) {
            optional.kitchen_square_cor = +state.kitchen_square_cor
        }

        if (state.balcony_cor) {
            optional.balcony_cor = state.balcony_cor === 'yes'
        }

        if (state.metro_step_way_cor) {
            optional.metro_stepway_cor = state.metro_step_way_cor
        }

        if (state.repair_state) {
            optional.repair_state = state.repair_state
        }

        if (state.auction_cor) {
            optional.auction_cor = state.auction_cor === 'yes'
        }

        const DOMAIN = process.env.REACT_APP_DOMAIN
        const isValid = () => Object.values(required).every(el => !!el)


        if (isValid() && DOMAIN) {

            const params = {...required, ...optional}

            axios.get(`${DOMAIN}/analog`, {params})
                .then((res) => res.data)
                .then((data) => {
                    console.log(data)
                })
        } else {
            toast.error('Oops... something wrong')
        }

    }

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
                        value={state.balcony_cor}
                        setValue={handleChange('balcony_cor')}
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
                    <ESSelectField
                        label={'Корректировка на торг'}
                        value={state.auction_cor}
                        setValue={handleChange('auction_cor')}
                        options={AuctionOption}
                    />
                </Box>
            </Box>
            <Box>
                <InputFile setFile={handleChange('pool')} file={state.pool}/>
            </Box>
            <SendButton
                loading={loading}
                onClick={handleSend}
            />

        </Box>
    )
}
