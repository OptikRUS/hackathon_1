export const createStyle = () => ({
    root: {
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '40px',
        px: '30px'
    },
    requiredFields: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',

        '& .MuiFormControl-root': {
            mb: 3,
            width: '100%'
        }

    },
    optionalFields: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',

        '& .MuiFormControl-root': {
            mb: 3,
            width: '100%'
        }

    },
    mapWrapper: {
        width: '500px',
        mb: 3
    }

})
