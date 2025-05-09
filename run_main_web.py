from webapp.app import MainWeb
from single_node import BlockchainCommunity


def start_main_web():

    web = MainWeb(port=5050)
    web.start()

if __name__ == "__main__":
    start_main_web()