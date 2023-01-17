import argparse
import hashlib
import stat
import struct
import sys
import uuid
import time
#import arrow
import binascii
import os
from stat import *
from os.path import exists
from collections import namedtuple
from datetime import datetime
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument('-c') #case id
parser.add_argument('-i', action='append')
parser.add_argument('-n') #num entries
parser.add_argument('-y')
parser.add_argument('--why')
parser.add_argument('-o', nargs='*')
parser.add_argument('-r', action="store_true")
parser.add_argument('--reverse', action="store_true")

arguments = parser.parse_args()
actions = arguments.action

class block_list():

    def __init__(self, blocks = []): 
        self.blocks = blocks

    def test_function(self):
        hash = 'qwertyuuiop'
        timestamp = '04-12-22 16:59:00'
        case_id = 123456
        item_id = 98765654
        state = 'CHECKEDIN'

        self.hash = hash
        self.timestamp = timestamp
        self.case_id = case_id
        self.item_id = item_id
        self.state = state

        full_block = (hash, timestamp, case_id, item_id, state)
        self.blocks.append(full_block)

        pickle_file = open("blockchain.pickle", 'wb')
        pickle.dump(self.blocks, pickle_file)
        pickle_file.close()
        

        pickle_load = open('blockchain.pickle', 'rb')
        full_block = pickle.load(pickle_load)
        print("loaded full block 2nd function = ", full_block)

    def initial_block(self):
        if exists("blockchain.pickle") == False:
            hash = "0000000000000000000000000000000000000000"
            timestamp = datetime.timestamp(datetime.now())
            case_id = "INITIAL"
            item_id = "INITIAL"
            state = "INITIAL"

            current_block = (hash, timestamp, case_id, item_id, state)
            self.blocks.append(current_block)

            pickle_file = open("blockchain.pickle", 'wb')
            pickle.dump(self.blocks, pickle_file)
            pickle_file.close()

            pickle_load = open('blockchain.pickle', 'rb')
            full_block = pickle.load(pickle_load)
            print("loaded full block = ", full_block)

    def add_new_block(self, case_id, item_id):
        if exists("blockchain.pickle") == True:

            pickle_load = open('blockchain.pickle', 'rb')
            full_block = pickle.load(pickle_load)
            pickle_load.close()

            block_counter = -1
            
            try:
                for i in full_block:
                    print("rounds of try = ", i)
                    block_counter = block_counter + 1
                    print("block counter = ", block_counter)
            except:
                print("left try loop")

            block_string = str(full_block[block_counter]).encode("utf-8")

            hash = hashlib.sha1(block_string).hexdigest()

            timestamp = datetime.timestamp(datetime.now())
            case_id = case_id
            item_id = item_id
            state = "CHECKEDIN"

            current_block = (hash, timestamp, case_id, item_id, state)

            full_block.append(current_block)

            pickle_file = open("blockchain.pickle", 'wb')
            pickle.dump(full_block, pickle_file)
            pickle_file.close()

            print("block list = ", full_block)



if actions == "init":
    initial = block_list()
    initial.initial_block()
    initial.test_function()

if actions == "add":
    argumentos = {}
    argumentos["case_id"] = arguments.c
    argumentos["item_id"] = arguments.i
    if argumentos["case_id"] and argumentos["item_id"]:
        # add_new_block((generate_prev_hash(argumentos["case_id"], argumentos["item_id"], 'blockchain')))
        initial = block_list()
        initial.add_new_block(argumentos["case_id"], argumentos["item_id"])
    else: 
        sys.exit(0)