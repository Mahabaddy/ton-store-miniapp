// scripts/emit_init.ts
var import_fs = require("fs");
var import_core2 = require("@ton/core");

// build/store_Store.ts
var import_core = require("@ton/core");
function initStore_init_args(src) {
  return (builder) => {
    const b_0 = builder;
    b_0.storeAddress(src.owner);
  };
}
async function Store_init(owner) {
  const __code = import_core.Cell.fromHex("b5ee9c7241020b01000184000114ff00f4a413f4bcf2c80b01020162020601ced0eda2edfb01d072d721d200d200fa4021103450666f04f86102f862ed44d0d2000197fa40d31f596c1296fa400101d170e203925f03e07022d74920c21f953102d31f03de21c00021c121b08e1310235f0301a4c87f01ca005902cecb1fc9ed54e023f901340303019082f0158e394e7cc73a9aeb362957fe037665588aef16f3bd68580c13ab84097cf22abae302c0008e1801c21f8e1101a4c87f01ca005902cecb1fc9ed54db31e05b925f03e2f2c0820401b630318200c080f84222c705f2f470810082708824553010246d50436d03c8cf8580ca00cf8440ce01fa028069cf40025c6e016eb0935bcf819d58cf8680cf8480f400f400cf81e2f400c901fb0001c87f01ca005902cecb1fc9ed540500240000000073746f726520776974686472617702012007090139be28ef6a268690000cbfd20698facb6094b7d200080e8b8716d9e3610c080002210139bc95ff6a268690000cbfd20698facb6094b7d200080e8b8716d9e3610c0a000220cc11f13a");
  const builder = (0, import_core.beginCell)();
  builder.storeUint(0, 1);
  initStore_init_args({ $$type: "Store_init_args", owner })(builder);
  const __data = builder.endCell();
  return { code: __code, data: __data };
}
var Store_errors = {
  2: { message: "Stack underflow" },
  3: { message: "Stack overflow" },
  4: { message: "Integer overflow" },
  5: { message: "Integer out of expected range" },
  6: { message: "Invalid opcode" },
  7: { message: "Type check error" },
  8: { message: "Cell overflow" },
  9: { message: "Cell underflow" },
  10: { message: "Dictionary error" },
  11: { message: "'Unknown' error" },
  12: { message: "Fatal error" },
  13: { message: "Out of gas error" },
  14: { message: "Virtualization error" },
  32: { message: "Action list is invalid" },
  33: { message: "Action list is too long" },
  34: { message: "Action is invalid or not supported" },
  35: { message: "Invalid source address in outbound message" },
  36: { message: "Invalid destination address in outbound message" },
  37: { message: "Not enough Toncoin" },
  38: { message: "Not enough extra currencies" },
  39: { message: "Outbound message does not fit into a cell after rewriting" },
  40: { message: "Cannot process a message" },
  41: { message: "Library reference is null" },
  42: { message: "Library change action error" },
  43: { message: "Exceeded maximum number of cells in the library or the maximum depth of the Merkle tree" },
  50: { message: "Account state size exceeded limits" },
  128: { message: "Null reference exception" },
  129: { message: "Invalid serialization prefix" },
  130: { message: "Invalid incoming message" },
  131: { message: "Constraints error" },
  132: { message: "Access denied" },
  133: { message: "Contract stopped" },
  134: { message: "Invalid argument" },
  135: { message: "Code of a contract was not found" },
  136: { message: "Invalid standard address" },
  138: { message: "Not a basechain address" },
  49280: { message: "not owner" }
};
var Store_errors_backward = {
  "Stack underflow": 2,
  "Stack overflow": 3,
  "Integer overflow": 4,
  "Integer out of expected range": 5,
  "Invalid opcode": 6,
  "Type check error": 7,
  "Cell overflow": 8,
  "Cell underflow": 9,
  "Dictionary error": 10,
  "'Unknown' error": 11,
  "Fatal error": 12,
  "Out of gas error": 13,
  "Virtualization error": 14,
  "Action list is invalid": 32,
  "Action list is too long": 33,
  "Action is invalid or not supported": 34,
  "Invalid source address in outbound message": 35,
  "Invalid destination address in outbound message": 36,
  "Not enough Toncoin": 37,
  "Not enough extra currencies": 38,
  "Outbound message does not fit into a cell after rewriting": 39,
  "Cannot process a message": 40,
  "Library reference is null": 41,
  "Library change action error": 42,
  "Exceeded maximum number of cells in the library or the maximum depth of the Merkle tree": 43,
  "Account state size exceeded limits": 50,
  "Null reference exception": 128,
  "Invalid serialization prefix": 129,
  "Invalid incoming message": 130,
  "Constraints error": 131,
  "Access denied": 132,
  "Contract stopped": 133,
  "Invalid argument": 134,
  "Code of a contract was not found": 135,
  "Invalid standard address": 136,
  "Not a basechain address": 138,
  "not owner": 49280
};
var Store_types = [
  { "name": "DataSize", "header": null, "fields": [{ "name": "cells", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "bits", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "refs", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }] },
  { "name": "SignedBundle", "header": null, "fields": [{ "name": "signature", "type": { "kind": "simple", "type": "fixed-bytes", "optional": false, "format": 64 } }, { "name": "signedData", "type": { "kind": "simple", "type": "slice", "optional": false, "format": "remainder" } }] },
  { "name": "StateInit", "header": null, "fields": [{ "name": "code", "type": { "kind": "simple", "type": "cell", "optional": false } }, { "name": "data", "type": { "kind": "simple", "type": "cell", "optional": false } }] },
  { "name": "Context", "header": null, "fields": [{ "name": "bounceable", "type": { "kind": "simple", "type": "bool", "optional": false } }, { "name": "sender", "type": { "kind": "simple", "type": "address", "optional": false } }, { "name": "value", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "raw", "type": { "kind": "simple", "type": "slice", "optional": false } }] },
  { "name": "SendParameters", "header": null, "fields": [{ "name": "mode", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "body", "type": { "kind": "simple", "type": "cell", "optional": true } }, { "name": "code", "type": { "kind": "simple", "type": "cell", "optional": true } }, { "name": "data", "type": { "kind": "simple", "type": "cell", "optional": true } }, { "name": "value", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "to", "type": { "kind": "simple", "type": "address", "optional": false } }, { "name": "bounce", "type": { "kind": "simple", "type": "bool", "optional": false } }] },
  { "name": "MessageParameters", "header": null, "fields": [{ "name": "mode", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "body", "type": { "kind": "simple", "type": "cell", "optional": true } }, { "name": "value", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "to", "type": { "kind": "simple", "type": "address", "optional": false } }, { "name": "bounce", "type": { "kind": "simple", "type": "bool", "optional": false } }] },
  { "name": "DeployParameters", "header": null, "fields": [{ "name": "mode", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "body", "type": { "kind": "simple", "type": "cell", "optional": true } }, { "name": "value", "type": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }, { "name": "bounce", "type": { "kind": "simple", "type": "bool", "optional": false } }, { "name": "init", "type": { "kind": "simple", "type": "StateInit", "optional": false } }] },
  { "name": "StdAddress", "header": null, "fields": [{ "name": "workchain", "type": { "kind": "simple", "type": "int", "optional": false, "format": 8 } }, { "name": "address", "type": { "kind": "simple", "type": "uint", "optional": false, "format": 256 } }] },
  { "name": "VarAddress", "header": null, "fields": [{ "name": "workchain", "type": { "kind": "simple", "type": "int", "optional": false, "format": 32 } }, { "name": "address", "type": { "kind": "simple", "type": "slice", "optional": false } }] },
  { "name": "BasechainAddress", "header": null, "fields": [{ "name": "hash", "type": { "kind": "simple", "type": "int", "optional": true, "format": 257 } }] },
  { "name": "Store$Data", "header": null, "fields": [{ "name": "owner", "type": { "kind": "simple", "type": "address", "optional": false } }, { "name": "depositCount", "type": { "kind": "simple", "type": "uint", "optional": false, "format": 32 } }] }
];
var Store_opcodes = {};
var Store_getters = [
  { "name": "owner", "methodId": 83229, "arguments": [], "returnType": { "kind": "simple", "type": "address", "optional": false } },
  { "name": "depositCount", "methodId": 103103, "arguments": [], "returnType": { "kind": "simple", "type": "int", "optional": false, "format": 257 } }
];
var Store_receivers = [
  { "receiver": "internal", "message": { "kind": "empty" } },
  { "receiver": "internal", "message": { "kind": "text" } },
  { "receiver": "internal", "message": { "kind": "text", "text": "withdraw" } }
];
var Store = class _Store {
  static storageReserve = 0n;
  static errors = Store_errors_backward;
  static opcodes = Store_opcodes;
  static async init(owner) {
    return await Store_init(owner);
  }
  static async fromInit(owner) {
    const __gen_init = await Store_init(owner);
    const address2 = (0, import_core.contractAddress)(0, __gen_init);
    return new _Store(address2, __gen_init);
  }
  static fromAddress(address2) {
    return new _Store(address2);
  }
  address;
  init;
  abi = {
    types: Store_types,
    getters: Store_getters,
    receivers: Store_receivers,
    errors: Store_errors
  };
  constructor(address2, init) {
    this.address = address2;
    this.init = init;
  }
  async send(provider, via, args, message) {
    let body = null;
    if (message === null) {
      body = new import_core.Cell();
    }
    if (typeof message === "string") {
      body = (0, import_core.beginCell)().storeUint(0, 32).storeStringTail(message).endCell();
    }
    if (message === "withdraw") {
      body = (0, import_core.beginCell)().storeUint(0, 32).storeStringTail(message).endCell();
    }
    if (body === null) {
      throw new Error("Invalid message type");
    }
    await provider.internal(via, { ...args, body });
  }
  async getOwner(provider) {
    const builder = new import_core.TupleBuilder();
    const source = (await provider.get("owner", builder.build())).stack;
    const result = source.readAddress();
    return result;
  }
  async getDepositCount(provider) {
    const builder = new import_core.TupleBuilder();
    const source = (await provider.get("depositCount", builder.build())).stack;
    const result = source.readBigNumber();
    return result;
  }
};

// scripts/emit_init.ts
async function main() {
  const treasuryRaw = (0, import_fs.readFileSync)("E:/Hermes/ton-testnet/secrets/wallet_address.txt", "utf-8").trim().replace(/^Address</, "").replace(/>$/, "");
  const treasury = import_core2.Address.parse(treasuryRaw);
  const store = await Store.fromInit(treasury);
  const init = store.init;
  if (!init?.code || !init?.data) throw new Error("init incomplete");
  const addr = (0, import_core2.contractAddress)(0, init).toString({ urlSafe: true });
  const codeB64 = init.code.toBoc().toString("base64");
  const dataB64 = init.data.toBoc().toString("base64");
  (0, import_fs.writeFileSync)("build/store_init.json", JSON.stringify({ address: addr, code: codeB64, data: dataB64 }, null, 2));
  console.log("OWNER   :", treasuryRaw);
  console.log("STORE   :", addr);
  console.log("code boc:", codeB64.length, "chars | data boc:", dataB64.length, "chars -> build/store_init.json");
}
main().catch((e) => {
  console.error("FATAL:", e?.message ?? e);
  process.exit(1);
});
