import os
import sys

from flask import Flask, jsonify, render_template, request

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import run_react_agent, save_waterfall_trace
from mcp_server import MCPRestaurantServer
from providers import get_llm_provider

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json(silent=True) or {}
    user_query = (payload.get("message") or "").strip()

    if not user_query:
        return jsonify({"answer": "Vui lòng nhập câu hỏi trước khi gửi."}), 400

    provider = get_llm_provider()
    mcp_server = MCPRestaurantServer()
    logs = run_react_agent(user_query, provider, mcp_server)
    save_waterfall_trace(logs)

    final_answer = next(
        (item.get("output") for item in reversed(logs) if item.get("action_type") == "FINAL_ANSWER"),
        "Không có câu trả lời.",
    )

    return jsonify({
        "answer": final_answer,
        "trace": logs,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
