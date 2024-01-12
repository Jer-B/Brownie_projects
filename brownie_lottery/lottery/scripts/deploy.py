from brownie import config, accounts, lottery, network, MockV3Aggregator
import web3
from scripts.helpful_scripts import (
    get_account,
    verify_contracts,
    mock_v3_deploy,
    LOCAL_BLOCKCHAINS_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
    get_contract,
)

# --------------
# Modification following refactoring
# --------------
# 1: add web3
# 2: after being done with mock function in helpful, import mock_v3_deploy from helpful
# 3: now can delete web3 as it is imported in helpful
# from web3 import Web3


def lottery_deploy():
    # get account from brownie list
    account = get_account(id="test_wallet")

    contract_deploy = lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery

    # print("get sender account...")
    # print("check chain...")
    # # deploy the contract lottery from our wallets as sender
    # # -----------------------
    # if network.show_active() not in LOCAL_BLOCKCHAINS_ENVIRONMENTS:
    #     price_feed_address = config["networks"][network.show_active()][
    #         "eth_usd_price_feed"
    #     ]
    #     print(network.show_active(), " network detected, grabbing price feed...")
    # else:
    #     print("Development chain detected...")
    #     if len(MockV3Aggregator) <= 0:
    #         print("no mock detected, create deployment for it...")

    #         mock_v3_deploy()
    #     print("Found a mock, grabbing the last one deployed...")
    #     price_feed_address = MockV3Aggregator[-1].address
    #     print(f"Price feed result:{price_feed_address}")

    # lottery_deploying = lottery.deploy(
    #     price_feed_address,
    #     {"from": account},
    #     publish_source=config["networks"][network.show_active()].get("verify"),
    # )
    # print("Contract Deployed")
    # return lottery_deploying


# get different account depending of the network
# !!grab it from helpful_scripts.py!!
# def get_account():
#    if network.show_active() == "development":
#        return accounts[0]
#    else:
#        return accounts.add(config["wallets"]["from_key"])


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    # then end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    lottery_deploy()
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
