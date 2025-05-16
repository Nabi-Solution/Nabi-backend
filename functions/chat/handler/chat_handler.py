from firebase_functions import db_fn
from chat.service.chat_service import process_chat
from firebase_admin import firestore
from utils.realtime import save_chat_message

def handle_chat(event: db_fn.Event[dict]):
    print("enter: handle_chat")
    try:
        message_data = event.data
        if not message_data:
            return

        print("enter: 1")
        sender = message_data.get("sender")
        if sender != "patient":
            return
        print("enter: 2")

        message = message_data.get("message")
        userSession_id = event.params["sessionId"]
        if not message or not userSession_id:
            return
        user_id, session_id = userSession_id.split('_', 1)

        print("enter: 3")
        reply = process_chat(user_id, session_id, message)
        print("reply:", reply)
        save_chat_message(session_id, reply, sender="ai")

    except Exception as e:
        return