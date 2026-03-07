python3 -m venv myenv
source venv/bin/activate
pip install streamlit
pip install chromadb ollama
pip freeze > requirements.txt

pip install requirements.txt

streamlit run main.py