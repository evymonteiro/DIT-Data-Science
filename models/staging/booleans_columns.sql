WITH raw_data AS (
    SELECT * 
    FROM `data-science-dit`.`dataset`.`dataset`
)
SELECT
    id_paciente,
    {{ padronize_boolean('obito') }} AS obito,
    {{ padronize_boolean('luz_eletrica') }} AS luz_eletrica,
    {{ padronize_boolean('em_situacao_de_rua') }} AS em_situacao_de_rua,
    {{ padronize_boolean('possui_plano_saude') }} AS possui_plano_saude,
    {{ padronize_boolean('vulnerabilidade_social') }} AS vulnerabilidade_social,
    {{ padronize_boolean('familia_beneficiaria_auxilio_brasil') }} AS familia_beneficiaria_auxilio_brasil,
    {{ padronize_boolean('crianca_matriculada_creche_pre_escola') }} AS crianca_matriculada_creche_pre_escola
FROM raw_data