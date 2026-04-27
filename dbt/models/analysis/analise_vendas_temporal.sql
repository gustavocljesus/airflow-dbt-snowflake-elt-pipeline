{{ config(schema='analytics', materialized='table') }}
SELECT
    DATE_TRUNC('day', v.data_venda_id) AS mes_venda,
    COUNT(v.venda_id) AS numero_vendas,
    SUM(v.valor_venda) AS total_vendas,
    AVG(v.valor_venda) AS valor_medio
FROM {{ ref('fct_vendas') }} v
GROUP BY DATE_TRUNC('day', v.data_venda_id)