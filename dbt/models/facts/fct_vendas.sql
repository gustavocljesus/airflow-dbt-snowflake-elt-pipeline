{{ config(schema='marts', materialized='incremental', unique_key='venda_id') }}
WITH vendas AS (
    SELECT
        v.id_vendas AS venda_id,
        vei.veiculo_sk,
        con.concessionaria_sk,
        ve.vendedor_sk,
        c.cliente_sk,
        to_date(v.data_venda) AS data_venda_id,
        v.valor_venda, 
        v.data_venda AS data_venda_ts,
        v.data_inclusao,
        v.data_atualizacao
    FROM {{ ref('stg_vendas') }} v
    JOIN {{ ref('dim_veiculos') }} vei 
        ON v.id_veiculos = vei.veiculo_id
    JOIN {{ ref('dim_concessionarias') }} con 
        ON v.id_concessionarias = con.concessionaria_id
    JOIN {{ ref('dim_vendedores') }} ve 
        ON v.id_vendedores = ve.vendedor_id
    JOIN {{ ref('dim_clientes') }} c
        ON v.id_clientes = c.cliente_id
)

SELECT
    venda_id,
    veiculo_sk,
    concessionaria_sk,
    vendedor_sk,
    cliente_sk,
    data_venda_id,
    valor_venda,
    data_venda_ts,
    data_inclusao,
    data_atualizacao
FROM vendas
{% if is_incremental() %}
    WHERE data_inclusao > (SELECT MAX(data_inclusao) FROM {{ this }})
{% endif %}