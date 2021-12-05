import pytest
from api.shared_methods import get_patient_from_db, get_patient_from_db_pt
from database_init import PatientTest


def test_get_mrns_from_database():
    from api.shared_methods import get_mrns_from_database
    # Add patients to test database
    clear_test_database()
    PatientTest(MRN=1, patient_name="Ann Ables").save()
    PatientTest(MRN=2, patient_name="Bob Boyles").save()
    PatientTest(MRN=300, patient_name="Chris Chou").save()
    expected = [1, 2, 300]
    answer = get_mrns_from_database(PatientTest.objects.raw({}))
    assert answer == expected
    clear_test_database()


def test_post_new_patient_info_route():
    from api.shared_methods import update_patient_fields_pt
    import image_toolbox as itb
    clear_test_database()

    # Test that patient is added successfully to database
    b64_image = itb.file_to_b64("images/test_image.png")
    b64_medical_image = itb.file_to_b64("images/esophagus2.jpg")
    MRN = 5
    pat5_info = {
        'MRN': MRN,
        'patient_name': "Bob Boyles",
        'ECG_trace': b64_image,
        'heart_rate': 60,
        'medical_image': b64_medical_image
    }
    expected_patient = PatientTest(MRN=MRN, patient_name="Bob Boyles",
                                   ECG_trace=[b64_image],
                                   heart_rate=[60],
                                   medical_image=[b64_medical_image])
    update_patient_fields_pt(MRN, pat5_info)
    answer_patient = get_patient_from_db_pt(MRN)
    assert answer_patient.MRN == expected_patient.MRN
    assert answer_patient.patient_name == expected_patient.patient_name
    assert (answer_patient.ECG_trace[0][:20] ==
            expected_patient.ECG_trace[0][:20])
    assert answer_patient.heart_rate == expected_patient.heart_rate
    assert (answer_patient.medical_image[0][:20] ==
            expected_patient.medical_image[0][:20])
    clear_test_database()


def test_field_from_patient():
    from api.shared_methods import field_from_patient

    # Add patients to test database
    from api.shared_methods import update_patient_fields_pt
    import image_toolbox as itb
    clear_test_database()

    # Test that patient is added successfully to database
    b64_image = itb.file_to_b64("images/test_image.png")
    b64_medical_image = itb.file_to_b64("images/esophagus2.jpg")
    MRN = 5
    pat5_info_1 = {
        'MRN': MRN,
        'patient_name': "Bob Boyles",
        'ECG_trace': b64_image,
        'heart_rate': 60,
        'medical_image': b64_medical_image
    }
    update_patient_fields_pt(MRN, pat5_info_1)
    pat5_info_2 = {
        'MRN': MRN,
        'ECG_trace': b64_image,
        'heart_rate': 65,
        'medical_image': b64_medical_image
    }
    update_patient_fields_pt(MRN, pat5_info_2)

    valid_fields = ['MRN', 'patient_name', 'ECG_trace',
                    'heart_rate', 'receipt_timestamps', 'medical_image']
    patient = get_patient_from_db_pt(MRN)

    expected = [5, "Bob Boyles", [b64_image, b64_image], [60, 65],
                [b64_medical_image, b64_medical_image]]

    result, sc = field_from_patient("MRN", valid_fields, patient)
    assert result == expected[0]
    result, sc = field_from_patient("patient_name", valid_fields, patient)
    assert result == expected[1]
    result, sc = field_from_patient("ECG_trace", valid_fields, patient)
    assert result == expected[2]
    result, sc = field_from_patient("heart_rate", valid_fields, patient)
    assert result == expected[3]
    result, sc = field_from_patient("medical_image", valid_fields, patient)
    assert result == expected[4]
    clear_test_database()


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


@pytest.mark.parametrize("input, expected", [
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


@pytest.mark.parametrize("mrn, name, hr, ecg, med, expected", [
    (1, "Ann Ables", None, None, None,
     {"MRN": 1, "patient_name": "Ann Ables"}),
    (2, "", 75, None, None,
     {"MRN": 2}),
    (3, "Bob Boyles", 65, "ecg_b64_str", "med_b64_str",
     {"MRN": 3, "patient_name": "Bob Boyles", "ECG_trace": "ecg_b64_str",
      "heart_rate": 65, "medical_image": "med_b64_str"})])
def test_create_pat_dict(mrn, name, hr, ecg, med, expected):
    from patient_gui import create_pat_dict
    answer = create_pat_dict(mrn, name, hr, ecg, med)
    assert answer == expected


def clear_test_database():
    PatientTest.objects.raw({}).delete()
