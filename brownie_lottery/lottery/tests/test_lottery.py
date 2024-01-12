from brownie import config, accounts, network, lottery, exceptions
from web3 import Web3

# Price test + entry fee / price = amount eth
def test_entry_fee():
    account = accounts[0]
    print(account)
    print("Deploying contract")
    _lottery = lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    print("Deployed")
    assert _lottery.getEntranceFee() > Web3.toWei(0.001, "ether")
    assert _lottery.getEntranceFee() < Web3.toWei(0.1, "ether")
