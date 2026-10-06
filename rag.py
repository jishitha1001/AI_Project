from sentence_transformers import SentenceTransformer
import faiss


def load_knowledge():

    with open(
        "knowledge/photography_tips.txt",
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    # Separate the knowledge into sections
    documents = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    return documents


def create_embeddings(documents):

    print("Loading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    embeddings = model.encode(documents)

    return model, embeddings


def create_vector_database(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_knowledge(query, documents, model, index):

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        query_embedding,
        k=2
    )

    results = []

    for index_number in indices[0]:

        results.append(
            documents[index_number]
        )

    return results