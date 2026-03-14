import streamlit as st
import numpy as np
from PIL import Image
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Food Classifier Pro", page_icon="🥗", layout="centered")

def speak(text):
    js_code = f"""<script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'ru-RU';
    window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js_code, height=0)

st.title("🥗 Умный классификатор: Версия 3.5")
st.write("Исправлена ошибка с определением риса и мяса!")

uploaded_file = st.file_uploader("Загрузите фото продукта...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Объект анализа', use_container_width=True)
    
    if st.button('🔥 Начать точный анализ'):
        with st.status("Изучаем детали...", expanded=True) as status:
            time.sleep(1)
            
            # Считаем каналы
            img_np = np.array(image)
            r, g, b = np.mean(img_np[:,:,0]), np.mean(img_np[:,:,1]), np.mean(img_np[:,:,2])
            
            # Вычисляем "насыщенность" (разница между каналами)
            # У серого/белого (рис) разница между R, G и B маленькая
            # У красного/коричневого (мясо) - большая
            saturation = np.max([r, g, b]) - np.min([r, g, b])
            
            # ЛОГИКА ОПРЕДЕЛЕНИЯ:
            if saturation < 25: # Если цвета почти одинаковые - это что-то белое/серое
                product = "Рис или светлый гарнир"
                is_cooked = (r + g + b) / 3 > 160 # Яркий - вареный, темный - сырой
            elif g > r and g > b:
                product = "Овощи или зелень"
                is_cooked = g < 120
            elif r > 100 and r > g: # Если преобладает красный/коричневый
                product = "Мясо или курица"
                # Готовое мясо обычно темнее сырого (коричневее)
                is_cooked = r < 180 
            else:
                product = "Продукт"
                is_cooked = r < 120

            status.update(label="Анализ завершен!", state="complete", expanded=False)

        if is_cooked:
            res_text = f"Это готовое блюдо. Похоже на {product}."
            st.success(f"### {res_text} ✅")
            speak(res_text)
            st.balloons()
        else:
            res_text = f"Это сырой продукт. Кажется, это {product}."
            st.warning(f"### {res_text} ❌")
            speak(res_text)

st.divider()
st.caption("Баг с рисом исправлен. Алгоритм теперь различает насыщенность цвета.")
