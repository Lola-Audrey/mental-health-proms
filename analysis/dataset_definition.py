from ehrql import create_dataset
from ehrql.tables.tpp import patients, practice_registrations, addresses, clinical_events
from codelists import ethnicity, phq_ob, phq_pro, gad_ob, gad_pro
dataset = create_dataset()

index_date = "2024-03-31"

has_registration = practice_registrations.for_patient_on(
    index_date
).exists_for_patient()

age = patients.age_on(index_date)
is_16_or_older = age >= 16
is_alive = patients.is_alive_on(index_date)

# Restrict events to last year window
previous_events = clinical_events.where(
    clinical_events.date.is_on_or_before(index_date)
    )

# proms score and procedure events 
phq9_score_event = previous_events.where(clinical_events.snomedct_code.is_in(phq_ob))
phq9_proc_event = previous_events.where(clinical_events.snomedct_code.is_in(phq_pro))
gad7_score_event = previous_events.where(clinical_events.snomedct_code.is_in(gad_ob))
gad7_proc_event = previous_events.where(clinical_events.snomedct_code.is_in(gad_pro))

invalid_phq9_score = phq9_score_event.where((clinical_events.numeric_value < 0) | (clinical_events.numeric_value > 27))
invalid_gad7_score = gad7_score_event.where((clinical_events.numeric_value < 0) | (clinical_events.numeric_value > 21))

# proms counts
phq9_score_count = phq9_score_event.count_for_patient()
phq9_proc_count = phq9_proc_event.count_for_patient()
gad7_score_count = gad7_score_event.count_for_patient()
gad7_proc_count = gad7_proc_event.count_for_patient()
prom_score_count = phq9_score_count + gad7_score_count

phq9_out_of_range_count = invalid_phq9_score.count_for_patient()
gad7_out_of_range_count = invalid_gad7_score.count_for_patient()

# proms flags
has_phq9_score = phq9_score_count > 0
has_gad7_score = gad7_score_count > 0

has_any_prom = (has_phq9_score | has_gad7_score)
more_than_one_prom = prom_score_count > 1

# dataset
dataset.define_population(has_registration & is_16_or_older & is_alive)

dataset.sex = patients.sex
dataset.age = age
dataset.imd = addresses.for_patient_on(index_date).imd_quintile
dataset.region = practice_registrations.for_patient_on(index_date).practice_nuts1_region_name
dataset.latest_ethnicity_group = (
  previous_events.where(clinical_events.snomedct_code.is_in(ethnicity))
  .sort_by(clinical_events.date)
  .last_for_patient().snomedct_code
  .to_category(ethnicity)
)
dataset.has_any_prom = has_any_prom
dataset.phq9_score_count = phq9_score_count
dataset.gad7_score_count = gad7_score_count
dataset.prom_score_count = prom_score_count
dataset.phq9_out_of_range_count = phq9_out_of_range_count 
dataset.gad7_out_of_range_count = gad7_out_of_range_count 