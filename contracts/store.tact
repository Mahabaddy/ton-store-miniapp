// Qubax Store — testnet payment contract
// Accepts plain TON deposits, counts them, owner can sweep the balance.
// Storage: owner address + deposit counter. Minimal surface, easy to verify.

contract Store {
    owner: Address;
    depositCount: Int as uint32;

    init(owner: Address) {
        self.owner = owner;
        self.depositCount = 0;
    }

    // Plain TON transfer (no body) = a deposit. Contract counts it.
    receive() {
        self.depositCount = self.depositCount + 1;
    }

    // TON transfers WITH a text comment also count as deposits
    receive(msg: String) {
        self.depositCount = self.depositCount + 1;
    }

    // Owner sweeps the full balance to themselves (contract stays alive)
    receive("withdraw") {
        require(sender() == self.owner, "not owner");
        send(SendParameters{
            to: self.owner,
            value: 0,
            mode: SendRemainingBalance | SendIgnoreErrors,
            bounce: false,
            body: "store withdraw".asComment()
        });
    }

    get fun owner(): Address {
        return self.owner;
    }

    get fun depositCount(): Int {
        return self.depositCount;
    }
}
