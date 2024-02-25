from time import time
import streamlit as st
import subprocess
import os
import shutil

# streamlit run app.py --server.port=8503 --server.address=0.0.0.0

# Function to inject custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def save_uploaded_file(uploadedfile):
    os.makedirs("/app/audio-in", exist_ok=True)
    with open(os.path.join("/app/audio-in", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return os.path.join("/app/audio-in", uploadedfile.name)

# Function to display audio files
def display_audio_files(output_dir, audio_path, audio_name):
    with st.container(border=True):
        st.write(f"original audio {audio_name}")
        st.audio(audio_path)
        
        for file_name in os.listdir(output_dir):
            if file_name.endswith(".wav"):
                file_path = os.path.join(output_dir, file_name)
                st.write(file_name.split(".")[0])
                st.audio(file_path, format='audio/wav')


def remove_audio_files(file_path, output_dir):
    os.remove(file_path)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    

def main():           
    st.set_page_config(
        page_title='DataCula music demixing',
        page_icon=':rocket:',
        initial_sidebar_state='collapsed',
        menu_items={
            'Get Help': "https://github.com/facebookresearch/demucs",
            'About': "# Datacula Music Demixing!"
        }
    )

    # Sidebar
    with st.sidebar:
        st.sidebar.markdown("With :heart: from [DataCula!](https://datacula.com)")
        st.header("Demucs")
        st.markdown(":studio_microphone: dockerized binary executable [facebook demucs](https://github.com/facebookresearch/demucs).")


    st.title(":postal_horn: Music Demixing")
    """
    We're very excited to release `dockerized, music demixing binary executable`, to demix a music into vocal and instruments.
    """

    tab1, tab2 = st.tabs([
        ":musical_score: Music Demixing",
        ":information_source: Information",
    ])

    # Injecting the CSS
    local_css("style.css")

    with tab1:
        st.markdown("Please upload your music to and let's try demixing!")
        uploaded_files = st.file_uploader("Choose a .mp3 or .wav file", type=["wav", "mp3"], accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                audio_path = save_uploaded_file(uploaded_file)
                output_dir = "/app/audio-out/" + uploaded_file.name.split(".")[0]
                
                # Run the command
                with st.spinner(f'processing audio {uploaded_file.name} ...'):
                    command = ["/app/separator", "--input", audio_path]
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()

                if process.returncode != 0:
                    remove_audio_files(audio_path, output_dir)
                    st.error(f"Error processing audio: {stderr.decode()}")
                else:
                    st.success(f"audio file {uploaded_file.name} is processed.")
                    display_audio_files(output_dir, audio_path, uploaded_file.name)
                    remove_audio_files(audio_path, output_dir)

    with tab2:
        st.markdown("`htdemucs` model is used as default model!")
        
    
if __name__ == "__main__":
    main()