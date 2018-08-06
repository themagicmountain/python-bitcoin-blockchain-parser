import sys
import pymysql.cursors
import binascii

sys.path.append('..')
from blockchain_parser.blockchain import Blockchain

connection = pymysql.connect(host='localhost',
                             user='python',
                             password='python',
                             db='bitcoin',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blockchain = Blockchain(sys.argv[1])

# To get the blocks ordered by height, you need to provide the path of the
# `index` directory (LevelDB index) being maintained by bitcoind. It contains
# .ldb files and is present inside the `blocks` directory
try:
    with connection.cursor() as cursor:
        for block in blockchain.get_ordered_blocks(sys.argv[1] + '/index', start=0, end=534801):
            for transaction in block.transactions:
                sql = """INSERT INTO bitcoin.transaction (
                previous_block_hash,
                block_hash,
                block_height,
                timestamp,
                difficulty,
                nonce,
                transaction_id,
                transaction_hash,
                transaction_hex,
                transaction_n_inputs,
                transaction_n_outputs,
                transaction_version,
                transaction_locktime,
                transaction_is_segwit
                ) VALUES(
                "%s", "%s", "%s",
                "%s", "%s", "%s",
                "%s", "%s", "%s",
                "%s", "%s", "%s",
                "%s", "%s"
                )
                """ % (
                    block.header.previous_block_hash,
                    block.hash,
                    block.height,
                    block.header._timestamp,
                    block.header.difficulty,
                    block.header.nonce,
                    transaction.txid,
                    transaction.hash,
                    binascii.hexlify(transaction.hex),
                    transaction.n_inputs,
                    transaction.n_outputs,
                    transaction.version,
                    transaction.locktime,
                    int(transaction.is_segwit)
                )
                # print(sql)
                cursor.execute(sql)
            connection.commit()
finally:
    connection.close()
