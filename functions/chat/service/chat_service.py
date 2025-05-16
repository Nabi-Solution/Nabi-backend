import os
from dotenv import load_dotenv
import google.generativeai as genai

from utils.firestore import get_user_disease
from config.settings import SYSTEM_PROMPTS, DISEASE_PROMPTS
from utils.realtime import get_chat_history, save_chat_message


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def process_chat(user_id: str, session_id: str, user_msg: str) -> list[dict]:
    # 1. 질병 정보 가져오기
    disease = get_user_disease(user_id)
    disease_prompt = DISEASE_PROMPTS.get(disease, "")
    print("disease_prompt: ", disease_prompt)

    # 2. 실시간 DB에서 이전 대화 가져오기
    previous_chats_raw = get_chat_history(session_id)
    print("previous_chats_raw: ", previous_chats_raw)

    # 3. history 변환: 실시간 DB에서 가져온 걸 Gemini 형식으로 매핑
    history = []
    for chat_dict in previous_chats_raw:
        for _, chat in chat_dict.items():
            if "sender" in chat and "message" in chat:
                history.append({
                    "role": "user" if chat["sender"] == "patient" else "model",
                    "parts": [{"text": chat["message"]}]
                })

    # 4. system prompt 구성 (role 없이)
    prompt_text = "\n\n".join(SYSTEM_PROMPTS)  # 역슬래시 두 번 말고 그냥 줄바꿈!
    if disease_prompt:
        prompt_text += "\n\n" + disease_prompt
    all_prompt = {
        "role": "user",
        "parts": [{"text": prompt_text}]
    }
    history.insert(0, all_prompt)
    print("history: ", history)

    # 5. Gemini API 호출
    try:
        model = genai.GenerativeModel("gemini-2.0-light")
        chat = model.start_chat(history=history)
        response = chat.send_message(user_msg)
        print("7.response: ", response.text)
    except Exception as e:
        print("Error occurred:", e)
        response = None  # 예외 발생 시 response 미정의 방지

    # 6. Realtime DB에 대화 저장
    if response and hasattr(response, "text"):
        save_chat_message(session_id, response.text, sender="ai")
    else:
        save_chat_message(session_id, "(AI 응답 없음)", sender="ai")
