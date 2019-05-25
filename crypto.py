import hashlib    # For calculating SHA hashes
import datetime   # For getting current timestamps


class Block:
    def __init__(self, timestamp, transactions, previousBlock=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousBlock = previousBlock
        self.difficultyIncrement = 0
        self.hash = self.calculateHash(transactions, timestamp)

    def calculateHash(self, data, timestamp, difficultyIncrement=0):
        data = str(data) + str(timestamp) + str(difficultyIncrement)
        data = data.encode()
        hash = hashlib.sha256(data)
        return hash.hexdigest()

    def mineBlock(self, difficulty):
        difficultyIncrement = 0
        difficultyCheck = "7" * difficulty
        while self.hash[:difficulty] != difficultyCheck:
            self.hash = self.calculateHash(
                self.transactions, self.timestamp, difficultyIncrement)
            difficultyIncrement += 1


class Blockchain:
    def __init__(self):
        self.chain = []
        self.chain.append(Block(str(datetime.datetime.now()), "First Block"))
        self.difficulty = 5
        self.pendingTransaction = []
        self.reward = 10

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def minePendingTrans(self, minerRewardAddress):
        newBlock = Block(str(datetime.datetime.now()), self.pendingTransaction)
        newBlock.mineBlock(self.difficulty)
        newBlock.previousBlock = self.getLastBlock().hash
        self.chain.append(newBlock)
        rewardTrans = Transaction("System", minerRewardAddress, self.reward)
        self.pendingTransaction = [rewardTrans]

    def createTrans(self, transaction):
        self.pendingTransaction.append(transaction)

    def getBalance(self, walletAddress):
        balance = 0
        for block in self.chain:
            if block.previousBlock == "":
                continue
            for transaction in block.trans:
                if transaction.fromWallet == walletAddress:
                    balance -= transaction.amount
                if transaction.toWallet == walletAddress:
                    balance += transaction.amount
        return balance


class Transaction:
    def __init__(self, fromWallet, toWallet, amount):
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.amount = amount


my_crypto = Blockchain()
my_crypto.createTrans(Transaction("Erick", "Alex", 3.2))
my_crypto.createTrans(Transaction("Erick", "Raymond", 1))
my_crypto.createTrans(Transaction("Alex", "Raymond", 5.12))

print("Tony Stark started minning")
my_crypto.minePendingTrans("Tony Stark")

my_crypto.createTrans(Transaction("Zining", "Alex", 0.01))
my_crypto.createTrans(Transaction("Klay", "Erick", 100))
my_crypto.createTrans(Transaction("Raymond", "Erick", 0.0000001))

print("Tony Stark started minning")
my_crypto.minePendingTrans("Tony Stark")

print("Tony Stark balance - " + str(my_crypto.getBalance("Tony Stark")))
