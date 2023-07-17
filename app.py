import io
import os
import streamlit as st


def redirect_to_url(url):
    js = f"window.location.href='{url}'"
    html = f"<script>{js}</script>"
    st.markdown(html, unsafe_allow_html=True)


def create_ip_file(datafiles):
    if datafiles:
        for datafile in datafiles:
            if datafile is not None:
                file_path = os.path.join("inputs", f"{datafile.name}")
                with open(file_path, "wb") as f:
                    f.write(datafile.read())


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
    os.makedirs('inputs', exist_ok=True)
    # input
    # key = str(uuid.uuid4())
    key = 0

    #
    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>',
    #          unsafe_allow_html=True)
    # st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>',
    #          unsafe_allow_html=True)

    anyinput = st.radio("Any input files for Langchain Code",
                        ("No", "Yes"))

    left_column, right_column = st.columns(2)

    with left_column:
        input_file = st.file_uploader("Upload Your Langchain File", type="py")

    # if anyinput == 'Yes':
    #     with right_column:
    #         datafiles = st.file_uploader('Upload additional input files ',
    #                                      accept_multiple_files=True)
    #         #create_ip_file(datafiles)

    if anyinput == 'No':
        if input_file is not None:
            run_all_file(input_file)
    elif anyinput == 'Yes':
        with right_column:
            datafiles = st.file_uploader('Upload additional input files ',
                                         accept_multiple_files=True)
        if len(datafiles) != 0:
            create_ip_file(datafiles)
            run_all_file(input_file)
    #
    # if input_file is not None:
    #     if (anyinput == 'Yes') and (len(datafiles)!=0):
    #         create_ip_file(datafiles)
    #         run_all_file(input_file)
    #     elif anyinput == 'No':
    #         run_all_file(input_file)


def run_all_file(input_file):
    with io.TextIOWrapper(input_file, encoding="utf-8", newline="") as file_wrapper:
        file_contents = file_wrapper.read()

    # Create a new file with the same contents
    with open("qwerty1234567890.py", "w", newline="") as new_file:
        new_file.write(file_contents)
        # with right_column:
        #     st.write("")
        #     st.write("")
        #     st.code(f"File Name: {input_file.name}")
        #     st.code(f"File Size: {len(file_contents)} bytes")
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


# @st.cache_resource
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
