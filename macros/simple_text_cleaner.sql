{% macro clean_text_simple(text) %}
  UPPER(
    regexp_replace(
      regexp_replace(
        regexp_replace(
          {{ text }},
          r'\[|\]', -- Remove colchetes
          ''
        ),
        r'\'|\"', -- Remove aspas simples e duplas
        ''
      ),
      r'\s+', -- Remove espaços extras
      ' '
    )
  )
{% endmacro %}