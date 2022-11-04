import io

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse

from parser_class import CianParser
from estimate import PoolEstimate

app = FastAPI()


@app.post("/")
async def get_xlsx_table(bbox: str,
                         room_type: str,
                         house_material_type: str,
                         floor: str,
                         min_year: str,
                         max_year: str,
                         pool: UploadFile = File(...),
                         ):
    """
    bbox: регион прямоуголника\n
    room_type: количество комнат\n
    house_material_type: материал дома\n
    floor: этажность\n
    min_year: мин год постройки\n
    max_year: макс год постройки\n
    pool: файл пула\n
    """
    response = CianParser(bbox=bbox,
                          room_type=room_type,
                          floor=floor,
                          house_material_type=house_material_type,
                          min_year=min_year,
                          max_year=max_year
                          )
    estimation = PoolEstimate(pool.file._file)
    return estimation.calculate_cor(response.get_doc)
    # return StreamingResponse(io.BytesIO(response.get_doc),
    #                          media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
