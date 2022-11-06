export interface TAnalogInResponse {
    'ID': number;
    'Метро': string;
    'Адрес': string;
    'Площадь, м2': string;
    'Дом': string;
    'Цена': string;
    'Телефоны': string;
    'Название ЖК': string;
    'Ссылка на объявление': string;
    'Площадь квартиры, кв.м': string;
    'Этажность дома': string;
    'Этаж расположения': string;
    'Материал': number;
    'Цена/м': number;
    'Итого сумма, кв метр': number;
}


export interface TEtalonInResponse {
    'Местоположение': string;
    'Количество комнат': number;
    'Сегмент(Новостройка, современное жилье, старый жилой фонд)': string;
    'Этажность дома': number;
    'Материал стен(Кипич, панель, монолит)': number;
    'Этаж расположения': number | null;
    'Площадь квартиры, кв.м?': number | null;
    'Площадь кухни, кв.м?': number | null;
    'Наличие балкона / лоджии': number | null;
    'Удаленность от станции метро, мин.пешком': number | null;
    'Состояние(без отделки, муниципальный ремонт, с современная отделка)': number | null;
    'Цена за кв метр': number;
}

export interface TPoolInResponse {
        'Местоположение': string;
        'Количество комнат': number;
        'Сегмент': string;
        'Этажность дома': number;
        'Материал стен': string;
        'Этаж расположения': number;
        'Площадь квартиры, кв.м': number;
        'Площадь кухни, кв.м': number;
        'Балкон': number;
        'Удаленность от станции метро, мин. пешком': number;
        'Ремонт': string;
        'ЭтажК': number;
        'ПлощадьК': number;
        'БалконК': number;
        'КухняК': number;
        'РемонтК': number;
        'Итого сумма, кв метр': number;
    }
