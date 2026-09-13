"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    @staticmethod
    def _pick_restaurant(prompt_lower: str) -> str:
        if "món chay" in prompt_lower or "chay" in prompt_lower:
            return "The Green Garden"
        if "pizza" in prompt_lower or "nhóm bạn" in prompt_lower or "nhóm" in prompt_lower:
            return "Pizza House"
        if "sang" in prompt_lower or "sushi" in prompt_lower or "nhật" in prompt_lower:
            return "Sushi Sakura"
        if "không gian yên tĩnh" in prompt_lower or "món việt" in prompt_lower or "việt nam" in prompt_lower or "gia đình" in prompt_lower:
            return "Nhà hàng Mộc Lan"
        if "gần trường" in prompt_lower or "gợi ý" in prompt_lower or "địa điểm" in prompt_lower:
            return "Nhà hàng Mộc Lan"
        return "Nhà hàng Mộc Lan"

    @staticmethod
    def _extract_booking_info(prompt: str):
        prompt_lower = prompt.lower()
        restaurant_name = None
        for candidate in ["nhà hàng mộc lan", "mộc lan", "the green garden", "green garden", "pizza house", "sushi sakura"]:
            if candidate in prompt_lower:
                restaurant_name = candidate
                break

        time_text = None
        if "19:00" in prompt or "19h" in prompt_lower or "19 giờ" in prompt_lower:
            time_text = "19:00"
        elif "tối nay" in prompt_lower:
            time_text = "tối nay"
        elif "sáng" in prompt_lower:
            time_text = "sáng"
        elif "trưa" in prompt_lower:
            time_text = "trưa"

        table_size = None
        for match in ["2 người", "3 người", "4 người", "5 người", "6 người", "7 người", "8 người"]:
            if match in prompt_lower:
                table_size = match
                break
        if table_size is None:
            if "cho 2" in prompt_lower or "2 khách" in prompt_lower:
                table_size = "2 người"
            elif "cho 3" in prompt_lower or "3 khách" in prompt_lower:
                table_size = "3 người"
            elif "cho 4" in prompt_lower or "4 khách" in prompt_lower:
                table_size = "4 người"

        preference = None
        if "món chay" in prompt_lower or "chay" in prompt_lower:
            preference = "món chay"
        elif "không gian yên tĩnh" in prompt_lower or "yên tĩnh" in prompt_lower:
            preference = "không gian yên tĩnh"
        elif "nhóm bạn" in prompt_lower or "nhóm" in prompt_lower:
            preference = "phù hợp nhóm bạn"
        elif "sang trọng" in prompt_lower or "nhật" in prompt_lower:
            preference = "không gian sang trọng"

        return {
            "restaurant_name": restaurant_name,
            "time_text": time_text,
            "table_size": table_size,
            "preference": preference,
        }

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        prompt_lower = prompt.lower()
        if "đặt bàn" in prompt_lower or "đặt chỗ" in prompt_lower or "đặt lịch" in prompt_lower:
            info = self._extract_booking_info(prompt)
            missing = []
            if not info["restaurant_name"]:
                missing.append("nhà hàng")
            if not info["time_text"]:
                missing.append("thời gian")
            if not info["table_size"]:
                missing.append("số lượng người")
            if missing:
                return (
                    "[Mock Chatbot Response]: Tôi có thể hỗ trợ đặt bàn, nhưng trước tiên tôi cần bạn xác nhận "
                    + ", ".join(missing) + ". "
                    + "Bạn muốn đặt ở nhà hàng nào, vào thời gian nào và cho bao nhiêu người?"
                )
            return f"[Mock Chatbot Response]: Tôi có thể hỗ trợ đặt bàn cho {info['table_size']} tại {info['restaurant_name']} vào {info['time_text']}."
        if "nhà hàng" in prompt_lower or "ăn" in prompt_lower or "món" in prompt_lower:
            selected = self._pick_restaurant(prompt_lower)
            if selected == "The Green Garden":
                return "[Mock Chatbot Response]: Gợi ý cho bạn: The Green Garden (món chay, không gian xanh, phù hợp nếu bạn muốn ăn lành mạnh)."
            if selected == "Pizza House":
                return "[Mock Chatbot Response]: Gợi ý cho bạn: Pizza House (pizza, phù hợp nhóm bạn, không gian trẻ trung)."
            if selected == "Sushi Sakura":
                return "[Mock Chatbot Response]: Gợi ý cho bạn: Sushi Sakura (món Nhật, không gian sang trọng, phù hợp cho bữa ăn hạng sang)."
            return "[Mock Chatbot Response]: Gợi ý cho bạn: Nhà hàng Mộc Lan (món Việt, không gian yên tĩnh, phù hợp gia đình và hẹn hò)."
        return f"[Mock Chatbot Response]: Tôi đã nhận được câu hỏi '{prompt}'. Tôi có thể gợi ý nhà hàng phù hợp để bạn chọn."

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()

        if "đặt bàn" in prompt_lower or "đặt chỗ" in prompt_lower or "đặt lịch" in prompt_lower:
            info = self._extract_booking_info(prompt)
            missing = []
            if not info["restaurant_name"]:
                missing.append("tên nhà hàng")
            if not info["time_text"]:
                missing.append("thời gian đặt bàn")
            if not info["table_size"]:
                missing.append("số lượng khách")

            if missing:
                suggestions = [
                    "Nhà hàng Mộc Lan (món Việt, yên tĩnh)",
                    "The Green Garden (món chay, không gian xanh)",
                    "Pizza House (phù hợp nhóm bạn)"
                ]
                return {
                    "type": "text",
                    "content": (
                        "Tôi có thể hỗ trợ đặt bàn, nhưng bạn chưa cho tôi đủ thông tin để xác nhận. "
                        f"Bạn cần cho tôi {', '.join(missing)}. "
                        f"Một số lựa chọn phù hợp: {', '.join(suggestions)}. "
                        "Hãy cho tôi biết nhà hàng bạn muốn, thời gian và số lượng người, tôi sẽ giúp đặt chỗ cho bạn."
                    ),
                    "thought": "Khách hàng muốn đặt bàn nhưng thiếu thông tin cần thiết; nên hỏi xác nhận trước khi gọi tool đặt chỗ."
                }

            # Chỉ gọi tool khi đã có đầy đủ dữ liệu người dùng cung cấp
            restaurant_name = self._pick_restaurant(prompt_lower)
            if info["restaurant_name"]:
                restaurant_name = {
                    "mộc lan": "Nhà hàng Mộc Lan",
                    "the green garden": "The Green Garden",
                    "green garden": "The Green Garden",
                    "pizza house": "Pizza House",
                    "sushi sakura": "Sushi Sakura",
                }.get(info["restaurant_name"], self._pick_restaurant(prompt_lower))

            preference = info["preference"] or "không gian yên tĩnh"
            table_size_value = 4
            if info["table_size"] == "2 người":
                table_size_value = 2
            elif info["table_size"] == "3 người":
                table_size_value = 3
            elif info["table_size"] == "5 người":
                table_size_value = 5
            elif info["table_size"] == "6 người":
                table_size_value = 6

            datetime_str = info["time_text"] if info["time_text"] and info["time_text"] != "tối nay" else "19:00 15/09/2026"
            if info["time_text"] == "tối nay":
                datetime_str = "19:00 15/09/2026"

            return {
                "type": "tool_call",
                "tool_name": "schedule_appointment",
                "arguments": {
                    "customer_id": "KH001",
                    "datetime_str": datetime_str,
                    "restaurant_name": restaurant_name,
                    "table_size": table_size_value,
                    "preference": preference
                },
                "thought": f"Khách hàng đã cung cấp đủ thông tin để xác nhận đặt bàn. Tôi sẽ gọi tool schedule_appointment cho {restaurant_name}."
            }

        if "tìm" in prompt_lower or "gợi ý" in prompt_lower or "nhà hàng" in prompt_lower or "ăn" in prompt_lower or "món" in prompt_lower or "địa điểm" in prompt_lower:
            restaurant_name = self._pick_restaurant(prompt_lower)
            return {
                "type": "tool_call",
                "tool_name": "restaurant_query",
                "arguments": {
                    "restaurant_name": restaurant_name,
                    "customer_id": "KH001"
                },
                "thought": f"Câu hỏi yêu cầu tra cứu nhà hàng phù hợp. Tôi sẽ gọi tool restaurant_query để kiểm tra thông tin chi tiết của {restaurant_name}."
            }

        return {
            "type": "text",
            "content": "[Mock Agent Response]: Tôi có thể gợi ý một số nhà hàng phù hợp theo vị trí, mức giá và phong cách ẩm thực của bạn.",
            "thought": "Câu hỏi chung về nhà hàng, đưa ra gợi ý ngắn gọn và phù hợp với nhu cầu khách hàng."
        }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
