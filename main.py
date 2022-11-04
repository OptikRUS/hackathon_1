import io

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse

from parser_class import CianParser
from estimate import PoolEstimate

app = FastAPI()


@app.post("/")
async def get_xlsx_table(region: str, etalon: UploadFile = File(...)):
    response = CianParser(region)
    estimation = PoolEstimate(etalon.file._file)
    return estimation.calculateCor(response.get_doc)
    # return StreamingResponse(io.BytesIO(response.get_doc),
    #                          media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
