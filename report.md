# Báo cáo Lab 16 — Reflexion Agent

## Thông tin học viên
- **Họ và tên**: Dam Manh Dung
- **Mã học viên**: 2A202600741

## Kết quả quá trình Implementation
### 1. Thông tin cấu hình hệ thống
- Môi trường: Quản lý package bằng `uv`.
- Mô hình LLM: Custom API `Qwen` (Call qua OpenAI SDK).
- Dataset: `hotpot_dev_distractor_v1.json` được trích xuất ngẫu nhiên 100 sample chuẩn sang file `data/evaluation_100.json`.

### 2. Kết quả Benchmark & Autograde
- File kết quả Benchmark: `outputs/qwen_run/report.json`
- Số lượng record: 100
- **Điểm Autograde**: **92/100**
- Hệ thống Fallback API khi hết Quota của Qwen hoạt động hoàn hảo, đảm bảo không bị gián đoạn khi thực thi vòng lặp Reflexion.

### 3. Đánh giá tính năng (Reflexion Loop)
Agent Reflexion có khả năng tự nhận dạng đáp án sai qua hàm `evaluator()`, sinh lỗi (failure mode) qua `reflector()` và thực hiện `attempt_count > 1` để đưa ra câu trả lời cuối cùng chính xác nhất.
