import wikipedia
import re
import os
import json

def clean_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)           # fazla yeni satırları azalt
    text = re.sub(r'\[[0-9]+\]', '', text)      # referans numaralarını sil
    return text.strip()

def get_wikipedia_page(topic: str = "Cybersecurity", save_path: str = "data/wikipedia_cybersecurity.txt"):
    os.makedirs("data", exist_ok=True)
    try:
        page = wikipedia.page(topic, auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        # Eğer disambiguation çıkarsa ilk seçeneği alıyoruz
        choice = e.options[0]
        page = wikipedia.page(choice, auto_suggest=False)

    content = clean_text(page.content)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(content)

    meta = {"title": page.title, "url": page.url}
    # metadata dosyası 
    with open("data/wikipedia_meta.json", "w", encoding="utf-8") as mf:
        json.dump(meta, mf, ensure_ascii=False, indent=2)

    print(f"✅ Wikipedia verisi kaydedildi: {save_path}")
    print(f"🔗 Sayfa: {page.url}")
    return save_path, meta

if __name__ == "__main__":
    get_wikipedia_page("Cybersecurity")
