import argparse
import hashlib
import sys
from stat import *
from os.path import exists
from datetime import datetime
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument('-c')
parser.add_argument('-i')

arguments = parser.parse_args()
actions = arguments.action

class block_list():

    def __init__(self, blocks = []): 
        self.blocks = blocks
        print("INITIAL Block Found")
        print("Use command 'help' to print a list of commands")
        print("")

    def help(self):
        print("Commands:")
        print("add -c -i: Appends a new block to the list, requires a Case ID and unique Item ID")
        print("checkout -i: Checks out the specified item, requires a Item ID that has previously been added to the blockchain and is currently checkedin")
        print("checkin -i: Checks in the specified item, requires a Item ID that has previously been added to the blockchain and is currently checked out")
        print("remove -i: Appends a new block to the chain indicating the specified item has been removed, requires item ID that has been previously added to the chain")
        print("verify: Verifies the integrity of the blockchain by checking is any previous evidence item has been tampered with")
        print("log: Prints all the previous blocks")
        print("help: Prints this list of commands")

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

    def add_new_block(self, case_id, item_id):
        if exists("blockchain.pickle") == True:

            pickle_load = open('blockchain.pickle', 'rb')
            full_block = pickle.load(pickle_load)
            pickle_load.close()

            block_counter = -1
            
            try:
                for i in full_block:
                    check_for_duplicate = False
                    block_counter = block_counter + 1

                    if i[3] == item_id:
                        sys.exit[0]

            except:
                print("ERROR: Item ID is already in use, please assign a unique item ID")
                return 0

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

            print("Hash = ", hash)
            print("Timestamp = ", timestamp)
            print("Case ID = ", case_id)
            print("Item ID = ", item_id)
            print("State = ", state)
        
        else:
            print("INITIAL Block Not Found, Initializing First Block")
            self.initial_block()

    def checkout(self, item_id):
        
        pickle_load = open('blockchain.pickle', 'rb')
        full_block = pickle.load(pickle_load)
        pickle_load.close()

        count = -1
        found_block = 0
        found_matching_item = False
        
        for i in full_block:

            count = count + 1
            
            if str(item_id) in i:

                if "CHECKEDIN" in i:
                    found_block = count
                    found_matching_item = True

                else: 
                    found_matching_item = False

        if found_matching_item == True:
            grabbed_block = full_block[found_block]

            block_string = str(grabbed_block).encode("utf-8")
            block_hash = hashlib.sha1(block_string).hexdigest()
            timestamp = datetime.timestamp(datetime.now())

            new_block = (block_hash, timestamp, grabbed_block[2], grabbed_block[3], "CHECKEDOUT")

            full_block.append(new_block)

            pickle_file = open("blockchain.pickle", 'wb')
            pickle.dump(full_block, pickle_file)
            pickle_file.close()

            print("Hash = ", block_hash)
            print("Timestamp = ", timestamp)
            print("Case ID = ", grabbed_block[2])
            print("Item ID = ", grabbed_block[3])
            print("State = ", "CHECKEDOUT")
            

        else:
            print("ERROR: Could not find a matching block or item is not checked in")

    def checkin(self, item_id):
        
        pickle_load = open('blockchain.pickle', 'rb')
        full_block = pickle.load(pickle_load)
        pickle_load.close()

        count = -1
        found_block = 0
        found_matching_item = False
        
        for i in full_block:

            count = count + 1
            
            if item_id in i:

                if "CHECKEDOUT" in i:
                    found_block = count
                    found_matching_item = True

                else:
                    found_matching_item = False

        if found_matching_item == True:
            grabbed_block = full_block[found_block]

            block_string = str(grabbed_block).encode("utf-8")
            block_hash = hashlib.sha1(block_string).hexdigest()
            timestamp = datetime.timestamp(datetime.now())

            new_block = (block_hash, timestamp, grabbed_block[2], grabbed_block[3], "CHECKEDIN")

            full_block.append(new_block)

            pickle_file = open("blockchain.pickle", 'wb')
            pickle.dump(full_block, pickle_file)
            pickle_file.close()

            print("Hash = ", block_hash)
            print("Timestamp = ", timestamp)
            print("Case ID = ", grabbed_block[2])
            print("Item ID = ", grabbed_block[3])
            print("State = ", "CHECKEDIN")

        else:
            print("ERROR: Could not find a matching block or item is not checked out")

    def remove(self, item_id):
            
            pickle_load = open('blockchain.pickle', 'rb')
            full_block = pickle.load(pickle_load)
            pickle_load.close()

            count = -1
            found_block = 0
            found_matching_item = False
            
            for i in full_block:

                count = count + 1
                
                if item_id in i:

                    if "REMOVED" in i:
                        found_matching_item = False

                    else:
                        found_block = count
                        found_matching_item = True

            if found_matching_item == True:
                grabbed_block = full_block[found_block]

                block_string = str(grabbed_block).encode("utf-8")
                block_hash = hashlib.sha1(block_string).hexdigest()
                timestamp = datetime.timestamp(datetime.now())

                new_block = (block_hash, timestamp, grabbed_block[2], grabbed_block[3], "REMOVED")

                full_block.append(new_block)

                pickle_file = open("blockchain.pickle", 'wb')
                pickle.dump(full_block, pickle_file)
                pickle_file.close()

                print("Hash = ", block_hash)
                print("Timestamp = ", timestamp)
                print("Case ID = ", grabbed_block[2])
                print("Item ID = ", grabbed_block[3])
                print("State = ", "REMOVED")

            else:
                print("ERROR: Could not find a matching block or item is already removed")

    def verify(self):
        
        pickle_load = open('blockchain.pickle', 'rb')
        full_block = pickle.load(pickle_load)
        pickle_load.close()

        count = 0

        for i in full_block:
        
            count = count + 1

            block_string = str(i).encode("utf-8")
            block_hash = hashlib.sha1(block_string).hexdigest()

            try:
                grabbed_block = full_block[count]

            except:
                break

            if grabbed_block[0] == block_hash:
                pass
            else:
                print("FAILURE at block:", count)

                print("Block Number =", count)
                print("Hash =", grabbed_block[0])
                print("Timestamp =", grabbed_block[1])
                print("Case ID =", grabbed_block[2])
                print("Item ID =", grabbed_block[3])
                print("State =", grabbed_block[4])
                return 0

        print("SUCCESS: Blockchain is valid")
            
    def log(self):

        pickle_load = open('blockchain.pickle', 'rb')
        full_block = pickle.load(pickle_load)
        pickle_load.close()

        count = 0

        for i in full_block:

            try:
                grabbed_block = full_block[count]

            except:
                break

            print("Block Number =", count + 1)
            print("Hash =", grabbed_block[0])
            print("Timestamp =", grabbed_block[1])
            print("Case ID =", grabbed_block[2])
            print("Item ID =", grabbed_block[3])
            print("State =", grabbed_block[4])
            print("")

            count = count + 1




if actions == "init":
    initial = block_list()
    initial.initial_block()

if actions == "add":
    given = {}
    given["case_id"] = arguments.c
    given["item_id"] = arguments.i
    if given["case_id"] and given["item_id"]:
        initial = block_list()
        initial.add_new_block(given["case_id"], given["item_id"])
    else: 
        print("ADD command requires Case ID (-c) and Item ID (-i)")
        sys.exit[0]

if actions == "checkout":
    given = {}
    given["item_id"] = arguments.i
    if given["item_id"]:
        initial = block_list()
        initial.checkout(given["item_id"])

if actions == "checkin":
    given = {}
    given["item_id"] = arguments.i
    if given["item_id"]:
        initial = block_list()
        initial.checkin(given["item_id"])

if actions == "remove":
    given = {}
    given["item_id"] = arguments.i
    if given["item_id"]:
        initial = block_list()
        initial.remove(given["item_id"])

if actions == "verify":
    initial = block_list()
    initial.verify()

if actions == "log":
    initial = block_list()
    initial.log()

if actions == "help":
    initial = block_list()
    initial.help()