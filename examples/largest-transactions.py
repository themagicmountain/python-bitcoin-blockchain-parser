import sys
import os
import pickle
import random
sys.path.append('..')
from blockchain_parser.blockchain import Blockchain, get_block
from blockchain_parser.block import Block
from datetime import datetime

def get_blocks_starting_at_time(timestamp, blockIndexes):
    begin = blockIndexes[0].height
    end = blockIndexes[-1].height
    return get_blocks_start_at_time_helper(timestamp, blockIndexes, begin, end)

"""
414257
414258
414258
414257
414257
414258
414257
414258
414257
414257
414258
414257
414258
414257
414257
414257
414258
414258
414258
414257
414257
414257

my retarded binary search is stuck here. 
"""


def get_blocks_start_at_time_helper(timestamp, blockIndexes, begin, end):
    """
    binary search starting at a random point in the interval
    """
    if end - begin <= 1:
        return begin
    start = random.randint(begin, end)
    # print("begin: {}, end: {}".format(begin, end))
    # print("start: {}".format(start))
    blkFile = os.path.join(sys.argv[1], "blk%05d.dat" % blockIndexes[start].file)
    block = Block(get_block(blkFile, blockIndexes[start].data_pos))
    blockheader = block.header
    block_timestamp = blockheader.timestamp
    if block_timestamp < timestamp: 
        return get_blocks_start_at_time_helper(timestamp, blockIndexes, start, end)
    else: 
        return get_blocks_start_at_time_helper(timestamp, blockIndexes, begin, start)


# Instantiate the Blockchain by giving the path to the directory 
# containing the .blk files created by bitcoind
blockchain = Blockchain(sys.argv[1])
blockIndexes = None
cache = os.path.join(os.getcwd(), './cache')
index = os.path.join(sys.argv[1], './index')

if cache and os.path.exists(cache):
    # load the block index cache from a previous index
    with open(cache, 'rb') as f:
        blockIndexes = pickle.load(f)

if blockIndexes is None:
    # build the block index
    blockIndexes = blockchain._Blockchain__getBlockIndexes(index)
    if cache and not os.path.exists(cache):
        # cache the block index for re-use next time
        with open(cache, 'wb') as f:
            pickle.dump(blockIndexes, f)

print get_blocks_starting_at_time(datetime.strptime("1 Jun 2016", "%d %b %Y"), blockIndexes)


    

"""
DBBlockIndex(0000000000000000002697892c0b3aafc89ffd290e155fc02ee560dd830abbf6, height=540355, file_no=1365, file_pos=62892141), 
DBBlockIndex(0000000000000000000c65107d3eed77143a113da4dc8d2bfce5ccdb07ab4181, height=540356, file_no=1365, file_pos=34860059), 
DBBlockIndex(0000000000000000001756bdec8507351d4641a46241b47b1196c2a17d6ef46a, height=540357, file_no=1365, file_pos=57926439),
 DBBlockIndex(00000000000000000019e2a619dbc462cf10a0739c7f2c1bb8cf952c7aa1c1d3, height=540358, file_no=1365, file_pos=53520749), 
 DBBlockIndex(0000000000000000001247039ef97e89106918db52494515f16459777a4410ed, height=540359, file_no=1365, file_pos=66371075), 
 DBBlockIndex(000000000000000000265451995268f3ea6bb88d0300e9f2040c9c2f990b0eb8, height=540360, file_no=1365, file_pos=64160763), 
 DBBlockIndex(00000000000000000023ffc636a44a6fde8113b8ecd1788cb197071da66b9c43, height=540361, file_no=1365, file_pos=36478865), 
 DBBlockIndex(00000000000000000019e26cb8443941f1645cfaba092f46873fa74459feb63a, height=540362, file_no=1365, file_pos=61668674), 
 DBBlockIndex(00000000000000000002b4457b9be2a4b9700d4bd12230e3a40234415e0ddb67, height=540363, file_no=1365, file_pos=40029897), 
 DBBlockIndex(0000000000000000000c140ca018a4bcee02e7d429945ee4f17359256787fe77, height=540364, file_no=1365, file_pos=54771114), 
 DBBlockIndex(0000000000000000000f5bb58635da45f639a5e34c8cb5f7b1da3ee7812f0d80, height=540365, file_no=1365, file_pos=59074847), 
 DBBlockIndex(00000000000000000008342b16e9a1cb0c8c729aaac806ef866950db6dd5f019, height=540366, file_no=1365, file_pos=42484074), 
 DBBlockIndex(0000000000000000000706c1a53e96ede3137fc86c665c28c23068348e9be2cf, height=540367, file_no=1365, file_pos=65261771), 
 DBBlockIndex(0000000000000000001435b9c776b3f506c953e86c5679f961dbfad63bc4e81a, height=540368, file_no=1365, file_pos=43616983), 
 DBBlockIndex(000000000000000000157f59bfd097fe14ce804a2994db7d5b04ecc8e7730369, height=540369, file_no=1365, file_pos=67523539), 
 DBBlockIndex(000000000000000000204cbc06bc1b10911259ae6acbfa59d09ac27cc181a714, height=540370, file_no=1365, file_pos=68749314)]

"""