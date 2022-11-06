import LoadingButton from '@mui/lab/LoadingButton';
import Box from '@mui/material/Box';
import SendIcon from '@mui/icons-material/Send';


type TSendButtonProps = {
    onClick: () => void
    loading: boolean
}


export const SendButton = ({onClick, loading}: TSendButtonProps) => {


    return (
        <Box>
            <Box
                sx={{
                    margin: '0 auto',
                    width: 'fit-content'
                }}
            >
                <LoadingButton
                    onClick={onClick}
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
