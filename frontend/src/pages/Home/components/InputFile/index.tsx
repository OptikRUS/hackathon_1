import {ChangeEvent, memo} from "react";
import {Box, Button} from "@mui/material";
import {toast} from "react-toastify";


const cutFileName = (name: string) => {

    if (name.length > 15) {
        return name.slice(0, 15) + '...'
    }
    return name
}

type TInputFileProps = {
    file: null | File,
    setFile: (file: File) => void
}

const correctFormats = ['xlsx', 'xls']

const isCorrectFile = (file: null | File): file is File => {
    const splintedFile = file?.name.split('.') || false
    return splintedFile && splintedFile.length > 1 && correctFormats.includes(splintedFile[splintedFile.length - 1])
}


const InputFileRaw = ({file, setFile}: TInputFileProps) => {


    const onChange = (e: ChangeEvent<HTMLInputElement>) => {

        const file = e.currentTarget.files && e.currentTarget.files[0]

        if (isCorrectFile(file)) {
            setFile(file)
        } else {
            toast.error(`Поддерживаются только форматы: ${correctFormats.join(', ')}`)
        }


    }

    return (
        <Box sx={{ml: 3}}>
            <Button sx={{width: '200px'}} variant="contained" color="success" component="label">
                {file ? cutFileName(file.name) : 'Прикрепить пул'}
                <input onChange={onChange} hidden type="file"/>
            </Button>
        </Box>
    )
}

export const InputFile = memo(InputFileRaw, (prevProps, nextProps) => prevProps.file?.name === nextProps.file?.name)
