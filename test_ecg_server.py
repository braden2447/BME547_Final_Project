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


@pytest.mark.parametrize("original_size, expected", [
    ([100, 100], [200, 200]),
    ([100, 400], [50, 200]),
    ([200, 100], [300, 150]),
    ([500, 200], [300, 120])])
def test_adj_factor(original_size, expected):
    from patient_gui import adj_factor
    assert adj_factor(original_size) == expected


def test_img_to_b64_str():
    from patient_gui import img_to_b64_str
    answer = img_to_b64_str("images/test_image.png")
    expected = "iVBORw0KGgoAAAANSUhE"
    assert answer[0:20] == expected


def test_patient_dict_upload():
    pass


def clear_test_database():
    PatientTest.objects.raw({}).delete()
