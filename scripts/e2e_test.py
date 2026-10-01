"""End-to-end test of the Store contract on testnet:
1. recipient_1 wallet deposits 0.02 TON (with comment) -> depositCount 1 -> 2
2. owner (treasury) sends "withdraw" -> contract balance sweeps to treasury
Prints evidence at every step.
"""
import asyncio
import os
import sys

from pytoniq import LiteBalancer, WalletV4R2, Address

HERE = os.path.dirname(os.path.abspath(__file__))
STORE_ADDR = "EQA31CWYIcZnBxDlMJUvlLwECP37xZkxYs16Xf4fuGrZoHxd"
TREASURY_MNEMONIC = "E:/Hermes/ton-testnet/secrets/mnemonic.txt"
RECIPIENT_MNEMONIC = "E:/Hermes/ton-testnet/secrets/recipients/recipient_1.txt"


def load_mnemo(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split()


async def get_count(p, addr):
    res = await p.run_get_method(addr, "depositCount", [])
    return int(res[0])


async def acc_state(p, addr):
    st = await p.get_account_state(addr)
    return int(getattr(st, "balance", 0) or 0), getattr(st, "state", "")


async def main() -> None:
    store = Address(STORE_ADDR)
    provider = LiteBalancer.from_testnet_config(trust_level=2)

    async with provider as p:
        print("== initial state ==")
        count0 = await get_count(p, store)
        bal0, _ = await acc_state(p, store)
        print(f"depositCount = {count0}, store balance = {bal0/1e9:.4f} TON")

        # --- 1. deposit from recipient_1 ---
        rec = await WalletV4R2.from_mnemonic(provider=p, mnemonics=load_mnemo(RECIPIENT_MNEMONIC))
        print(f"recipient wallet: {rec.address.to_str()}")
        try:
            await rec.get_seqno()
            print("recipient wallet deployed")
        except Exception:
            print("recipient wallet undeployed -> deploying via external ...")
            await rec.deploy_via_external()
            for _ in range(20):
                await asyncio.sleep(3)
                try:
                    await rec.get_seqno()
                    print("recipient wallet deployed ✓")
                    break
                except Exception:
                    pass
        msg = rec.create_wallet_internal_message(
            destination=store, value=int(0.02 * 1e9),
            body="e2e test deposit", bounce=False)
        await rec.raw_transfer(msgs=[msg])
        print("deposit tx sent (0.02 TON + comment)")

        count1 = count0
        for _ in range(40):
            await asyncio.sleep(3)
            try:
                count1 = await get_count(p, store)
                if count1 > count0:
                    break
            except Exception:
                pass
        bal1, _ = await acc_state(p, store)
        print(f"AFTER DEPOSIT: depositCount = {count1} (was {count0}), store balance = {bal1/1e9:.4f} TON")
        if count1 != count0 + 1:
            print("FAIL: deposit not counted")
            sys.exit(1)
        print("DEPOSIT TEST PASSED ✓")

        # --- 2. owner withdraw ---
        w = await WalletV4R2.from_mnemonic(provider=p, mnemonics=load_mnemo(TREASURY_MNEMONIC))
        assert w.address.to_str() == "EQB6kBT9XIYXvPeZoI5sciyG4YPqT0aCPMU6MIgMvHHvhIp7"
        msg = w.create_wallet_internal_message(
            destination=store, value=int(0.01 * 1e9),
            body="withdraw", bounce=False)
        await w.raw_transfer(msgs=[msg])
        print("withdraw tx sent from owner")

        bal2 = bal1
        for _ in range(40):
            await asyncio.sleep(3)
            bal2, st2 = await acc_state(p, store)
            if bal2 < bal1 - int(0.005 * 1e9):
                break
        print(f"AFTER WITHDRAW: store balance = {bal2/1e9:.4f} TON (was {bal1/1e9:.4f})")
        if bal2 < bal1 - int(0.005 * 1e9):
            print("WITHDRAW TEST PASSED ✓ (swept to owner)")
        else:
            print("withdraw not observed yet — check explorer")
            sys.exit(2)

        count_final = await get_count(p, store)
        print(f"FINAL: depositCount = {count_final}")
        print(f"EXPLORER: https://testnet.tonviewer.com/{STORE_ADDR}")


if __name__ == "__main__":
    asyncio.run(main())
