/**
 * Qubax Store — testnet deploy of the Store contract.
 *
 * Uses the EXISTING treasury mnemonic from E:/Hermes/ton-testnet/secrets/
 * (same key pair => same WalletV4R2 address as the pytoniq side).
 * TESTNET ONLY.
 */
import { readFileSync } from 'fs';
import * as path from 'path';
import * as fs from 'fs';

import {
  Address, Cell, beginCell, toNano, contractAddress, StateInit,
} from '@ton/core';
import { TonClient, WalletContractV4, internal } from '@ton/ton';
import { mnemonicToPrivateKey } from '@ton/crypto';
import { Store } from '../build/store_Store.ts';

const TREASURY_SECRETS = 'E:/Hermes/ton-testnet/secrets';

function loadMnemonic(): string[] {
  return readFileSync(path.join(TREASURY_SECRETS, 'mnemonic.txt'), 'utf-8').trim().split(/\s+/);
}

async function main() {
  const client = new TonClient({
    endpoint: 'https://testnet.toncenter.com/api/v2/jsonRPC',
  });

  // 1. Treasury wallet (v4r2, default wallet_id 698983191 — matches pytoniq)
  const key = await mnemonicToPrivateKey(loadMnemonic());
  const wallet = WalletContractV4.create({ workchain: 0, publicKey: key.publicKey });
  const walletAddr = wallet.address.toString({ urlSafe: true });
  console.log('TREASURY :', walletAddr);

  const w = client.open(wallet);
  const seqno = await w.getSeqno();
  const balance = await w.getBalance();
  console.log('SEQNO    :', seqno, ' BALANCE_NANO:', balance.toString());

  // 2. Build Store init (owner = treasury)
  const store = Store.fromInit(wallet.address);
  const storeInit = store.init!;
  const storeAddr = contractAddress(0, storeInit);
  console.log('STORE    :', storeAddr.toString({ urlSafe: true }));

  const already = await client.getContractState(storeAddr);
  console.log('STORE STATE:', ['uninit', 'active', 'frozen'][already.state] ?? already.state);

  if (already.state === 1) {
    const opened = client.open(store);
    try {
      const count = await opened.getDepositCount();
      console.log('ALREADY DEPLOYED. depositCount =', count.toString());
      return;
    } catch { /* fall through to deploy */ }
  }

  if (balance < toNano('0.1')) {
    console.error('REFUSED: treasury balance < 0.1 TON. Fund from faucet first.');
    process.exit(1);
  }

  // 3. Deploy: send state-init + tiny amount to the Store address
  const value = toNano('0.05');
  const fee = toNano('0.05');
  if (balance < value + fee) {
    console.error('REFUSED: not enough for value+fees');
    process.exit(1);
  }

  console.log('Deploying Store with', value.toString(), 'nano ...');
  await w.sendTransfer({
    seqno,
    secretKey: key.secretKey,
    messages: [internal({
      to: storeAddr,
      value,
      bounce: false,
      init: storeInit,
      body: beginCell().endCell(), // empty body -> receive() deposit, count = 1
    })],
  });
  console.log('Deploy tx sent. Polling getDepositCount (up to 2 min) ...');

  const opened = client.open(store);
  for (let i = 0; i < 40; i++) {
    await new Promise(r => setTimeout(r, 3000));
    try {
      const count = await opened.getDepositCount();
      console.log(`CONFIRMED on testnet. depositCount = ${count} (explorer: https://testnet.tonviewer.com/${storeAddr.toString({ urlSafe: true })})`);
      return;
    } catch { /* not deployed yet */ }
  }
  console.log('Not confirmed yet — run this script again in a minute.');
}

main().catch(e => { console.error('FATAL:', e?.message ?? e); process.exit(1); });
