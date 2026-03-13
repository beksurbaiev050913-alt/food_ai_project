import streamlit as st
import numpy as np
from PIL import Image
import os
import gdown

st.set_page_config(page_title="AI Food Classifier", page_icon="🍳")

# Функция загрузки (просто скачиваем файл)
@st.cache_resource
def download_model():
    file_id = '1xXHmbuRvexNDQU9aWy17oxsIXX05V-0u'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.h5'
    if not os.path.exists(output):
        with st.spinner('Загрузка нейросети...'):
            gdown.download(url, output, quiet=False)
    return output

st.title("🍳 Raw vs Cooked Classifier")
st.info("Внимание: На бесплатном сервере TensorFlow может не запуститься. Если вы видите это сообщение, значит сайт работает!")

try:
    model_path = download_model()
    uploaded_file = st.file_uploader("Загрузите фото еды", type=["jpg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file).convert('RGB').resize((224, 224))
        st.image(img, use_container_width=True)
        st.warning("Для анализа фото на этом сервере не хватает памяти. Но база сайта успешно настроена!")
        
except Exception as e:
    st.error(f"Ошибка: {e}")
