from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from parser_class import CianParser
from estimate import PoolEstimate

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
async def main():
    return {"message": "Hello World"}


@app.post("/")
async def get_xlsx_table(bbox: str,
                         room_type: str,
                         house_material_type: str,
                         floor: str,
                         min_year: str,
                         max_year: str,
                         address: str,
                         segment: str,
                         auction_cor: bool = None,
                         floor_cor: str = None,
                         square_cor: str = None,
                         kitchen_square_cor: str = None,
                         balcony_cor: str = None,
                         metro_stepway_cor: str = None,
                         repair_state: str = None,
                         pool: UploadFile = File(...),
                         ):
    """
    # Параметры для CIAN:\n
    `bbox:` регион прямоуголника\n
    `room_type:` количество комнат\n
    `house_material_type:` материал дома\n
    `floor:` этажность\n
    `min_year:` мин год постройки\n
    `max_year:` макс год постройки\n

    `pool:` файл пула\n
    <br>
    # Корректировка аналога:\n
    `address:` адрес\n
    `segment:` сегмент\n
    `auction_cor:` аукцион\n
    `floor_cor:` этаж расположения\n
    `square_cor:` корректировка на площадь\n
    `kitchen_square_cor:` корректировка на площадь кухни\n
    `balcony_cor:` корректировка на площадь балкона\n
    `metro_stepway_cor:` количество минут до метро\n
    `repair_state:` состояниие ремонта\n
    """
    response = CianParser(bbox=bbox,
                          room_type=room_type,
                          floor=floor,
                          house_material_type=house_material_type,
                          min_year=min_year,
                          max_year=max_year
                          )

    estimation = PoolEstimate(data=response.get_doc)
    return estimation.calculate_cor(
        address=address,
        room_count=room_type,
        material=house_material_type,
        segment=segment,
        max_floor=floor,
        auction_cor=auction_cor,
        floor_cor=floor_cor,
        square_cor=square_cor,
        kitchen_square_cor=kitchen_square_cor,
        balcony_cor=balcony_cor,
        metro_stepway_cor=metro_stepway_cor,
        repair_state=repair_state
    )
