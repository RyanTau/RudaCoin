import hashlib
from datetime import datetime
import binascii
from numpy import broadcast, true_divide
class Block:
    def __init__(self, index, hash, previous_hash, timestamp, data, difficulty, nonce):
        self.index = index
        self.hash = hash
        self. previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce


def calculateHash(index, previousHash, timestamp, data, difficulty, nonce):
    val = str(index) + str(previousHash) + str(timestamp) + str(data) +str(difficulty) + str(nonce)
    encoded = val.encode()
    result = hashlib.sha256(encoded).hexdigest()
    return result

genesisBlock = Block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', None, 1465154705, 'my genesis block!!',1,1)

blockchain = [genesisBlock]

def getLatestBlock():
    return blockchain[-1]
                                                                                                                                                                                                                                                                                                                                                                                                       
def getBlockchain():
    return blockchain


def generateNextBlock(blockData):
    previousBlock = getLatestBlock()
    nextIndex = previousBlock.index + 1
    nextTimeStamp =str(datetime.now().time())
    nextHash = calculateHash(nextIndex, previousBlock.hash, nextTimeStamp, blockData)
    newBlock = Block(nextIndex,nextHash, previousBlock.hash,nextTimeStamp, blockData)
    return newBlock

def isValidNewBlock(newBlock, previousBlock):
    if(previousBlock.index + 1 != newBlock.index):
        print("invalid index")
        return False
    elif(previousBlock.hash != newBlock.previous_hash):
        print('invalid previoushash')
        return False
    elif(calculateHash(newBlock.index, previousBlock.hash, newBlock.timestamp, newBlock.data) != newBlock.hash):
        print(calculateHash(newBlock.index, newBlock.hash, newBlock.timestamp, newBlock.data))
        print("it")
        return False
    
    return True

def isValidBlockStructure(block):
    return type(block.index) == 'int' and type(block.has) == "string" and type(block.previvoushHash) == "string" and type(block.previousHash) == "string" and type(block.timestamp) == "string" and type(block.data) == "string"
def isValidChain(blockchaintovalidate):
    if(blockchaintovalidate[0] != genesisBlock):
        return False
    #check all other blocks
    for i in range(1,len(blockchaintovalidate)):
        if not isValidNewBlock(blockchaintovalidate[i], blockchaintovalidate[i-1]):
            return False
    
    return True

def replaceChain(newBlocks):
    if(isValidChain(newBlocks) and len(newBlocks)) > len(getBlockchain()):
        blockchain = newBlocks
        broadcastLatest()
    else:
        print("recieeved is invalid")

 
#print(hashlib.sha256("hipuss".encode()).hexdigest()) 

'''PROOF OF WORK'''

def hashMatchesDiffculty(hash, difficulty):
    hashInBinary = bin(int("4",16))[2:]
    requiredPrefix = "0"*difficulty
    return hashInBinary.startswith(requiredPrefix)


def findBlock(index, previousHash, timestamp, data, difficulty):
    nonce = 0
    while(True):
        hash = calculateHash(index, previousHash, timestamp, data, difficulty, nonce)
        if (hashMatchesDiffculty(hash,difficulty)):
            return Block(index, hash, previousHash, timestamp, data, difficulty, nonce)
        nonce += 1

BLOCK_GENERATION_INTERVAL = 10
DIFFICULTY_ADJUSTMENT_INTERVAL = 10

def getDifficulty(aBlockChain):
    latestblock = aBlockChain[-1]
    if (latestBlock.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and latestBlock.index != 0):
        return getAdjustestedDifficulty(latestblock, aBlockchain)
    else:
        return latestBlock.difficulty

def getAdjustedDifficulty(latestBlock,aBlockChain):
    prevAdjustmentBlock = aBlockChain[len(blockchain)- DIFFICULTY_ADJUSTMENT_INTERVAL]
    timeExpected = BLOCK_GENERATION_INTERVAL * DIFFICULTY_ADJUSTMENT_INTERVAL
    timeTaken = latestBlock.timestamp - prevAdjustmentBlock.timestamp
    if(timeTaken < timeExpected/2):
        return prevAdjustmentBlock 
    elif timeTaken > timeExpected * 2:
        return prevAdjustmentBlock.difficulty - 1
    else:
        return prevAdjustmentBlock.difficulty 


def isValidTimestamp(newBlock, previousBlock):
    return (previousBlock.timestamp -60 < newBlock.timestamp and newBlock.timestamp - 60 < datetime.now().time() )




