import streamlit as st
import numpy as np
from PIL import Image
import os
import gdown
import tensorflow as tf

st.set_page_config(page_title="Food Classifier", page_icon="🍳")

@st.cache_resource
def load_model_from_drive():
    file_id = '1xXHmbuRvexNDQU9aWy17oxsIXX05V-0u'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.h5'
    if not os.path.exists(output):
        with st.spinner('Загрузка модели...'):
            gdown.download(url, output, quiet=False)
    # Загружаем только структуру для предсказаний
    return tf.keras.models.load_model(output)

st.title("🍳 Raw vs Cooked Classifier")

try:
    model = load_model_from_drive()
    uploaded_file = st.file_uploader("Загрузите фото еды", type=["jpg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption='Ваше фото', use_container_width=True)
        
        # Обработка
        img = image.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
        
        if st.button('Проверить'):
            prediction = model.predict(img_array)
            res = "СЫРОЕ 🥩" if prediction[0] > 0.5 else "ГОТОВОЕ 🍗"
            st.success(f"Результат: {res}")
except Exception as e:
    st.error(f"Ошибка: {e}")
