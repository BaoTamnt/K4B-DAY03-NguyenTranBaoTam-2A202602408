"""
📚 [REFERENCE ONLY / CODE MẪU THAM KHẢO]
🧠 CẤP ĐỘ 3: NATIVE MCP AGENT (Native Tool Calling + MCP Server Integration)
⚠️ Lưu ý: File này chỉ dùng để đọc tham khảo kiến trúc. Không chỉnh sửa hay debug file này.
"""

import json

def get_weather(city: str) -> str:
    return f"Thời tiết {city}: 28°C, Nắng nhẹ."

def run_level3_demo():
    print("=== DEMO CẤP ĐỘ 3: NATIVE MCP AGENT ===")
    user_goal = "Tra cứu thông tin nhà hàng phù hợp cho nhóm 4 người"
    print(f"🎯 Goal: {user_goal}")
    print("🧠 [Thought]: Phát sinh Native Tool Call 'restaurant_query'...")
    print("🛠️ [Native Tool Call]: restaurant_query({'restaurant_name': 'Nhà hàng Mộc Lan'})")
    print("👁️ [MCP Server Observation]: {'restaurant_name': 'Nhà hàng Mộc Lan', 'cuisine': 'Việt Nam', 'price_range': '150.000 - 300.000 VNĐ/người', 'rating': 4.6}")
    print("🏁 [Final Answer]: Nhà hàng Mộc Lan phù hợp cho nhóm 4 người với món Việt, mức giá 150k-300k/người và đánh giá 4.6.")

if __name__ == "__main__":
    run_level3_demo()
