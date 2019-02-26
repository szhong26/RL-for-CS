# RL-for-CS

# Introduction
The code in this repository contains a single GPU implementation of Alphazero for solving the Compressed Sensing Problem. Given a fixed(or unfixed) matrix A of size m by n, m<<n, , and an observed vector y = Ax, where x is an unknown k-sparse vector, Alphazero attempts to iteratively pick the k support locations of x. 
# File Explanation
"alphazero_compressedsensing_nonoise_hierarchical" and "alphazero_compressedsensing_nonoise_hierarchical_v2" are the current most stable versions. The difference between these two is that v2(the second file) contains functionality for hierarchical learning and code for manipulating the Monte Carlo Tree during training. 

"current_version/alphazero_compressedsensing_nonoise_hierarchical_v2" is the most recent code(which may contain bugs) which provides optimizations for GPU and CPU usage. The goal is to add functionality for parallel MCTS simulations and move linear algebra computations and Monte Carlo Tree Search over to the GPU. 
# Contact
If there are any questions, please email me at sichen.zhong@stonybrook.edu
