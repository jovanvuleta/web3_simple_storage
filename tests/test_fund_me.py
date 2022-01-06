from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee, "gas_price": 10000000000, "gas_limit": 30000000})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account, "gas_price": 10000000000, "gas_limit": 30000000})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = '0x15d34aaf54267db7d7c367839aaf71a00a2c6a65'  # Not owner of the contract, address from hardhat
    # fund_me.withdraw({"from": bad_actor, "gas_price": 10000000000, "gas_limit": 30000000})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor, "gas_price": 10000000000, "gas_limit": 30000000})

