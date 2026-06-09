import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

# Memuat API Key dari file rahasia .env
load_dotenv()
console = Console()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    console.print("[bold red]Error:[/] API Key tidak ditemukan di file .env!")
    sys.exit(1)

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    console.print(f"[bold red]Gagal terhubung ke Gemini API:[/] {e}")
    sys.exit(1)

# Instruksi Utama Robot: Menjadi Guru Bahasa Arab yang Ramah
SYSTEM_PROMPT = """
Anda adalah "Arabic Mahir", seorang kakak tutor virtual yang super ramah, lembut, sabar, dan penuh semangat!
Tugas Anda adalah mengajar Maharah Kalam (Berbicara) yang berfokus pada Sharaf (Perubahan Kata) untuk tingkat Pemula.
Gunakan bahasa Indonesia yang santai dicampur bahasa Arab dasar, penuh emoji, dan suportif.
Ajak pengguna belajar melalui 3 pilihan mode: 1. Percakapan Santai, 2. Games Asah Otak, 3. Tantangan Berbicara.
"""

def print_header():
    console.clear()
    welcome_text = Text()
    welcome_text.append("✨ ARABIC MAHIR ✨\n", style="bold magenta")
    welcome_text.append("Belajar Kalam & Sharaf Seru Bersama Kakak Tutor 📚🎉\n", style="italic cyan")
    console.print(Panel(welcome_text, border_style="magenta", expand=False, justify="center"))

def main():
    print_header()
    console.print("\n[bold yellow]Pilih ruang belajar kita hari ini yuk: [/]")
    console.print("[bold cyan]1.[/] 🗣️ Mode Percakapan Santai")
    console.print("[bold cyan]2.[/] 🧠 Mode Games Asah Otak")
    console.print("[bold cyan]3.[/] 🎭 Mode Tantangan Berbicara")
    
    mode_choice = Prompt.ask("\nMau masuk ke mode nomor berapa?", choices=["1", "2", "3"], default="1")
    
    try:
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
        )
    except Exception as e:
        console.print(f"[bold red]Gagal memulai sesi chat:[/] {e}")
        sys.exit(1)
        
    console.clear()
    print_header()
    console.print(f"\n[bold green]Sistem:[/] Berhasil masuk ke Ruang Belajar! Ketik 'exit' untuk keluar.\n")
    
    with console.status("[bold magenta]Kakak Tutor sedang bersiap... ✨[/]"):
        response = chat.send_message("Halo! Sapa saya dengan ramah sebagai kakak tutor yang ceria dan pakai banyak emoji ya!")
    
    console.print(Panel(response.text, title="✨ Arabic Mahir", border_style="magenta"))
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]Kamu[/]")
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[bold magenta]Arabic Mahir:[/] Sampai jumpa lagi! Belajar yang rajin ya! 👋✨\n")
                break
            if not user_input.strip():
                continue
            with console.status("[bold blue]Kakak Tutor sedang menyimak... 🎧[/]"):
                response = chat.send_message(user_input)
            console.print("\n" + Panel(response.text, title="✨ Arabic Mahir", border_style="magenta"))
        except:
            break

if __name__ == "__main__":
    main()