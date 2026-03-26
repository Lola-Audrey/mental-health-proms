from datetime import date
from dataset_definition import dataset

# Test data structure with patients and expected outcomes
test_data = {
    # CORRECTLY NOT IN POPULATION (Patients: 1, 2, 4)
    # Test patient 1: No registration on index date
    1: {
        "patients": {"date_of_birth": date(1980, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(2020, 1, 1),
                "end_date": date(2023, 12, 31),
                "practice_nuts1_region_name": "North West",
            },
        ],
        "addresses": [
            {
                "start_date": date(2020, 1, 1),
                "end_date": date(2023, 12, 31),
                "imd_rounded": 4500,
            },
        ],
        "clinical_events": [
            {
                "date": date(2024, 1, 15),
                "snomedct_code": "720433000",  # PHQ-9 score code
                "numeric_value": 15,
            },
        ],
        "expected_in_population": False,
    },
    # Test patient 2: Too young - under 16 years old
    2: {
        "patients": {"date_of_birth": date(2016, 6, 1)},
        "practice_registrations": [
            {
                "start_date": date(2020, 1, 1),
                "practice_nuts1_region_name": "North West",
            },
        ],
        "addresses": [
            {
                "start_date": date(2020, 1, 1),
                "imd_rounded": 4500,
            },
        ],
        "clinical_events": [],
        "expected_in_population": False,
    },
    # Test patient 4: Not alive on index date
    4: {
        "patients": {
            "date_of_birth": date(1970, 1, 1),
            "date_of_death": date(2024, 1, 1),
        },
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
                "practice_nuts1_region_name": "East Midlands",
            },
        ],
        "addresses": [
            {
                "start_date": date(2010, 1, 1),
                "imd_rounded": 4500,
            },
        ],
        "clinical_events": [
            {
                # PHQ-9 score code
                "date": date(2023, 6, 15),
                "snomedct_code": "720433000",
                "numeric_value": 14,
            },
        ],
        "expected_in_population": False,
    },
    # CORRECTLY IN POPULATION (Patients 5, 6, 7, 8, 9)
    # Test patient 5: Both valid PHQ-9 and GAD-7 scores
    5: {
        "patients": {
            "date_of_birth": date(1970, 1, 1),
            "sex": "female",
        },
        "practice_registrations": [
            {
                "start_date": date(2005, 1, 1),
                "practice_nuts1_region_name": "East",
            },
        ],
        "addresses": [
            {
                "start_date": date(2005, 1, 1),
                "imd_rounded": 3000,
            },
        ],
        "clinical_events": [
            {
                # PHQ-9 score code
                "date": date(2024, 1, 10),
                "snomedct_code": "720433000",
                "numeric_value": 18,
            },
            {
                # GAD-7 score code
                "date": date(2024, 2, 20),
                "snomedct_code": "445455005",
                "numeric_value": 10,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "sex": "female",
            "age": 54,
            "imd": "1 (most deprived)",
            "region": "East",
            "latest_ethnicity_group": None,
            "has_any_prom_score": True,
            "has_more_than_one_prom_score": True,
            "phq9_score_count": 1,
            "gad7_score_count": 1,
            "prom_score_count": 2,
            "phq9_out_of_range_count": 0,
            "gad7_out_of_range_count": 0,
            "phq9_procedure_count": 0,
            "gad7_procedure_count": 0,
            "has_prom_proc_score_mismatch": True,
        },
    },
    # Test patient 6: Multiple valid PROM scores
    6: {
        "patients": {
            "date_of_birth": date(1965, 1, 1),
            "sex": "male",
        },
        "practice_registrations": [
            {
                "start_date": date(2008, 1, 1),
                "practice_nuts1_region_name": "London",
            },
        ],
        "addresses": [
            {
                "start_date": date(2008, 1, 1),
                "imd_rounded": 32000,
            },
        ],
        "clinical_events": [
            {
                # PHQ-9 score code
                "date": date(2024, 1, 5),
                "snomedct_code": "720433000",
                "numeric_value": 8,
            },
            {
                # PHQ-9 score code again
                "date": date(2024, 1, 15),
                "snomedct_code": "720433000",
                "numeric_value": 11,
            },
            {
                # GAD-7 score code
                "date": date(2024, 2, 28),
                "snomedct_code": "445455005",
                "numeric_value": 7,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "sex": "male",
            "age": 59,
            "imd": "5 (least deprived)",
            "region": "London",
            "latest_ethnicity_group": None,
            "has_any_prom_score": True,
            "has_more_than_one_prom_score": True,
            "phq9_score_count": 2,
            "gad7_score_count": 1,
            "prom_score_count": 3,
            "phq9_out_of_range_count": 0,
            "gad7_out_of_range_count": 0,
            "phq9_procedure_count": 0,
            "gad7_procedure_count": 0,
            "has_prom_proc_score_mismatch": True,
        },
    },
    # Test patient 7: Out of range PHQ-9 score
    # But still in population as it has out-of-range events
    7: {
        "patients": {
            "date_of_birth": date(1988, 1, 1),
            "sex": "female",
        },
        "practice_registrations": [
            {
                "start_date": date(2018, 1, 1),
                "practice_nuts1_region_name": "South East",
            },
        ],
        "addresses": [
            {
                "start_date": date(2018, 1, 1),
                "imd_rounded": 17000,
            },
        ],
        "clinical_events": [
            {
                # PHQ-9 score code
                # Out of range (0-27)
                "date": date(2024, 2, 14),
                "snomedct_code": "720433000",
                "numeric_value": 28,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "sex": "female",
            "age": 36,
            "imd": "3",
            "region": "South East",
            "latest_ethnicity_group": None,
            "has_any_prom_score": True,
            "has_more_than_one_prom_score": False,
            "phq9_score_count": 1,
            "gad7_score_count": 0,
            "prom_score_count": 1,
            "phq9_out_of_range_count": 1,
            "gad7_out_of_range_count": 0,
            "phq9_procedure_count": 0,
            "gad7_procedure_count": 0,
            "has_prom_proc_score_mismatch": True,
        },
    },
    # Test patient 8: Out of range GAD-7 score
    # But still in population as it has out-of-range events
    8: {
        "patients": {
            "date_of_birth": date(1990, 1, 1),
            "sex": "male",
        },
        "practice_registrations": [
            {
                "start_date": date(2016, 1, 1),
                "practice_nuts1_region_name": "South West",
            },
        ],
        "addresses": [
            {
                "start_date": date(2016, 1, 1),
                "imd_rounded": 26000,
            },
        ],
        "clinical_events": [
            {
                "date": date(2024, 3, 10),
                # GAD-7 score code
                "snomedct_code": "445455005",
                # Out of range (0-21)
                "numeric_value": 22,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "sex": "male",
            "age": 34,
            "imd": "4",
            "region": "South West",
            "latest_ethnicity_group": None,
            "has_any_prom_score": True,
            "has_more_than_one_prom_score": False,
            "phq9_score_count": 0,
            "gad7_score_count": 1,
            "prom_score_count": 1,
            "phq9_out_of_range_count": 0,
            "gad7_out_of_range_count": 1,
            "phq9_procedure_count": 0,
            "gad7_procedure_count": 0,
            "has_prom_proc_score_mismatch": True,
        },
    },
    # Test patient 9: Mix of valid and out-of-range scores
    9: {
        "patients": {
            "date_of_birth": date(1978, 1, 1),
            "sex": "female",
        },
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
                "practice_nuts1_region_name": "North East",
            },
        ],
        "addresses": [
            {
                "start_date": date(2010, 1, 1),
                "imd_rounded": 7500,
            },
        ],
        "clinical_events": [
            {
                # PHQ-9 score code
                # Valid
                "date": date(2024, 1, 20),
                "snomedct_code": "720433000",
                "numeric_value": 16,
            },
            {
                # PHQ-9 score code
                # Out of range
                "date": date(2024, 2, 10),
                "snomedct_code": "720433000",
                "numeric_value": -1,
            },
            {
                # GAD-7 score code
                # Valid
                "date": date(2024, 3, 5),
                "snomedct_code": "445455005",
                "numeric_value": 9,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "sex": "female",
            "age": 46,
            "imd": "2",
            "region": "North East",
            "latest_ethnicity_group": None,
            "has_any_prom_score": True,
            "has_more_than_one_prom_score": True,
            "phq9_score_count": 2,
            "gad7_score_count": 1,
            "prom_score_count": 3,
            "phq9_out_of_range_count": 1,
            "gad7_out_of_range_count": 0,
            "phq9_procedure_count": 0,
            "gad7_procedure_count": 0,
            "has_prom_proc_score_mismatch": True,
        },
    },
}
