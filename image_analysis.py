from PIL import Image, ImageStat
import cv2
import numpy as np


# ==========================================
# BRIGHTNESS ANALYSIS
# ==========================================

def analyze_brightness(image):

    grayscale = image.convert("L")

    statistics = ImageStat.Stat(
        grayscale
    )

    brightness = statistics.mean[0]

    if brightness < 80:
        result = "Dark"

    elif brightness > 180:
        result = "Bright"

    else:
        result = "Good"

    return result, brightness


# ==========================================
# CONTRAST ANALYSIS
# ==========================================

def analyze_contrast(image):

    grayscale = image.convert("L")

    statistics = ImageStat.Stat(
        grayscale
    )

    contrast = statistics.stddev[0]

    if contrast < 40:
        result = "Low"

    elif contrast > 80:
        result = "High"

    else:
        result = "Good"

    return result, contrast


# ==========================================
# COMPOSITION ANALYSIS
# ==========================================

def analyze_composition(image):

    width, height = image.size

    aspect_ratio = width / height

    if aspect_ratio > 1.5:

        composition = "Landscape-oriented"

    elif aspect_ratio < 0.75:

        composition = "Portrait-oriented"

    else:

        composition = "Balanced frame"

    return composition


# ==========================================
# SHARPNESS / FOCUS ANALYSIS
# ==========================================

def analyze_sharpness(image_path):

    image = cv2.imread(
        image_path
    )

    grayscale = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Laplacian detects rapid changes
    # in image details.

    sharpness = cv2.Laplacian(
        grayscale,
        cv2.CV_64F
    ).var()


    if sharpness < 100:

        result = "Possibly blurry"

    elif sharpness < 300:

        result = "Moderately sharp"

    else:

        result = "Sharp"


    return result, sharpness


# ==========================================
# EDGE / DETAIL ANALYSIS
# ==========================================

def analyze_edges(image_path):

    image = cv2.imread(
        image_path
    )

    grayscale = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.Canny(
        grayscale,
        100,
        200
    )

    edge_pixels = np.count_nonzero(
        edges
    )

    total_pixels = edges.size

    edge_percentage = (
        edge_pixels /
        total_pixels
    ) * 100


    if edge_percentage < 3:

        result = "Low visual detail"

    elif edge_percentage < 10:

        result = "Moderate visual detail"

    else:

        result = "High visual detail"


    return result, edge_percentage


# ==========================================
# COMPLETE IMAGE ANALYSIS
# ==========================================

def analyze_image(image_path):

    image = Image.open(
        image_path
    )


    # --------------------------------------
    # BASIC ANALYSIS
    # --------------------------------------

    brightness_result, brightness_value = (
        analyze_brightness(image)
    )


    contrast_result, contrast_value = (
        analyze_contrast(image)
    )


    composition = analyze_composition(
        image
    )


    # --------------------------------------
    # COMPUTER VISION ANALYSIS
    # --------------------------------------

    sharpness_result, sharpness_value = (
        analyze_sharpness(image_path)
    )


    detail_result, detail_value = (
        analyze_edges(image_path)
    )


    # --------------------------------------
    # RETURN RESULTS
    # --------------------------------------

    return {

        "width": image.width,

        "height": image.height,


        "brightness": brightness_result,

        "brightness_value": round(
            brightness_value,
            2
        ),


        "contrast": contrast_result,

        "contrast_value": round(
            contrast_value,
            2
        ),


        "composition": composition,


        "sharpness": sharpness_result,

        "sharpness_value": round(
            sharpness_value,
            2
        ),


        "visual_detail": detail_result,

        "visual_detail_value": round(
            detail_value,
            2
        )
    }