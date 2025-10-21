from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import json

# .env dosyasını yükle
load_dotenv()

# .env'den anahtarı güvenli şekilde al
GEMINI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

# Eğer lokal embedding kullanıyorsanız True yapın, API ile kullanıyorsanız False
USE_LOCAL_EMBEDDING = False 

def get_embeddings_model():
    """Kullanılacak embedding modelini döndürür."""
    if USE_LOCAL_EMBEDDING:
        # Lokal modeller için gerekli kütüphaneyi içe aktar
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("💡 Lokal Embedding Modeli Kullanılıyor...")
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    else:
        # Gemini API Embeddings
        if not GEMINI_API_KEY:
            raise ValueError("Google Gemini API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin.")
        print("💡 Google Generative AI Embeddings Modeli Kullanılıyor...")
        return GoogleGenerativeAIEmbeddings(
            # Güncel ve önerilen embedding modelini kullan
            model="text-embedding-004", 
            google_api_key=GEMINI_API_KEY 
        )

def build_vector_database(data_path="data/wikipedia_cybersecurity.txt", persist_dir="vector_db"):
    print(f"📖 {data_path} verisi yükleniyor...")
    loader = TextLoader(data_path, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    print(f"📄 Veri {len(docs)} parçaya ayrıldı.")

    meta_path = "data/wikipedia_meta.json"
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

    # Metadata'yı belgelere ekle
    for d in docs:
        d.metadata = d.metadata or {}
        d.metadata["source_title"] = meta.get("title", "Cybersecurity - Wikipedia")
        d.metadata["source_url"] = meta.get("url", "")

    # Embedding modelini al
    embeddings = get_embeddings_model()
    
    # Vektör DB'yi oluştur
    os.makedirs(persist_dir, exist_ok=True)
    db = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_dir) 
    db.persist()
    print("✅ Vektör veritabanı oluşturuldu:", persist_dir)

if __name__ == "__main__":
    if not os.path.exists("data/wikipedia_cybersecurity.txt"):
        print("Veri dosyası bulunamadı. Lütfen önce data_preparation.py dosyasını çalıştırın.")
    else:
        build_vector_database()
