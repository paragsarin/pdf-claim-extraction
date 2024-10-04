from langchain.llms import OpenAI
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
from langchain_core.output_parsers import JsonOutputParser
import os
from langchain_core.messages.utils import get_buffer_string
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

 


#Function to extract data from text
def extracted_data(pages_data):

    load_dotenv()
    
    
    template = """
        This is an claim accident report from a customer: {pages}
        ### INSTRUCTION:
        The text is claim accident report from a customer.Your task is to extract the Date Of Claim, Claim Status, Location Address 1 from this data  and return them in JSON format with the following keys: 
       Date Of Claim, Claim Status, Location Address 1.remove any dollar symbols.
        Only return the valid JSON.
        ### VALID JSON:   
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    
    llm=ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")
    chain_extract = prompt_template | llm
    output = chain_extract.invoke(input={"pages": str(pages_data)})
    
    return output


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list):
    
    claims = []
    for filename in user_pdf_list:
        
       
        raw_data=get_pdf_text(filename)
        

        llm_extracted_data=extracted_data(raw_data)
        json_parser = JsonOutputParser()
        res = json_parser.parse(llm_extracted_data.content)
 
        claims.append(res)
        
    return  claims