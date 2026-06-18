# Feature Specification: Lab 16 Reflexion Agent

**Feature Branch**: `002-lab-reflexion-agent`

**Created**: 2026-06-18

**Status**: Draft

**Input**: User description: "Doc file README.md va cac file lien quan trong README  de hieu yeu cau Lab."

## Clarifications

### Session 2026-06-18
- Q: Lựa chọn nền tảng LLM nào làm mặc định để tích hợp? → A: Custom: Tôi dùng model qwen. Cụ thể các api-key được lưu về @.env và cách call model của api-key nằm ở @docs/qwen-api.md

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Replace Mock Runtime with Actual LLM (Priority: P1)
Hệ thống cần sử dụng LLM thật (như OpenAI, Gemini, Claude, vLLM) thay vì mock cố định để đánh giá khả năng suy luận, reflection của LLM.
**Why this priority**: Yêu cầu cốt lõi của bài lab là đánh giá agent thực tế.
**Independent Test**: Có thể chạy `python run_benchmark.py` và quan sát thấy LLM trả về các đáp án khác nhau dựa trên prompt.
**Acceptance Scenarios**:
1. **Given** một câu hỏi trong dataset, **When** Agent gọi `actor_answer`, **Then** kết quả được sinh ra từ LLM thật thay vì mock.
2. **Given** một câu trả lời cần đánh giá, **When** Agent gọi `evaluator`, **Then** LLM trả về `JudgeResult` theo schema.

### User Story 2 - Implement Reflexion Loop (Priority: P1)
Agent cần khả năng tự phản chiếu (self-reflection) để rút kinh nghiệm từ các lần trả lời sai trước đó.
**Why this priority**: Đây là cơ chế Reflexion bắt buộc của lab.
**Independent Test**: Kiểm tra xem `reflection_memory` có được cập nhật khi câu trả lời sai hay không.
**Acceptance Scenarios**:
1. **Given** một câu trả lời sai, **When** agent thực hiện vòng lặp Reflexion, **Then** `reflector()` được gọi và sinh ra `ReflectionEntry`.
2. **Given** một `ReflectionEntry` mới, **When** chuẩn bị prompt cho lần thử kế tiếp, **Then** bộ nhớ reflection được đưa vào prompt.

### User Story 3 - Create Evaluation Dataset (Priority: P1)
Cần có một bộ dataset gồm ít nhất 100 câu hỏi QA dạng multi-hop để đánh giá agent.
**Why this priority**: Autograder yêu cầu tối thiểu 100 records để đạt điểm tối đa cho phần Experiment.
**Independent Test**: Có thể chạy `python run_benchmark.py --dataset data/my_test_set.json` trên tập 100 câu hỏi thành công.
**Acceptance Scenarios**:
1. **Given** hệ thống đã hoàn thiện, **When** chạy benchmark, **Then** hệ thống xử lý thành công >=100 câu hỏi.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Hệ thống MUST triển khai hoàn chỉnh `JudgeResult` và `ReflectionEntry` trong `schemas.py`.
- **FR-002**: Hệ thống MUST hoàn thành logic Reflexion trong `agents.py` (dòng 31-35).
- **FR-003**: Hệ thống MUST cung cấp các System Prompts (Actor, Evaluator, Reflector) đầy đủ trong `prompts.py`.
- **FR-004**: Hàm `actor_answer()`, `evaluator()`, và `reflector()` trong `mock_runtime.py` MUST gọi đến một LLM thực tế thay vì trả về mock cố định.
- **FR-005**: Hệ thống MUST tính toán `token_estimate` và `latency_ms` thực tế từ API response.
- **FR-006**: Phải có tối thiểu 1 dataset kiểm thử chứa >=100 câu hỏi định dạng `QAExample`.

### Key Entities
- **QAExample**: Dữ liệu câu hỏi, chứa câu hỏi, gold answer và context.
- **JudgeResult**: Kết quả đánh giá của Evaluator (is_correct, feedback).
- **ReflectionEntry**: Phân tích lỗi và chiến thuật mới cho lần thử sau.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: `autograde.py` chấm điểm Core Flow đạt tối đa 80/80 điểm.
- **SC-002**: Benchmark report có `num_records >= 100`.
- **SC-003**: Report thỏa mãn: ≥20 examples chi tiết, ≥3 failure modes được phân tích, discussion ≥250 ký tự.

## Assumptions
- Sử dụng API Qwen LLM. API keys được cấu hình trong `.env`. Hướng dẫn gọi API tham khảo từ `docs/qwen-api.md`.
- Nguồn dataset HotpotQA hoặc tương đương sẽ được lấy để tạo 100 câu hỏi.
