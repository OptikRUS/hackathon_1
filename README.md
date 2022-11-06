# Real estate calculation
Приложение пасчёта эталона по аналогу, расчёт пула по эталону, отображение аналогов на карте, возможность корректировки стоимости 
в зависимости от параметром

<a href="https://github.com/OptikRUS/ht/blob/files/tz.pdf" target="_blank">Техническое задание</a>

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
        <img src="https://raw.githubusercontent.com/OptikRUS/ht/2e495ca87815537ba668657bfa79c7f684bbf646/1.png" alt="img from doc">
    </details>
  * <details>
      <summary>POST-запрос</summary>
        <img src="https://raw.githubusercontent.com/OptikRUS/ht/2e495ca87815537ba668657bfa79c7f684bbf646/2.png" alt="img from doc">
    </details>

[//]: # (## Пользовательская документация:)
