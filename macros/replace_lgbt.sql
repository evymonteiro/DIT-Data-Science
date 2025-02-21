{% macro replace_lgbt(text) %}
  UPPER(
    regexp_replace(
      regexp_replace(
        regexp_replace(
          {{ text }},
          r'(gay/lesbica|lesbica/gay|gay|lésbica)',
          'HOMOSSEXUAL'
        ),
        r'HOMOSSEXUAL\sHOMOSSEXUAL',
        'HOMOSSEXUAL'
      ),
      r'\s+',
      ' '
    )
  )
{% endmacro %}