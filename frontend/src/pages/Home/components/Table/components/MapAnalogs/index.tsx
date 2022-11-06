import {TCoords} from "src/common/types";
import {Circle, Map, Placemark} from "@pbe/react-yandex-maps";
import { useSelector} from "react-redux";
import {getCurrentCoords} from "src/common/store/estation";
import {useEffect, useState} from "react";


type TMapAnalogsProps = {
    addresses: string[]
}


export const MapAnalogs = ({addresses}: TMapAnalogsProps) => {

    const currentCoords = useSelector(getCurrentCoords)

    const [addrCoords, setAddrCoords] = useState<TCoords[]>([])


    const defaultState = {
        center: currentCoords || [55.751574, 37.573856],
        zoom: 9,
    };

    useEffect(() => {
        addresses.forEach(address => {
            const geocode = window.ymaps.geocode(address) as Promise<any>


            geocode.then((res: any) => {
                const coords = res.geoObjects.get(0).geometry.getCoordinates() as TCoords

                setAddrCoords((prevState) => [...prevState, coords])

            })
        })


    }, [addresses])


    return (
        <Map width={500} height={500} defaultState={defaultState}>
            {currentCoords && <Circle
                options={{
                    draggable: false,
                    fillColor: '#DB709377',
                    strokeColor: '#990066',
                    strokeOpacity: 0.8,
                    strokeWidth: 5,
                }}
            />}
            {addrCoords.length > 0 && addrCoords.map(coords => <Placemark geometry={coords}/>)}
        </Map>
    )
}
