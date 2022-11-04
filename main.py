import io

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse

from parser_class import CianParser
from estimate import PoolEstimate

app = FastAPI()


@app.post("/")
async def get_xlsx_table(bbox: str,
                         room_type: str,
                         pool: UploadFile = File(...),
                         ):
    response = CianParser(bbox, room_type)
    estimation = PoolEstimate(pool.file._file)
    return estimation.calculate_cor(response.get_doc)
    # return StreamingResponse(io.BytesIO(response.get_doc),
    #                          media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
