import {TEtalonInResponse} from "src/common/types";
import {TPoolInResponse} from "src/common/types/response";
import {Box, Typography} from "@mui/material";
import {useMemo} from "react";
import {DataGrid} from "@mui/x-data-grid";

type TPoolTableProps = { etalon: TEtalonInResponse[], pool: TPoolInResponse[] }

export const PoolTable = ({etalon, pool}: TPoolTableProps) => {

    const etalonData = useMemo(() => {
        const newData: Record<any, any> = {}
        const newEtalon = etalon[0]

        Object.entries(newEtalon).forEach(([key, value]) => {
            if (!!value) {
                newData[key] = value
            }
        })

        return newData

    }, [etalon])

    const analogData = useMemo(() => {


        const analogs = pool

        const columns = Object.keys(analogs[0]).map(k => ({
            field: k,
            headerName: k,
            width: k === 'Адрес' ? 500 : 300
        })).filter(el => el.field !== 'ID')

        const rows = analogs.map((el, index) => ({...el, id: index}))

        return {columns, rows}

    }, [pool])


    const cellStyle = {
        border: 'inherit',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '10px'
    }

    return (
        <Box sx={{mt: 3}}>
            <Typography variant={'h2'} textAlign={'center'} sx={{my: 3}}>Ваш эталон</Typography>
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
            <Typography variant={'h2'} textAlign={'center'} sx={{my: 3}}>Пул объектов</Typography>
            <Box sx={{height: '400px', width: '100%', mt: 3}}>
                <DataGrid
                    getRowHeight={() => 'auto'}
                    rows={analogData.rows}
                    columns={analogData.columns}
                    pageSize={5}
                    rowsPerPageOptions={[5]}
                    checkboxSelection
                />
            </Box>
        </Box>
    )
}
