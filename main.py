import json

from fastapi import FastAPI, UploadFile, File, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

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


@app.get("/analog")
async def get_etalon_and_analog(
        bbox: str,
        room_type: int,
        house_material_type: int,
        floor: int,
        min_year: int,
        max_year: int,
        address: str,
        segment: str,
        auction_cor: bool = None,
        floor_cor: int = None,
        square_cor: float = None,
        kitchen_square_cor: float = None,
        balcony_cor: bool = None,
        metro_stepway_cor: int = None,
        repair_state: str | int = None,
        estimation=Depends(PoolEstimate)
):
    """
    # Параметры для CIAN:\n
    `bbox:` регион прямоуголника\n
    `room_type:` количество комнат\n
    `house_material_type:` материал дома\n
    `floor:` этажность\n
    `min_year:` мин год постройки\n
    `max_year:` макс год постройки\n

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
    try:
        response = CianParser(bbox=bbox,
                              room_type=room_type,
                              floor=floor,
                              house_material_type=house_material_type,
                              min_year=min_year,
                              max_year=max_year
                              )

        etalon, analog = estimation.calculate_cor(
            data=response.get_doc,
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

        with open('etalon.json', 'w') as outfile:
            json.dump(etalon, outfile)
        return {"etalon": etalon, "analog": analog}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/etalon")
async def pool_estimate(pool: UploadFile = File(...), estimation=Depends(PoolEstimate)):
    """
    `pool:` файл пула\n
    """
    try:
        with open('etalon.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have etalon file")
    return estimation.calculate_pull(pull=pool.file._file, etalon_json=data)
