# Inetrview-Question-creator
Inetrview-Question-creator using Gen AI

### Description:

User upload a pdf file to the ui and it generate the question along with answer in csv file. UI allwoing to donwload csv file.

1. When user uplaod a file then file would be save in static/docs folder
2. If user click on Generate Q&A after uplaoding file then it generate the csv file with question and answer in csv file and save it in static/output folder and for download it would be provided anchor tag for this file with folder location


## How to run:

1. Create an environment

```bash
conda create -n interview python=3.10 -y


conda activate interview

```

2. Activate the environment

```bash
conda activate interview
```


2. install requirements

```bash
pip install -r requirements.txt
```

### Front end
1. Upload the pdf file

```bash
    formData.append('pdf_file', file);
    formData.append('filename', file.name)
    let response = await fetch('/upload', {
        method: "POST",
        body: formData                
    });                
    processUploadResponse(response);  
    });
```
JavaScript snippet that handles a file upload via a POST request to a server endpoint (/upload) and with user input pdf_file and filename and trigger processUploadResponse with our api endpoint response

2. Analyze the pdf file

```bash
    formData.append('pdf_filename', json.pdf_filename)
    fetch('/analyze', {
        method: "POST",
        body: formData                
    }).then(processAnalyzeResponse)
```
JavaScript snippet that handles a analyze file via a POST request to a server endpoint (/analyze) and with user input pdf_filename andand trigger processAnalyzeResponse with our api endpoint response


### Key Learning

1. Document 
```bash
from langchain.docstore.document import Document
```
When working with the langchain library, the Document class from langchain.docstore.document is used to encapsulate text data along with associated metadata. This class is essential for organizing and managing text data, especially when integrating with vector stores and retrieval systems like FAISS.

2. load_summarize_chain
```bash
ques_gen_chain = load_summarize_chain(llm = llm_ques_gen_pipeline, 
                                          chain_type = "refine", 
                                          verbose = True, 
                                          question_prompt=PROMPT_QUESTION, 
                                          refine_prompt=REFINE_PROMPT_QUESTION)
```
The load_summarize_chain function from the langchain library is used to create a summarization chain. In this specific case, we are using it to create a chain for generating questions, with the chain type set to "refine". This means that the chain will refine its output iteratively to improve the final result

2. FAISS
```bash
embeddings = OpenAIEmbeddings()

vector_store = FAISS.from_documents(document_answer_gen, embeddings)
```
FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors.

##### How FAISS Works

Indexing: FAISS creates an index from a set of vectors, allowing for efficient similarity searches. This can involve various algorithms and data structures optimized for different types of queries and data sizes.

Searching: Once the index is built, FAISS can perform similarity searches. Given a query vector, FAISS retrieves the most similar vectors from the index. This is typically done using metrics like cosine similarity or Euclidean distance.

Retrieving: The indices returned by FAISS can be used to fetch the corresponding documents or data points from your dataset.


3. RetrievalQA

```bash
answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen, 
                                               chain_type="stuff", 
                                               retriever=vector_store.as_retriever())
```
##### How It Works Internally
Retriever:

The retriever is responsible for finding and returning relevant documents from the vector store based on the query.
It does this by calculating the similarity between the query embedding and the document embeddings.
Language Model Chain:

The language model chain (in this case, the "stuff" chain) takes the retrieved documents and the original query as input.
The model uses this combined input to generate the final answer.



### website to create the HLD

```img``` contians high level diagram and project structure

https://whimsical.com/my-files-DYKW9Y6C38pZfzhgzMqfrt
