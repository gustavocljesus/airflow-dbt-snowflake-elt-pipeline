{{ config(schema='marts', materialized='table') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['id_estados']) }} AS estado_sk,
    id_estados AS estado_id,
    estado AS nome_estado,
    sigla,
    data_inclusao,
    data_atualizacao
FROM {{ ref('stg_estados') }}
