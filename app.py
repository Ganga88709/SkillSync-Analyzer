from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai
import os
import io
import base64 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
            images=pdf2image.convert_from_bytes(uploaded_file.read())
            first_page=images[0]
            img_byte_arr=io.BytesIO()
            first_page.save(img_byte_arr,format='JPEG')
            img_byte_arr=img_byte_arr.getvalue()
            pdf_parts=[
                {
                    "mime_type":"image/jpeg",
                    "data":base64.b64encode(img_byte_arr).decode()
                }
            ]
            return pdf_parts
    else:
        raise FileNotFoundError("File not uploaded")
st.set_page_config(page_title="ATS Application")
st.header("SkillSync Analyzer")
input_text=st.text_area("Job Description:",key="input")
uploaded_file=st.file_uploader("Upload your file(PDF)..",type=["pdf"])
submit1=st.button("Tell me about my resume")
        #submit2=st.button("How can I impovise my skills")
submit2=st.button("Percentage match")

if uploaded_file is not None:
        st.write("File Uploaded Successfully")
        prompt1="""
            You are an experienced Technical Human Resource Manager in the field of Data Science,Full Stack,Big Data Engineering,Devops
            .Your task is to review the provided resume againist the job description.
            Please share your professional evolution on whether the candidate's profile aligns
            with the role.Highlights strengths and weaknesses of the applicant to the specified job description
            """
        prompt2="""
            you are a skilled ATS(Applicant Tracking System) scanner with a deep understanding
            of Data Science,Full Stack,Big Data Engineering,Devops and deep ATS functionality,
            your task is to evaluate the resume againist the provided job description.
            give me the percentage match if the resume match with the job description.First the output 
            should come as percentage and then keywords missing in that resume
            """
        if submit1:
            if uploaded_file is not None:
                 pdf_content=input_pdf_setup(uploaded_file)
                 response=get_gemini_response(prompt1,pdf_content,input_text)
                 st.subheader("The Response is:")
                 st.write(response)
            else:
                 st.write("Please upload the resume")
        if submit2:
            if uploaded_file is not None:
                 pdf_content=input_pdf_setup(uploaded_file)
                 response=get_gemini_response(prompt2,pdf_content,input_text)
                 st.subheader("The Response is:")
                 st.write(response)
            else:
                 st.write("Please upload the resume")
        
    
             
                   
     

