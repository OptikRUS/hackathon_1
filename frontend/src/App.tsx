import React, {useMemo, useState} from 'react';
import {Home} from "./pages/Home";
import {YMaps} from "@pbe/react-yandex-maps";
import {Provider as ReduxProvider} from 'react-redux'
import {store} from "src/common/store";
import {createTheme, ThemeProvider} from "@mui/material/styles";
import {ColorModeContext} from './common/context';
import {ThemeToggler} from "./common/components";
import {Box} from "@mui/material";
import {ToastContainer} from "react-toastify";


function App() {
    const [mode, setMode] = useState<'light' | 'dark'>('dark');
    const colorMode = useMemo(
        () => ({
            toggleColorMode: () => {
                setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
            },
        }),
        [],
    );

    const theme = useMemo(
        () =>
            createTheme({
                palette: {
                    mode,
                },
            }),
        [mode],
    );

    return (
        <ReduxProvider store={store}>
            <ColorModeContext.Provider value={colorMode}>
                <ThemeProvider theme={theme}>
                    <YMaps
                        query={{
                            apikey: process.env.REACT_APP_API_SECRET_KEY
                        }}
                    >
                        <Box
                            sx={{
                                bgcolor: 'background.default',
                                color: 'text.primary',
                                height: '100%'
                            }}
                        >
                            <ThemeToggler/>
                            <Home/>
                        </Box>
                        <ToastContainer/>

                    </YMaps>
                </ThemeProvider>
            </ColorModeContext.Provider>
        </ReduxProvider>

    );
}

export default App;
