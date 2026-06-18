---
description: "Task list for Streamlit UI Dashboard implementation"
---

# Tasks: Streamlit UI Dashboard

**Input**: Design documents from `specs/003-streamlit-ui/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure cho Streamlit UI

- [x] T001 Create `src/ui/` and `tests/ui/` directories with `__init__.py` files
- [x] T002 Add `streamlit`, `plotly`, `pandas` to project dependencies (cập nhật requirements/pyproject.toml)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create `src/ui/app.py` with basic `st.set_page_config`, Sidebar config (chọn dataset) và tab layout (Run Benchmark & Report)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Upload Dataset and Configure Run (Priority: P1) 🎯 MVP

**Goal**: Người dùng có thể chạy benchmark trực tiếp từ giao diện với realtime progress bar.

**Independent Test**: Giao diện tab "Run Benchmark" gọi script python nền thành công và cập nhật `%`.

### Implementation for User Story 1

- [x] T004 [US1] Create `src/ui/components/benchmark_runner.py` to handle the Run Benchmark tab UI
- [x] T005 [US1] Refactor/import core logic từ `src/reflexion_lab/agents.py` (hoặc `run_benchmark.py`) vào Streamlit, tích hợp `st.progress` state
- [x] T006 [US1] Integrate `benchmark_runner` function vào tab tương ứng trong `src/ui/app.py`

**Checkpoint**: User Story 1 hoàn chỉnh, người dùng có thể Start Benchmark từ web UI.

---

## Phase 4: User Story 2 - Visualize Benchmark Report (Priority: P1)

**Goal**: Hiển thị báo cáo trực quan với biểu đồ Plotly và phân tích lỗi.

**Independent Test**: Dashboard đọc được file `report.json` và render chính xác biểu đồ cột cùng accordion lỗi.

### Tests for User Story 2 ⚠️

- [x] T007 [P] [US2] Implement unit test cho parser dữ liệu report trong `tests/ui/test_report_parser.py`

### Implementation for User Story 2

- [x] T008 [P] [US2] Implement data entities (`ReportMetrics`, `FailureDetail`) và logic đọc file JSON trong `src/ui/utils/report_parser.py`
- [x] T009 [US2] Create `src/ui/components/report_viewer.py` to render Plotly charts (Exact Match, Avg Attempts)
- [x] T010 [US2] Bổ sung hiển thị thẻ mở rộng (`st.expander`) cho các câu trả lời sai vào `src/ui/components/report_viewer.py`
- [x] T011 [US2] Integrate `report_viewer` function vào tab Report trong `src/ui/app.py`

**Checkpoint**: Cả hai tính năng cốt lõi (Run Benchmark & Report Visualization) đã hoạt động.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T012 Chạy kiểm thử End-to-End theo các kịch bản trong `specs/003-streamlit-ui/quickstart.md`
- [x] T013 Tối ưu UX/UI (thêm style, xử lý catch Exception hiển thị bằng `st.error`)
- [x] T014 Cập nhật lại README chính của repo để hướng dẫn lệnh chạy `streamlit run src/ui/app.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately
- **Foundational (Phase 2)**: Depends on Setup
- **User Stories (Phase 3 & 4)**: Depend on Foundational. Vì cả hai đều là P1, có thể làm US1 trước để MVP chạy được, sau đó đến US2.
- **Polish (Phase 5)**: Depends on US1 and US2.

### Parallel Opportunities

- Unit test (T007) và Data parsing logic (T008) có thể được thực thi song song.
- UI Component cho Report (T009) có thể code song song với logic Parsing (sau khi chốt format Output của data model).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Hoàn thành Phase 1 & 2 (khung ứng dụng).
2. Xây dựng xong Phase 3 (US1) để user có thể click nút Start và thấy thanh process chạy thật thay cho terminal.
3. Stop và Test độc lập.

### Incremental Delivery
1. Foundation ready.
2. Thêm US1 -> UI chạy benchmark được.
3. Thêm US2 -> UI hiển thị được báo cáo.
4. Final Review (Phase 5).
