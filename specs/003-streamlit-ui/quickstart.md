# Quickstart: Validation Guide for Streamlit UI

Tài liệu này hướng dẫn các bước kiểm chứng tính năng Giao diện Streamlit Dashboard hoạt động đúng như đặc tả sau khi đã được lập trình xong (Phase 2).

## Prerequisites
- Môi trường `uv` đã được kích hoạt: `source .venv/bin/activate`
- Chắc chắn rằng đã cài đặt các dependency cần thiết:
  ```bash
  uv pip install streamlit plotly pandas
  ```
- File `data/evaluation_100.json` (hoặc `hotpot_mini.json`) đã tồn tại trong thư mục dự án.

## Validation Scenarios

### Scenario 1: Khởi động Dashboard và Kiểm tra Giao diện (Smoke Test)
**Mục tiêu**: Đảm bảo ứng dụng load lên được, chia đúng tab và không lỗi.

1. **Khởi động server**:
   ```bash
   streamlit run src/ui/app.py
   ```
2. **Hành động mong đợi**: 
   - Browser tự động mở địa chỉ `http://localhost:8501`.
   - Có Sidebar bên trái với tùy chọn "Select Dataset".
   - Có khu vực chính chứa 2 tabs: "Run Benchmark" và "Report".

### Scenario 2: Chạy Benchmark và Progress Bar
**Mục tiêu**: Xác thực tiến trình chạy không làm treo UI (SC-003).

1. Ở Sidebar, chọn dataset `data/hotpot_mini.json` (tập nhỏ để chạy nhanh).
2. Tại tab "Run Benchmark", bấm nút **Start Benchmark**.
3. **Hành động mong đợi**:
   - Nút Start bị disable (mờ đi).
   - Thanh `st.progress` xuất hiện, báo % thay đổi liên tục (Ví dụ: "Đang xử lý 1/8...").
   - Giao diện không bị treo trắng xóa.
   - Khi chạy xong hiện thông báo "Hoàn thành!" và nút Start hiện lại.

### Scenario 3: Trực quan hóa Biểu đồ và Failure Modes
**Mục tiêu**: Xác thực UI vẽ đúng biểu đồ Plotly và danh sách các câu sai (FR-003, FR-004).

1. Chuyển sang tab **Report** (sau khi đã chạy benchmark xong, hoặc hệ thống tự read từ file `report.json` mới nhất).
2. **Hành động mong đợi**:
   - Hiển thị 2 biểu đồ cột/tròn tương tác (Exact Match, Avg Attempts) so sánh ReAct và Reflexion.
   - Bên dưới biểu đồ, có danh sách các câu trả lời sai.
   - Mỗi câu hiển thị dạng thẻ `st.expander` (nhấn vào sẽ trỏ xuống nội dung dài gồm: câu hỏi, đáp án đúng, đáp án Agent).
