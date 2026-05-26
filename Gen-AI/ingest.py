import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils import get_vector_db

# ---------------- LOAD ENV ----------------

load_dotenv()

# ---------------- INGESTION FUNCTION ----------------

def run_ingestion():

    docs = []

    # check data folder exists
    if not os.path.exists("data"):

        print("ERROR: 'data' folder not found.")
        return

    # load all pdf files
    for file in os.listdir("data"):

        if file.endswith(".pdf"):

            try:

                print(f"Loading PDF: {file}")

                loader = PyPDFLoader(
                    os.path.join("data", file)
                )

                loaded_docs = loader.load()

                docs.extend(loaded_docs)

            except Exception as e:

                print(f"Error loading {file}: {e}")

    # no documents found
    if not docs:

        print("No PDF documents found.")
        return

    print(f"\nTotal Pages Loaded: {len(docs)}")

    # ---------------- CHUNKING ----------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30
    )

    chunks = splitter.split_documents(docs)

    print(f"Total Chunks Created: {len(chunks)}")

    # ---------------- VECTOR DATABASE ----------------

    try:

        db = get_vector_db()

        db.add_documents(chunks)

        print("\nDatabase Successfully Loaded")

    except Exception as e:

        print(f"\nDatabase Error: {e}")

# ---------------- MAIN ----------------

if __name__ == "__main__":

    run_ingestion()