from scripts.helpful_scripts import get_account
from brownie import interface, network, config


def main():
    get_weth()


def get_weth():
    """

    Mints Weth in exchange of deposited eth

    """
    # 1 get the ABI
    # 2 Get weth contract address
    # 3 get_account
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["Weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
