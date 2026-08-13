import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"


st.set_page_config(
    page_title="Oracle EBS Assistant",
    page_icon="🤖",
    layout="centered",
)


def format_response(data: object) -> str:
    """Convert backend tool results into natural language."""

    if isinstance(data, dict):
        po_number = data.get("po_number")
        status = data.get("status")
        supplier = data.get("supplier")
        amount = data.get("amount")

        if po_number:
            parts = [f"Purchase order {po_number}"]

            if status:
                parts.append(f"is {str(status).lower()}")

            if supplier:
                parts.append(f"It was supplied by {supplier}")

            if amount is not None:
                parts.append(f"with a total amount of {amount:,}")

            return ". ".join(parts) + "."

        return ", ".join(
            f"{key.replace('_', ' ').title()}: {value}" for key, value in data.items()
        )

    if isinstance(data, list):
        if not data:
            return "No results were found."

        lines = []

        for item in data:
            if isinstance(item, dict):
                lines.append(
                    ", ".join(
                        f"{key.replace('_', ' ').title()}: {value}"
                        for key, value in item.items()
                    )
                )
            else:
                lines.append(str(item))

        return "\n\n".join(lines)

    return str(data)


st.title("🤖 Oracle EBS Assistant")
st.caption("POC — Oracle EBS Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


prompt = st.chat_input("Ask about a purchase order...")


if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = requests.post(
                API_URL,
                json={"message": prompt},
                timeout=120,
            )

            response.raise_for_status()

            result = response.json()

            if result["success"]:
                answer = format_response(result["data"])
                st.write(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )
            else:
                error = result["error"] or "Request failed."
                st.error(error)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": f"Error: {error}",
                    }
                )

        except requests.RequestException as exc:
            error = f"Backend unavailable: {exc}"
            st.error(error)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error,
                }
            )
