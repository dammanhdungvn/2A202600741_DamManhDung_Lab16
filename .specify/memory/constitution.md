<!--
Sync Impact Report:
- Version change: [INITIAL] -> 1.0.0
- Modified principles: N/A (Initial setup)
- Added sections: Production Quality, Clean Architecture, Database Transactions, RESTful API, Test Coverage.
- Removed sections: Placeholder sections
- Templates requiring updates: ✅ None pending
- Follow-up TODOs: Determine original RATIFICATION_DATE.
-->
# Course Registration System Constitution

## Core Principles

### I. Production Quality & Clean Code
Tất cả mã nguồn phải đạt tiêu chuẩn production. Tuân thủ nghiêm ngặt các nguyên lý Clean Code (đặt tên rõ ràng, hàm nhỏ gọn, dễ đọc, dễ bảo trì). Tuyệt đối không được phép nhồi nhét mã nguồn vào một vài tệp.

### II. Clean Architecture
Phải tuân thủ nghiêm ngặt Clean Architecture. Mã nguồn phải được phân chia thành các thư mục và tầng riêng biệt:
- **Controller**: Chỉ xử lý HTTP request/response và routing.
- **Use Case (Service)**: Chứa toàn bộ logic nghiệp vụ (business logic).
- **Repository**: Xử lý giao tiếp với cơ sở dữ liệu, không rò rỉ chi tiết DB ra ngoài.

### III. Database Transactions
Mọi thao tác ghi dữ liệu (Create, Update, Delete) phải được bọc trong Database Transaction để đảm bảo tính toàn vẹn và nhất quán của dữ liệu.

### IV. RESTful API & Centralized Error Handling
Các API phải tuân thủ nghiêm ngặt chuẩn RESTful (sử dụng đúng các HTTP methods, URI naming, status codes).
Hệ thống phải triển khai cơ chế xử lý lỗi tập trung (Centralized Error Handling) để bắt các exception và trả về phản hồi lỗi thống nhất cho client.

### V. Test Coverage & Testing
Tỷ lệ bao phủ kiểm thử (Test coverage) tối thiểu phải đạt 80%. Tất cả các logic nghiệp vụ (trong Use Case) phải được viết unit test đầy đủ.

## Governance

Constitution này là tài liệu cao nhất định hướng cho việc phát triển dự án. Tất cả các thành viên tham gia dự án PHẢI tuân thủ các quy tắc trên trong quá trình phát triển và Code Review.
- Code Review phải xác minh tính tuân thủ với Clean Architecture.
- Bất kỳ PR nào làm giảm coverage xuống dưới 80% đều sẽ bị từ chối.
- Các sửa đổi đối với Constitution phải được thảo luận, phê duyệt và thay đổi phiên bản theo Semantic Versioning.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Provide initial date | **Last Amended**: 2026-06-18
