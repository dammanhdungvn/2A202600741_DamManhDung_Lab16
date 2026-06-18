# Research & Decisions

## 1. Tích hợp quá trình Benchmark vào Streamlit (UX non-blocking)
**Decision**: Import logic từ `src.reflexion_lab.agents` (hoặc `run_benchmark.py`) và thực thi trực tiếp trên thread của Streamlit, kết hợp với cơ chế truyền callback để cập nhật `st.progress`.

**Rationale**: 
- Streamlit chạy script theo mô hình top-down. Nếu dùng `subprocess` để gọi terminal thì việc parse log thời gian thực sẽ phức tạp và dễ lỗi (phụ thuộc vào stdout buffer).
- Thay vì gọi script `run_benchmark.py`, ta có thể import logic cốt lõi. Giao diện sẽ bị block (người dùng không thể click các nút khác) khi vòng lặp đang chạy, nhưng `st.progress` và `st.write` vẫn sẽ cập nhật trạng thái UI sau mỗi câu hỏi. Đây là behavior an toàn nhất để tránh người dùng nhấn Start nhiều lần.

**Alternatives considered**: 
- Chạy subprocess ngầm và dùng `st_autorefresh`: Quá phức tạp và cần quản lý file trạng thái (state file).
- Dùng `threading`: Streamlit không quản lý tốt background threads, dễ gặp lỗi `Missing ScriptRunContext`.

## 2. Trực quan hóa Biểu đồ
**Decision**: Sử dụng thư viện `plotly.express` tích hợp với lệnh `st.plotly_chart` thay vì `st.bar_chart` mặc định.

**Rationale**: 
- `plotly` cho phép biểu đồ có tính tương tác cao (hover xem chi tiết tooltip, zoom), đặc biệt hữu ích khi xem sự khác biệt nhỏ giữa Exact Match của ReAct và Reflexion. Streamlit hỗ trợ Plotly native rất tốt.

**Alternatives considered**: 
- Dùng `st.bar_chart` (dựa trên Altair): Nhanh, nhẹ nhưng khó custom label và tooltip hiển thị số attempts.

## 3. Quản lý State của Dashboard
**Decision**: Sử dụng `st.session_state` để lưu trữ trạng thái chạy (đang chạy hay đã xong) và lưu trữ trực tiếp cấu hình dataset path.

**Rationale**: Giúp ứng dụng giữ được data khi người dùng chuyển qua lại giữa các tab (Ví dụ: Chuyển từ tab Run sang tab Report).
