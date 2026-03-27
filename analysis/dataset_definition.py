from ehrql import create_dataset, months
from ehrql.tables.tpp import (
    patients,
    practice_registrations,
    addresses,
    clinical_events,
)
from variables_library import get_invalid_scores
from codelists import (
    ethnicity_cod,
    phq9_observable_entity_cod,
    phq9_procedure_cod,
    gad7_observable_entity_cod,
    gad7_procedure_cod,
)

dataset = create_dataset()

index_date = "2024-03-31"
time_interval = months(12)

# Define study population
has_registration = practice_registrations.for_patient_on(
    index_date
).exists_for_patient()

age = patients.age_on(index_date)
is_16_or_older = age >= 16
is_alive = patients.is_alive_on(index_date)

# Restrict events to one year interval before index date
previous_events = clinical_events.where(
    clinical_events.date.is_on_or_between(index_date - time_interval, index_date)
)

# Get PROMs score and procedure events
phq9_score_event = previous_events.where(
    clinical_events.snomedct_code.is_in(phq9_observable_entity_cod)
)
phq9_procedure_event = previous_events.where(
    clinical_events.snomedct_code.is_in(phq9_procedure_cod)
)
gad7_score_event = previous_events.where(
    clinical_events.snomedct_code.is_in(gad7_observable_entity_cod)
)
gad7_procedure_event = previous_events.where(
    clinical_events.snomedct_code.is_in(gad7_procedure_cod)
)

# Check for questionnaire scores that are outside the possible range
invalid_phq9_scores = get_invalid_scores(phq9_score_event, "phq9")
invalid_gad7_scores = get_invalid_scores(gad7_score_event, "gad7")

# PROMs-related patient counts
dataset.count_phq9_score = phq9_score_event.count_for_patient()
dataset.count_phq9_procedure = phq9_procedure_event.count_for_patient()
dataset.count_gad7_score = gad7_score_event.count_for_patient()
dataset.count_gad7_procedure = gad7_procedure_event.count_for_patient()
dataset.count_all_proms_score = dataset.count_phq9_score + dataset.count_gad7_score
dataset.count_all_proms_procedure = (
    dataset.count_phq9_procedure + dataset.count_gad7_procedure
)

dataset.count_phq9_out_of_range = invalid_phq9_scores.count_for_patient()
dataset.count_gad7_out_of_range = invalid_gad7_scores.count_for_patient()

# PROMs flags
dataset.has_phq9_score = dataset.count_phq9_score > 0
dataset.has_gad7_score = dataset.count_gad7_score > 0
dataset.has_phq9_procedure = dataset.count_phq9_procedure > 0
dataset.has_gad7_procedure = dataset.count_gad7_procedure > 0
dataset.has_any_proms_score = dataset.has_phq9_score | dataset.has_gad7_score

# Demographic variables
dataset.sex = patients.sex
dataset.age = age
dataset.imd = addresses.for_patient_on(index_date).imd_quintile
dataset.region = practice_registrations.for_patient_on(
    index_date
).practice_nuts1_region_name
dataset.latest_ethnicity_group = (
    previous_events.where(clinical_events.snomedct_code.is_in(ethnicity_cod))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .snomedct_code.to_category(ethnicity_cod)
)

# Define population
dataset.define_population(has_registration & is_16_or_older & is_alive)
