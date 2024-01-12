# First put in place functions logic
# import accounts from brownie to use wallets.
# add config to take informations from yaml file
# import contract
from brownie import accounts, config, SimpleStorage, network

# add env variable for accounts method 2
# import os


def deploy_simple_storage():

    # 1 when both def are empty-> pass
    # pass
    # 2 put in place a brownie account from default ganach blockchain
    # account = accounts[0]
    # print(account)
    # 3 add own wallet to brownie + private key, brownie is password encrypted, safest security
    # account = accounts.load("test_wallet")
    # print(account)
    # 4 third way to add an account is by environment variables
    # using .env files and brownie-config.yaml files and os
    # account = accounts.add(os.getenv("private_key"))
    # print(account)
    # 5 from yaml file
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    # 6 get accounts depending on the used network
    account = get_account()
    print(account)

    # deploy SimpleStorage.sol
    # as it returns an object and brownie smart enough to know
    # wether it needs to make a state change (transact) or need to read (call)
    # so we can put it into a variable

    simple_storage = SimpleStorage.deploy({"from": account})
    print("Deploy: ", simple_storage)

    # retrieve a value from the retrieve function of the contract
    stored_value = simple_storage.retrieve()
    print("Initial Stored Value: ", stored_value)
    # should return 0 at the moment

    # make a transaction to store a value into the store function
    # as it makes a transaction, specify from where (which wallet)
    # store value 15
    store_transaction = simple_storage.store(15, {"from": account})
    store_transaction.wait(1)
    # wait couple blocks for confirmation like in web3.py
    # check
    # updated stored value
    updated_stored_value = simple_storage.retrieve()
    print("updated value: ", updated_stored_value)


# to avoid repeated and useless accounts management depending on a network lets do a conditional function
def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
