import asyncio

from pathlib import Path
import requests
from pytonlib import TonlibClient
from tonsdk.utils import to_nano

from client.jetton_data.mint_bodies import create_jetton_minter
from client.wallet import wallet, wallet_address


async def get_client():
    url = 'https://ton.org/testnet-global.config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=2, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_seqno(client: TonlibClient, address: str):
    data = await client.raw_run_method(method='seqno', stack_data=[], address=address)
    return int(data['stack'][0][1], 16)



async def deploy_minter():
    minter = create_jetton_minter()

    client = await get_client()
    seqno = await get_seqno(client, wallet_address)

    collection_state_init = minter.create_state_init()['state_init']

    query = wallet.create_transfer_message(to_addr=minter.address.to_string(),
                                           amount=to_nano(0.02, 'ton'),
                                           state_init=collection_state_init,
                                           seqno=int(seqno))

    await client.raw_send_message(query['message'].to_boc(False))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(deploy_minter())
