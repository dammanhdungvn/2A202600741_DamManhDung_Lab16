import os
import streamlit as st
import plotly.graph_objects as go
from src.ui.utils.report_parser import parse_report, ReportMetrics

def render_report_viewer():
    if "latest_report" in st.session_state and os.path.exists(st.session_state["latest_report"]):
        report_path = st.session_state["latest_report"]
    else:
        # Default report if available
        if os.path.exists("outputs/sample_run/report.json"):
            report_path = "outputs/sample_run/report.json"
        elif os.path.exists("outputs/streamlit_run/report.json"):
            report_path = "outputs/streamlit_run/report.json"
        else:
            st.warning("Chưa có báo cáo nào. Vui lòng chạy Benchmark trước.")
            return

    st.write(f"Đang hiển thị báo cáo từ: `{report_path}`")
    
    try:
        metrics = parse_report(report_path)
    except Exception as e:
        st.error(f"Lỗi đọc file báo cáo: {e}")
        return
        
    # Render Charts
    st.subheader("1. Metric So sánh (ReAct vs Reflexion)")
    
    col1, col2 = st.columns(2)
    
    # Exact Match Chart
    with col1:
        fig_em = go.Figure(data=[
            go.Bar(name='ReAct', x=['Exact Match'], y=[metrics.react_em], marker_color='#1f77b4'),
            go.Bar(name='Reflexion', x=['Exact Match'], y=[metrics.reflexion_em], marker_color='#ff7f0e')
        ])
        fig_em.update_layout(barmode='group', title="Tỷ lệ Chính xác (Exact Match)", yaxis=dict(range=[0, 1]))
        st.plotly_chart(fig_em, use_container_width=True)
        
    # Avg Attempts Chart
    with col2:
        fig_att = go.Figure(data=[
            go.Bar(name='ReAct', x=['Avg Attempts'], y=[metrics.react_avg_attempts], marker_color='#1f77b4'),
            go.Bar(name='Reflexion', x=['Avg Attempts'], y=[metrics.reflexion_avg_attempts], marker_color='#ff7f0e')
        ])
        fig_att.update_layout(barmode='group', title="Số lần thử trung bình (Avg Attempts)")
        st.plotly_chart(fig_att, use_container_width=True)
        
    # Render Failures
    st.subheader(f"2. Phân tích lỗi ({len(metrics.failure_modes)} câu hỏi)")
    
    if not metrics.failure_modes:
        st.success("Không có câu trả lời sai nào!")
    else:
        for failure in metrics.failure_modes:
            with st.expander(f"❌ QID: {failure.question_id} ({failure.agent_type})"):
                st.markdown(f"**Agent Type:** {failure.agent_type}")
                st.markdown(f"**Đáp án đúng:** `{failure.gold_answer}`")
                st.markdown(f"**Đáp án Agent:** `{failure.predicted_answer}`")
                st.markdown(f"**Số lần thử:** {failure.attempts}")
                st.markdown(f"**Loại lỗi (Failure Mode):** {failure.failure_mode}")
                st.markdown(f"**Số lần Reflexion:** {failure.reflection_count}")
