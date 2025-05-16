from google.cloud import firestore

db = firestore.Client()

def get_user_disease(user_id: str):
    doc = db.collection("users").document(user_id).get()
    return doc.to_dict().get("disease") if doc.exists else None

def save_report(report_id, user_id, report_type, start_date, end_date, file_url):
    db.collection("reports").document(report_id).set({
        "patientId": user_id,
        "type": report_type,
        "period": {
            "startDate": start_date,
            "endDate": end_date
        },
        "createdAt": firestore.SERVER_TIMESTAMP,
        "fileUrl": file_url
    })

def get_chat_session_ids(user_id: str, start_date, end_date):
    # userId가 일치하고, startedAt이 범위에 속하는 세션만 가져오기
    query = db.collection("chatSessions") \
        .where("userId", "==", user_id) \
        .where("startedAt", ">=", start_date) \
        .where("startedAt", "<=", end_date)
    docs = query.stream()
    session_ids = [doc.id for doc in docs]
    return session_ids