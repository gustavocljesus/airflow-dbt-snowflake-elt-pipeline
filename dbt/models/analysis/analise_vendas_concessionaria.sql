{{ config(schema='analytics', materialized='table') }}
SELECT
    con.concessionaria_id AS id,
    con.nome_concessionaria AS concessionaria,
    c.nome_cidade AS cidade,
    e.nome_estado AS estado,
    COUNT(v.venda_id) AS numero_vendas,
    SUM(v.valor_venda) AS total_vendas,
    AVG(v.valor_venda) AS valor_medio
FROM {{ ref('fct_vendas') }} v
JOIN {{ ref('dim_concessionarias') }} con 
    ON v.concessionaria_sk = con.concessionaria_sk
JOIN {{ ref('dim_cidades') }} c 
    ON con.cidade_sk = c.cidade_sk
JOIN {{ ref('dim_estados') }} e 
    ON c.estado_sk = e.estado_sk
GROUP BY 
    con.concessionaria_id, 
    con.nome_concessionaria, 
    c.nome_cidade, 
    e.nome_estado