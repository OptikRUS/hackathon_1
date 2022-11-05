import {TCoords} from "src/common/types";
import {Circle, Map, Placemark, SearchControl} from "@pbe/react-yandex-maps";
import {useDispatch, useSelector} from "react-redux";
import {getCurrentCoords, setAddressToRedux, setCoordsToRedux} from "src/common/store/estation";

export const EstateMap = () => {


    const currentCoords = useSelector(getCurrentCoords)
    const dispatch = useDispatch()


    const defaultState = {
        center: [55.751574, 37.573856],
        zoom: 8,
    };

    const handleSubmitSearch = (e: any) => {
        const address = e.originalEvent.request as string

        dispatch(setAddressToRedux(address))

        const geocode = window.ymaps.geocode(address) as Promise<any>


        geocode.then((res: any) => {
            const coords = res.geoObjects.get(0).geometry.getCoordinates() as TCoords

            dispatch(setCoordsToRedux(coords))


        })
    }


    return (
        <Map width={500} height={500} defaultState={defaultState}>
            <SearchControl onSubmit={handleSubmitSearch} options={{float: 'right'}}/>
            {currentCoords && <Circle
                geometry={[currentCoords, 1000]}
                options={{
                    draggable: false,
                    fillColor: '#DB709377',
                    strokeColor: '#990066',
                    strokeOpacity: 0.8,
                    strokeWidth: 5,
                }}
            />}
            {currentCoords && <Placemark geometry={currentCoords}/>}
        </Map>
    )
}
