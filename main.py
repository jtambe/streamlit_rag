import importlib.util
import os


def _load_streamlit_ui_module():
    module_path = os.path.join(os.path.dirname(__file__), "streamlit-ui.py")
    spec = importlib.util.spec_from_file_location("streamlit_ui_module", module_path)
    if spec is None or spec.loader is None:
        raise ImportError("Unable to load streamlit-ui.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


streamlit_ui_module = _load_streamlit_ui_module()
streamlit_ui_module.run_app()