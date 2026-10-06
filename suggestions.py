def generate_suggestions(result):

    suggestions = []


    # ==========================================
    # BRIGHTNESS
    # ==========================================

    if result["brightness"] == "Dark":

        suggestions.append(
            "The photo is dark. Try increasing "
            "exposure or using more available light."
        )

    elif result["brightness"] == "Bright":

        suggestions.append(
            "The photo is quite bright. Reduce "
            "exposure slightly if highlights are overexposed."
        )

    else:

        suggestions.append(
            "The brightness looks good."
        )


    # ==========================================
    # CONTRAST
    # ==========================================

    if result["contrast"] == "Low":

        suggestions.append(
            "The photo has low contrast. Try "
            "increasing contrast slightly during editing."
        )

    elif result["contrast"] == "High":

        suggestions.append(
            "The photo has high contrast. Check "
            "for very dark shadows or bright highlights."
        )

    else:

        suggestions.append(
            "The contrast looks good."
        )


    # ==========================================
    # COMPOSITION
    # ==========================================

    if result["composition"] == "Landscape-oriented":

        suggestions.append(
            "For landscape photos, try using the "
            "Rule of Thirds, Leading Lines and "
            "foreground elements."
        )

    elif result["composition"] == "Portrait-oriented":

        suggestions.append(
            "For portrait photos, keep the subject "
            "clear and try using Negative Space."
        )

    else:

        suggestions.append(
            "Try placing the main subject according "
            "to the Rule of Thirds."
        )


    # ==========================================
    # SHARPNESS
    # ==========================================

    if result["sharpness"] == "Possibly blurry":

        suggestions.append(
            "The photo may be blurry. Try holding "
            "the camera steady and using a faster "
            "shutter speed."
        )

    elif result["sharpness"] == "Moderately sharp":

        suggestions.append(
            "The photo has moderate sharpness. "
            "Try focusing carefully on the main subject."
        )

    else:

        suggestions.append(
            "The photo appears sharp and well-focused."
        )


    # ==========================================
    # VISUAL DETAIL
    # ==========================================

    if result["visual_detail"] == "Low visual detail":

        suggestions.append(
            "The image has low visual detail. "
            "Consider adding interesting textures, "
            "patterns or stronger subject separation."
        )

    elif result["visual_detail"] == "Moderate visual detail":

        suggestions.append(
            "The image has a moderate amount of detail. "
            "Look for stronger textures, patterns or "
            "leading lines when possible."
        )

    else:

        suggestions.append(
            "The image contains a high amount of visual detail."
        )


    return suggestions