import os
from langchain_community.llms import Ollama
import torch
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings

ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
DB_DIR: str = os.path.join(ABS_PATH, "dburl")
# EMBEDDING = OllamaEmbeddings(model="llama3")


def model_res_generator(model, messages, llm_model):
    if torch.cuda.is_available():
        # Set the global PyTorch device to GPU
        device = torch.device("cuda")
        #torch.set_default_tensor_type("torch.cuda.FloatTensor")
    else:
        # Use CPU if no GPU available
        device = torch.device("cpu")

    # response = model.predict(messages)
    EMBEDDING = OllamaEmbeddings(model=llm_model)
    vectordb = Chroma(persist_directory=f"{DB_DIR}_{llm_model}", embedding_function=EMBEDDING)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever)
    response = qa(messages)

    return response

def run_analysis(job_description, llm_model):
    prompt = """

    ================================================================================
    - Remove all HTML elements.
    - If the job description above is not in English, DO NOT ANALYSE IT, just return the Verdict as "Not suitable". Skip creating cover letter and resume.
    - If the job description is in English, then do the following:
        - Assume the role of expert prompt engineer, expert career coach, expert data analyst.
        - Analyze the compatibility between the skills in the database and the job descriptions.
        - Judge if the job is suitable based on the skills.
    
    The output you give should be as below:
    Language of the job: State which language the job is posted in.
    Verdict: Either suitable or not suitable
    Skills needed: List the skills needed to be successful at the job
    Reason: The reasons why it is suitable or not suitable
    Improvement: Based on the available skills, suggest what the candidate can do to improve the chance of getting the job.
    """




    if job_description != "":
        
        # Use a llama3 llm from Ollama
        # llm = Ollama(model="llama3")
        llm = Ollama(model=llm_model)

        full_prompt = f"job description:\n{job_description}\n\n \n\n {prompt}"
        messages = model_res_generator(llm, full_prompt, llm_model)

        return messages

def main():
    run_analysis("", "")


if __name__ == '__main__':
    main()