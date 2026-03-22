{{ config(schema='marts', materialized='table') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['id_clientes']) }} AS cliente_sk,
    id_clientes AS cliente_id,
    cliente AS nome_cliente,
    endereco,
    co.concessionaria_sk,
    data_inclusao,
    data_atualizacao
FROM {{ ref('stg_clientes') }} c
JOIN {{ ref('dim_concessionarias') }} co
    ON c.id_concessionarias = co.concessionaria_id
