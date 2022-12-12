import hashlib
import json,os
import sys

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pprint import pprint

transactions = [ "[3, 4, 5, 6]", "[4, 5, 6, 7]", "[5, 6, 7, 8]", "[6, 7, 8, 9]", "[7, 8, 9, 10]", "[8, 9, 10, 11]", "[9, 10, 11, 12]", "[10, 11, 12, 13]", "[11, 12, 13, 14]", "[12, 13, 14, 15]", "[13, 14, 15, 16]"]


nonce = 0
alice_blknum = 0   
bob_blknum = 1 

# alice mine block	
def alice():
    cond = True
    global nonce
    global alice_blknum
    fr = open("block" + str(alice_blknum) + ".json", "r")    
    preblk = fr.read()
    fr.close()
    hashval = hashlib.sha256(preblk.encode()).hexdigest()
    while(cond):
        tx = json.dumps({'Block number ': alice_blknum+1, 'Hash': hashval, 'Transaction': transactions[alice_blknum], 'Nonce': nonce}, sort_keys=True, indent=4, separators=(',', ': '))
        hashout = hashlib.sha256(tx.encode()).hexdigest()
        if int(hashout[0:5], 16) == 0:
            cond = False
        nonce = nonce + 1
        
   
    fw = open("block"+ str(alice_blknum+1) + ".json", "w+")
    fw.write(tx)
    fw.close()
    with open("block"+ str(alice_blknum+1) + ".json") as json_file:
        toPub = json.load(json_file)

    pubnub.publish()\
    .channel('Channel-ier4zmxv0')\
    .message({"sender": pnconfig.uuid, "content": toPub})\
    .pn_async(my_publish_callback)
    
# bob verfiy alice's block
def bobVerify():
    global alice_blknum
    fr1 = open('block' + str(alice_blknum) + '.json','r')
    blk1 = fr1.read()
    hashval1 = hashlib.sha256(blk1.encode()).hexdigest()
    print("block" + str(alice_blknum) + "['Hash']: " + hashval1)

    fr1.close()

    fr2 = open('block' + str(alice_blknum+1) + '.json','r')
    blk2 = fr2.read()
    hashval2  = json.loads(blk2)['Hash']
    print("block" + str(alice_blknum+1) + "['Hash']: " + hashval2)

    fr2.close()

    if hashval1 == hashval2:
        print('Verified!')
        alice_blknum = alice_blknum + 2  # 1 , 3 , 5 , 7 , 9 , 11
    else:
        print('Error')
        sys.exit()

# bob mine new block
def bob():
    cond = True
    global nonce
    global bob_blknum
    fr = open("block" + str(bob_blknum) +".json", "r")    
    preblk = fr.read()
    fr.close()
    hashval = hashlib.sha256(preblk.encode()).hexdigest()
    while(cond):
        tx = json.dumps({'Block number ': bob_blknum+1, 'Hash': hashval, 'Transaction': transactions[bob_blknum], 'Nonce': nonce}, sort_keys=True, indent=4, separators=(',', ': '))
        hashout = hashlib.sha256(tx.encode()).hexdigest()
        if int(hashout[0:5], 16) == 0:
            cond = False
        nonce = nonce + 1
        #print(hashout)
    fw = open("block" + str(bob_blknum+1) + ".json", "w+")
    fw.write(tx)
    fw.close()


    with open("block" + str(bob_blknum+1) + ".json") as json_file:
        toPub = json.load(json_file)

    pubnub.publish()\
    .channel('Channel-ier4zmxv0')\
    .message({"sender": "Bob", "content": toPub})\
    .pn_async(my_publish_callback)

# alice verify bob's block
def aliceVerify():
    global bob_blknum
    fr1 = open('block' + str(bob_blknum) + '.json','r')
    blk1 = fr1.read()
    hashval1 = hashlib.sha256(blk1.encode()).hexdigest()
    print("block" + str(bob_blknum) + "['Hash']: " + hashval1)

    fr1.close()

    fr2 = open('block' + str(bob_blknum+1) + '.json','r')
    blk2 = fr2.read()
    hashval2  = json.loads(blk2)['Hash']
    print("block" + str(bob_blknum+1) + "['Hash']: " + hashval2)

    fr2.close()

    if hashval1 == hashval2:
        print('Verified!')
        bob_blknum = bob_blknum + 2 # 0 , 2, 4, 6, 8 , 10
    else:
        print('Error')
        sys.exit()

# pub nub

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-924a121e-9498-11ec-8158-ea060f348a12'
pnconfig.publish_key = 'pub-c-d953e118-5fe5-4705-ac4d-8246afab0b21'
pnconfig.uuid = 'Alice'
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];



def main():
    print("==============================Welcome to Mining game==============================")
    input("Press <Enter> for Alice to start minning block1")
    print("please wait...")
    alice()
    print("block1 generated!\n")
    input("Press <Enter> for Bob to verify block1")
    bobVerify()
    print()
    input("Press <Enter> for Bob to mine block2")
    print("please wait...")
    bob()
    print("block2 generated!\n")
    input("Press <Enter> for Alice to verify block2")
    aliceVerify()
    print('')
    input("Press <Enter> for Alice to mine block3")
    print("please wait...")
    alice()
    print("block3 generated!\n")
    input("Press <Enter> for Bob to verify block3")
    bobVerify()
    print('')
    input("Press <Enter> for Bob to start minning block4")
    print("please wait...")
    bob()
    print("block4 generated!\n")
    input("Press <Enter> for Alice to verify block4")
    aliceVerify()
    print('')
    input("Press <Enter> for Alice to mine block5")
    print("please wait...")
    alice()
    print("block5 generated!\n")
    input("Press <Enter> for Bob to verify block5")
    bobVerify()
    print('')
    input("Press <Enter> for Bob to mine block6")
    print("please wait...")
    bob()
    print("block6 generated!\n")
    input("Press <Enter> for Alice to verify block6")
    aliceVerify()
    print('')
    input("Press <Enter> for Alice to mine block7")
    print("please wait...")
    alice()
    print("block7 generated!\n")
    input("Press <Enter> for Bob to verify block7")
    bobVerify()
    print('')
    input("Press <Enter> for Bob to mine block8")
    print("please wait...")
    bob()
    print("block8 generated!\n")
    input("Press <Enter> for Alice to verify block8")
    aliceVerify()
    print('')
    input("Press <Enter> for Alice to mine block9")
    print("please wait...")
    alice()
    print("block9 generated!\n")
    input("Press <Enter> for Bob to verify block9")
    bobVerify()
    print('')
    input("Press <Enter> for Bob to mine block10")
    print("please wait...")
    bob()
    print("block10 generated!\n")
    input("Press <Enter> for Alice to verify block10")
    aliceVerify()
    print('')
    input("Press <Enter> for Alice to mine block11")
    print("please wait...")
    alice()
    print("block11 generated!\n")
    input("Press <Enter> for Bob to verify block11")
    bobVerify()
    
 
if __name__ == "__main__":
    main()


