import subprocess
import threading

def run_process():
    subprocess.run(['python', './secondary_thread'])  # Specify the script path

def run_server():
    subprocess.run(['python', '../Server/allert_server.py'])  # Specify the script path

if __name__ == "__main__":
    thread = threading.Thread(target=run_process)
    thread.start()
    thread2 = threading.Thread(target=run_server)
    thread2.start()
    thread.join()  # Wait for the thread to finish
    
    thread2.join()  # Wait for the thread to finish