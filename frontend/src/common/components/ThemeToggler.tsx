import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import {useTheme} from '@mui/material/styles';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import {useContext} from "react";
import {ColorModeContext} from "src/common/context";


export const ThemeToggler = () => {
    const theme = useTheme();
    const colorMode = useContext(ColorModeContext);
    return (
        <Box>
            <Box
                sx={{
                    marginLeft: 'auto',
                    width: 'fit-content'
                }}
            >
                {theme.palette.mode} mode
                <IconButton sx={{ml: 1}} onClick={colorMode.toggleColorMode} color="inherit">
                    {theme.palette.mode === 'dark' ? <Brightness7Icon/> : <Brightness4Icon/>}
                </IconButton>
            </Box>
        </Box>
    );
}


