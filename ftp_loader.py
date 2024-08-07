import streamlit as st
import ftplib
import os

# Create a session state object to store the user's login status
session_state = st.session_state
if "logged_in" not in session_state:
    session_state.logged_in = False

# Create the login page
def login_page():
    st.title("FTP File Uploader")
    ftp_server = st.text_input("FTP Server Address")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 20px;
            padding: 10px 60px;
            display: block;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Login"):
        try:
            ftp = ftplib.FTP(ftp_server)
            ftp.login(user=username, passwd=password)
            session_state.logged_in = True
            session_state.ftp = ftp
            session_state.username = username
            st.success("Logged in successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Create the upload page
def upload_page():


    with st.sidebar:
        st.write(f"Logged in as: {session_state.username}")
        st.markdown(
        """
        <style>
        .stButton>button:last-child {
            background-color: #FF0000;
            color: white;
            border-radius: 20px;
            padding: 5px 80px;
            display: block;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        
        if st.button("Logout",key="logout-button"):
            session_state.logged_in = False
            session_state.ftp.quit()
            st.success("Logged out successfully!")
            st.rerun()

    st.header("Upload File")
    local_file = st.file_uploader("Select a file to upload",accept_multiple_files=True)
    change_extension = st.checkbox("Change file extension")

    if local_file is None:
        st.error("Please select a file to upload.")

    if change_extension:
        new_extension = st.text_input("Enter the new file extension needed")

    if st.button("Upload",key="upload-button"):
        with st.spinner("Uploading file..."):
            try:
                for local_file in local_files:
                    # Rename the uploaded file with the user's specified extension
                    file_name, old_extension = os.path.splitext(local_file.name)
                    if change_extension:
                        new_file_name = file_name + new_extension
                    else:
                        new_file_name = local_file.name
    
                    ftp = session_state.ftp
                    ftp.storbinary(f"STOR {new_file_name}", local_file)
                    st.success(f"File {new_file_name} uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Display the list of files on the FTP server
    st.subheader("Files on FTP Server")
    files = session_state.ftp.nlst()
    for file in files:
        st.write(file)

    # Allow the user to remove a file from the FTP server
    remove_file = st.checkbox("Remove file from server")
    if remove_file:
        file_to_remove = st.selectbox("Select a file to remove", files)
        if st.button("Remove",disabled=len(files)==0):
            with st.spinner("Removing file..."):
                try:
                    ftp = session_state.ftp
                    ftp.delete(file_to_remove)
                    st.success("File removed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Display the login page or the upload page, depending on the user's login status
if not session_state.logged_in:
    login_page()
else:
    upload_page()
