import streamlit as st
import os

def render_docs_module(df, upload_dir):
    st.subheader("📸 Field Inspection Photos & Milestone Documentation")
    
    selected_site = st.selectbox(
        "Select Target Site:", 
        options=df['Site ID'] + " - " + df['Name']
    )
    
    site_id = selected_site.split(" - ")[0]
    site_folder = os.path.join(upload_dir, site_id)
    os.makedirs(site_folder, exist_ok=True)

    col_upload, col_gallery = st.columns([1, 2])

    with col_upload:
        st.markdown(f"#### Upload Files for `{site_id}`")
        uploaded_files = st.file_uploader(
            "Choose Inspection Images or PDFs", 
            type=["png", "jpg", "jpeg", "pdf"], 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(site_folder, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success(f"Successfully saved {len(uploaded_files)} file(s) for {site_id}!")

    with col_gallery:
        st.markdown(f"#### Uploaded Document Gallery (`{site_id}`)")
        files_in_folder = os.listdir(site_folder)
        
        if files_in_folder:
            for file_name in files_in_folder:
                file_path = os.path.join(site_folder, file_name)
                ext = file_name.split(".")[-1].lower()
                
                if ext in ["png", "jpg", "jpeg"]:
                    st.image(file_path, caption=file_name, use_container_width=True)
                else:
                    st.info(f"📄 Document Attached: `{file_name}`")
        else:
            st.caption("No photos or documents uploaded yet for this site.")
