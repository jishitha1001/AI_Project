import ollama


MODEL_NAME = "llama3.2"


def generate_ai_advice(
    image_analysis,
    photography_tips
):
    """
    Generate personalized photography advice
    using the local Ollama LLM.
    """

    tips = "\n\n".join(
        photography_tips
    )

    prompt = f"""
You are an expert photography assistant.

Analyze the following photo information
and provide simple, practical photography advice
for a beginner photographer.

IMAGE ANALYSIS:

Brightness:
{image_analysis['brightness']}

Brightness Value:
{image_analysis['brightness_value']}

Contrast:
{image_analysis['contrast']}

Contrast Value:
{image_analysis['contrast_value']}

Composition:
{image_analysis['composition']}

Sharpness:
{image_analysis['sharpness']}

Sharpness Value:
{image_analysis['sharpness_value']}

Visual Detail:
{image_analysis['visual_detail']}

Visual Detail Value:
{image_analysis['visual_detail_value']}

Image Size:
{image_analysis['width']} x {image_analysis['height']}


RELEVANT PHOTOGRAPHY KNOWLEDGE:

{tips}


Give your response in this format:

Composition:
Give one or two useful suggestions.

Lighting:
Give one or two useful suggestions.

Focus and Sharpness:
Give one or two useful suggestions.

Overall Improvement:
Give two or three practical suggestions.

Keep the answer simple and beginner-friendly.

IMPORTANT:
Only make conclusions supported by the
image analysis and photography knowledge.

Do not claim that you detected a specific
person, object, face, or scene because the
current analysis does not identify objects.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response[
        "message"
    ][
        "content"
    ]