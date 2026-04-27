import subprocess
import threading
import time

def run_grpc():
    subprocess.run(["python", "grpc_server.py"])

def run_bridge():
    time.sleep(3)
    subprocess.run(["python", "grpc_bridge.py"])

t1 = threading.Thread(target=run_grpc)
t2 = threading.Thread(target=run_bridge)

t1.start()
t2.start()

t1.join()
t2.join()
