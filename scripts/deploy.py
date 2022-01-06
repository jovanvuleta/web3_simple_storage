from brownie import FundMe, MockV3Aggregator, accounts, config, network
# from brownie.network.gas.strategies import GasNowStrategy
from web3 import Web3

# from brownie_fund_me.scripts.helpful_scripts import get_account, deploy_mocks

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "hardhat-local"]


def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print('Yessss')
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:
        # deploy_mocks()
        print(f"The active network is {network.show_active()}")
        print("Deploying mocks")
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(
                18,
                Web3.toWei(2000, "ether"),
                {"from": account, "gas_price": 10000000000000, "gas_limit": 30000000, "allow_revert": True}
            )
        print("Mocks Deployed!")
        price_feed_address = MockV3Aggregator[-1].address

    print(f"Price feed address: {price_feed_address}")
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account, "gas_price": 10000000000000, "gas_limit": 30000000, "allow_revert": True},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    # fund_me = FundMe.deploy(
    #     "0x9326BFA02ADD2366b30bacB125260Af641031331",
    #     {"from": account},
    #     publish_source=True
    # )
    print(f"Contract deployed to {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
