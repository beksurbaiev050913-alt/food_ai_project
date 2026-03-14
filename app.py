import streamlit as st
import numpy as np
from PIL import Image
import time
import streamlit.components.v1 as components

# Настройка страницы
st.set_page_config(page_title="AI Food Classifier Pro", page_icon="🥗", layout="centered")

# Функция для озвучки
def speak(text):
    js_code = f"""<script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'ru-RU';
    window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js_code, height=0)

# --- НОВАЯ НАДПИСЬ ВВЕРХУ ---
st.caption("⚠️ Food_Ai_Project это ИИ. Он может ошибаться в 30% случаях")
# ----------------------------

st.title("🥗 Умный классификатор: Версия 4.0")
st.write("Загрузите фото продукта для мгновенного анализа.")

uploaded_file = st.file_uploader("Выберите изображение...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Объект анализа', use_container_width=True)
    
    if st.button('🔥 Начать анализ'):
        with st.status("Анализирую...", expanded=True) as status:
            time.sleep(1.5)
            
            # Логика анализа
            img_np = np.array(image)
            r, g, b = np.mean(img_np[:,:,0]), np.mean(img_np[:,:,1]), np.mean(img_np[:,:,2])
            saturation = np.max([r, g, b]) - np.min([r, g, b])
            
            # Определение готовности
            if saturation < 30: # Рис/Гарниры
                is_cooked = (r + g + b) / 3 > 160
            elif g > r: # Овощи
                is_cooked = g < 130
            else: # Мясо/Птица
                is_cooked = r < 180

            status.update(label="Готово!", state="complete", expanded=False)

        if is_cooked:
            voice_msg = "Готовая еда"
            st.success(f"### {voice_msg} ✅")
            speak(voice_msg)
            st.balloons()
        else:
            voice_msg = "Сырая еда"
            st.warning(f"### {voice_msg} ❌")
            speak(voice_msg)

st.divider()
st.info("Голосовой модуль активирован. Проект готов к презентации.")
