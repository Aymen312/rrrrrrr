import streamlit as st
from transformers import pipeline
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA



from langchain.llms import GooglePalm

llm = GooglePalm(google_api_key=" AIzaSyC0iuHNDRg8wq-mm4ofNsxMLplw4bZNpvo", temperature=0.7)

def main():
    st.title("Analyseur de documents PDF avec Gemini 1.5")

    uploaded_file = st.file_uploader("Choisissez un fichier PDF", type=["pdf"])

    if uploaded_file is not None:
        # Chargement du document PDF
        loader = UnstructuredPDFLoader(uploaded_file)
        documents = loader.load()

        # Division du texte en chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # Encodage des chunks en vecteurs
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_texts(
            [text.page_content for text in texts], 
            embeddings, 
            metadatas=[{"source": text.metadata["source"]} for text in texts]
        )

        # Création de la chaîne de recherche et réponse
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
        )

        # Interface de question-réponse
        query = st.text_input("Posez une question sur le document :")
        if query:
            result = qa.run(query)
            st.write(result)
