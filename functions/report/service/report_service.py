import uuid
import datetime
import os
from firebase_admin import firestore, db  # db 추가
from google.cloud import storage
from google.generativeai import GenerativeModel
from xhtml2pdf import pisa
from utils.firestore import get_user_disease, save_report
from config.settings import REPORT_PROMPTS
from dotenv import load_dotenv
load_dotenv()

db_fs = firestore.client()
realtime_db = db  # 실시간 DB

def get_all_messages_from_sessions(user_id: str, start_date: datetime.datetime, end_date: datetime.datetime):
    sessions = db_fs.collection("chatSessions").where("userId", "==", user_id).stream()
    chat_session_ids = [session.id for session in sessions]

    filtered_msgs = []
    for session_id in chat_session_ids:
        ref = realtime_db.reference(f"/chatSessions/{session_id}/chatMessages")
        snapshot = ref.get()
        if snapshot:
            for msg_id, msg in snapshot.items():
                msg_time = msg.get("time")
                if (
                    msg_time and
                    start_date.timestamp() <= float(msg_time) <= end_date.timestamp()
                ):
                    filtered_msgs.append(msg)
    return filtered_msgs

def generate_report(user_id: str, report_type: str) -> dict:
    assert report_type in ["7days", "14days", "30days"]
    now = datetime.datetime.utcnow()
    days = int(report_type.replace("days", ""))
    start_date = now - datetime.timedelta(days=days)
    end_date = now

    filtered_data = get_all_messages_from_sessions(user_id, start_date, end_date)

    # 프롬프트 생성
    user_ref = db_fs.collection("users").document(user_id)
    user_info = user_ref.get().to_dict()
    disease = user_info.get("disease", "")
    report_prompt = REPORT_PROMPTS.get(disease, "")

    model = GenerativeModel("gemini-1.5-pro")
    data_for_ai = f"{report_prompt}\n\nUser messages:\n" + "\n".join(msg['message'] for msg in filtered_data)
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": data_for_ai}]}]
    )
    html_str = getattr(response, 'text', '').strip()  # 안전하게 받기

    # HTML→PDF 변환
    pdf_filename = f"report-{uuid.uuid4()}.pdf"
    pdf_path = f"/tmp/{pdf_filename}"  # 임시폴더 권장
    with open(pdf_path, "wb") as f:
        pisa_status = pisa.CreatePDF(html_str, dest=f)
        if pisa_status.err:
            raise Exception("PDF 변환 실패")

    # Cloud Storage 업로드
    bucket_name = os.getenv("BUCKET_NAME")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    destination_blob_name = f"reports/{pdf_filename}"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(pdf_path)
    file_url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"

    # Firestore에 저장
    report_id = str(uuid.uuid4())
    save_report(
        report_id=report_id,
        user_id=user_id,
        report_type=report_type,
        start_date=start_date,
        end_date=end_date,
        file_url=file_url
    )

    return {
        "reportId": report_id,
        "fileUrl": file_url
    }
