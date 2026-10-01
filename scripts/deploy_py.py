"""Qubax Store — testnet deploy via pytoniq (liteservers, no API rate limits).

Reads build/store_init.json (address + code/data bocs from the JS bindings),
assembles the StateInit cell, sends the deploy internal message from the
treasury wallet (v4r2), then polls account state + depositCount get-method.

TESTNET ONLY.
"""
import asyncio
import base64
import json
import os
import sys

from pytoniq import LiteBalancer, WalletV4R2, Address
from pytoniq_core import StateInit, Cell

HERE = os.path.dirname(os.path.abspath(__file__))
INIT_JSON = os.path.join(HERE, "..", "build", "store_init.json")
MNEMONIC_PATH = os.path.join(HERE, "..", "..", "ton-testnet", "secrets", "mnemonic.txt")


def load_mnemonic():
    with open(MNEMONIC_PATH, encoding="utf-8") as f:
        return f.read().split()


async def main() -> None:
    with open(INIT_JSON, encoding="utf-8") as f:
        info = json.load(f)
    store_addr = Address(info["address"])

    code_cell = Cell.from_boc(base64.b64decode(info["code"]))[0]
    data_cell = Cell.from_boc(base64.b64decode(info["data"]))[0]
    init_cell = StateInit(code=code_cell, data=data_cell)

    provider = LiteBalancer.from_testnet_config(trust_level=2)
    async with provider as p:
        wallet = await WalletV4R2.from_mnemonic(provider=p, mnemonics=load_mnemonic())
        print("TREASURY :", wallet.address.to_str())

        st = await p.get_account_state(wallet.address)
        balance = int(getattr(st, "balance", 0) or 0)
        print(f"BALANCE  : {balance/1e9:.3f} TON")

        acc = await p.get_account_state(store_addr)
        acc_state = getattr(acc, "state", None)
        print("STORE    :", store_addr.to_str(), f"(state: {acc_state})")

        if acc_state == "active":
            print("Store is ALREADY active.")
        else:
            print("Deploying 0.05 TON + state-init ...")
            if balance < int(0.12 * 1e9):
                print("REFUSED: treasury needs >= 0.12 TON (fund via faucet).")
                sys.exit(1)
            msg = wallet.create_wallet_internal_message(
                destination=store_addr,
                value=int(0.05 * 1e9),
                state_init=init_cell,
                body=None,
                bounce=False,
            )
            await wallet.raw_transfer(msgs=[msg])
            print("Deploy tx SENT.")

        for i in range(40):
            await asyncio.sleep(3)
            try:
                acc = await p.get_account_state(store_addr)
                if getattr(acc, "state", None) == "active":
                    try:
                        res = await p.run_get_method(store_addr, "depositCount", [])
                        print(f"CONFIRMED ACTIVE. depositCount = {res[0]}")
                        print(f"EXPLORER: https://testnet.tonviewer.com/{store_addr.to_str()}")
                        return
                    except Exception as e:
                        print(f"active but get-method not ready ({e}); retrying ...")
            except Exception as e:
                print(f"poll {i}: {e}")
        print("Not confirmed yet — check explorer / rerun.")
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())
