from firebase_admin import db
import time

def save_chat_message(session_id: str, message: str, sender: str = "ai", type_: str = "text"):
    print("8. Saving chat message")
    ref = db.reference(f"/chatSessions/{session_id}/chatMessages/")
    ref.push({
        "sessionId": session_id,
        "sender": sender,
        "message": message,
        "type": type_,
        "time": time.time()
    })

def get_chat_history(session_id: str) -> list[dict]:
    ref = db.reference(f"chatSessions/{session_id}")
    snapshot = ref.order_by_child("time").get()
    if not snapshot:
        return []
    return list(snapshot.values())

def get_all_messages_from_sessions(session_ids):
    all_messages = []
    for session_id in session_ids:
        ref = db.reference(f"/chatSessions/{session_id}/chatMessages")
        messages = ref.get()
        if messages:
            # 메시지들 모아서 리스트로
            all_messages.extend(list(messages.values()))
    return all_messages