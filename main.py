import streamlit as st
from openai import OpenAI
import base64

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="도로 운영 AI 분석 시스템",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ 도로 운영 AI 분석 시스템")
st.markdown("도로 이미지를 업로드하면 AI가 분석하여 운영 보고서를 자동으로 생성합니다.")

# ---------------------------
# OpenAI 클라이언트 초기화
# ---------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY가 설정되지 않았습니다. Streamlit Secrets에 추가하세요.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------
# 이미지 업로드
# ---------------------------
uploaded_file = st.file_uploader(
    "📷 도로 이미지를 업로드하세요",
    type=["jpg", "jpeg", "png"]
)

# ---------------------------
# 분석 실행
# ---------------------------
if uploaded_file is not None:

    st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)

    if st.button("🔍 AI 분석 실행"):

        with st.spinner("AI가 도로 상황을 분석 중입니다..."):

            # 이미지 base64 인코딩
            image_bytes = uploaded_file.read()
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "당신은 도로운영 및 교통관리 전문가입니다."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": """
                                    업로드된 도로 이미지를 분석하고 아래 형식으로 보고서를 작성하세요.

                                    1. 도로 상태 분석
                                    2. 교통 흐름 추정
                                    3. 위험 요소 식별
                                    4. 유지보수 필요 여부
                                    5. 운영 개선 제안
                                    """
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{encoded_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000
                )

                result = response.choices[0].message.content

                st.success("✅ 분석 완료")

                st.markdown("## 📊 도로운영 분석 보고서")
                st.markdown(result)

                # 다운로드 기능
                st.download_button(
                    label="📄 보고서 다운로드",
                    data=result,
                    file_name="도로운영_분석보고서.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")

else:
    st.info("좌측에서 도로 이미지를 업로드하세요.")
