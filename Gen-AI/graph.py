from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

# ---------------- EMBEDDINGS ----------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------- VECTOR DATABASE ----------------

vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vectordb.as_retriever(
    search_kwargs={"k": 1}
)

# ---------------- LLM ----------------

llm = ChatOllama(
    model="phi3",
    temperature=0,
    num_predict=200
)

# ---------------- GRAPH STATE ----------------

class GraphState(TypedDict):
    question: str
    context: str
    answer: str
    confidence: float
    escalation: bool

# ---------------- RETRIEVE NODE ----------------

def retrieve_node(state: GraphState):

    try:

        docs = retriever.invoke(state["question"])

        if not docs:

            return {
                "context": "",
                "confidence": 0.2
            }

        context = "\n".join(
            [doc.page_content for doc in docs]
        )

        return {
            "context": context,
            "confidence": 0.9
        }

    except Exception as e:

        return {
            "context": "",
            "confidence": 0.1
        }

# ---------------- GENERATE NODE ----------------

def generate_node(state: GraphState):

    prompt = f"""
You are a professional customer support assistant.

Answer ONLY from the given context.

If the answer is not available in the context say:
'I could not find the answer in the provided documents.'

Context:
{state['context']}

Question:
{state['question']}
"""

    try:

        response = llm.invoke(prompt)

        return {
            "answer": response.content.strip(),
            "escalation": False
        }

    except Exception as e:

        return {
            "answer": f"LLM Error: {str(e)}",
            "escalation": True
        }

# ---------------- HITL ESCALATION NODE ----------------

def escalation_node(state: GraphState):

    return {
        "answer": (
            "This query requires human assistance. "
            "Your request has been escalated to a support agent."
        ),
        "escalation": True
    }

# ---------------- ROUTING LOGIC ----------------

def route_query(state: GraphState):

    question = state["question"].lower()

    # low confidence check
    if state["confidence"] < 0.4:
        return "escalate"

    # sensitive query detection
    sensitive_keywords = [
        "legal",
        "court",
        "lawsuit",
        "complaint",
        "hack",
        "security breach",
        "cancel account",
        "refund issue"
    ]

    for word in sensitive_keywords:

        if word in question:
            return "escalate"

    return "generate"

# ---------------- BUILD LANGGRAPH ----------------

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)
workflow.add_node("escalate", escalation_node)

workflow.add_edge(START, "retrieve")

workflow.add_conditional_edges(
    "retrieve",
    route_query,
    {
        "generate": "generate",
        "escalate": "escalate"
    }
)

workflow.add_edge("generate", END)
workflow.add_edge("escalate", END)

# ---------------- COMPILE APPLICATION ----------------

app = workflow.compile()