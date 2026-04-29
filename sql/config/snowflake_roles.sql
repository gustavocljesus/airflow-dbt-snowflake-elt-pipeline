-- Permissões básicas de acesso
GRANT USAGE ON DATABASE <database> TO ROLE <role>;
GRANT USAGE ON ALL SCHEMAS IN DATABASE <database> TO ROLE <role>;

-- Permissões de leitura para consumo de dados
GRANT SELECT ON ALL TABLES IN DATABASE <database> TO ROLE <role>;
GRANT SELECT ON ALL VIEWS IN DATABASE <database> TO ROLE <role>;

-- Permissões para materializações do dbt
GRANT CREATE TABLE ON ALL SCHEMAS IN DATABASE <database> TO ROLE <role>;
GRANT CREATE VIEW ON ALL SCHEMAS IN DATABASE <database> TO ROLE <role>;
GRANT CREATE SCHEMA ON DATABASE <database> TO ROLE <role>;