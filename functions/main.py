from firebase_functions import https_fn, db_fn
import config.firebase
from chat.handler.chat_handler import handle_chat
from report.handler.report_handler import handle_report

@db_fn.on_value_created(reference="/chatSessions/{sessionId}/chatMessages/{messageId}")
def on_message_created(event: db_fn.Event[dict]):
    return handle_chat(event)

@https_fn.on_request()
def report(request):
    return handle_report(request)
