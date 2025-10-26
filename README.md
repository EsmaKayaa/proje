🚀 Akbank GenAI Bootcamp: Cybersecurity RAG Chatbot

Bu proje, Akbank GenAI Bootcamp: Yeni Nesil Proje Kampı kapsamında geliştirilmiştir.
Amaç, Retrieval-Augmented Generation (RAG) mimarisini kullanarak “Cybersecurity” (Siber Güvenlik) konulu bir akıllı chatbot oluşturmaktır.
Chatbot, Wikipedia’dan alınan içerikleri temel alarak, kullanıcıların siber güvenlik ile ilgili sorularına doğru, kaynaklı ve doğal dilde cevaplar verir.

🎯 Projenin Amacı

Günümüzde siber güvenlik hem bireyler hem kurumlar için kritik öneme sahip bir konudur.
Ancak bu konuda hızlı ve doğru bilgiye ulaşmak çoğu zaman zordur.
Bu proje ile amaçlanan:

Wikipedia’dan alınan siber güvenlik içeriğini kullanarak,

Google Gemini API destekli,

RAG (Retrieval-Augmented Generation) temelli bir chatbot geliştirmek,

Ve bu chatbotu hem web arayüzü (Streamlit) hem de terminal (CLI) üzerinden erişilebilir hale getirmektir.

📚 Veri Seti Hakkında

Bu projede kullanılan veri seti, Wikipedia üzerinden alınmıştır.
Veri toplama süreci data_preparation.py dosyasında otomatik olarak gerçekleştirilmiştir.

📄 Veri Hazırlama Süreci

Wikipedia kütüphanesi kullanılarak “Cybersecurity” başlıklı sayfa indirildi.

Gereksiz karakterler, referans numaraları ve fazla satır boşlukları temizlendi.

Temizlenen içerik data/wikipedia_cybersecurity.txt dosyasına kaydedildi.

Sayfa başlığı ve URL bilgisi data/wikipedia_meta.json içinde saklandı.

Örnek meta verisi:

{
  "title": "Cybersecurity",
  "url": "https://en.wikipedia.org/wiki/Cybersecurity"
}

🧠 Kullanılan Yöntemler ve Teknolojiler

Teknoloji                           Kullanım Amacı

LangChain	                          RAG zinciri oluşturma, belge işleme
Chroma	                            Vektör veritabanı (embedding saklama)
Google Gemini API (Generative AI)	  Embedding & LLM yanıt üretimi
Wikipedia API                     	Veri kaynağı
Streamlit	                          Web arayüzü
Python-dotenv	                      API anahtarı yönetimi

🔍 RAG Mimarisi

Retrieval-Augmented Generation (RAG) modeli iki temel aşamadan oluşur:

Retriever (Bilgi Getirici): Kullanıcının sorusuna en uygun belge parçalarını Chroma vektör veritabanı içinden bulur.

Generator (Cevap Üretici): Bulunan belgeleri Google Gemini modeline aktararak, anlamlı ve doğal bir cevap üretir.

Akış Diyagramı:

Soru --> Retriever (Chroma DB) --> İlgili Belgeler --> LLM (Gemini) --> Cevap + Kaynak

🧩 Çözüm Mimarisi

Proje 4 ana bileşenden oluşur:

Dosya	Açıklama
data_preparation.py	   Wikipedia’dan veriyi çeker, temizler ve kaydeder.
build_vector_db.py	   Metinleri böler, embedding uygular ve Chroma DB oluşturur.
cli_chatbot.py	       Terminal tabanlı sohbet arayüzü.
app.py	               Streamlit tabanlı web arayüzü.

Genel Yapı:

cybersecurity-rag-chatbot/
│
├── data/
│   ├── wikipedia_cybersecurity.txt
│   ├── wikipedia_meta.json
│
├── vector_db/
│
├── app.py
├── cli_chatbot.py
├── build_vector_db.py
├── data_preparation.py
├── .env
├── requirements.txt
└── README.md

⚙️ Kodun Çalışma Kılavuzu
1️⃣ Ortam Kurulumu
git clone https://github.com/EsmaKayaa/cybersecurity-rag-chatbot.git
cd cybersecurity-rag-chatbot

2️⃣ Sanal Ortam (Virtual Env) Kurulumu
python -m venv venv
source venv/bin/activate     # (Mac/Linux)
# venv\Scripts\activate      # (Windows)

3️⃣ Gerekli Kütüphaneleri Yükle

requirements.txt içeriği:

langchain
langchain_community
langchain-google-genai
chromadb
wikipedia
streamlit
python-dotenv


Komut:

pip install -r requirements.txt

4️⃣ .env Dosyasını Hazırla

.env dosyası oluşturun ve içine Google Gemini API anahtarını ekleyin:

GOOGLE_GENAI_API_KEY=senin_gemini_api_anahtarın


API anahtarı almak için: Google AI Studio - API Keys

💻 Çalıştırma Adımları
Adım 1. Wikipedia Verisini Çek
python data_preparation.py

Adım 2. Vektör Veritabanını Oluştur
python build_vector_db.py

Adım 3. Chatbot’u Başlat
a) Terminal Versiyonu
python cli_chatbot.py

b) Web Arayüzü (Streamlit)
streamlit run app.py


Ardından tarayıcıda açın: http://localhost:8501

🌐 Web Arayüzü & Product Kılavuzu
🧭 Akış

Streamlit arayüzü sade ve sezgisel bir deneyim sunar:

“Sorunu yaz” kutusuna metninizi girin.

“Gönder” butonuna tıklayın.

Model, Wikipedia veritabanını tarar ve yanıtı üretir.

Cevap ekrana yazılır, altında kaynak linkleri görüntülenir.

🖼️ Ekran Görünümü (Örnek)
🤖 Cybersecurity RAG Chatbot
-----------------------------------------
Soru: What is a DDoS attack?

✅ Cevap: A DDoS (Distributed Denial of Service) attack is a cyber attack ...
📚 Kaynak: Cybersecurity - Wikipedia

🧾 Web Linki (Deploy)

Local URL: http://localhost:8501
  Network URL: http://192.168.1.17:8501

🔍 Elde Edilen Sonuçlar Özet

RAG mimarisiyle çalışan bir chatbot başarıyla oluşturulmuştur.

Model, Wikipedia verilerinden doğru ve kaynaklı yanıtlar üretmektedir.

Hem terminal hem web ortamında etkileşimli çalışmaktadır.

Gemini 2.5 Flash modeli hızlı, doğal ve açıklayıcı cevaplar üretmiştir.

Örnek Soru-Cevap:

❓ Soru: What are common types of cyber attacks?
💬 Cevap: Common cyber attacks include phishing, malware, ransomware, DDoS attacks, and man-in-the-middle attacks.
📚 Kaynak: Cybersecurity - Wikipedia

🧑‍💻 Geliştirici Notu

Bu proje, LangChain ve Google Gemini API kullanılarak modern bir RAG sisteminin sıfırdan nasıl kurulabileceğini göstermektedir.
Hedef; açık kaynaklı verilerle çalışan, kullanıcıya kaynaklı ve güvenilir yanıtlar sunan bir yapay zekâ chatbotu geliştirmektir.

🏁 Lisans

Bu proje eğitim amaçlı olarak geliştirilmiştir.
Açık kaynaklıdır; üzerinde değişiklik yapılabilir, geliştirilebilir ve paylaşılabilir.

📎 İletişim

 E-posta: esmkyaa1@gmail.com
 
 GitHub: https://github.com/EsmaKayaa
 
 LinkedIn: https://www.linkedin.com/in/esma-kaya-6a811b335/


