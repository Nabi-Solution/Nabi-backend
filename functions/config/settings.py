import os
from dotenv import load_dotenv
from chat.prompts.disease_prompts import HIGH_BLOOD_PROMPT, DEPRESSION_PROMPT, ASTHMA_PROMPT
from report.prompts.report_prompts import HIGH_BLOOD_REPORT_PROMPT, DEPRESSION_REPORT_PROMPT, ASTHMA_REPORT_PROMPT
from chat.prompts.system_prompts import (
    INTRO_PROMPT,
    FINAL_QUESTION_PROMPT,
    GO_BACK_PROMPT,
    EARLY_EXIT_PROMPT,
    AUTO_DATE_PROMPT,
    JSON_OUTPUT_PROMPT
)


load_dotenv()

# 시스템 프롬프트 텍스트 조합
SYSTEM_PROMPTS = [
    INTRO_PROMPT,
    FINAL_QUESTION_PROMPT,
    GO_BACK_PROMPT,
    EARLY_EXIT_PROMPT,
    AUTO_DATE_PROMPT,
    JSON_OUTPUT_PROMPT
]

# 질병별 프롬프트
DISEASE_PROMPTS = {
    "depression": DEPRESSION_PROMPT,
    "asthma": ASTHMA_PROMPT,
    "highBlood": HIGH_BLOOD_PROMPT
}

# 질병별 레포트 프롬프트
REPORT_PROMPTS = {
    "depression": DEPRESSION_REPORT_PROMPT,
    "asthma": ASTHMA_REPORT_PROMPT,
    "highBlood": HIGH_BLOOD_REPORT_PROMPT
}


# 대화 종료 키워드
END_MESSAGE = "Thank you for sharing. Your record is complete for today. Take care, and I’ll be here tomorrow too."
