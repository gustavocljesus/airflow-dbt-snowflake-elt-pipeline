{{ config(schema='analytics', materialized='table') }}
SELECT
    ven.vendedor_id AS id,
    ven.nome_vendedor AS vendedor,
    c.nome_concessionaria AS concessionaria,
    COUNT(v.venda_id) AS numero_vendas,
    SUM(v.valor_venda) AS total_vendas,
    AVG(v.valor_venda) AS valor_medio
FROM {{ ref('fct_vendas') }} v
JOIN {{ ref('dim_vendedores') }} ven 
    ON v.vendedor_sk = ven.vendedor_sk
JOIN {{ ref('dim_concessionarias') }} c 
    ON c.concessionaria_sk = ven.concessionaria_sk
GROUP BY 
    ven.vendedor_id, 
    ven.nome_vendedor,  
    c.nome_concessionaria
