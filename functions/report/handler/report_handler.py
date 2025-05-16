from flask import request, jsonify
from report.service.report_service import generate_report

def handle_report(request):
    if request.method != "POST":
        return jsonify({"error": "POST method required."}), 405

    try:
        data = request.get_json()
        user_id = data.get("userId")
        report_type = data.get("type")  # "7days" | "14days" | "30days"

        if not user_id or not report_type:
            return jsonify({"error": "Missing 'userId' or 'type'"}), 400

        result = generate_report(user_id, report_type)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
