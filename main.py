import ollama
import json
import os
from datetime import datetime
from prompts import SYSTEM_PROMPT

client = ollama.Client(host='http://100.65.216.10:11434')

crisis_keywords = [
    'bunuh diri', 'mengakhiri hidup', 'menyakiti diri', 
    'menyayat', 'ingin mati', 'gak sanggup lagi', 
    'tidak sanggup lagi', 'capek hidup', 'pengen hilang'
]

log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)

messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]  # pakai SYSTEM_PROMPT dari prompts.py

print("SAGE siap membantu! (ketik 'exit' untuk keluar)\n")

while True:
    user_input = input("Anda: ")
    if user_input.lower() == 'exit':
        break
    
    detected_crisis = any(keyword in user_input.lower() for keyword in crisis_keywords)
    if detected_crisis:
        print("\n⚠️  [SISTEM: Kata kunci sensitif terdeteksi respons darurat diprioritaskan]\n")
    
    messages.append({'role': 'user', 'content': user_input})
    response = client.chat(model='qwen2.5:3b', messages=messages)
    reply = response['message']['content']
    print("\nSAGE:", reply, "\n")
    messages.append({'role': 'assistant', 'content': reply})

filename = os.path.join(log_folder, f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(messages, f, ensure_ascii=False, indent=2)

print(f"Riwayat percakapan disimpan ke: {filename}")