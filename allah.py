import streamlit as st
from transformers import pipeline
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings  # Or another embedding provider
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

from langchain.llms import GooglePalm

# Your Google Cloud API key
google_api_key = "AIzaSyC0iuHNDRg8wq-mm4ofNsxMLplw4bZNpvo"  # Replace with your actual key
llm = GooglePalm(google_api_key=google_api_key, temperature=0.7)

def main():
    st.title("Analyseur de documents PDF avec Gemini 1.5")

    uploaded_file = st.file_uploader("Choisissez un fichier PDF", type=["pdf"])

    if uploaded_file is not None:
        # Load the PDF document
        loader = UnstructuredPDFLoader(uploaded_file)
        documents = loader.load()

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # Embed the chunks using OpenAI embeddings or another provider
        embeddings = OpenAIEmbeddings()  # Or use another embedding provider
        vectorstore = Chroma.from_texts(
            [text.page_content for text in texts], 
            embeddings, 
            metadatas=[{"source": text.metadata["source"]} for text in texts]
        )

        # Create the RetrievalQA chain
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
        )

        # Question-answering interface
        query = st.text_input("Posez une question sur le document :")
        if query:
            result = qa.run(query)
            st.write(result)

if __name__ == "__main__":
    main()
