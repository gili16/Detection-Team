import subprocess
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_process():
    subprocess.run(['python', 'Thread/secondary_thread.py'])  # Specify the script path

def run_server():
    subprocess.run(['python', 'Server/allert_server.py'])  # Specify the script path

if __name__ == "__main__":
    try:
        thread = threading.Thread(target=run_process)
        thread.start()
        thread2 = threading.Thread(target=run_server)
        thread2.start()
        thread.join()  # Wait for the thread to finish
        
        thread2.join()  # Wait for the thread to finish
    except KeyboardInterrupt:
        thread._stop()
        thread2._stop()