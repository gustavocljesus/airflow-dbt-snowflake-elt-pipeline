{{ config(schema='analytics', materialized='table') }}
SELECT
    vei.veiculo_id AS id,
    vei.nome_veiculo AS veiculo,
    vei.tipo AS tipo,
    vei.valor_sugerido AS valor_sugerido,
    COUNT(v.venda_id) AS numero_vendas,
    SUM(v.valor_venda) AS total_vendas,
    AVG(v.valor_venda) AS valor_medio
FROM {{ ref('fct_vendas') }} v
JOIN {{ ref('dim_veiculos') }} vei 
    ON v.veiculo_sk = vei.veiculo_sk
GROUP BY 
    vei.veiculo_id, 
    vei.nome_veiculo, 
    vei.tipo, 
    vei.valor_sugerido