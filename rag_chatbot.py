from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# .env'den anahtarı güvenli şekilde al
GEMINI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

# build_vector_db.py dosyanızdaki ayarla uyumlu olmalıdır!
USE_LOCAL_EMBEDDING = False 

def get_embeddings_model():
    """Kullanılacak embedding modelini döndürür."""
    if USE_LOCAL_EMBEDDING:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    else:
        if not GEMINI_API_KEY:
            raise ValueError("Google Gemini API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin.")
        # Güncel ve önerilen embedding modelini kullan
        return GoogleGenerativeAIEmbeddings(
            model="text-embedding-004", 
            google_api_key=GEMINI_API_KEY
        )

def run_chatbot():
    # Embedding modelini tanımla
    embeddings = get_embeddings_model()
    
    # Hata Çözümü: Chroma yüklenirken embedding fonksiyonu belirtilmeli!
    db = Chroma(
        persist_directory="vector_db",
        embedding_function=embeddings 
    )
    retriever = db.as_retriever(search_kwargs={"k": 3})

    if not GEMINI_API_KEY:
         raise ValueError("Google Gemini API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin.")

    # LLM modeli (Güncel model)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=GEMINI_API_KEY 
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    print("💬 Cybersecurity RAG Chatbot hazır! (Çıkmak için 'quit' yaz.)")

    while True:
        query = input("\nSoru: ").strip()
        if not query:
            continue
        if query.lower() == "quit":
            break

        try:
            print("⏳ Cevap aranıyor...")
            output = qa({"query": query})
            answer = output["result"]
            docs = output.get("source_documents", [])

            print("\n--- Cevap ---")
            print(answer)
            print("\n--- Kaynaklar (snippet + url) ---")
            for i, d in enumerate(docs):
                txt = d.page_content
                snippet = txt[:350].replace("\n", " ") + ("..." if len(txt) > 350 else "")
                url = d.metadata.get("source_url", "")
                title = d.metadata.get("source_title", "")
                print(f"\n[{i+1}] {title} {(' - ' + url) if url else ''}\n{snippet}")
        except Exception as e:
            print(f"Hata oluştu: {e}")
            print("Lütfen API anahtarınızın doğru olduğundan ve veritabanınızın oluşturulduğundan emin olun.")

if __name__ == "__main__":
    run_chatbot()
