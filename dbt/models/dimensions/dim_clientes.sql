{{ config(schema='marts', materialized='table') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['id_clientes']) }} AS cliente_sk,
    c.id_clientes AS cliente_id,
    c.cliente AS nome_cliente,
    c.endereco,
    co.concessionaria_sk,
    c.data_inclusao,
    c.data_atualizacao
FROM {{ ref('stg_clientes') }} c
JOIN {{ ref('dim_concessionarias') }} co
    ON c.id_concessionarias = co.concessionaria_id
