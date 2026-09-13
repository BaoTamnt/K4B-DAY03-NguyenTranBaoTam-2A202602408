"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "restaurant_query",
        "description": "Tra cứu thông tin nhà hàng, món ăn và ưu tiên của khách hàng theo tên nhà hàng hoặc tiêu chí đặt bàn.",
        "parameters": {
            "type": "object",
            "properties": {
                "restaurant_name": {
                    "type": "string",
                    "description": "Tên nhà hàng cần tra cứu (ví dụ: 'Nhà hàng Mộc Lan')"
                },
                "customer_id": {
                    "type": "string",
                    "description": "Mã khách hàng hoặc mã đặt chỗ nếu cần (ví dụ: 'KH001')"
                }
            },
            "required": []
        }
    },

    {
        "name": "schedule_appointment",
        "description": (
            "Đặt bàn tại nhà hàng dựa trên thời gian, "
            "tên nhà hàng, số lượng người và yêu cầu đặc biệt "
            "của khách hàng."
        ),
        "parameters": {
            "type": "object",
            "properties": {

                "customer_id": {
                    "type": "string",
                    "description": (
                        "Mã khách hàng đặt bàn, "
                        "ví dụ: 'KH001'."
                    )
                },

                "datetime_str": {
                    "type": "string",
                    "description": (
                        "Thời gian muốn đặt bàn, "
                        "ví dụ: '19:00 15/09/2026'."
                    )
                },

                "restaurant_name": {
                    "type": "string",
                    "description": (
                        "Tên nhà hàng muốn đặt bàn, "
                        "ví dụ: 'Nhà hàng Mộc Lan'."
                    )
                },

                "table_size": {
                    "type": "integer",
                    "description": (
                        "Số lượng người cần đặt bàn, "
                        "ví dụ: 4."
                    )
                },

                "preference": {
                    "type": "string",
                    "description": (
                        "Sở thích hoặc yêu cầu đặc biệt của khách hàng, "
                        "ví dụ: 'món chay', 'không gian yên tĩnh', "
                        "'bàn gần cửa sổ'."
                    )
                }
            },

            "required": [
                "customer_id",
                "datetime_str",
                "restaurant_name"
            ]
        }
    }
]


# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_RESTAURANT_DATABASE = {

    "Nhà hàng Mộc Lan": {
        "cuisine": "Việt Nam",
        "location": "Cầu Giấy, Hà Nội",
        "price_range": "150.000 - 300.000 VNĐ/người",
        "rating": 4.6,
        "features": [
            "món Việt",
            "không gian yên tĩnh",
            "phù hợp gia đình"
        ]
    },

    "The Green Garden": {
        "cuisine": "Healthy",
        "location": "Đống Đa, Hà Nội",
        "price_range": "120.000 - 250.000 VNĐ/người",
        "rating": 4.5,
        "features": [
            "món chay",
            "healthy food",
            "không gian xanh"
        ]
    },

    "Pizza House": {
        "cuisine": "Pizza",
        "location": "Hà Đông, Hà Nội",
        "price_range": "100.000 - 220.000 VNĐ/người",
        "rating": 4.4,
        "features": [
            "pizza",
            "phù hợp nhóm bạn",
            "không gian trẻ trung"
        ]
    },

    "Sushi Sakura": {
        "cuisine": "Nhật Bản",
        "location": "Ba Đình, Hà Nội",
        "price_range": "250.000 - 500.000 VNĐ/người",
        "rating": 4.7,
        "features": [
            "sushi",
            "sashimi",
            "không gian sang trọng"
        ]
    }
}


def execute_restaurant_query(restaurant_name: str = "", customer_id: str = "") -> str:
    """Thực thi tra cứu thông tin nhà hàng theo tên hoặc mã khách hàng."""
    restaurant = (restaurant_name or customer_id or "").strip()
    if not restaurant:
        return json.dumps({
            "status": "VALIDATION_ERROR",
            "message": "Tên nhà hàng hoặc mã khách hàng không được để trống."
        }, ensure_ascii=False)

    matched = MOCK_RESTAURANT_DATABASE.get(restaurant)
    if matched:
        return json.dumps({
            "status": "SUCCESS",
            "restaurant_name": restaurant,
            "data": matched,
            "message": f"Thông tin nhà hàng '{restaurant}' đã được tra cứu thành công."
        }, ensure_ascii=False)

    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy nhà hàng '{restaurant}' trong hệ thống dữ liệu mẫu.",
        "available_restaurants": list(MOCK_RESTAURANT_DATABASE.keys())
    }, ensure_ascii=False)


def execute_schedule_appointment(
    customer_id: str,
    datetime_str: str,
    restaurant_name: str,
    table_size: int = 2,
    preference: str = "Không có yêu cầu đặc biệt"
) -> str:
    """
    Thực thi việc đặt bàn tại nhà hàng.
    """

    customer_id = customer_id.strip()

    if not customer_id:
        return json.dumps(
            {
                "status": "VALIDATION_ERROR",
                "message": "Mã khách hàng không được để trống."
            },
            ensure_ascii=False
        )

    restaurant_name = restaurant_name.strip()

    if restaurant_name not in MOCK_RESTAURANT_DATABASE:
        return json.dumps(
            {
                "status": "RESTAURANT_NOT_FOUND",
                "restaurant": restaurant_name,
                "available_restaurants": list(
                    MOCK_RESTAURANT_DATABASE.keys()
                ),
                "message": (
                    f"Không tìm thấy nhà hàng "
                    f"'{restaurant_name}'."
                )
            },
            ensure_ascii=False
        )

    # Kiểm tra xem nhà hàng có tồn tại trong cơ sở dữ liệu mô phỏng
    restaurant = MOCK_RESTAURANT_DATABASE.get(restaurant_name)
    if not restaurant:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy thông tin nhà hàng '{restaurant_name}'"
        }, ensure_ascii=False)

    # Giả lập logic đặt bàn (ở đây chỉ trả về phản hồi thành công)
    confirmation_id = f"CONF-{customer_id}-{datetime_str.replace(' ', '').replace(':', '')}"
    return json.dumps({
        "status": "SUCCESS",
        "confirmation_id": confirmation_id,
        "customer_id": customer_id,
        "datetime": datetime_str,
        "restaurant_name": restaurant_name,
        "table_size": table_size,
        "preference": preference
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "restaurant_query": execute_restaurant_query,
    "schedule_appointment": execute_schedule_appointment
}


def dispatch_tool_call(
    tool_name: str,
    arguments: Dict[str, Any]
) -> str:
    """
    Hàm trung chuyển yêu cầu từ Agent tới Tool tương ứng.
    """

    # Kiểm tra tool tồn tại
    if tool_name not in TOOL_ROUTER:
        return json.dumps(
            {
                "status": "UNKNOWN_TOOL",
                "error": (
                    f"Tool '{tool_name}' không tồn tại!"
                )
            },
            ensure_ascii=False
        )

    # Thực thi tool
    try:
        return TOOL_ROUTER[tool_name](**arguments)

    except TypeError as e:
        return json.dumps(
            {
                "status": "INVALID_ARGUMENTS",
                "tool": tool_name,
                "error": str(e)
            },
            ensure_ascii=False
        )

    except Exception as e:
        return json.dumps(
            {
                "status": "EXECUTION_ERROR",
                "tool": tool_name,
                "error": str(e)
            },
            ensure_ascii=False
        )