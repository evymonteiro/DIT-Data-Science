WITH raw_data AS (
    SELECT *
    FROM `data-science-dit.dataset.dataset`
)

SELECT
    id_paciente,
    
    -- A partir da análise de Quartis:
    CASE 
        WHEN pressao_sistolica > 250 THEN pressao_sistolica / 10
        ELSE pressao_sistolica
    END AS pressao_sistolica_cm,  -- Pressão Sistólica em mmHg
    
    CASE 
        WHEN pressao_diastolica > 150 THEN pressao_diastolica / 10
        ELSE pressao_diastolica
    END AS pressao_diastolica_cm,  -- Pressão Diastólica em mmHg
    
    -- valores > 300cm serão divididos por 100, para corrigir em cm
    CASE
        WHEN altura > 300 THEN altura / 100
        ELSE altura
    END AS altura_cm,
    
    -- valores > 250 serão convertidos de hectogramas para kg, dividindo por 100
    CASE 
        WHEN peso > 250 THEN peso / 100
        ELSE peso
    END AS peso_kg,
FROM raw_data