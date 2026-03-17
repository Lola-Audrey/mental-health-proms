from ehrql import codelist_from_csv

phq_ob = codelist_from_csv("codelists/user-Lola_O-phq9_score_codes.csv", column="code")
phq_pro = codelist_from_csv("codelists/user-Lola_O-phq9_procedure_codes.csv", column="code")

gad_ob = codelist_from_csv("codelists/user-Lola_O-gad7_score_codes.csv", column="code")
gad_pro = codelist_from_csv("codelists/user-Lola_O-gad7_procedure_codes.csv", column="code")

ethnicity = codelist_from_csv("codelists/opensafely-ethnicity-snomed-0removed.csv", column="code", category_column="Grouping_6")
