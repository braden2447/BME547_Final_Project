import pytest
from database_init import PatientTest


def test_get_mrns_from_database():
    from api.shared_methods import get_mrns_from_database
    # Add patients to test database
    PatientTest(MRN=1, patient_name="Ann Ables").save()
    PatientTest(MRN=2, patient_name="Bob Boyles").save()
    PatientTest(MRN=300, patient_name="Chris Chou").save()
    expected = [1, 2, 300]
    answer = get_mrns_from_database(PatientTest.objects.raw({}))
    clear_test_database()
    assert answer == expected


pytest.mark.parametrize("input, expected", [
    (60, (60, True)),
    (-4, (-4, True)),
    (-1, (-1, True)),
    ("60", (60, True)),
    ("-4", (-4, True)),
    ("-1", (-1, True)),
    ("Python", (-1, False)),
    ("negative one", (-1, False)),
    ("Five", (-1, False)),
    ("", (-1, False)),
    (100, (100, True))])
def test_str_to_int(input, expected):
    from api.shared_methods import str_to_int
    answer = str_to_int(input)
    assert answer == expected


def clear_test_database():
    PatientTest.objects.raw({}).delete()
