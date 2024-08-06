import streamlit as st
import ftplib
import os

# Create the UI
st.title("FTP File Uploader")
ftp_server = st.text_input("FTP Server Address")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
local_file = st.file_uploader("Select a file to upload")
change_extension = st.checkbox("Change file extension")

if local_file is None:
    st.error("Please select a file to upload.")

if change_extension:
    new_extension = st.text_input("Enter the new file extension needed")

# Connect to the FTP server and upload the file
if st.button("Upload"):
    with st.spinner("Uploading file..."):
        try:
            # Rename the uploaded file with the user's specified extension
            file_name, old_extension = os.path.splitext(local_file.name)
            if change_extension:
                new_file_name = file_name + new_extension
            else:
                new_file_name = local_file.name

            ftp = ftplib.FTP(ftp_server)
            ftp.login(user=username, passwd=password)
            ftp.storbinary(f"STOR {new_file_name}", local_file)
            st.success("File uploaded successfully!")

            # List the files in the FTP server's current directory
            files = ftp.nlst()
            st.write("Files in the FTP server's current directory:")
            for file in files:
                st.write(file)
        except Exception as e:
            st.error(f"Error: {str(e)}")
