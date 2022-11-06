import {TStateForResponse} from "../../index";
import {Box, Typography} from "@mui/material";
import {InputFile} from "../InputFile";
import {useMemo} from "react";
import {DataGrid} from '@mui/x-data-grid';
import {MapAnalogs} from "./components/MapAnalogs";

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

        const table = {columns, rows}

        return table

    }, [tableData])


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
                {Object.values(etalonData).map(value => <Box
                    sx={cellStyle}
                    key={value}>{value}</Box>)}
            </Box>
            <Typography variant={'h2'} textAlign={'center'} sx={{my: 3}}>Список аналагов</Typography>
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
        </Box>
    )
}
