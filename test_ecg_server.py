import pytest
from database_init import PatientTest


def test_get_mrn_route():
    from api.shared_methods import get_mrns_from_database
    # Add patients to test database
    PatientTest(MRN=1, patient_name="Ann Ables").save()
    PatientTest(MRN=2, patient_name="Bob Boyles").save()
    PatientTest(MRN=300, patient_name="Chris Chou").save()
    expected = [1, 2, 300]
    answer = get_mrns_from_database(PatientTest.objects.raw({}))
    clear_test_database()
    assert answer == expected


def clear_test_database():
    PatientTest.objects.raw({}).delete()
