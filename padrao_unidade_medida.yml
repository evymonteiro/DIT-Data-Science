WITH raw_data AS (
    SELECT * 
    FROM `data-science-dit`.`dataset`.`dataset`
)

SELECT
    id_paciente,
    {{ clean_text_name('doencas_condicoes') }} AS doencas_condicoes,
    {{ clean_text_name('meios_comunicacao') }} AS meios_comunicacao,
    {{ clean_text_name('meios_transporte') }} AS meios_transporte,
    {{ clean_text_name('em_caso_doenca_procura') }} AS em_caso_doenca_procura
FROM raw_data