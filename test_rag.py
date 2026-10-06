from rag import (
    load_knowledge,
    create_embeddings,
    create_vector_database,
    search_knowledge
)


print("Loading photography knowledge...")

documents = load_knowledge()

print("Knowledge sections:", len(documents))


model, embeddings = create_embeddings(
    documents
)


index = create_vector_database(
    embeddings
)


query = input(
    "\nWhat photography advice do you need? "
)


results = search_knowledge(
    query,
    documents,
    model,
    index
)


print("\n----------- RELEVANT TIPS -----------")

for number, result in enumerate(
    results,
    start=1
):

    print(f"\n{number}.")
    print(result)

print("--------------------------------------")