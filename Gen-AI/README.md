# LangGraph RAG System
    
    ## Setup Instructions
    1. Install dependencies: `pip install -r requirements.txt`
    2. Add your Gemini API key to `.env`
    
    ## Execution Order
    1. Run `python create_pdfs.py` to generate the knowledge base.
    2. Run `python ingest.py` to embed documents into ChromaDB.
    3. Run `python main.py` to launch the chatbot.