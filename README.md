# Hybrid-Algo-for-sequence-alignment

- The Sequence Alignment problem is one of the fundamental problems of Biological Sciences, aimed at finding the similarity of two amino-acid sequences. Comparing amino-acids is of prime importance to humans, since it gives vital information on evolution and development. Saul B. Needleman and Christian D. Wunsch devised a dynamic programming algorithm to the problem and got it published in 1970. Since then, numerous improvements have been made to improve the time complexity and space complexity.

- In this project, a hybrid solution using Divide & Conquer and Dynamic Programming to find the optimal alignment between two DNA has been devised.

- Memory efficient DP solution using only 2*n matrix, where each row is alternately calculated using previous row.

- Divide and Conquer approach is combined with DP to regenerate optimal alignment by backtracking and adding subproblem outputs. Model
performs with a computation of run time O(n*m) and space complexity O(n+m).

