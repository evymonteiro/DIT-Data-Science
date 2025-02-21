{% macro clean_text_name(text) %}
    upper(
        trim(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        regexp_replace(
                            normalize({{ text }}, nfd), 
                            r'\p{M}', ''),  -- Remove acentos
                        r'\["|\]|\\"|\\\'|,",', ''),  -- Remove colchetes, aspas e vírgulas
                    r'\\', ''),  -- Remove barras invertidas
                r'\d', ''  -- Remove todos os números
            )
        )
    )
{% endmacro %}