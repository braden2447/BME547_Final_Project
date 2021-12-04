import pytest
import base64

from image_toolbox import ndarray_to_b64


def test_file_to_b64():
    from image_toolbox import file_to_b64
    answer = file_to_b64("images/test_image.png")
    expected = "iVBORw0KGgoAAAANSUhE"
    assert answer[0:20] == expected
    answer = file_to_b64("images/esophagus 1.jpg")
    expected = "/9j/4AAQSkZJRgABAgAA"
    assert answer[0:20] == expected


def test_b64_to_file():
    from image_toolbox import b64_to_file, file_to_b64
    import os
    from os.path import exists
    import filecmp

    b64_image = file_to_b64("images/test_image.png")
    save_file_path = "images/test_image_test.png"
    b64_to_file(b64_image, save_file_path)
    answer = filecmp.cmp("images/test_image.png",
                         save_file_path)
    assert answer and exists(save_file_path)
    os.remove(save_file_path)


def test_b64_to_ndarray():
    from image_toolbox import b64_to_ndarray
    from image_toolbox import file_to_b64
    import numpy as np

    input_b64 = file_to_b64("images/test_image.png")
    answer_ndarray = b64_to_ndarray(input_b64)
    expected_ndarray = np.ones((98, 3))
    assert (answer_ndarray[1] == expected_ndarray).all()


def test_ndarray_to_b64():
    from image_toolbox import b64_to_ndarray, ndarray_to_b64
    from image_toolbox import file_to_b64
    import numpy as np

    input_b64 = file_to_b64("images/test_image.png")
    answer_ndarray = b64_to_ndarray(input_b64)
    answer_b64 = ndarray_to_b64(answer_ndarray)
    expected_b64 = "iVBORw0KGgoAAAANSUhE"
    assert answer_b64[:20] == expected_b64
