import streamlit as st
from pathlib import Path
from src.reflexion_lab.agents import ReActAgent, ReflexionAgent
from src.reflexion_lab.reporting import build_report, save_report
from src.reflexion_lab.utils import load_dataset, save_jsonl

def render_benchmark_runner(selected_dataset: str):
    st.write("Cấu hình phiên chạy:")
    
    col1, col2 = st.columns(2)
    with col1:
        out_dir = st.text_input("Output Directory", value="outputs/streamlit_run")
    with col2:
        max_attempts = st.number_input("Reflexion Max Attempts", min_value=1, max_value=5, value=3)
        
    if st.button("Start Benchmark", type="primary"):
        run_benchmark_ui(selected_dataset, out_dir, max_attempts)

def run_benchmark_ui(dataset_path: str, out_dir: str, reflexion_attempts: int):
    st.info(f"Đang tải dataset: `{dataset_path}`...")
    try:
        examples = load_dataset(dataset_path)
    except Exception as e:
        st.error(f"Lỗi khi load dataset: {e}")
        return
        
    total = len(examples)
    if total == 0:
        st.warning("Dataset rỗng.")
        return
        
    st.write(f"Tìm thấy **{total}** câu hỏi. Bắt đầu đánh giá...")
    react = ReActAgent()
    reflexion = ReflexionAgent(max_attempts=reflexion_attempts)
    
    react_records = []
    reflexion_records = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, example in enumerate(examples):
        status_text.text(f"Đang xử lý câu hỏi {i+1}/{total}... (ID: {example.id})")
        
        # Chạy ReAct
        react_record = react.run(example)
        react_records.append(react_record)
        
        # Chạy Reflexion
        reflexion_record = reflexion.run(example)
        reflexion_records.append(reflexion_record)
        
        # Cập nhật progress
        progress = (i + 1) / total
        progress_bar.progress(progress)
        
    status_text.text("Hoàn thành quá trình đánh giá. Đang lưu báo cáo...")
    
    # Save reports
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    all_records = react_records + reflexion_records
    save_jsonl(out_path / "react_runs.jsonl", react_records)
    save_jsonl(out_path / "reflexion_runs.jsonl", reflexion_records)
    
    # mode="mock" or "api". We just use "api" but the mock_runtime handles fallback so it's fine.
    report = build_report(all_records, dataset_name=Path(dataset_path).name, mode="api")
    json_path, md_path = save_report(report, out_path)
    
    st.success(f"🎉 Benchmark hoàn tất! Đã lưu báo cáo tại: `{json_path}`")
    st.session_state["latest_report"] = str(json_path)
