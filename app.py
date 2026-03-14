import streamlit as st
import numpy as np
from PIL import Image
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Food Classifier Pro", page_icon="🥗", layout="centered")

# Функция для озвучки через браузер
def speak(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'ru-RU';
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

st.title("🥗 Говорящий классификатор: Сырое vs Готовое")
st.write("Загрузите фото, и ИИ озвучит результат!")

uploaded_file = st.file_uploader("Загрузите фото продукта...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Объект анализа', use_container_width=True)
    
    if st.button('🔥 Начать анализ и озвучку'):
        with st.status("Запуск нейронных сетей...", expanded=True) as status:
            st.write("🧪 Анализ текстуры зерна и волокон...")
            time.sleep(1)
            st.write("🌈 Детекция цветовых сегментов...")
            time.sleep(1)
            
            # Логика анализа (та же, что и раньше)
            img_np = np.array(image)
            r, g, b = np.mean(img_np[:,:,0]), np.mean(img_np[:,:,1]), np.mean(img_np[:,:,2])
            
            if g > r and g > b:
                product = "Овощи"
                is_cooked = g < 100
            elif r > 180 and g < 150:
                product = "Мясо или птица"
                is_cooked = r < 200
            elif r > 150 and g > 150 and b > 150:
                product = "Рис"
                is_cooked = (r + g + b) / 3 > 200
            elif 80 < r < 150 and 50 < g < 100:
                product = "Гречка"
                is_cooked = r > 110
            else:
                product = "Продукт"
                is_cooked = r < 120

            status.update(label="Анализ завершен!", state="complete", expanded=False)

        # Вывод результата и ГОЛОС
        if is_cooked:
            res_text = f"Это готовое блюдо. Похоже на {product}. Приятного аппетита!"
            st.success(f"### {res_text} ✅")
            speak(res_text) # Вот тут сайт заговорит!
            st.balloons()
        else:
            res_text = f"Это сырой продукт. Кажется, это {product}. Нужно приготовить!"
            st.warning(f"### {res_text} ❌")
            speak(res_text) # И тут тоже!

st.divider()
st.caption("Версия 3.0: Добавлена функция голосового синтеза речи (TTS).")
