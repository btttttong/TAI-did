from multiprocessing import Process
import os
from single_node import start_node
from threading import Thread

NUM_PEERS = 4

def run_peer(port_offset):
    dev_mode = True
    os.environ["PORT_OFFSET"] = str(port_offset)
    web_port = 8080 + port_offset
    start_node(node_id=port_offset, developer_mode=dev_mode, web_port=web_port)

if __name__ == "__main__":
    processes = []
    for i in range(NUM_PEERS):
        p = Process(target=run_peer, args=(i,))
        p.start()
        processes.append(p)
        is_main_run = True

    for p in processes:
        p.join()
