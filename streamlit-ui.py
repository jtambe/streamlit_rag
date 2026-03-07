import importlib.util
import os

import streamlit as st


def _load_similarity_module():
	module_path = os.path.join(os.path.dirname(__file__), "similarity-search.py")
	spec = importlib.util.spec_from_file_location("similarity_search_module", module_path)
	if spec is None or spec.loader is None:
		raise ImportError("Unable to load similarity-search.py")

	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


similarity_module = _load_similarity_module()


def run_app():
	st.set_page_config(page_title="Thoughtful AI Support Agent", layout="centered")
	st.title("🤖 Thoughtful AI Support Agent")
	st.markdown("Ask me anything about Thoughtful AI's automation agents!")

	if "messages" not in st.session_state:
		st.session_state.messages = []

	for msg in st.session_state.messages:
		with st.chat_message(msg["role"]):
			st.markdown(msg["content"])

	user_input = st.chat_input("Type your question here...")

	if user_input:
		st.session_state.messages.append({"role": "user", "content": user_input})
		with st.chat_message("user"):
			st.markdown(user_input)

		response = similarity_module.get_response(user_input)
		st.session_state.messages.append({"role": "assistant", "content": response})
		with st.chat_message("assistant"):
			st.markdown(response)


if __name__ == "__main__":
	run_app()
