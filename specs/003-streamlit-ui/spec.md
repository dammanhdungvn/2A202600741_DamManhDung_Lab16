# Feature Specification: Streamlit UI Dashboard

**Feature Branch**: `003-streamlit-ui`

**Created**: 2026-06-18

**Status**: Draft

**Input**: User description: "Toi muon tao them giao dien bang streamlit bao phu het chuc nang cua lab va truc quan hoa report. Y tuong cua toi la vay."

## Clarifications
### Session 2026-06-18
- Q: Cách xử lý UX khi tiến trình Benchmark chạy ngầm kéo dài → A: Hiển thị thanh tiến trình st.progress (%) kèm theo dòng trạng thái.
- Q: Mức độ chi tiết khi hiển thị các câu trả lời sai (Failure Modes) → A: Hiển thị dạng danh sách thẻ mở rộng (st.expander), mỗi thẻ chứa chi tiết của 1 câu sai để tiện đọc nội dung dài.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload Dataset and Configure Run (Priority: P1)
Người dùng muốn có thể cấu hình thông số (loại Agent, file dataset) và chạy benchmark trực tiếp từ giao diện Streamlit thay vì dùng lệnh terminal.
**Why this priority**: Cần điểm khởi đầu để kích hoạt toàn bộ chức năng của lab thông qua UI.
**Independent Test**: Giao diện load lên, người dùng chọn file dataset `evaluation_100.json` và ấn nút "Start Benchmark", hệ thống gọi script python nền thành công.
**Acceptance Scenarios**:
1. **Given** người dùng mở Dashboard, **When** tải lên/chọn dataset và ấn Start, **Then** hệ thống bắt đầu chạy benchmark và hiển thị thanh tiến trình (progress bar).

### User Story 2 - Visualize Benchmark Report (Priority: P1)
Người dùng muốn xem trực quan báo cáo sau khi chạy, bao gồm so sánh giữa ReAct và Reflexion (EM score, số attempts, độ trễ) bằng các biểu đồ.
**Why this priority**: "Trực quan hóa report" là yêu cầu cốt lõi. Giúp đánh giá agent dễ dàng hơn việc đọc file JSON.
**Independent Test**: Dashboard load được file `report.json` có sẵn và render các biểu đồ cột/tròn chính xác.
**Acceptance Scenarios**:
1. **Given** có file `report.json`, **When** người dùng mở tab Report, **Then** hệ thống hiển thị biểu đồ so sánh EM score và số attempts của ReAct và Reflexion.

### Edge Cases
- Chuyện gì xảy ra nếu tiến trình benchmark mất quá nhiều thời gian? Hệ thống sẽ hiển thị thanh tiến trình `st.progress` (%) kèm theo dòng trạng thái (VD: "Đang xử lý câu hỏi X/Y...") để người dùng theo dõi.
- Nếu format file dataset không đúng chuẩn QAExample? (Streamlit sẽ hiện cảnh báo lỗi màu đỏ).

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Hệ thống MUST có giao diện sidebar hoặc form để upload dataset và điền cấu hình API Key/URL (nếu cần đổi).
- **FR-002**: Hệ thống MUST hiển thị realtime logs hoặc progress bar khi benchmark đang chạy.
- **FR-003**: Hệ thống MUST đọc kết quả từ `report.json` và vẽ biểu đồ so sánh giữa ReAct và Reflexion (dùng st.bar_chart hoặc Plotly).
- **FR-004**: Hệ thống MUST hiển thị chi tiết các câu trả lời sai (failure modes) dưới dạng danh sách thẻ mở rộng (`st.expander`) để tối ưu không gian và dễ đọc.

### Key Entities
- **DashboardState**: Trạng thái của phiên Streamlit (ví dụ: đang chờ chạy, đang chạy benchmark, hiển thị kết quả).
- **ReportMetrics**: Dữ liệu EM, latency, attempts được parse để vẽ biểu đồ.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Toàn bộ luồng `run_benchmark` và hiển thị kết quả report có thể được thực thi thành công từ giao diện chỉ với 1 click.
- **SC-002**: UI cung cấp tối thiểu 2 biểu đồ so sánh trực quan cho điểm Exact Match và Average Attempts giữa 2 kỹ thuật Agent.
- **SC-003**: Giao diện không bị treo (freeze) và báo lỗi trong quá trình hệ thống đang chờ API call nền.

## Assumptions
- Sử dụng framework Streamlit mặc định, không cần CSS/JS custom phức tạp.
- Giao diện chạy ở local (người dùng mở qua `streamlit run app.py`).
