import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import gdown

# Настройка страницы
st.set_page_config(
    page_title="Raw vs Cooked Food Classifier",
    page_icon="🍳",
    layout="wide"
)

# Функция для загрузки модели из Google Drive
@st.cache_resource
def load_model_from_drive():
    file_id = '1xXHmbuRvexNDQU9aWy17oxsIXX05V-0u'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'food_classifier_model.h5'
    
    if not os.path.exists(output):
        with st.spinner('Загрузка нейросети из облака... Это займет около минуты.'):
            gdown.download(url, output, quiet=False)
    
    return tf.keras.models.load_model(output)

# Загружаем модель
try:
    model = load_model_from_drive()
except Exception as e:
    st.error(f"Ошибка при загрузке модели: {e}")

st.title("🍳 Классификатор еды: Сырое или Готовое?")
st.write("Загрузите фото блюда, и ИИ определит его состояние.")

uploaded_file = st.file_uploader("Выберите изображение...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Загруженное фото', use_container_width=True)
    
    # Подготовка фото для модели
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    if st.button('Определить состояние'):
        prediction = model.predict(img_array)
        # Предполагаем, что 0 - готовое, 1 - сырое (зависит от твоего обучения)
        res = "СЫРОЕ 🥩" if prediction[0] > 0.5 else "ГОТОВОЕ 🍗"
        st.success(f"Результат: {res}")
