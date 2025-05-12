# slowpoke 2
## Prerequisites
To understand this writeup, you should understand that the derivative of a function is the rate of change of said function, and that integration is the reverse of differentiation, i.e. the basic concepts of calculus.
## Writeup
This challenge gives you the rate of change of the state in terms of $x$. With calculus, you can integrate the rate of change to get $f(x)$.  
However, the rate of change is from $x$ to $x+1$. This is a discrete rate of change. Knowing this, you cannot use regular calculus. You have to use discrete calculus (integration) to calculate $f(x)$. Then just take $state-f(1337...36)+f(0)$ to recover flag.    

Solve script uses sagemath's built-in function to calculate the discrete integral, more commonly known as the discrete sum.