import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv 
import os

load_dotenv() # .env dosyasını yükle

# .env'den anahtarı güvenli şekilde al
GEMINI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

# build_vector_db.py dosyanızdaki ayarla uyumlu olmalıdır!
USE_LOCAL_EMBEDDING = False 

def get_embeddings_model(api_key):
    """Kullanılacak embedding modelini döndürür."""
    if USE_LOCAL_EMBEDDING:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    else:
        # Güncel ve önerilen embedding modelini kullan
        return GoogleGenerativeAIEmbeddings(
            model="text-embedding-004", 
            google_api_key=api_key
        )

st.set_page_config(page_title="Cybersecurity RAG Chatbot", layout="centered")
st.title("🤖 Cybersecurity RAG Chatbot")
st.write("Wikipedia'dan alınmış 'Cybersecurity' içeriği ile desteklenen soru-cevap sistemi.")

if not GEMINI_API_KEY:
    st.error("Google Gemini API anahtarı `.env` dosyasından yüklenemedi. Lütfen kontrol edin (Değişken adı: GOOGLE_GENAI_API_KEY).")
elif not os.path.exists("vector_db"):
    st.warning("Vektör veritabanı bulunamadı. Lütfen önce `data_preparation.py` ve ardından `build_vector_db.py` dosyalarını çalıştırın.")
else:
    try:
        # 1. Embedding modelini oluştur
        embeddings = get_embeddings_model(GEMINI_API_KEY)

        # 2. Chroma yüklenirken embedding fonksiyonu belirtilmeli!
        db = Chroma(
            persist_directory="vector_db",
            embedding_function=embeddings 
        )
        retriever = db.as_retriever(search_kwargs={"k": 3})

        # LLM modelini oluştur (Daha yetenekli Gemini modelini kullandık)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", # Güncel LLM modeli
            google_api_key=GEMINI_API_KEY 
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

        # Streamlit Arayüzü
        question = st.text_input("Sorunu yaz ve Enter'a bas veya 'Gönder' butonuna tıkla:")
        if st.button("Gönder") and question:
            with st.spinner("Cevap aranıyor..."):
                output = qa({"query": question})
                answer = output["result"]
                sources = output.get("source_documents", [])

            st.markdown("### ✅ Cevap")
            st.write(answer)

            st.markdown("### 📚 Kullanılan Kaynaklar")
            for i, d in enumerate(sources):
                snippet = d.page_content[:400].replace("\n", " ") + ("..." if len(d.page_content) > 400 else "")
                url = d.metadata.get("source_url", "")
                title = d.metadata.get("source_title", "Wikipedia")
                st.write(f"**[{i+1}] {title}** | {url}")
                st.code(snippet, language='text')
    except Exception as e:
        st.error(f"Uygulama başlatılırken bir hata oluştu: {e}")
        st.error("Lütfen API anahtarınızın geçerli olduğundan ve tüm bağımlılıkların yüklü olduğundan emin olun.")
