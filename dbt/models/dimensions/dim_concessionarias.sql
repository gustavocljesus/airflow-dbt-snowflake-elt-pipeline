{{ config(schema='marts', materialized='table') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['id_concessionarias']) }} AS concessionaria_sk,
    id_concessionarias AS concessionaria_id,
    nome_concessionaria,
    ci.cidade_sk,
    data_inclusao,
    data_atualizacao
FROM {{ ref('stg_concessionarias') }} c
JOIN {{ ref('dim_cidades') }} ci
    ON c.id_cidades = ci.cidade_id
