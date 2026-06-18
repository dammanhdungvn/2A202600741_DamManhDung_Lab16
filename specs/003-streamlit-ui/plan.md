# Implementation Plan: Streamlit UI Dashboard

**Branch**: `003-streamlit-ui` | **Date**: 2026-06-18 | **Spec**: [spec.md](file:///home/dammanhdungvn/workspace/ai-in-action/day15/phase1-track3-lab1-advanced-agent/specs/003-streamlit-ui/spec.md)

**Input**: Feature specification from `specs/003-streamlit-ui/spec.md`

## Summary

Xây dựng một giao diện web bằng Streamlit cho phép người dùng chạy quá trình đánh giá (Benchmark) và trực quan hóa kết quả (Report) của dự án Reflexion Agent hiện tại. Dự án sẽ dùng Streamlit để đóng vai trò như tầng Controller/View, gọi các logic đã có sẵn hoặc chạy file python như một tiến trình con.

## Technical Context

**Language/Version**: Python (cùng version hiện tại của lab, quản lý bằng `uv`)

**Primary Dependencies**: Streamlit, pandas, plotly (để vẽ biểu đồ tương tác)

**Storage**: File hệ thống (`data/evaluation_100.json`, `outputs/*/report.json`)

**Testing**: Pytest (Streamlit `AppTest` framework cho UI)

**Target Platform**: Trình duyệt web (Local Streamlit server)

**Project Type**: Data Dashboard / Web UI

**Performance Goals**: UI không bị đơ (freeze) khi hệ thống call LLM nền; parse file `report.json` và vẽ biểu đồ mượt mà.

**Constraints**: Bắt buộc phải kết nối được với mã nguồn hiện tại của Lab 16 mà không phá vỡ Clean Architecture.

**Scale/Scope**: 1 trang Dashboard với Sidebar cấu hình, 1 tab chạy Benchmark, 1 tab hiển thị Kết quả & Biểu đồ.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Production Quality & Clean Code**: Áp dụng cho Streamlit code (tách components, không nhồi nhét tất cả vào app.py).
- [x] **II. Clean Architecture**: Streamlit đóng vai trò là tầng *Controller/UI*. Logic chạy benchmark thuộc về *Use Case* hiện có, Streamlit sẽ gọi thông qua interface hoặc subprocess.
- [N/A] **III. Database Transactions**: Không áp dụng vì chỉ thao tác đọc/ghi file JSON.
- [x] **IV. Centralized Error Handling**: Bắt lỗi khi parse JSON hoặc chạy timeout, hiển thị `st.error()` thay vì crash ứng dụng.
- [x] **V. Test Coverage**: Đảm bảo logic parse report có unit test.

## Project Structure

### Documentation (this feature)

```text
specs/003-streamlit-ui/
├── plan.md              
├── research.md          
├── data-model.md        
├── quickstart.md        
├── contracts/           
└── tasks.md             
```

### Source Code (repository root)

```text
src/
├── reflexion_lab/       # Mã nguồn hiện tại của lab
│   └── ...
├── ui/                  # Thư mục mới cho Streamlit app
│   ├── app.py           # Entry point
│   ├── components/      # Các UI component (benchmark_runner.py, report_viewer.py)
│   └── utils/           # Các hàm hỗ trợ parse report
tests/
└── ui/                  # Test cho thư mục UI
```

**Structure Decision**: Tách riêng thư mục `ui/` trong `src/` để đảm bảo Clean Architecture, phân tách rõ ràng với tầng core `reflexion_lab`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Không | | |
