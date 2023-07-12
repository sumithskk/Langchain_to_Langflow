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
                st.write("")
                st.write("")
                st.code(f"File Name: {input_file.name}")
                st.code(f"File Size: {len(file_contents)} bytes")
        container = st.sidebar.container()
        with container:
            st.text_area(
                f"{input_file.name}",
                file_contents,
                height=400,
                key="readonly_textarea",
                disabled=True,
            )
        run_main()
        download_json()



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
        font-size: 10px;
    }
    </style>

    <h2 class="title">Download Json File</h2>
    """,
        unsafe_allow_html=True,
    )
    file = "converted.json"

    col1, col2 = st.columns([0.3, 1])
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
        url = "http://137.135.90.38:7860/"
        st.markdown(
            f"""
        <a href={url}><button style="display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 500;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    color: white;
    width: auto;
    user-select: none;
    background-color: rgb(19, 23, 32);
    border: 1px solid rgba(250, 250, 250, 0.2);;">Langflow</button></a>
        """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()