# arrowey   
An easy, 2D esolang made from an almost-unreadable programming language, both implemented in this repo.   
*Do not clone the repo to try to run arrowey in a production environment, the code **will** have problems and 
**will** crash sometimes because it is between versions!* If you wish to run arrowey, check out the releases page.   

There isn't really a "spec", there's only this implementation of arrowey, the spec is in my head. 
I'll write documentation later on, at first I want to get it into working shape 
(i.e. at least most syntax implemented in the parser and first run of a basic I/O and arithmetics program).   

   
*NOTE: I'm very irregularly working on this project as I don't always have time for it because of school...*   
   
   
# Notes about arrowey itself
* arrowey is a strongly-typed language, meaning that you have to explicitly convert variables to a different type to use 
them as that different type, ints and floats are the only exceptions from that rule and can e.g. directly be inserted 
used together in arithmetic operations without explicit conversion, in that case the operation always returns a float.
* If given, variable type assignments are strictly enforced. Untyped variables are technically typed `any` and can thus 
hold any type. Here, no exception for ints and floats is made, so you cannot assign an integer or float to a string-only
typed variable. You also can't assign a float to an int variable or vice versa, so keep that in mind when trying to do 
arithmetic with mixed numbers. 