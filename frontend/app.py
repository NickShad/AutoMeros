import streamlit as st
from PIL import Image
import numpy as np
import cv2
import os
import tempfile
from io import BytesIO

import sys
sys.path.append(os.path.abspath("../"))
from backend.segmentation import segment_image


LABELS_PATH = f"../backend/classes_names.txt"



def main():
    st.set_page_config(layout="wide", page_title="Сегментация автомобиля")
    st.title("Анализ деталей автомобиля")

    # Кнопка загрузки изображения
    uploaded_file = st.file_uploader(
        "Загрузите изображение автомобиля",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            # Записываем загруженные данные во временный файл
            tmp_file.write(uploaded_file.read())
            temp_image_path = tmp_file.name

        # Обработка и сегментация
        seg_image_path, segments = segment_image(temp_image_path)

        # Двухколоночный layout
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Оригинальное изображение")
            st.image(temp_image_path, use_container_width=True)

            st.subheader("Сегментированное изображение")
            st.image(seg_image_path, use_container_width=True)

        with col2:
            st.subheader("Детали автомобиля")

            # Контейнер с прокруткой
            scroll_container = st.container()

            # Рассчитаем количество строк для сетки 2 колонки
            rows = (len(segments) + 1) // 2

            with open(LABELS_PATH) as labels_file:
                labels = labels_file.read().split('\n')

            with scroll_container:
                # Создаем сетку 2 колонки
                for row in range(rows):
                    cols = st.columns(2)
                    for col_idx in range(2):
                        idx = row * 2 + col_idx
                        if idx < len(segments):
                            segment = segments[idx]
                            with cols[col_idx]:
                                st.image(
                                    segment.path,
                                    caption=f'{labels[segment.class_idx]} {segment.conf}',
                                    use_container_width='auto'
                                )


if __name__ == "__main__":
    main()