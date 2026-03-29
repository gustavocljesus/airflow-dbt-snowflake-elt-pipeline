{{ config(schema='marts', materialized='table') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['id_vendedores']) }} AS vendedor_sk,
    v.id_vendedores AS vendedor_id,
    v.nome_vendedor,
    c.concessionaria_sk,
    v.data_inclusao,
    v.data_atualizacao
FROM {{ ref('stg_vendedores') }} v
JOIN {{ ref('dim_concessionarias') }} c
    ON v.id_concessionarias = c.concessionaria_id
