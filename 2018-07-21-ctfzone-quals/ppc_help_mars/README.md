# Help Mars, ppc+osint

It was a programming challenge, in which we had to find the shortest set of database strings (of which there
were a few millions), that concatenated together would give target string (that we had to find on the internet
as osint part of the challenge). The strings weren't very long; around 100 characters each, and the target string
was two orders of magnitude longer. Simple brute force wouldn't work.

Instead, we opted for dynamic programming solution: for each substring of the target, we calculated the minimal
solution by brute forcing first division point and fetching subproblem solution from memoized array. This gave
us runtime of `O(N*N*M)`, where `N` is length of the target, and `M` - maximum length of database strings (with
possibly some logarithmic overhead from Python data structures). Full code attached.
