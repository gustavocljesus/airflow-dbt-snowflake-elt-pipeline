{{ config(schema='marts', materialized='table') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['id_cidades']) }} AS cidade_sk,
    id_cidades AS cidade_id,
    nome_cidade,
    e.estado_sk,
    data_inclusao,
    data_atualizacao
FROM {{ ref('stg_cidades') }} c
JOIN {{ ref('dim_estados') }} e
    ON c.id_estados = e.estado_id
