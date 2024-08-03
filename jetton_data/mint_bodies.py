from tonsdk.contract.token.ft import JettonMinter, JettonWallet
from tonsdk.contract import Address
from tonsdk.utils import to_nano, bytes_to_b64str
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from client.wallet import wallet_mnemonics, wallet_address
from pytonlib import TonlibClient


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)


def create_jetton_minter():
    minter = JettonMinter(admin_address=Address('EQAE6BbwsJcA88IoIDZEl2Qa0WdC_2PPeZ1wAJ7pAQhCCOjz'),
                          jetton_content_uri='https://raw.githubusercontent.com/yungwine/pyton-lessons/master/lesson-6/token_data.json',
                          jetton_wallet_code_hex=JettonWallet.code)

    return minter


def create_mint_body(jetton_apply: int):
    minter = create_jetton_minter()

    body = minter.create_mint_body(destination=Address('EQAE6BbwsJcA88IoIDZEl2Qa0WdC_2PPeZ1wAJ7pAQhCCOjz'),
                                   jetton_amount=to_nano(int(jetton_apply), 'ton'))
    return body


def create_change_owner_body():
    minter = create_jetton_minter()

    body = minter.create_change_admin_body(
        new_admin_address=Address('EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'))
    return body


def create_burn_body():
    body = JettonWallet().create_burn_body(
        jetton_amount=to_nano(int('burn amount'), 'ton'))
    return body


mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=wallet_mnemonics, version=WalletVersionEnum.v4r2,
                                                          workchain=0)

"""mint tokens"""
body = create_mint_body()
minter = create_jetton_minter()

query = wallet.create_transfer_message(to_addr=minter.address.to_string(),
                                       amount=to_nano(0.04, 'ton'),
                                       seqno=int('wallet seqno'),
                                       payload=body)

"""change owner address"""
body = create_change_owner_body()
minter = create_jetton_minter()

query = wallet.create_transfer_message(to_addr=minter.address.to_string(),
                                       amount=to_nano(0.04, 'ton'),
                                       seqno=int('wallet seqno'),
                                       payload=body)

"""burn tokens"""
body = create_burn_body()

query = wallet.create_transfer_message(to_addr='address of your jetton wallet',
                                       amount=to_nano(0.04, 'ton'),
                                       seqno=int('wallet seqno'),
                                       payload=body)

"""then send boc to blockchain"""
boc = bytes_to_b64str(query["message"].to_boc(False))
