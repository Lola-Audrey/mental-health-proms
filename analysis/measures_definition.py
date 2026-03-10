from ehrql import INTERVAL, create_measures, months, case, when, years
from ehrql.tables.tpp import patients, practice_registrations, addresses, clinical_events
from codelists import ethnicity, phq_ob, phq_pro, gad_ob, gad_pro

measures = create_measures()

selected_events = clinical_events.where(clinical_events.date <= INTERVAL.end_date)

# Base Population
aged_16_or_older = patients.age_on(INTERVAL.end_date) >= 16
is_alive = patients.is_alive_on(INTERVAL.end_date)
is_registered = (
    practice_registrations.where(practice_registrations.start_date <= INTERVAL.end_date)
    .except_where(practice_registrations.end_date < INTERVAL.end_date)
    .exists_for_patient()
)
base_population = aged_16_or_older & is_alive & is_registered
# Grouping
age = patients.age_on(INTERVAL.start_date)
age_band = case(
    when((age >= 0) & (age < 20)).then("0-19"),
    when((age >= 20) & (age < 40)).then("20-39"),
    when((age >= 40) & (age < 60)).then("40-59"),
    when((age >= 60) & (age < 80)).then("60-79"),
    when(age >= 80).then("80+"),
)


ethnicity = (
    selected_events.where(clinical_events.snomedct_code.is_in(ethnicity))
    .sort_by(clinical_events.date)
    .last_for_patient().snomedct_code
    .to_category(ethnicity)
)
  
ethnicity_group = case(
    when(ethnicity == "1").then("White"),
    when(ethnicity == "2").then("Mixed"),
    when(ethnicity == "3").then("Asian or Asian British"),
    when(ethnicity == "4").then("Black or Black British"),
    when(ethnicity == "5").then("Chinese or Other Ethnic Groups"),
)

region = practice_registrations.for_patient_on(INTERVAL.end_date).practice_nuts1_region_name
imd = addresses.for_patient_on(INTERVAL.end_date).imd_quintile
has_recorded_ethnicity = ethnicity.is_not_null()  
has_recorded_imd = imd.is_not_null()
has_recorded_region = region.is_not_null()
has_recorded_age = age.is_not_null()
has_recorded_sex = patients.sex.is_not_null()

# PROMs measures

# Patients that completed a questionnaire for Depression or Anxiety at least once in the last year
phq9_score_event = selected_events.where(clinical_events.snomedct_code.is_in(phq_ob))
gad7_score_event = selected_events.where(clinical_events.snomedct_code.is_in(gad_ob))       
phq9_score_count = phq9_score_event.count_for_patient()
gad7_score_count = gad7_score_event.count_for_patient()     
has_completed_phq9 = phq9_score_count >= 1
has_completed_gad7 = gad7_score_count >= 1

has_at_least_one_prom = (has_completed_phq9 | has_completed_gad7)

measures.define_measure(
    name="patients_completed_at_least_one_prom",
    numerator=has_at_least_one_prom,
    denominator=base_population,
    intervals= years(10).ending_on("2024-03-31")
)



 