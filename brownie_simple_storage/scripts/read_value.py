from brownie import SimpleStorage, accounts, config, network


def read_contract():
    # SimpleStorage is an array
    # To run on rinkeby as default chain doesnt keep history
    # array will be empty
    # print(SimpleStorage[0])

    # contract address variable
    # -1 for most recent deployment
    # 0 for 1st made deployment
    simple_storage = SimpleStorage[-1]


def main():
    read_contract()
