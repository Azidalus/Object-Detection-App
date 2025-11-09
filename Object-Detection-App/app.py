import streamlit as st
from src.detection import segment_image
from src.tracking import track_video

st.set_page_config(page_title='Object Detection')
st.title('Object Detection')
st.markdown('Обнаружить людей или птиц на видео? Запросто!')

col1, col2 = st.columns(['Загрузите видео, на котором есть люди и/или птицы'])
with col1:
    uploaded_file = st.file_uploader('Выберите файл', type=['jpg','jpeg','png','mp4'])

with col2:
    st.write('...или выберите одно из тестовых')
    video_file = open("assets/videos/Crows.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)

if uploaded_file || a vid is selected:
    st.button('', on_click=track_video())