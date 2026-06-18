import os
import sys
# Thêm thư mục gốc của project vào sys.path để Python nhận diện được package `src`
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import glob

st.set_page_config(
    page_title="Reflexion Benchmark Dashboard",
    page_icon="🤖",
    layout="wide"
)

def get_available_datasets():
    # Return all json files in data/
    return glob.glob("data/*.json")

def main():
    st.sidebar.title("Configuration")
    
    # Dataset Selection
    available_datasets = get_available_datasets()
    selected_dataset = st.sidebar.selectbox(
        "Select Dataset", 
        available_datasets,
        index=available_datasets.index("data/evaluation_100.json") if "data/evaluation_100.json" in available_datasets else 0
    )
    
    # API Configuration
    st.sidebar.subheader("API Configuration")
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.environ.get("QWEN_API_KEY"):
        st.sidebar.success("✅ Qwen API Key đã được cấu hình bảo mật từ file `.env`")
    else:
        st.sidebar.error("❌ Chưa tìm thấy Qwen API Key trong file `.env`!")
        
    st.title("Reflexion Agent Benchmark")
    
    # Tab Layout
    tab1, tab2 = st.tabs(["▶️ Run Benchmark", "📊 Report Visualization"])
    
    with tab1:
        st.header("Run Benchmark")
        from src.ui.components.benchmark_runner import render_benchmark_runner
        render_benchmark_runner(selected_dataset)
        
    with tab2:
        st.header("Report Visualization")
        from src.ui.components.report_viewer import render_report_viewer
        render_report_viewer()

if __name__ == "__main__":
    main()
