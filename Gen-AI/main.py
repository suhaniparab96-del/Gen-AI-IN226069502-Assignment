from graph import app

# ---------------- CHAT FUNCTION ----------------

def chat():

    print("\n======================================")
    print("   RAG CUSTOMER SUPPORT CHATBOT")
    print("======================================\n")

    print("Type 'exit' to quit.\n")

    while True:

        try:

            question = input("User: ").strip()

            # empty input check
            if not question:

                print("\nPlease enter a valid question.\n")
                continue

            # exit condition
            if question.lower() == "exit":

                print("\nGoodbye!\n")
                break

            # invoke langgraph app
            result = app.invoke({

                "question": question,
                "context": "",
                "answer": "",
                "confidence": 0.0,
                "escalation": False

            })

            print("\nAssistant:")
            print(result["answer"])

            print(f"\nEscalation: {result['escalation']}")

            print("-" * 50)

        except KeyboardInterrupt:

            print("\n\nChatbot stopped by user.\n")
            break

        except Exception as e:

            print(f"\nError: {e}\n")

# ---------------- MAIN ----------------

if __name__ == "__main__":

    chat()