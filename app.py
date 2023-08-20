from track import *
import tempfile
import cv2
import torch
import streamlit as st
import os


if __name__ == '__main__':
    st.set_page_config(page_icon="👨‍⚕️", 
                       page_title="Drip Infusion Dashboard", 
                       layout = 'wide', 
                       initial_sidebar_state = 'auto')
    st.title('Monitoring Drip Infusion')

    # upload video
    video_file_buffer = st.sidebar.file_uploader("Upload a video", type=['mp4', 'mov', 'avi'])

    if video_file_buffer:
        st.sidebar.text('Input video')
        st.sidebar.video(video_file_buffer)
        # save video from streamlit into "videos" folder for future detect
        with open(os.path.join('videos', video_file_buffer.name), 'wb') as f:
            f.write(video_file_buffer.getbuffer())

    st.sidebar.title('Settings')
    # custom class
    # custom_class = st.sidebar.checkbox('Custom classes')
    assigned_class_id = [0]
    names = ['tetesan']

    # if custom_class:
    #     assigned_class_id = []
    #     assigned_class = st.sidebar.multiselect('Select custom classes', list(names))
    #     for each in assigned_class:
    #         assigned_class_id.append(names.index(each))
    
    # st.write(assigned_class_id)

    # setting hyperparameter
    confidence = st.sidebar.slider('Confidence', min_value=0.0, max_value=1.0, value=0.5)
    line = st.sidebar.number_input('Line position', min_value=0.0, max_value=1.0, value=0.50, step=0.1)


    
    status = st.empty()
    stframe = st.empty()
    if video_file_buffer is None:
        status.markdown('<font size= "4"> **Status:** Waiting for input </font>', unsafe_allow_html=True)
    else:
        status.markdown('<font size= "4"> **Status:** Ready </font>', unsafe_allow_html=True)

    tetesan, timer, fps = st.columns(3)
    with tetesan:
        st.markdown('**Tetesan**')
        tetesan_text = st.markdown('__')
    
    with timer:
        st.markdown('**Time**')
        timer_text = st.markdown('__')

    with fps:
        st.markdown('**FPS**')
        fps_text = st.markdown('__')


    track_button = st.sidebar.button('START')
    # reset_button = st.sidebar.button('RESET ID')
    if track_button:
        # reset ID and count from 0
        reset()
        opt = parse_opt()
        opt.conf_thres = confidence
        opt.source = f'videos/{video_file_buffer.name}'

        status.markdown('<font size= "4"> **Status:** Running... </font>', unsafe_allow_html=True)
        with torch.no_grad():
            detect(opt, stframe, tetesan_text, timer_text, line, fps_text, assigned_class_id)
        status.markdown('<font size= "4"> **Status:** Finished ! </font>', unsafe_allow_html=True)
        # end_noti = st.markdown('<center style="color: blue"> FINISH </center>',  unsafe_allow_html=True)

    # if reset_button:
        # reset()
    #     st.markdown('<h3 style="color: blue"> Reseted ID </h3>', unsafe_allow_html=True)
