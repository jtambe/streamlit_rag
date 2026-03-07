import json
import os
from difflib import SequenceMatcher


def _get_similarity_threshold(default_value=0.2):
	try:
		return float(os.getenv("SIMILARITY_THRESHOLD", str(default_value)))
	except ValueError:
		return default_value


SIMILARITY_THRESHOLD = _get_similarity_threshold()


def load_qa_data():
	"""Load Q&A data from input_data.json."""
	file_path = os.path.join(os.path.dirname(__file__), "input_data.json")
	with open(file_path, "r", encoding="utf-8") as file:
		data = json.load(file)
	return data.get("questions", [])


QA_DATA = load_qa_data()


def find_similar_question(user_input, threshold=SIMILARITY_THRESHOLD):
	"""Find the most relevant predefined answer using similarity matching."""
	best_match = None
	best_score = 0.0

	for idx, qtn in enumerate(QA_DATA):
		qtn_score = SequenceMatcher(None, user_input.lower(), qtn["question"].lower()).ratio()
		print(f"Comparing '{user_input}' with qtn: {idx} - Similarity Score: {qtn_score}")
		ans_score = SequenceMatcher(None, user_input.lower(), qtn["answer"].lower()).ratio()
		print(f"Comparing '{user_input}' with ans: {idx} - Similarity Score: {ans_score}")
		combined_score = SequenceMatcher(
			None,
			user_input.lower(),
			qtn["question"].lower() + qtn["answer"].lower(),
		).ratio()
		print(f"Comparing '{user_input}' with combined qtn+ans: {idx} - Similarity Score: {combined_score}")

		max_score = max(qtn_score, ans_score, combined_score)
		print(f"max_score: {max_score}")

		if max_score >= best_score:
			best_score = max_score
			best_match = qtn

	return best_match if best_score >= threshold else None


def get_response(user_input):
	"""Get response from predefined data or fallback message."""
	if not user_input.strip():
		return "Please enter a question to get started! 😊"

	match = find_similar_question(user_input)

	if match:
		return match["answer"]

	return (
		"I'm not sure about that. I'm specifically trained to answer questions about "
		"Thoughtful AI's automation agents (EVA, CAM, and PHIL). Feel free to ask me about them!"
	)
