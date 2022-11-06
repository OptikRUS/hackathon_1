import LoadingButton from '@mui/lab/LoadingButton';
import Box from '@mui/material/Box';
import SendIcon from '@mui/icons-material/Send';
import {useState} from "react";


export const SendButton = () => {

    const [loading, setLoading] = useState(false);

    function handleClick() {
        setLoading((prevState) => !prevState);
    }

    return (
        <Box>
            <Box
                sx={{
                    margin: '0 auto',
                    width: 'fit-content'
                }}
                onClick={handleClick}
            >
                <LoadingButton
                    size="large"
                    endIcon={<SendIcon/>}
                    loading={loading}
                    loadingPosition="end"
                    variant="contained"
                >
                    Рассчитать эталон
                </LoadingButton>
            </Box>
        </Box>
    );

}
