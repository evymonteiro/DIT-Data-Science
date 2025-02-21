WITH raw_data AS (
    SELECT * 
    FROM `data-science-dit`.`dataset`.`dataset`
)

SELECT
    id_paciente,
    {{ clean_text_simple('raca_cor') }} AS raca_cor,
    {{ clean_text_simple('bairro') }} AS bairro,
    {{ clean_text_simple('religiao') }} AS religiao,
    {{ clean_text_simple('escolaridade') }} AS escolaridade,
    {{ clean_text_simple('nacionalidade') }} AS nacionalidade,
    {{ replace_lgbt(clean_text_simple('orientacao_sexual')) }} AS orientacao_sexual
FROM raw_data