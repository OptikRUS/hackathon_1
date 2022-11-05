import {Box, Typography} from "@mui/material";
import {useSelector} from "react-redux";
import {getCurrentAddress} from "src/common/store/estation";

export const SelectedMapField = () => {

    const currentAddress = useSelector(getCurrentAddress)


    return (
        <Box sx={{mb: 3}}>
            <Typography
                align={'center'}
            >
                {currentAddress ? `Выбранный адрес: ${currentAddress}` : 'Введите адрес на карте, по которому будет производиться расчет'}
            </Typography>
        </Box>
    )
}
