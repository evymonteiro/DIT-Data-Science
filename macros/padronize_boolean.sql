-- Altera colunas booleanas para o padrão 0 e 1. 
{% macro padronize_boolean(column_name) %}
    CASE
        WHEN {{ column_name }} IN ('True', '1') THEN 1
        WHEN {{ column_name }} IN ('False', '0') THEN 0
        ELSE CAST({{ column_name }} AS INT64)
    END
{% endmacro %}