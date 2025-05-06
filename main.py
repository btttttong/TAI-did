from multiprocessing import Process
import os
from single_node import start_node
from threading import Thread

NUM_PEERS = 4

def run_peer(port_offset):
    dev_mode = True
    os.environ["PORT_OFFSET"] = str(port_offset)
    start_node(dev_mode)

if __name__ == "__main__":
    processes = []
    for i in range(NUM_PEERS):
        p = Process(target=run_peer, args=(i,))
        p.start()
        processes.append(p)
        is_main_run = True

    for p in processes:
        p.join()
