import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from skimage.io import imsave


def b64_to_file(b64_string, new_filename):
    """Converts b64 string to image file, saved
    as new_filename

    Args:
        b64_string: string variable containing the image bytes
                    encoded as a base64 string
        new_filename: filepath to save file as

    Returns:
       an image file on the local computer with the path and name
       contained in the new_filename variable
    """
    image_bytes = base64.b64decode(b64_string)
    with open(new_filename, "wb") as out_file:
        out_file.write(image_bytes)
    return None


def file_to_b64(filename):
    """Converts image file ti b64 string

    Args:
        filename: string variable containing the path and name of the
                 image file on computer
        new_filename: filepath to save file as

    Returns:
       b64_string: string variable containing the image bytes encoded
                   as a base64 string
    """
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')

    return b64_string


def b64_to_ndarray(b64_string):
    """Converts b64 string to numpy ndarray

    Args:
        b64_string: string variable containing the image bytes
                   encoded as a base64 string

    Returns:
       img_ndarray: variable containing an ndarray with image data
    """
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def ndarray_to_b64(img_ndarray):
    """Converts b64 string to numpy ndarray

    Args:
        img_ndarray:  variable containing an ndarray with image data

    Returns:
       b64_string: string variable containing image bytes encoded
                   as a base64 string
    """
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    y = base64.b64encode(f.getvalue())
    b64_string = str(y, encoding='utf-8')
    return b64_string


def plot_image(img_ndarray):
    """Converts b64 string to numpy ndarray

    Args:
       img_ndarray: variable containing an ndarray with image data

    Returns:
       A `matplotlib` window with an image
    """
    plt.imshow(img_ndarray, interpolation='nearest')
    plt.show()
