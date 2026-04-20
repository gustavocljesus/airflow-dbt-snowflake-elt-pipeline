{{ config(schema='marts', materialized='table') }}

WITH datas AS (
    SELECT
        DATEADD(day, SEQ4(), TO_DATE('2010-01-01')) AS data
    FROM TABLE(GENERATOR(ROWCOUNT => 9500))
)

SELECT
    data AS data_id,
    DAY(data) AS dia,
    MONTH(data) AS mes,
    YEAR(data) AS ano,
    QUARTER(data) AS trimestre,
    DAYOFWEEK(data) AS dia_da_semana,
    DAYNAME(data) AS nome_dia_semana,
    MONTHNAME(data) AS nome_mes
FROM datas
WHERE data <= TO_DATE('2035-12-31')