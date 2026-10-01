/**
 * Qubax Store — offline state-init emitter -> build/store_init.json
 * Emits code+data cells separately (Python reassembles StateInit).
 */
import { readFileSync, writeFileSync } from 'fs';
import { Address, contractAddress } from '@ton/core';
import { Store } from '../build/store_Store.ts';

async function main() {
  const treasuryRaw = readFileSync('E:/Hermes/ton-testnet/secrets/wallet_address.txt', 'utf-8')
    .trim().replace(/^Address</, '').replace(/>$/, '');
  const treasury = Address.parse(treasuryRaw);

  const store = await Store.fromInit(treasury);
  const init = store.init!;
  if (!init?.code || !init?.data) throw new Error('init incomplete');

  const addr = contractAddress(0, init).toString({ urlSafe: true });
  const codeB64 = init.code.toBoc().toString('base64');
  const dataB64 = init.data.toBoc().toString('base64');

  writeFileSync('build/store_init.json', JSON.stringify({ address: addr, code: codeB64, data: dataB64 }, null, 2));
  console.log('OWNER   :', treasuryRaw);
  console.log('STORE   :', addr);
  console.log('code boc:', codeB64.length, 'chars | data boc:', dataB64.length, 'chars -> build/store_init.json');
}

main().catch(e => { console.error('FATAL:', e?.message ?? e); process.exit(1); });
