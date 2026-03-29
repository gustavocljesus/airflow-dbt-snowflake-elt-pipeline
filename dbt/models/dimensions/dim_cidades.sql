{{ config(schema='marts', materialized='table') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['id_cidades']) }} AS cidade_sk,
    c.id_cidades AS cidade_id,
    c.nome_cidade,
    e.estado_sk,
    c.data_inclusao,
    c.data_atualizacao
FROM {{ ref('stg_cidades') }} c
JOIN {{ ref('dim_estados') }} e
    ON c.id_estados = e.estado_id
