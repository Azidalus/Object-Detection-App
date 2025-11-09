import streamlit as st
from src.tracking import track_video, prepare_video_for_streamlit, prep_video
import streamlit_antd_components as sac
import streamlit_shadcn_ui as ui
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_lottie import st_lottie
import json
from streamlit_extras import stylable_container
import streamlit.components.v1 as components
import time

st.session_state = 0
def state():
    st.session_state = 1
st.set_page_config(page_title='Object Detection')
st.title('Object Detection')
st.write('Обнаружить людей или птиц на видео? Запросто!')
video_path = "assets/videos/Crows.mp4"
image_path = "assets/images/img.jpg"

# Применить CSS-стили из style.css к элементам на странице
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css('assets/style.css')

'''
def callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = cv2.cvtColor(cv2.Canny(img, threshold1, threshold2), cv2.COLOR_GRAY2BGR)
    return av.VideoFrame.from_ndarray(img, format="bgr24")
webrtc_streamer(key="example", video_frame_callback=callback)
'''
sac.segmented(
    items=[
            sac.SegmentedItem(label='Pigeon SVG', icon='assets/images/Pigeon.svg'),
            sac.SegmentedItem(label='img img', icon='assets/images/img.jpg'),
            sac.SegmentedItem(label='Pigeon json', icon='assets/images/Pigeon.json')
    ], align='center', size='lg', color='violet', bg_color='violet'
)

#col1, col2 = st.columns([1, 1], gap='medium')

with st.container(horizontal_alignment="center"):
#with col1:
    st.write('Загрузите видео')
    uploaded_file = st.file_uploader('', type=['jpeg','jpg','png','mp4'], label_visibility="collapsed")
    
    # Переделка file_uploader'a
    st.html(
    """
    <style>
        [data-testid='stFileUploaderDropzoneInstructions'] > div::before {
            content: 'Перетащите сюда видео';
        }
        [data-testid='stBaseButton-secondary']::after {
            line-height: initial;
            content: "или кликните";
            text-indent: 0;
        }
    </style>
    """
    )
st.markdown('**...или**', width="content")


with st.container(horizontal_alignment="center", border=True, key="my_blue_container"):
#with col2:
    st.markdown('Выберите одно из тестовых')
    vid1, vid2, vid3 = st.columns([1, 1, 1])
    with vid1:
        video_file = open("assets/videos/Crows.mp4", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes, muted=True, loop=True, autoplay=True)
        st.button('Выбрать', key=1, type='primary', on_click=state)
        
    with vid2:
        video_file = open("assets/videos/Crows.mp4", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes, muted=True, loop=True)
        st.button('Выбрать', key=2, type='primary')
    
    with vid3:
        video_file = open("assets/videos/Crows.mp4", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes, muted=True, loop=True)
        st.button('Выбрать', key=3, type='primary')
    
'''
    sac.buttons([sac.ButtonsItem(label='select'), 
                sac.ButtonsItem(label='select')], 
                align='center', gap='xl', index='None')
'''
if uploaded_file: 
    # Display next part of app
    st.write('Подождите')
    '''
    st.write('img')
    with open("assets/images/Pigeon.txt", "r") as f:
        svg_content = f.read()
    # Inject raw SVG
    st.html(svg_content)

    st.html("""
    <iframe src="https://raw.githubusercontent.com/Azidalus/Object-Detection-App/main/Pigeon.svg"
            width="200" height="200" frameborder="0"></iframe>
    """)
    st.write('v1components svg')
    st.components.v1.html(
        """
        <svg 
            src="assets/images/Pigeon.svg" 
            height="87"
            width="100"/>
        """,
        height=300,
    )
    
    st.write('v1components img')
    st.components.v1.html(
        """
        <img 
            src="assets/images/Pigeon.svg" 
            height="87"
            width="100"/>
        """,
        height=300,
    )
    '''
    
    

    col1, col2 = st.columns([1, 1])
    path = 'assets/images/Pigeon.json'
    with open(path,'r') as f:
        url = json.load(f)
    st_lottie(url,height=300,width=300,speed=1,loop=True,quality='high', key='pigeon')
    with col1:
        with st.empty():
            my_bar = st.progress(0, text='')
            st_lottie(url,height=300,width=300,speed=1,loop=True,quality='high', key='pigeon')
            for percent_complete in range(100):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1, text='**Загрузка...**')
        track_video('assets/videos/Crows.mp4', 'outputs/videos/Crows_tracked.mp4')
        video_file = open("outputs/videos/Crows_tracked.avi", "rb")
        video_bytes = video_file.read()
        #video_bytes = prep_video('assets/videos/Crows.mp4', 'outputs/videos/Crows_tracked.mp4')
        #video_bytes = prepare_video_for_streamlit('outputs/videos/Crows_tracked.mp4')
        st.video(video_bytes, muted=True)
        '''
        response_container = st.empty()                                    
        with response_container.container():
            progress_bar_cols = st.columns([2,5,2])                                
            with progress_bar_cols[1]:                                                                            
                my_bar = st.progress(0, text='')
                render_animation()  
        '''                  
                
        html_code = """
        <script>
        var iframe = document.querySelector("div.st-key-pigeon");
        if (iframe) {
            iframe.contentDocument.style.background = 'black';
        }
        </script>
        """
        components.html(html_code, height=0, width=0)
        st.markdown("""
                    <style>
                        body:has(svg) {
                            display: contents !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)
        
        st.markdown("""
                    <style>
                        .st-key-pigeon body {
                            background-color: black !important;
                            background: black !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)
       
        
    with col2:
        st.write('ver 2: path')
        st_lottie(path,height=300,width=300,speed=1,loop=True,quality='high')
    #   <div id="lottie" style="width: 300px; height: 300px; background: none;"></div>


    
    