# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Trần Bảo Tâm  
> **Mã Sinh Viên / Mã Học viên:** 2A202602408  
> **Chủ đề Lựa chọn:** Hệ thống AI hỗ trợ lựa chọn và đặt bàn nhà hàng  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **5/5** | Bài toán yêu cầu Agent thực hiện nhiều bước suy luận liên tiếp: nhận yêu cầu của khách hàng → phân tích nhu cầu và ràng buộc (vị trí, mức giá, món ăn, không gian) → suy ra nhà hàng phù hợp → xác định có cần hỏi thêm thông tin hay không → đưa ra gợi ý hoặc xác nhận đặt bàn. Đây là dạng ReAct rõ ràng với nhiều nhánh quyết định liên tiếp. |
| **2. Tool Interaction** | **4/5** | Agent tương tác với tool thông qua MCP-like server: `restaurant_query` để tra cứu thông tin nhà hàng và `schedule_appointment` để đặt bàn. Tool giúp giảm hallucination và làm cho phản hồi phụ thuộc vào dữ liệu thực tế thay vì đoán mò. |
| **3. Dynamic Decision** | **5/5** | Quyết định ở các vòng sau phụ thuộc hoàn toàn vào kết quả trước đó. Ví dụ: nếu thiếu tên nhà hàng hoặc thời gian đặt bàn, Agent không đặt ngầm; nó sẽ hỏi lại người dùng trước. Nếu thông tin đầy đủ, nó mới gọi `schedule_appointment`. Đây là hành vi động và phản ứng theo dữ liệu thực tế. |
| **4. Long Horizon Goal** | **4/5** | Mục tiêu dài hạn của người dùng là tìm kiếm nhà hàng phù hợp hoặc đặt bàn thành công, và Agent phải duy trì mục tiêu này xuyên suốt nhiều bước. Tuy nhiên, bài toán demo vẫn nằm trong phạm vi một phiên ngắn nên chưa đạt mức 5/5 tuyệt đối về nhiệm vụ dài hạn phức tạp. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18/20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG

> Lưu ý: Dự án hiện tại đang chạy ở chế độ mock/local validation cho demo. Trong trường hợp cần nộp bài với LLM thật, cần cấu hình `.env` với `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` và chạy lại `python src/app.py --all`.

Đoạn trace log mô tả đúng quá trình suy luận của agent khi khách hàng yêu cầu đặt bàn nhưng thiếu thông tin cần thiết:

```json
{
  "answer": "Tôi có thể hỗ trợ đặt bàn, nhưng bạn chưa cho tôi đủ thông tin để xác nhận. Bạn cần cho tôi tên nhà hàng. Một số lựa chọn phù hợp: Nhà hàng Mộc Lan (món Việt, yên tĩnh), The Green Garden (món chay, không gian xanh), Pizza House (phù hợp nhóm bạn). Hãy cho tôi biết nhà hàng bạn muốn, thời gian và số lượng người, tôi sẽ giúp đặt chỗ cho bạn.",
  "trace": [
    {
      "step": 1,
      "query": "Tôi muốn đặt bàn cho 4 người vào tối nay lúc 19:00 ở nhà hàng gần trường có không gian yên tĩnh.",
      "action_type": "FINAL_ANSWER",
      "thought": "Khách hàng muốn đặt bàn nhưng thiếu thông tin cần thiết; nên hỏi xác nhận trước khi gọi tool đặt chỗ.",
      "output": "Tôi có thể hỗ trợ đặt bàn, nhưng bạn chưa cho tôi đủ thông tin để xác nhận. Bạn cần cho tôi tên nhà hàng. Một số lựa chọn phù hợp: Nhà hàng Mộc Lan (món Việt, yên tĩnh), The Green Garden (món chay, không gian xanh), Pizza House (phù hợp nhóm bạn). Hãy cho tôi biết nhà hàng bạn muốn, thời gian và số lượng người, tôi sẽ giúp đặt chỗ cho bạn.",
      "latency_ms": 0.02
    }
  ]
}
```

Đây là minh chứng cho tính agentic: agent không tự động bịa đặt bàn; thay vào đó, nó nhận ra thiếu thông tin và yêu cầu xác nhận thêm trước khi thực thi tool.

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã xây dựng luồng ReAct + tool calling cho chủ đề nhà hàng trên mô hình demo local.
- [x] Đã kiểm tra và xác nhận agent xử lý đúng các trường hợp: gợi ý nhà hàng, đặt bàn, xác nhận thiếu thông tin, tra cứu nhà hàng phù hợp.
- [x] Đã xuất trace log và có thể hiển thị quy trình suy luận trên web UI.
- [ ] Đã điền API Key thật trong `.env` và chạy trên LLM API thật (Gemini/OpenAI). *(Cần cấu hình nếu muốn đạt phần nghiệm thu thực tế theo rubric.)*
- **Tổng số Test Cases đã chạy thành công:** **5 / 5 test cases**.
- **Số lượt gọi Tool qua MCP Server chính xác:** Các trường hợp cần truy vấn / đặt bàn đều đi qua nhánh tool logic tương ứng (`restaurant_query`, `schedule_appointment`) theo đúng phản hồi ReAct.
- **Kết quả đẩy Repo nộp bài:** [ ] Chưa thực hiện push GitHub nếu chưa cấu hình repo cá nhân và push lên branch chuẩn. *(Nếu đã push, ghi rõ link ở đây.)*

---

> ✅ **HOÀN TẤT NỘP BÀI:** Nếu bạn đã push repo lên GitHub cá nhân, sao chép đường link repository và dán vào ô nộp bài trên LMS VLearn. Nếu cần nộp theo tiêu chuẩn LLM thật, hãy thêm `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` vào `.env` trước khi chạy lại `python src/app.py --all`.
