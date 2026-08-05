import hashlib
import time

class Block:

    def __init__(self, index, timestamp, data, previousHash=""):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.nonce = 0

        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previousHash}{self.nonce}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
        print(f"Block mined message: Block {self.index} successfully mined!")
        print(f"Current block hash: {self.hash}")
        print(f"Previous block hash: {self.previousHash}")
        print(f"Nonce value: {self.nonce}\n")


class Blockchain:
    def __init__(self, difficulty=2):
        
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):

        genesis = Block(0, time.time(), "Genesis Block", "0")
        print("Mining Genesis Block...")
        genesis.mine_block(self.difficulty)
        return genesis

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):

        new_block.previousHash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previousHash != previous_block.hash:
                return False

        return True



if __name__ == "__main__":
    
    my_blockchain = Blockchain(difficulty=2)

    print("Mining Block 1...")
    my_blockchain.add_block(Block(1, time.time(), "Alice sends 10 coins to Bob"))
    
    print("Mining Block 2...")
    my_blockchain.add_block(Block(2, time.time(), "Bob sends 5 coins to Charlie"))
    
    print("Mining Block 3...")
    my_blockchain.add_block(Block(3, time.time(), "Charlie sends 2 coins to Dave"))
    
    print("Mining Block 4...")
    my_blockchain.add_block(Block(4, time.time(), "Dave sends 1 coin to Alice"))
    
    print("Mining Block 5...")
    my_blockchain.add_block(Block(5, time.time(), "Alice sends 15 coins to Eve"))

    print("========================================")
    print(f"Blockchain validity before tampering: {my_blockchain.is_chain_valid()}")
    print("========================================\n")

    print("--> HACKER ACTION: Modifying data in Block 2...")
    my_blockchain.chain[2].data = "Bob sends 5000 coins to Charlie (HACKED)"
    
    print("\n========================================")
    print(f"Blockchain validity after tampering: {my_blockchain.is_chain_valid()}")
    print("========================================")