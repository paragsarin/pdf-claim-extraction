import streamlit as st
from dotenv import load_dotenv
from utils import *


def main():
    load_dotenv()

    st.set_page_config(page_title="Claim data Extraction Bot")
    st.title("Claim data Extraction Bot...💁 ")
    st.subheader("I can help you in extracting invoice data")


    # Upload the Invoices (pdf files)
    pdf = st.file_uploader("Upload claim forms here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)

    submit=st.button("Extract Data")

    if submit:
        with st.spinner('Wait for it...'):
            claims=create_docs(pdf)
            for claim in claims:
                 st.markdown("<b>Date Of Claim - </b>"+claim["Date Of Claim"], unsafe_allow_html=True)
                 st.markdown("<b>Claim Status - </b>"+claim["Claim Status"], unsafe_allow_html=True)
                 st.markdown("<b>Location - </b>"+claim["Location Address 1"], unsafe_allow_html=True)
                 st.write("------------------------------------------------------------------------------------------------")
         
            
        st.success("Hope I was able to save your time❤️")


#Invoking main function
if __name__ == '__main__':
    main()
