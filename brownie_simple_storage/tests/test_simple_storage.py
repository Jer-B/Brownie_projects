# import required tools
from brownie import SimpleStorage, accounts


# define functions


def test_deploy():
    # testing is separated in 3 categories

    # Arrange -> get everything setup
    # get account to use
    account = accounts[0]

    # Acting -> interact with tools (deploying, transactions etc...)
    # deploy contract
    simple_storage = SimpleStorage.deploy({"from": account})
    # get starting value from retrieve
    starting_value = simple_storage.retrieve()
    # We expect it to be 0
    expect = 0
    # failure test
    # expect =15

    # Assert -> value comparison to check true / false
    assert starting_value == expect


def test_updated():
    # arrange
    # get account
    account = accounts[0]

    # Act
    # deploy
    simple_storage = SimpleStorage.deploy({"from": account})

    # make transaction to value 15
    store_transaction = simple_storage.store(15, {"from": account})
    final_value = simple_storage.retrieve()
    expect = 15

    # assert
    assert final_value == expect

    # Onliy viewable with test -s command
    print("Test Done !")
