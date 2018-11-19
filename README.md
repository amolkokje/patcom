
In a loop, there has to be atleast 4 iterations to justify the conversion
Remove the last iteration of the loop, to use with the Start, Stop instructions
Here, I have described a very basic example of how my algorith implementation works

## No Repeats - Example
NOP v0
NOP v1
NOP v2
NOP v1
NOP v2
NOP v1
NOP v2
NOP v1
NOP v2
NOP v1
NOP v2
EXIT v3

STI 3 v1  # Loop Count - 1
L:
NOP v2
JNI L v1  # Last iteration is not part of the loop 
NOP v2

## Example - Repeats in the beginning only

IDXI 3 v1
NOP v2
IDXI 3 v1
NOP v2
IDXI 3 v1
NOP v2
IDXI 3 v1
NOP v2

STI 3 v1  # Loop Count - 1 
L:
IDXI 2 v1  # Repeat Count - 1 of beginning
NOP v2
JNI L v1  # Last iteration is not part of the loop
IDXI 2 v1  # Repeat Count - 1
NOP v2

## Example - Repeats in the end only

NOP v1
IDXI 3 v2
NOP v1
IDXI 3 v2
NOP v1
IDXI 3 v2
NOP v1
IDXI 3 v2

STI 3 v1  # Loop Count -1
L:
IDXI 3 v2  # Repeat Count of ending, ending vector as is
JNI L v1  # Last iteration is not part of the loop
IDXI 3 v2 

## Example - Repeats in the beginning and ending both

IDXI 3 v1
IDXI 4 v2
IDXI 3 v1
IDXI 4 v2
IDXI 3 v1
IDXI 4 v2
IDXI 3 v1
IDXI 4 v2
IDXI 3 v1
IDXI 4 v2

STI 3 v1  # Loop Count -1 
L:
IDXI 2 v1  # Repeat Count -1 of the beginning
IDXI 4 v2  # Repeat Count of the ending, ending vector as is
JNI L v1
IDXI 2 v1  # Repeat Count -1 of the beginning
IDXI 4 v2  # Repeat Count of the ending, ending vector as is
