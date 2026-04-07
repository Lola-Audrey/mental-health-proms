from ehrql import codelist_from_csv

phq9_observable_entity_cod = codelist_from_csv(
    "codelists/user-Lola_O-phq9_score_codes.csv",
    column="code",
)
phq9_procedure_cod = codelist_from_csv(
    "codelists/user-Lola_O-phq9_procedure_codes.csv",
    column="code",
)

gad7_observable_entity_cod = codelist_from_csv(
    "codelists/user-Lola_O-gad7_score_codes.csv",
    column="code",
)
gad7_procedure_cod = codelist_from_csv(
    "codelists/user-Lola_O-gad7_procedure_codes.csv",
    column="code",
)

ethnicity_cod = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column="code",
    category_column="Grouping_6",
)
