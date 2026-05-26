from fpdf import FPDF

def create_pdf(filename, title, content_lines):
    pdf = FPDF()
    pdf.add_page()
    
    # Title formatting
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    
    # Content formatting
    pdf.set_font("Arial", size=12)
    for line in content_lines:
        if line.startswith("**") or line.startswith("##"):
            pdf.set_font("Arial", 'B', 12)
            clean_line = line.replace("**", "").replace("##", "")
            pdf.multi_cell(0, 10, txt=clean_line)
            pdf.set_font("Arial", size=12)
        else:
            clean_line = line.replace("* ", "- ")
            pdf.multi_cell(0, 8, txt=clean_line)
            
    pdf.output(filename)
    print(f"Successfully created: {filename}")

# --- Content for HLD Document ---
hld_content = [
    "## System Overview",
    "* The project is a Retrieval-Augmented Generation (RAG) Customer Support Chatbot built using LangGraph.",
    "* It processes PDF documents to create a knowledge base and uses a state graph to route user queries to an LLM or escalate them to a human agent based on confidence scores and sensitive keywords.",
    "",
    "## Core Architecture Components",
    "* Document Ingestion Pipeline: Extracts text from PDF files located in a local directory, splits the text into manageable chunks, and stores them in a vector database.",
    "* Vector Database: Utilizes ChromaDB for persistent storage of document embeddings, enabling semantic search.",
    "* Embedding Model: Employs HuggingFace's local embedding model to convert text chunks and user queries into vector representations.",
    "* Language Model (LLM): Uses Ollama with the 'phi3' model to generate responses based on the retrieved context.",
    "* Workflow Orchestrator: Implements LangGraph to define a state machine with nodes for retrieval, generation, and human-in-the-loop (HITL) escalation.",
    "",
    "## Data Flow",
    "* Ingestion Phase: PDFs -> PyPDFLoader -> RecursiveCharacterTextSplitter -> HuggingFace Embeddings -> ChromaDB.",
    "* Query Phase: User Input -> Workflow Start -> Retrieval Node -> Routing Logic -> Generate Node OR Escalate Node -> Final Output."
]

# --- Content for LLD Document ---
lld_content = [
    "## State Management (GraphState)",
    "* The application state is maintained using a TypedDict containing the following keys: question (string), context (string), answer (string), confidence (float), and escalation (boolean).",
    "",
    "## Node Specifications (graph.py)",
    "* retrieve_node: Invokes the ChromaDB retriever to fetch the top 1 document (k=1). Sets confidence to 0.9 if a document is found, or 0.2/0.1 upon failure or empty results.",
    "* generate_node: Constructs a strict prompt commanding the LLM to answer only from the provided context. Updates the state with the LLM's response and sets escalation to False.",
    "* escalation_node: Generates a hardcoded response stating the query requires human assistance and flags escalation as True in the state.",
    "",
    "## Routing Logic (route_query)",
    "* Evaluates the confidence score from the retrieval node; returns 'escalate' if the score is below 0.4.",
    "* Scans the lowercase user question against a list of sensitive keywords (e.g., 'legal', 'lawsuit', 'security breach', 'refund issue').",
    "* Returns 'escalate' if any sensitive keyword is detected; otherwise, returns 'generate'.",
    "",
    "## Database and Embeddings Configuration",
    "* Model: Uses 'sentence-transformers/all-MiniLM-L6-v2' via HuggingFaceEmbeddings.",
    "* Storage: ChromaDB persists data to a local 'chroma_db' directory.",
    "",
    "## Ingestion Logic (ingest.py)",
    "* Validates the existence of a 'data' folder and loads all '.pdf' files.",
    "* Uses RecursiveCharacterTextSplitter configured with a chunk size of 300 and a chunk overlap of 30."
]

# --- Content for Technical Documentation ---
tech_content = [
    "## Prerequisites & Dependencies",
    "* Python environment with the packages listed in requirements.txt installed.",
    "* Ollama installed locally and configured to run the 'phi3' model.",
    "* Required libraries include: langchain, langgraph, chromadb, pypdf, sentence-transformers, and python-dotenv.",
    "",
    "## Environment Configuration",
    "* Create a .env file in the root directory.",
    "* Add required API keys, such as GOOGLE_API_KEY=your_google_api_key, to the .env file (though the system primarily relies on local HuggingFace/Ollama models).",
    "",
    "## Execution Sequence",
    "* Step 1: Place all relevant source PDFs into a folder named 'data' in the root directory. Run the data generation script if applicable to your setup.",
    "* Step 2: Execute 'python ingest.py' to parse the PDFs, chunk the text, compute embeddings, and populate the local 'chroma_db' vector store.",
    "* Step 3: Execute 'python main.py' to launch the interactive RAG Customer Support Chatbot in the terminal.",
    "",
    "## Usage Instructions",
    "* Upon running 'main.py', the terminal will display an interactive prompt (User:).",
    "* Type queries to test the RAG generation and routing logic.",
    "* Test escalation by typing queries containing keywords like 'legal' or 'hack'.",
    "* Type 'exit' to terminate the application safely."
]

# Generate the files
if __name__ == "__main__":
    create_pdf("HLD_Document.pdf", "High-Level Design (HLD) Document", hld_content)
    create_pdf("LLD_Document.pdf", "Low-Level Design (LLD) Document", lld_content)
    create_pdf("Technical_Documentation.pdf", "Technical Documentation", tech_content)