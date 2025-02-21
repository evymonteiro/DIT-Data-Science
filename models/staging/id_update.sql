{{ config(
    materialized='view'
) }}

WITH pacientes AS (
    SELECT *,
           COUNT(id_paciente) OVER (PARTITION BY id_paciente) AS count_id_paciente
    FROM `data-science-dit`.`dataset`.`dataset`
)

SELECT 
    -- Caso o id_paciente seja duplicado, gera um novo ID.
    CASE 
        WHEN count_id_paciente > 1 THEN GENERATE_UUID()  --Não unico
        ELSE id_paciente
    END AS id_paciente,
    sexo,
    obito,
    bairro,
    raca_cor,
    ocupacao,
    religiao,
    luz_eletrica,
    data_cadastro,
    escolaridade,
    nacionalidade,
    renda_familiar,
    data_nascimento,
    em_situacao_de_rua,
    frequenta_escola,
    meios_transporte,
    doencas_condicoes,
    identidade_genero,
    meios_comunicacao,
    orientacao_sexual,
    possui_plano_saude,
    em_caso_doenca_procura,
    situacao_profissional,
    vulnerabilidade_social,
    data_atualizacao_cadastro,
    familia_beneficiaria_auxilio_brasil,
    crianca_matriculada_creche_pre_escola,
    altura,
    peso,
    pressao_sistolica,
    pressao_diastolica,
    n_atendimentos_atencao_primaria,
    n_atendimentos_hospital,
    updated_at,
    tipo
FROM pacientes