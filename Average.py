'''
CS-G513 Homework #2: problem 2
PROGRAM TO ESTIMATE THE EXTENT OF DIFFUSION AND CONFUSION
Requirements :file "message.txt"  - plain text to be Encrypted
			  file "key.txt"  - encryption key to be used
output : the average number of bits changed
NOTE : The position at which to change the bit in cipher text is generated randomly
'''
import sys
import numpy as np

from BitVector import *

expansion_permutation = [
						 31, 0, 1, 2, 3, 4, 3, 4,
						  5, 6, 7, 8, 7, 8, 9, 10,
						 11, 12, 11, 12, 13, 14, 15, 16,
						 15, 16, 17, 18, 19, 20, 19, 20,
						 21, 22, 23, 24, 23, 24, 25, 26,
						 27, 28, 27, 28, 29, 30, 31, 0
						]

permutation = [
			   15,  6, 19, 20, 28, 11, 27, 16,
			    0, 14, 22, 25,  4, 17, 30,  9,
			    1,  7, 23, 13, 31, 26,  2,  8,
			   18, 12, 29,  5, 21, 10,  3, 24
			  ]

initial_permuation=[57, 49, 41, 33, 25, 17, 9,  1,
					59, 51, 43, 35, 27, 19, 11, 3,
					61, 53, 45, 37, 29, 21, 13, 5,
					63, 55, 47, 39, 31, 23, 15, 7,
					56, 48, 40, 32, 24, 16, 8,  0,
					58, 50, 42, 34, 26, 18, 10, 2,
					60, 52, 44, 36, 28, 20, 12, 4,
					62, 54, 46, 38, 30, 22, 14, 6
					]

inverse_init_permutation = [
							39,  7, 47, 15, 55, 23, 63, 31,
							38,  6, 46, 14, 54, 22, 62, 30,
							37,  5, 45, 13, 53, 21, 61, 29,
							36,  4, 44, 12, 52, 20, 60, 28,
							35,  3, 43, 11, 51, 19, 59, 27,
							34,  2, 42, 10, 50, 18, 58, 26,
							33,  1, 41,  9, 49, 17, 57, 25,
							32,  0, 40,  8, 48, 16, 56, 24
						   ]
s_boxes = {i:None for i in range(8)}
s_boxes[0] = [ [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
			   [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
			   [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
			   [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13] ]

s_boxes[1] = [ [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
			   [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
			   [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
			   [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9] ]

s_boxes[2] = [ [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
			   [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
			   [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
			   [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12] ]

s_boxes[3] = [ [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
			   [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
			   [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
			   [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14] ]

s_boxes[4] = [ [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
			   [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
			   [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
			   [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3] ]

s_boxes[5] = [ [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
			   [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
			   [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
			   [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13] ]

s_boxes[6] = [ [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
			   [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
			   [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
			   [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12] ]

s_boxes[7] = [ [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
			   [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
			   [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
			   [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11] ]

round_keys = []
ciphertextblk1=[] #original ciphertext blocks
def substitute( expanded_half_block ):
    '''
    This method implements the step "Substitution with 8 S-boxes"step
	Method input: The 48 bit expanded half block
	Method output : the 32 bit compressed half block
	'''
    output = BitVector (size = 32)
    segments = [expanded_half_block[x*6:x*6+6] for x in range(8)]
    for sindex in range(len(segments)):
        row = 2*segments[sindex][0] + segments[sindex][-1]
        column = int(segments[sindex][1:-1])
        output[sindex*4:sindex*4+4] = BitVector(intVal = s_boxes[sindex][row][column], size = 4)
    return output

def get_encryption_key():
	''' This method 1.reads key.txt for key,
					2.creates a bitvector from the string(64 bit)
					3.Permutes the key according to key_permutation_1(56 bit)
		Method input: None
		Method output : 56 bit key
	'''
	key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,
                          9,1,58,50,42,34,26,18,10,2,59,51,43,35,
                         62,54,46,38,30,22,14,6,61,53,45,37,29,21,
                         13,5,60,52,44,36,28,20,12,4,27,19,11,3]

	with open("key.txt","r") as keyfile:
		key = keyfile.read().strip("\n")
	if len(key) != 8:
		print("\nKey generation needs 8 characters exactly\n")
		sys.exit("check your key and Try again!")
	key = BitVector(textstring = key)
	key = key.permute(key_permutation_1)
	return key

def generate_round_keys(encryption_key):
	''' This method 1.Shifts the key from previous round based on the key schedule
					2.Permutes the 56-bit key -> 48 bit key
		Method input: 56 bit encryption key
		Method output : a list of 16 48-bit key for each round
	'''
	key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,
                          3,25,7,15,6,26,19,12,1,40,51,30,36,46,
                         54,29,39,50,44,32,47,43,48,38,55,33,52,
                         45,41,49,35,28,31
						 ]
	shifts_for_round_key_gen = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
	key = encryption_key.deep_copy()
	for round_count in range(16):
		[LKey, RKey] = key.divide_into_two()
		shift = shifts_for_round_key_gen[round_count]
		LKey << shift
		RKey << shift
		key = LKey + RKey #this goes to the next round
		round_key = key.permute(key_permutation_2)
		round_keys.append(round_key)
	return round_keys

def round_logic(left,right,logic,roundnumber):
	''' This method implements the n rounds of subsitution and permutation
		step of the DES algorithm recursively
		Method input: left - the 32 bit left part of the block
					  right - the 32 bits right part of the block
					  logic - method invokes fo rencryption of decryption
					  		  can take values"E" or "D",
					  roundnumber - the round# if current method invocation
		Method output : left and right part of the block at the end of 16 rounds
	'''
	newRight = right.permute( expansion_permutation ) 	##part of funtion f # expansion
	out_xor = newRight ^ round_keys[roundnumber]		##part of funtion f #xoring text and key
	out_sbox=substitute(out_xor).permute(permutation)   ##part of funtion f subtitution and permutation
	nextRight = out_sbox ^ left
	nextLeft  = right
	if logic is "E":
		if roundnumber == 15:
			return [nextLeft,nextRight]
		else:
			roundnumber = roundnumber+1
			return round_logic(nextLeft,nextRight,logic,roundnumber)
	elif logic is "D" :
		if roundnumber == 0:
			return [nextLeft,nextRight]
		else:
			roundnumber = roundnumber-1
			return round_logic(nextLeft,nextRight,logic,roundnumber)

def get_message(filename):
	''' This method reads the given file and returns it's content after
		stripping extra newlines##
		Method input: filename - file to be read
		Method output :text - contents of the file
	'''
	with open(filename,"r",encoding="utf8") as filedes:
		text= filedes.read().strip("\n")
	return text

def divide_into_blocks(v,size):
	'''divides the bitvector of our message into blocks
		Method input: v - bitvector of the whole message
					  size - the size of each block
		Method output :vecList - list of bitvectors of size 64
	'''
	veclist=[]
	for i in range(0,len(v),size):
		if i+size < len(v):
			val = v[i:i+size]
			veclist.append(val)
		else:
			val = v[i:]
			if len(val) < 64: #last block of the msg might be less than 64bit
				val.pad_from_right(64-len(val))  #padding with zeros
			veclist.append(val)
	return veclist

def encrypt(k,bitvecs):
	''' Encrypts the message using DES algorithm
		Method input: none
		Method output:Ciphertext
	'''
	ciphertextblock =[]
	round_keys = generate_round_keys(k)
	for bitvec in bitvecs:
		if  len(bitvec) > 0:
			bitvec = bitvec.permute(initial_permuation)
			[LE, RE] = bitvec.divide_into_two()
			[FLE,FRE] = round_logic(LE,RE,"E",0) # E for encryption
			preoutput = FRE+FLE # 32 bit swap
			output = preoutput.permute(inverse_init_permutation)#inverse of initial permutation
			ciphertextblock.append(output)
	return ciphertextblock

def diffusion(key,bitvecs,pos):
	''' This method calculates the diffusion in the ciphertext
		Method input: key - 56 bit encryption key
					  pos - the postion in the blocks where the bit has to be changed
		Method output: returns a list where each element is count of changed bits in
					   each block of the ciphertext
	'''
	#to measure diffusion changing a bit of chiphertext
	for vec in bitvecs:
		if vec[pos] == 0:vec[pos]=1 #changing the "pos" bit of all the blocks
		else: vec[pos]=0
	ciphertextblk2 = encrypt(key,bitvecs)
	number_of_blocks = len(ciphertextblk2)
	change_count =[0]*number_of_blocks 	# this holds the count of bits changed
	blk=0
	for text1,text2 in zip(ciphertextblk1,ciphertextblk2):
		for i in range(len(text1)):
			if text1[i]!=text2[i] : change_count[blk] +=1
		blk+=1
	return change_count

def confusion(pos,bitvec,key):
	''' Method to calculate the confusion by chnaging a bit of the key
		Method input: pos - position of the bit to be changed
					  bitvec - blocks of plaintext bitvector objects
		Method output: returns number of bits changed in the ciphertext
	'''
	if key[pos] == 0:key[pos]=1 #changing the "pos" bit of the key
	else: key[pos]=0
	round_keys.clear() # need  to clear them for new key
	lv= BitVector(textstring = message)
	bitve = divide_into_blocks(lv,64)
	ciphertextblk2 = encrypt(key,bitve)
	number_of_blocks = len(ciphertextblk2)
	blk=0
	change_count =[0]*number_of_blocks
	for text1,text2 in zip(ciphertextblk1,ciphertextblk2):
		for i in range(len(text1)):
			if text1[i]!=text2[i] : change_count[blk] +=1
		blk+=1
	return sum(change_count)

def resetsboxes():
	''' This method randomizes the values in the s_boxes list
		range[0,15]
		duplicates are allowed to be present in the list
	'''
	for i in range(8):
		for j in range(4):
			#np.random.shuffle(s_boxes[i][j]) # no duplicates
			s_boxes[i][j]=np.random.random_integers(0,15,16).tolist() #duplicates in a list

def sbox_analysis(diffPos,key,bitvecs):
	''' Resets the values of sboxes and calulates diffusion
		Method input: diffPos-position at which to cmplement the bit
		Method output: prints the average value
	'''
	round_keys.clear()
	resetsboxes()
	ciphertextblk1 = encrypt(key,bitvecs)
	#Measuring diffusion
	bitvecs_copy = copy(bitvecs)
	avgDiffusionList = diffusion(key,bitvecs_copy,diffPos) # getting a list of diffusion for change in every position
	print("DIFFUSION TEST:")
	print("Tested by complementing bit at position %s in every plaintext block"%diffPos)
	print("Number of bits changed in everyblock:")
	print(avgDiffusionList)
	print("Average number of bits changed over %s blocks->" %len(bitvecs),calculate_average(avgDiffusionList),"\n")


def calculate_average(countlist):
	''' calulates the average value from a list
		Method input: countlist - list 
		Method output: returns the average value
	'''
	y=np.array([np.array(xi) for xi in countlist])
	return np.mean(y)

def copy(v):
	new_v =[]
	for obj in v:
	    copy_obj=obj.deep_copy()
	    new_v.append(copy_obj)
	return new_v
#################start of script################
key_o= get_encryption_key() #original key
message = get_message("message.txt")
bv= BitVector(textstring = message)
bitvecs_o = divide_into_blocks(bv,64) #original
ciphertextblk1 = encrypt(key_o,bitvecs_o)  #original ciphertext
diffPos = int(np.random.random_integers(0,15,1))
confCount =  56 #int(input("Enter the number of key choices to test for (range 1-56):"))
sboxCount = 3 #int(input("Enter the number of times you want to reset the sboxes:"))
avgDiffusionList=[]
avgConfusionList=[]
bitvecs = copy(bitvecs_o)
avgDiffusionList = diffusion(key_o,bitvecs,diffPos) # getting a list of diffusion for change in a random position
print("-------------- ")
print("DIFFUSION TEST ")
print("-------------- ")
print("Tested by complementing bit at position %s in every plaintext block\n"%diffPos)
print("Number of bits changed in everyblock:")
print(avgDiffusionList)
print("\nAverage number of bits changed over %s blocks-> " %len(bitvecs_o),calculate_average(avgDiffusionList))
print("-------------- ")
key = key_o.deep_copy()
for position in range(confCount):
	avgConfusionList.append(confusion(position,bitvecs_o,key)) # getting a list of confusion for change in every position
print("-------------- ")
print("CONFUSION TEST")
print("-------------- ")
print("Tested by complementing for %s key choices\n"%confCount)
print("Number of bits changed in Ciphertext for every key choice:")
print(avgConfusionList)
print("\nAverage number of bits changed over %s key choices -> " %confCount,calculate_average(avgConfusionList))
print("------------------ ")
print("RANDOMIZING SBOXES")
print("------------------ ")
for i in range(sboxCount):
	print("#######")
	print("Test ",i+1)
	sbox_analysis(diffPos,key_o,bitvecs_o)
