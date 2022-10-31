import io

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from parser_class import CianParser

app = FastAPI()


@app.get("/")
async def get_xlsx_table(region: str):
    response = CianParser(region)
    return StreamingResponse(io.BytesIO(response.get_doc),
                             media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
