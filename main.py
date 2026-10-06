from image_analysis import analyze_image
from suggestions import generate_suggestions

from rag import (
    load_knowledge,
    create_embeddings,
    create_vector_database,
    search_knowledge
)

from llm import generate_ai_advice


print("==========================================")
print("       AI PHOTOGRAPHY ASSISTANT")
print("==========================================")


# ------------------------------------------
# STEP 1: Load Photography Knowledge
# ------------------------------------------

print("\nLoading photography knowledge...")

documents = load_knowledge()

model, embeddings = create_embeddings(documents)

index = create_vector_database(embeddings)

print("✓ Knowledge base loaded")


# ------------------------------------------
# STEP 2: Get Image
# ------------------------------------------

image_path = input(
    "\nEnter the path of your photo: "
)


try:

    # --------------------------------------
    # STEP 3: Analyze Image
    # --------------------------------------

    print("\nAnalyzing image...")

    result = analyze_image(image_path)

    print("\n----------- IMAGE ANALYSIS -----------")

    print(
        "Image Size:",
        result["width"],
        "x",
        result["height"]
    )

    print(
        "Brightness:",
        result["brightness"],
        f"({result['brightness_value']})"
    )

    print(
        "Contrast:",
        result["contrast"],
        f"({result['contrast_value']})"
    )

    print(
        "Composition:",
        result["composition"]
    )


    # --------------------------------------
    # STEP 4: Basic Suggestions
    # --------------------------------------

    suggestions = generate_suggestions(result)

    print("\n----------- BASIC SUGGESTIONS -----------")

    for number, suggestion in enumerate(
        suggestions,
        start=1
    ):

        print(
            f"{number}. {suggestion}"
        )


    # --------------------------------------
    # STEP 5: RAG Retrieval
    # --------------------------------------

    print("\nSearching photography knowledge...")

    query = f"""
    Give photography advice for an image with:

    Brightness: {result['brightness']}
    Contrast: {result['contrast']}
    Composition: {result['composition']}
    """

    relevant_tips = search_knowledge(
        query,
        documents,
        model,
        index
    )

    print("\n----------- RETRIEVED KNOWLEDGE -----------")

    for number, tip in enumerate(
        relevant_tips,
        start=1
    ):

        print(f"\n{number}.")
        print(tip)


    # --------------------------------------
    # STEP 6: LLM Generation
    # --------------------------------------

    print("\nGenerating AI advice...")

    ai_advice = generate_ai_advice(
        result,
        relevant_tips
    )


    # --------------------------------------
    # STEP 7: Final Output
    # --------------------------------------

    print("\n==========================================")
    print("          📸 AI PHOTO ADVICE")
    print("==========================================")

    print(ai_advice)

    print("\n==========================================")
    print("Analysis completed!")
    print("==========================================")


except FileNotFoundError:

    print("\n❌ Error: Image file not found.")


except Exception as e:

    print("\n❌ Something went wrong:")
    print(e)