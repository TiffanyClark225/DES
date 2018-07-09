# DES

The goal here was to understand the implementation of the DES (Data Encryption Standard) algorithm and to observe the effects of Diffusion and Confusion (also known as the Avalanche efect)

# Task 1

Encryption and Decryption by DES

DES.py -> Input : files required -> message.txt , key.txt , encrypted.txt(if only decryption is needed)
          output : the required decrypted and encrypted files
          
# Task 2

Average.py

Estimating the extent of confusion and diffusion.
To observe diffusion 1 bit of the plaintext is changed. To understand the effect on diffusion random sets of s boxes are generated.
Finally to observe the confusion 1 bit of the key is changed and compared.

Steps to execute the program :
>> python .\Average.py

Output: The average value in each case, it is seen that for every bit changed ,in the input or
the key ,on an average 50% bits are changed in the ciphertext . Randomizing the sboxes also
yields similar results.
1. Diffusion :After complementing the ciphertext bit at a random position in every block, in
this case position 7. Around 50% bits changed
2 Randomizing sboxes : output for randomized sboxes for 3 sets.
3.Confusion : 50 % bits of ciphertext changed
