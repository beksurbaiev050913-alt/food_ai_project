import streamlit as st
import os
import subprocess
import sys

# Магия: устанавливаем библиотеку прямо из кода
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import tensorflow as tf
except ImportError:
    with st.spinner('Настраиваем нейросеть... это только при первом запуске.'):
        install('tensorflow-cpu==2.15.0')
        import tensorflow as tf

import numpy as np
from PIL import Image
import gdown

st.set_page_config(page_title="AI Food Classifier")

@st.cache_resource
def load_model():
    file_id = '1xXHmbuRvexNDQU9aWy17oxsIXX05V-0u'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.h5'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return tf.keras.models.load_model(output)

st.title("🍳 Raw vs Cooked Classifier")

try:
    model = load_model()
    up = st.file_uploader("Загрузите фото", type=["jpg", "png"])
    if up:
        img = Image.open(up).convert('RGB').resize((224, 224))
        st.image(img, use_container_width=True)
        if st.button('Проверить'):
            arr = np.array(img) / 255.0
            arr = np.expand_dims(arr, axis=0)
            pred = model.predict(arr)
            res = "СЫРОЕ 🥩" if pred[0] > 0.5 else "ГОТОВОЕ 🍗"
            st.success(f"Результат: {res}")
except Exception as e:
    st.error(f"Ждем загрузки... Попробуйте обновить через минуту. Ошибка: {e}")
