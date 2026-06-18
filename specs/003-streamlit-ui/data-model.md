# Data Model: Streamlit UI

## Entities

### `DashboardState`
Lưu trữ trạng thái vòng đời của ứng dụng trong Streamlit (`st.session_state`).

**Fields**:
- `is_running` (bool): Đang trong quá trình chạy benchmark hay không.
- `current_progress` (int): Số lượng câu hỏi đã được xử lý xong.
- `total_questions` (int): Tổng số câu hỏi của dataset được chọn.
- `report_path` (str): Đường dẫn tới file report sau khi chạy xong để tab Report có thể load.

### `ReportMetrics`
Cấu trúc dữ liệu đã được parse từ file `report.json` phục vụ cho việc render bằng Plotly.

**Fields**:
- `react_em` (float): Exact match score của ReAct.
- `reflexion_em` (float): Exact match score của Reflexion.
- `react_avg_attempts` (float): Số lần thử trung bình của ReAct (luôn là 1).
- `reflexion_avg_attempts` (float): Số lần thử trung bình của Reflexion.
- `failure_modes` (List[FailureDetail]): Danh sách các câu sai để hiển thị trong `st.expander`.

### `FailureDetail`
Chi tiết của một câu trả lời sai.

**Fields**:
- `question_id` (str): ID của câu hỏi.
- `question` (str): Nội dung câu hỏi gốc.
- `agent_type` (str): Loại Agent bị lỗi (ReAct hay Reflexion).
- `expected_answer` (str): Đáp án đúng.
- `actual_answer` (str): Đáp án Agent đưa ra.
- `attempts` (int): Số lần đã thử.
- `trajectory` (str): Lịch sử suy luận và công cụ (nếu cần hiển thị).
