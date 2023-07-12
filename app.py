import os, io
import streamlit as st
import webbrowser

def redirect_to_url(url):
    js = f"window.location.href='{url}'"
    html = f"<script>{js}</script>"
    st.markdown(html, unsafe_allow_html=True)


def main():
    # st.set_page_config(layout="wide")
    st.markdown(
        """
    <style>
    body {
        font-family: "Helvetica", sans-serif;
    },
    .file-upload-btn .stFileUploader > div:first-child {
        padding: 0.5rem 0.75rem;
        font-size: 14px;
        line-height: 1.5;
        border-radius: 0.2rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("Langchain to Langflow")
    left_column, right_column = st.columns(2)
    with left_column:
        input_file = st.file_uploader("Upload your Langchain File", type="py")
    if input_file is not None:
        with io.TextIOWrapper(input_file, encoding="utf-8", newline="") as file_wrapper:
            file_contents = file_wrapper.read()

        # Create a new file with the same contents
        with open("input1.py", "w", newline="") as new_file:
            new_file.write(file_contents)
            temp_file_path = new_file.name
            with right_column:
                st.write('')
                st.write('')
                st.code(f"File Name: {input_file.name}")
                st.code(f"File Size: {len(file_contents)} bytes")
        container = st.sidebar.container()
        with container:
            st.text_area(f"{input_file.name}", file_contents, height=400, key="readonly_textarea", disabled=True)
        run_main()
        download_json()


@st.cache_resource
def run_main():
    with open("main.py", "r") as file:
        file_contents = file.read()
    exec(file_contents)


def download_json():
    st.markdown(
        """
    <style>
    .stBlock {
        flex: 0 0 70% !important;
        max-width: 10% !important;
    },
    .title {
        font-size: 20px;
    }
    </style>
    
    <h1 class="title">Download Json File</h1>
    """,
        unsafe_allow_html=True
    )
    file = "converted.json"

    col1, col2 = st.columns([0.3,1])
    with col1:
        if os.path.isfile(file):
            st.download_button(
                label="Download JSON",
                data=open(file, "rb"),
                file_name=file,
                mime="application/json",
            )
        else:
            st.write("JSON file not found.")
    with col2:
        if st.button("Langflow"):
            url = "http://137.135.90.38:7860/"
            webbrowser.open_new_tab(url=url)

if __name__ == "__main__":
    main()
