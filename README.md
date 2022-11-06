# Real estate calculation
* Приложение расчёта эталона по аналогу
* Расчёт пула по эталону и отображение аналогов на карте 
* Возможность корректировки стоимости в зависимости от параметров

[Техническое задание](https://github.com/OptikRUS/ht/blob/files/tz.pdf)

[//]: # ([Ссылка на приложение]&#40;ссылка на хост&#41; 🌐)

## Техническая документация:
* Переименуйте `.env.example` в `.env`
* Запуск проекта в docker: ```$ docker-compose up```
* Документация ендпоинтов(backend): ```http://0.0.0.0:8000/docs```
* Страница приложения(frontend): ```http://0.0.0.0:3000```

* ### Основные модули приложения:
  * **CianParser** - класс запроса выборки с сайта cian.ru
  * **PoolEstimate** - класс расчёта аналогов и эталонов
  * `/analog` и `/etalon` - ендпоинты для получения аналогов и эталонов
  * <details>
      <summary>GET-запрос</summary>
        <img src="https://github.com/OptikRUS/ht/blob/files/1.png" alt="img from doc">
    </details>
  * <details>
      <summary>POST-запрос</summary>
        <img src="https://github.com/OptikRUS/ht/blob/files/2.png" alt="img from doc">
    </details>

## Пользовательская интерфейс:
<details>
      <summary>Введение данных эталона</summary>
        <img src="https://github.com/OptikRUS/ht/blob/files/3.png" alt="UI image">
</details>
<details>
    <summary>Поиск и корректировка аналогов и расчёт эталона</summary>
      <img src="https://github.com/OptikRUS/ht/blob/files/4.png" alt="UI image">
</details>
<details>
    <summary>Расчёт и корректировка пула</summary>
      <img src="https://github.com/OptikRUS/ht/blob/files/5.png" alt="UI image">
</details>