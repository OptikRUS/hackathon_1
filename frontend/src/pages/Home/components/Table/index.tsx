import {TStateForResponse} from "../../index";
import {Box, Button, Typography} from "@mui/material";
import {InputFile} from "../InputFile";
import {useMemo, useState} from "react";
import {DataGrid} from '@mui/x-data-grid';
import {MapAnalogs} from "./components/MapAnalogs";
import axios from "axios";
import {toast} from "react-toastify";
import {TEtalonInResponse} from "src/common/types/response";
import {TPoolInResponse} from "src/common/types/response";
import {PoolTable} from "./components/PoolTable";

type TTableAnalogEtalonProps = {
    tableData: TStateForResponse
    file: null | File
    setFile: (file: File) => void
}

export const TableAnalogEtalon = ({tableData, file, setFile}: TTableAnalogEtalonProps) => {

    const etalonData = useMemo(() => {
        const newData: Record<any, any> = {}
        const etalon = tableData.etalon[0]

        Object.entries(etalon).forEach(([key, value]) => {
            if (!!value) {
                newData[key] = value
            }
        })

        return newData

    }, [tableData])

    const cellStyle = {
        border: 'inherit',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '10px'
    }


    const analogData = useMemo(() => {


        const analogs = tableData.analog

        const columns = Object.keys(analogs[0]).map(k => ({
            field: k,
            headerName: k,
            width: k === 'Адрес' ? 500 : 300
        })).filter(el => el.field !== 'ID')

        const rows = analogs.map(el => ({...el, id: el['ID']}))

        return {columns, rows}

    }, [tableData])

    const [poolState, setPoolState] = useState<{etalon: TEtalonInResponse[], pool: TPoolInResponse[]}>({
        etalon: [],
        pool: []
    })


    const sendPool = () => {

        const DOMAIN = process.env.REACT_APP_DOMAIN || 'http://127.0.0.1:8000'

        if (file) {

            const formData = new FormData()

            formData.append('pool', file)

            axios.post<[string, string]>(`${DOMAIN}/etalon`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(res => {
                const [etalon, newEtalon] = res.data

                const parsedEtalon = JSON.parse(etalon) as TEtalonInResponse[]
                const parsedPool = JSON.parse(newEtalon) as TPoolInResponse[]

                setPoolState(() => ({
                    etalon: parsedEtalon,
                    pool: parsedPool
                }))

            })
                .catch(err => {
                    if (err instanceof Error) {
                        toast.error(err.message)
                    }
                })
        } else {
            toast.error('Прикрепите файл')
        }


    }


    const analogAddresses = tableData.analog.map(el => el['Адрес'])

    return (
        <Box sx={{
            mt: 3,
            px: '20px',
        }}>
            <Typography variant={'h2'} textAlign={'center'} sx={{mb: 3}}>Ваш эталон</Typography>
            <Box sx={{
                display: 'grid',
                gridTemplateColumns: `repeat(${Object.keys(etalonData).length}, 1fr)`,
                border: (theme) => `solid 1px ${theme.palette.mode === 'light' ? 'black' : 'white'}`
            }}>
                {Object.keys(etalonData).map(etalonKey => <Box
                    sx={cellStyle}
                    key={etalonKey}>{etalonKey}</Box>)}
                {Object.values(etalonData).map((value, index) => <Box
                    sx={cellStyle}
                    key={`${value}-${index}`}>{value}</Box>)}
            </Box>
            <Typography variant={'h2'} textAlign={'center'} sx={{my: 3}}>Список аналогов</Typography>
            <Box sx={{height: '400px', width: '100%'}}>
                <DataGrid
                    getRowHeight={() => 'auto'}
                    rows={analogData.rows}
                    columns={analogData.columns}
                    pageSize={5}
                    rowsPerPageOptions={[5]}
                    checkboxSelection
                />
            </Box>
            <Box sx={{
                display: 'flex',
                justifyContent: 'center'
            }}>
                <MapAnalogs addresses={analogAddresses}/>
            </Box>

            <InputFile file={file} setFile={setFile}/>
            <Box sx={{mt: 3, display: 'flex', justifyContent: 'center'}}>
                <Button onClick={sendPool} sx={{width: '200px'}} variant="contained" component="label">
                    Рассчитать пул
                </Button>
            </Box>
            <Box>
                {poolState.etalon.length > 0 && <PoolTable pool={poolState.pool} etalon={poolState.etalon}/>}
            </Box>
        </Box>
    )
}
