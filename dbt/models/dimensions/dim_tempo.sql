{{ config(schema='marts', materialized='table') }}
WITH datas AS(
    SELECT
        dateadd(day, seq4(), '2010-01-01') AS data
    FROM table(
        generator(
            rowcount => datediff(day, '2010-01-01', '2035-12-31') + 1
        )
    )
)
SELECT
    data AS data_id,
    day(data) AS dia,
    month(data) AS mes,
    year(data) AS ano,
    quarter(data) AS trimestre,
    dayofweek(data) AS dia_da_semana,
    dayname(data) AS nome_dia_semana,
    monthname(data) AS nome_mes
FROM datas