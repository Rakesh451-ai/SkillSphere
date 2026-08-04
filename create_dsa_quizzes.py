import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
django.setup()

from django.utils import timezone
from dashboard.models import Quiz, QuizQuestion

def seed_quizzes():
    now = timezone.now()
    start_time = now - timedelta(days=1)
    end_time = now + timedelta(days=365)

    # 15 Topics with 25 questions each = 375 questions total
    quiz_data = [
        {
            "topic": "Array",
            "title": "Array Data Structure & Algorithmic Patterns Quiz",
            "description": "Master array memory layouts, 2-pointers, prefix sums, sliding window arrays, and multidimensional arrays from basic to advanced.",
            "questions": [
                {
                    "q": "1. What is the time complexity to access an element at index i in a standard static array of size N?",
                    "type": "single", "a": "O(N)", "b": "O(log N)", "c": "O(1)", "d": "O(N^2)", "ans": "C",
                    "exp": "Arrays store elements in contiguous memory. Address is computed in O(1) time using BaseAddress + i * ElementSize."
                },
                {
                    "q": "2. What is the worst-case time complexity of inserting an element at the beginning (index 0) of an array of size N?",
                    "type": "single", "a": "O(1)", "b": "O(N)", "c": "O(log N)", "d": "O(N log N)", "ans": "B",
                    "exp": "All N existing elements must be shifted right by one position, requiring O(N) operations."
                },
                {
                    "q": "3. In dynamic arrays (e.g. C++ vector, Python list), what is the amortized time complexity of appending an element to the end?",
                    "type": "single", "a": "O(1)", "b": "O(N)", "c": "O(N^2)", "d": "O(log N)", "ans": "A",
                    "exp": "Although resizing requires doubling capacity (O(N)), it occurs infrequently. The overall cost averaged over N appends is O(1) amortized."
                },
                {
                    "q": "4. Which property of arrays makes them extremely efficient for CPU execution compared to linked lists?",
                    "type": "single", "a": "Non-linear layout", "b": "Spatial Cache Locality", "c": "Dynamic pointer links", "d": "Automatic garbage collection", "ans": "B",
                    "exp": "Contiguous memory layout maximizes CPU L1/L2 cache line prefetches, minimizing cache misses."
                },
                {
                    "q": "5. Given a 2D array of dimensions R x C stored in row-major order, what is the formula for the offset of element at row i, col j?",
                    "type": "single", "a": "i * C + j", "b": "j * R + i", "c": "(i + j) * C", "d": "i * R + j", "ans": "A",
                    "exp": "In row-major ordering, row i skips i full rows of size C, so offset = i * C + j."
                },
                {
                    "q": "6. What technique computes the sum of any contiguous subarray [L, R] in O(1) time after O(N) preprocessing?",
                    "type": "single", "a": "Monotonic Stack", "b": "Prefix Sum Array", "c": "Binary Search", "d": "Two Pointers inward", "ans": "B",
                    "exp": "Sum(L, R) = Prefix[R] - Prefix[L-1]. After precomputing prefix sums in O(N), queries run in O(1)."
                },
                {
                    "q": "7. In a sorted array of N distinct elements, what is the maximum number of comparisons needed to search for a key using Binary Search?",
                    "type": "single", "a": "N", "b": "N/2", "c": "floor(log2(N)) + 1", "d": "N^2", "ans": "C",
                    "exp": "Binary search halves the search space each step, yielding floor(log2 N) + 1 maximum comparisons."
                },
                {
                    "q": "8. Which algorithm finds the maximum subarray sum in linear O(N) time?",
                    "type": "single", "a": "Kadane's Algorithm", "b": "Floyd's Cycle Algorithm", "c": "Dijkstra's Algorithm", "d": "KMP Algorithm", "ans": "A",
                    "exp": "Kadane's algorithm maintains running max_ending_here = max(arr[i], max_ending_here + arr[i]) in O(N) time."
                },
                {
                    "q": "9. What is the space complexity of reversing an array in-place using two pointers?",
                    "type": "single", "a": "O(N)", "b": "O(1)", "c": "O(log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "Swapping elements at left and right pointers inward modifies the existing array using O(1) extra space."
                },
                {
                    "q": "10. In the 'Dutch National Flag' algorithm (sorting 0s, 1s, 2s), how many pointers are maintained?",
                    "type": "single", "a": "1", "b": "2", "c": "3", "d": "4", "ans": "C",
                    "exp": "It maintains low, mid, and high pointers to partition elements into 0s, 1s, and 2s in a single O(N) pass."
                },
                {
                    "q": "11. If an array of size N contains numbers from 1 to N with one missing number, how can you find it in O(N) time and O(1) space?",
                    "type": "single", "a": "Sort and check", "b": "Sum formula N*(N+1)/2 minus actual sum", "c": "Hash table lookup", "d": "Nested loop search", "ans": "B",
                    "exp": "The sum of 1 to N is N*(N+1)/2. Subtracting the actual array sum yields the missing number in O(N) time & O(1) space."
                },
                {
                    "q": "12. What is the worst-case space complexity of storing a sparse matrix using a standard 2D array of size M x N?",
                    "type": "single", "a": "O(K) where K is non-zeros", "b": "O(M + N)", "c": "O(M * N)", "d": "O(1)", "ans": "C",
                    "exp": "A standard 2D array allocates memory for all M*N entries, even if most elements are zero."
                },
                {
                    "q": "13. In the 2Sum problem (find 2 elements in sorted array summing to Target), what is the optimal time & space complexity using Two Pointers?",
                    "type": "single", "a": "O(N) time, O(1) space", "b": "O(N log N) time, O(N) space", "c": "O(N^2) time, O(1) space", "d": "O(1) time, O(N) space", "ans": "A",
                    "exp": "With left=0 and right=N-1 pointers on a sorted array, moving inward takes O(N) time and O(1) extra space."
                },
                {
                    "q": "14. How can you rotate an array of N elements to the right by K steps in O(N) time and O(1) auxiliary space?",
                    "type": "single", "a": "Reverse full array, then reverse first K elements, then reverse remaining N-K elements", "b": "Create auxiliary array", "c": "Shift one-by-one K times", "d": "Sort the array", "ans": "A",
                    "exp": "3-step array reversal rotates in-place in linear O(N) time and constant O(1) space."
                },
                {
                    "q": "15. What is the worst-case time complexity of Majority Element algorithm (Boyer-Moore Voting Algorithm)?",
                    "type": "single", "a": "O(N^2)", "b": "O(N log N)", "c": "O(N)", "d": "O(2^N)", "ans": "C",
                    "exp": "Boyer-Moore Voting algorithm finds candidate majority element in 1 pass O(N) time and O(1) auxiliary space."
                },
                {
                    "q": "16. In 2D Matrix binary search on a sorted matrix of size M x N where matrix[i][j] < matrix[i][j+1] and matrix[i][C-1] < matrix[i+1][0], how is 1D index mid mapped to (row, col)?",
                    "type": "single", "a": "row = mid // N, col = mid % N", "b": "row = mid % M, col = mid // M", "c": "row = mid // M, col = mid % M", "d": "row = mid * N, col = mid + N", "ans": "A",
                    "exp": "Virtual 1D array of length M*N maps index to 2D coordinates via row = mid // N and col = mid % N."
                },
                {
                    "q": "17. What is the time complexity to find the median of two sorted arrays of sizes M and N using binary search on partitions?",
                    "type": "single", "a": "O(M + N)", "b": "O(log(min(M, N)))", "c": "O(M * N)", "d": "O(min(M, N))", "ans": "B",
                    "exp": "Binary search on partition point of smaller array runs in logarithmic O(log(min(M, N))) time."
                },
                {
                    "q": "18. What is the maximum number of contiguous subarrays in an array of size N?",
                    "type": "single", "a": "N", "b": "2^N", "c": "N * (N + 1) / 2", "d": "N!", "ans": "C",
                    "exp": "Choosing start L and end R indices yields N + (N-1) + ... + 1 = N*(N+1)/2 contiguous subarrays."
                },
                {
                    "q": "19. Which array operation requires O(N) time even in a sorted array?",
                    "type": "single", "a": "Binary Search", "b": "Finding Min/Max", "c": "Inserting a new element while preserving sorted order", "d": "Accessing element at index 0", "ans": "C",
                    "exp": "Inserting into a sorted array requires shifting elements to make room, taking O(N) worst-case time."
                },
                {
                    "q": "20. In Trapping Rain Water problem, what is the optimal time and space complexity using two pointers?",
                    "type": "single", "a": "O(N) time, O(1) space", "b": "O(N^2) time, O(N) space", "c": "O(N log N) time, O(1) space", "d": "O(N) time, O(N) space", "ans": "A",
                    "exp": "Two pointers maintaining left_max and right_max calculate trapped water in a single linear pass."
                },
                {
                    "q": "21. What does Product of Array Except Self problem require to achieve O(N) time without using division operation?",
                    "type": "single", "a": "Sorting array", "b": "Prefix products and Suffix products accumulation", "c": "Binary Search", "d": "Bitwise XOR", "ans": "B",
                    "exp": "Accumulating prefix products in one pass and suffix products in reverse pass yields answer in O(N) without division."
                },
                {
                    "q": "22. In Next Permutation algorithm, what is the first step to find lexicographically next greater permutation of an array?",
                    "type": "single", "a": "Reverse entire array", "b": "Find first decreasing element arr[i] from right where arr[i] < arr[i+1]", "c": "Sort array in ascending order", "d": "Swap first and last elements", "ans": "B",
                    "exp": "Scan from right to find pivot arr[i] < arr[i+1], then swap with next larger element on right and reverse suffix."
                },
                {
                    "q": "23. In an array of size N, what is the total number of non-empty subsequences?",
                    "type": "single", "a": "N*(N+1)/2", "b": "2^N - 1", "c": "N!", "d": "2*N", "ans": "B",
                    "exp": "Each element can either be included or excluded (2^N combinations), excluding empty set gives 2^N - 1."
                },
                {
                    "q": "24. What is the time complexity of 3Sum problem using sorting and two pointers?",
                    "type": "single", "a": "O(N^3)", "b": "O(N^2)", "c": "O(N log N)", "d": "O(N)", "ans": "B",
                    "exp": "Sorting takes O(N log N). Fixing 1 outer element and running 2 pointers inward takes O(N) per outer element, giving O(N^2) total."
                },
                {
                    "q": "25. In monotonic array checking, what is the best time complexity to determine if an array is strictly increasing or decreasing?",
                    "type": "single", "a": "O(1)", "b": "O(N)", "c": "O(N log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "A single linear pass scanning adjacent elements arr[i] vs arr[i+1] checks monotonicity in O(N) time."
                }
            ]
        },
        {
            "topic": "String",
            "title": "String Processing & Pattern Matching Algorithms Quiz",
            "description": "Master string immutability, pattern matching (KMP, Rabin-Karp, Z-algorithm), palindromic expansions, string building, and text parsing.",
            "questions": [
                {
                    "q": "1. What is the time complexity of checking if two strings of length N are anagrams using character frequency arrays?",
                    "type": "single", "a": "O(N log N)", "b": "O(N)", "c": "O(N^2)", "d": "O(1)", "ans": "B",
                    "exp": "Increment frequencies for string 1 and decrement for string 2 in a single pass of size N (O(N) time, O(1) char space)."
                },
                {
                    "q": "2. In Java / Python, strings are immutable. What does string concatenation s += 'a' inside a loop of size N cost overall in time?",
                    "type": "single", "a": "O(N)", "b": "O(N log N)", "c": "O(N^2)", "d": "O(1)", "ans": "C",
                    "exp": "Creating a new string buffer of length i at iteration i results in sum(1..N) = O(N^2) total work."
                },
                {
                    "q": "3. What auxiliary structure is recommended to perform efficient repeated string concatenations in Java/Python?",
                    "type": "single", "a": "Array of chars / StringBuilder", "b": "Immutable String", "c": "Linked List of nodes", "d": "Stack", "ans": "A",
                    "exp": "StringBuilder or list of characters appends in amortized O(1) time per operation, achieving total linear O(N) time."
                },
                {
                    "q": "4. What is the worst-case time complexity of Brute Force pattern matching of pattern P (len M) in text T (len N)?",
                    "type": "single", "a": "O(N + M)", "b": "O(N * M)", "c": "O(N log M)", "d": "O(M)", "ans": "B",
                    "exp": "At each of the N positions in text, comparing M characters takes O(M) operations in worst case (e.g. T='AAAAA', P='AAB')."
                },
                {
                    "q": "5. What array precomputed by KMP algorithm allows skipping unnecessary re-comparisons during pattern search?",
                    "type": "single", "a": "Z-array", "b": "Longest Prefix Suffix (LPS) / Failure Function", "c": "Prefix sum", "d": "Frequency table", "ans": "B",
                    "exp": "LPS array stores the length of the longest proper prefix that is also a suffix, enabling O(N + M) KMP matching."
                },
                {
                    "q": "6. What is the time complexity to construct the LPS array in KMP algorithm for pattern of length M?",
                    "type": "single", "a": "O(M^2)", "b": "O(M)", "c": "O(M log M)", "d": "O(2^M)", "ans": "B",
                    "exp": "Preprocessing the LPS array takes linear O(M) time by maintaining a matching prefix pointer."
                },
                {
                    "q": "7. What hashing technique does Rabin-Karp algorithm use to update substring hash in O(1) time while sliding a window across text?",
                    "type": "single", "a": "Cryptographic SHA256", "b": "Rolling Polynomial Hash", "c": "MD5 Hash", "d": "Static Modulo", "ans": "B",
                    "exp": "Rolling hash subtracts leaving char * p^(M-1) and adds entering char in O(1) time per window slide."
                },
                {
                    "q": "8. What algorithm finds the longest palindromic substring in strictly linear O(N) time?",
                    "type": "single", "a": "Manacher's Algorithm", "b": "KMP Algorithm", "c": "Kadane's Algorithm", "d": "Dijkstra's Algorithm", "ans": "A",
                    "exp": "Manacher's algorithm utilizes mirror symmetry across palindrome centers to compute all palindrome radii in O(N) time."
                },
                {
                    "q": "9. In Manacher's algorithm, why are special separator characters (like '#') inserted between string characters?",
                    "type": "single", "a": "To encrypt the string", "b": "To treat even-length and odd-length palindromes uniformly", "c": "To increase string speed", "d": "To avoid hash collisions", "ans": "B",
                    "exp": "Transforming 'aba' to '#a#b#a#' ensures all palindromes become odd length around a single center node."
                },
                {
                    "q": "10. What does Z[i] represent in the Z-Algorithm for string processing?",
                    "type": "single", "a": "Length of longest substring starting at index i matching prefix of string S", "b": "Count of vowels", "c": "Hash value at i", "d": "Index of next character", "ans": "A",
                    "exp": "Z-array entry Z[i] stores the length of the longest common prefix between S and the suffix of S starting at i."
                },
                {
                    "q": "11. What is the overall time complexity of Z-Algorithm to build Z-array for string of length N?",
                    "type": "single", "a": "O(N^2)", "b": "O(N log N)", "c": "O(N)", "d": "O(2^N)", "ans": "C",
                    "exp": "Z-algorithm maintains rightmost matching window boundary [L, R], achieving linear O(N) computation."
                },
                {
                    "q": "12. In Minimum Window Substring problem (find min window in S containing all chars of T), what algorithm pattern is optimal?",
                    "type": "single", "a": "Dynamic Programming Matrix", "b": "Sliding Window with Character Frequency Map", "c": "Depth First Search", "d": "Quick Sort", "ans": "B",
                    "exp": "Expanding right pointer and shrinking left pointer while tracking required character frequencies runs in O(|S| + |T|) time."
                },
                {
                    "q": "13. What is the time complexity of reversing words in a string of length N in-place?",
                    "type": "single", "a": "O(N log N)", "b": "O(N)", "c": "O(N^2)", "d": "O(1)", "ans": "B",
                    "exp": "Reversing full string then reversing individual words in-place takes two passes of linear O(N) time."
                },
                {
                    "q": "14. How many distinct non-empty substrings can be formed from a string of length N with distinct characters?",
                    "type": "single", "a": "2^N - 1", "b": "N * (N + 1) / 2", "c": "N!", "d": "N^2", "ans": "B",
                    "exp": "Substrings are contiguous. Selecting start and end positions yields N*(N+1)/2 distinct substrings."
                },
                {
                    "q": "15. In Longest Common Prefix problem among array of K strings of max length L, what is the worst-case time complexity using horizontal scanning?",
                    "type": "single", "a": "O(K * L)", "b": "O(K^2 * L)", "c": "O(L log K)", "d": "O(K + L)", "ans": "A",
                    "exp": "Comparing strings sequentially scans up to L characters across K strings, taking O(K * L) operations."
                },
                {
                    "q": "16. In Run-Length Encoding (compression), string 'AAABBC' compresses to:",
                    "type": "single", "a": "A3B2C1", "b": "ABC321", "c": "3A2B1C", "d": "A3B2C", "ans": "A",
                    "exp": "Consecutive repeated characters are replaced by character followed by count: A3B2C1 (or A3B2C)."
                },
                {
                    "q": "17. What is the time complexity of checking if string S is a rotation of string T of length N?",
                    "type": "single", "a": "O(N^2)", "b": "Check if length matches AND T is substring of S+S in O(N) time", "c": "O(N log N)", "d": "O(2^N)", "ans": "B",
                    "exp": "S+S contains all possible rotations of S. Checking if T is substring of S+S takes linear O(N) time."
                },
                {
                    "q": "18. What data structure allows finding all matching occurrences of K patterns in text T (len N) simultaneously in O(N + total_matches) time?",
                    "type": "single", "a": "Aho-Corasick Automaton", "b": "Binary Search Tree", "c": "Monotonic Stack", "d": "Heap", "ans": "A",
                    "exp": "Aho-Corasick builds failure links on a Trie of patterns, processing text in single O(N) linear sweep."
                },
                {
                    "q": "19. In Suffix Automaton, what is the maximum number of states for a string of length N > 2?",
                    "type": "single", "a": "2^N", "b": "2N - 1", "c": "N^2", "d": "N log N", "ans": "B",
                    "exp": "Suffix Automaton is a highly compact representation of all substrings of S with at most 2N-1 states and 3N-4 transitions."
                },
                {
                    "q": "20. What is the space complexity to store a Trie containing N words of average length L with lowercase English alphabet?",
                    "type": "single", "a": "O(N * L * 26)", "b": "O(N + L)", "c": "O(26^L)", "d": "O(1)", "ans": "A",
                    "exp": "Each Trie node contains an array of size 26 (alphabet size). Total nodes bounded by N * L, giving O(N * L * 26)."
                },
                {
                    "q": "21. What is the main cause of Hash Collisions in Rabin-Karp algorithm?",
                    "type": "single", "a": "Choosing alphabet size 26", "b": "Two different substrings producing identical numerical hash modulo M", "c": "Invalid string index", "d": "Unsorted string input", "ans": "B",
                    "exp": "Because infinite strings map to finite hash values under modulo M, different strings can produce equal hash values."
                },
                {
                    "q": "22. In Isomorphic Strings problem ('egg' and 'add'), two strings are isomorphic if:",
                    "type": "single", "a": "They have equal vowel count", "b": "Characters in S can be replaced to get T with a 1-to-1 unique mapping", "c": "They are reverse of each other", "d": "They have equal length", "ans": "B",
                    "exp": "Every character in S must map uniquely to a character in T with no two characters mapping to same target."
                },
                {
                    "q": "23. In Edit Distance (Levenshtein Distance) between string S (len M) and T (len N), what operations are allowed?",
                    "type": "single", "a": "Insert, Delete, Replace", "b": "Swap only", "c": "Append only", "d": "Reverse only", "ans": "A",
                    "exp": "Standard Levenshtein edit distance computes minimum insertions, deletions, or substitutions to transform S to T."
                },
                {
                    "q": "24. What is the time complexity of computing Edit Distance using 2D Dynamic Programming matrix?",
                    "type": "single", "a": "O(M + N)", "b": "O(M * N)", "c": "O(2^(M+N))", "d": "O(M^2)", "ans": "B",
                    "exp": "DP matrix of size (M+1) x (N+1) fills each state in O(1) time, yielding O(M * N) time."
                },
                {
                    "q": "25. Which string comparison algorithm is invariant to case sensitivity and extra whitespace when parsing tokens?",
                    "type": "single", "a": "Lexicographical strcmp", "b": "Normalized Tokenization & Trim String processing", "c": "Raw Byte comparison", "d": "CRC32 Checksum", "ans": "B",
                    "exp": "Trimming whitespace and lowercasing strings before tokenization standardizes comparisons across variations."
                }
            ]
        },
        {
            "topic": "Pointer",
            "title": "Pointers, Memory Allocation & Address Arithmetic Quiz",
            "description": "Master memory addresses, pointer arithmetic, double pointers, reference safety, heap vs stack memory, dynamic allocation, and memory leaks.",
            "questions": [
                {
                    "q": "1. What does a pointer variable store in C / C++?",
                    "type": "single", "a": "Integer value of variable", "b": "Memory address of another variable", "c": "Character ASCII code", "d": "Float value", "ans": "B",
                    "exp": "A pointer variable stores the memory address location where another variable resides."
                },
                {
                    "q": "2. Given int *ptr and sizeof(int) = 4, if ptr holds address 0x1000, what is the value of (ptr + 2)?",
                    "type": "single", "a": "0x1002", "b": "0x1004", "c": "0x1008", "d": "0x1016", "ans": "C",
                    "exp": "Pointer arithmetic scales addition by target type size: 0x1000 + 2 * sizeof(int) = 0x1000 + 8 = 0x1008."
                },
                {
                    "q": "3. What does dereferencing a pointer (*ptr) perform?",
                    "type": "single", "a": "Retrieves the memory address", "b": "Accesses the actual value stored at the address ptr points to", "c": "Deletes the pointer", "d": "Doubles the address", "ans": "B",
                    "exp": "The dereference operator '*' accesses or modifies the value located at the address held in ptr."
                },
                {
                    "q": "4. What is a 'Dangling Pointer'?",
                    "type": "single", "a": "A pointer initialized to NULL", "b": "A pointer referencing a memory location that has been deallocated/freed", "c": "A pointer pointing to constant string", "d": "A pointer to function", "ans": "B",
                    "exp": "Dangling pointers point to memory that was freed or went out of scope, causing undefined behavior on dereference."
                },
                {
                    "q": "5. What is a 'Null Pointer'?",
                    "type": "single", "a": "Pointer holding address 0 (nullptr) indicating it points to no valid memory", "b": "Pointer pointing to random address", "c": "Pointer in stack", "d": "Double pointer", "ans": "A",
                    "exp": "NULL / nullptr signifies an unassigned pointer pointing to no valid memory object."
                },
                {
                    "q": "6. What operator is used to get the memory address of an existing variable in C/C++?",
                    "type": "single", "a": "* operator", "b": "& (Address-of operator)", "c": "-> operator", "d": "% operator", "ans": "B",
                    "exp": "The address-of operator '&' returns the memory address location of a variable."
                },
                {
                    "q": "7. What is a 'Memory Leak' in C / C++?",
                    "type": "single", "a": "Reading uninitialized memory", "b": "Dynamically allocated heap memory (malloc/new) that is no longer accessible and never freed", "c": "Stack overflow", "d": "Writing past array bounds", "ans": "B",
                    "exp": "Failing to free dynamically allocated heap memory prevents memory reuse, leading to leaks."
                },
                {
                    "q": "8. What does double pointer int **ptr store?",
                    "type": "single", "a": "Address of an integer", "b": "Address of another pointer variable (pointer to pointer)", "c": "Two integers", "d": "Address of array end", "ans": "B",
                    "exp": "int **ptr stores the memory address of a pointer variable that points to an int."
                },
                {
                    "q": "9. In C, what function allocates requested bytes of uninitialized heap memory and returns a void pointer?",
                    "type": "single", "a": "calloc()", "b": "malloc()", "c": "realloc()", "d": "free()", "ans": "B",
                    "exp": "malloc(size) allocates requested bytes on heap without initializing memory contents."
                },
                {
                    "q": "10. How does calloc(n, size) differ from malloc(n * size)?",
                    "type": "single", "a": "calloc allocates faster", "b": "calloc initializes allocated memory bytes to zero", "c": "malloc clears memory", "d": "calloc allocates on stack", "ans": "B",
                    "exp": "calloc initializes all allocated bytes to zero; malloc leaves memory filled with garbage values."
                },
                {
                    "q": "11. What operator replaces (*ptr).member in C/C++ for structure pointers?",
                    "type": "single", "a": ". (dot operator)", "b": "-> (arrow operator)", "c": ":: (scope operator)", "d": "=> operator", "ans": "B",
                    "exp": "The arrow operator ptr->member is syntactic shortcut for dereferencing and accessing structure member (*ptr).member."
                },
                {
                    "q": "12. What happens when you attempt to dereference a NULL pointer (*nullptr)?",
                    "type": "single", "a": "Returns 0", "b": "Segmentation Fault / Crash (Undefined Behavior)", "c": "Allocates new memory", "d": "Returns garbage value", "ans": "B",
                    "exp": "Dereferencing NULL triggers access violation causing Segmentation Fault."
                },
                {
                    "q": "13. What is the size of a pointer variable (e.g. char*, int*, double*) on a 64-bit operating system architecture?",
                    "type": "single", "a": "1 byte", "b": "4 bytes", "c": "8 bytes", "d": "16 bytes", "ans": "C",
                    "exp": "On 64-bit systems, all pointers require 64 bits (8 bytes) to store memory addresses, regardless of target type."
                },
                {
                    "q": "14. What is a 'Wild Pointer'?",
                    "type": "single", "a": "A pointer initialized to NULL", "b": "An uninitialized pointer storing random garbage memory address", "c": "Pointer to void", "d": "Smart pointer", "ans": "B",
                    "exp": "Uninitialized pointers hold arbitrary memory addresses; dereferencing them is dangerous."
                },
                {
                    "q": "15. How can you pass a pointer by reference to a function in C to modify the original pointer itself?",
                    "type": "single", "a": "Pass single pointer int *ptr", "b": "Pass double pointer int **ptr_to_ptr", "c": "Pass variable value int x", "d": "Pass void pointer", "ans": "B",
                    "exp": "Passing double pointer int **ptr allows modifying the original pointer address inside caller scope."
                },
                {
                    "q": "16. In C++, what smart pointer type manages exclusive ownership of dynamic heap memory and prevents copy assignment?",
                    "type": "single", "a": "std::shared_ptr", "b": "std::unique_ptr", "c": "std::weak_ptr", "d": "raw pointer", "ans": "B",
                    "exp": "std::unique_ptr owns heap object exclusively and deallocates automatically when going out of scope."
                },
                {
                    "q": "17. What smart pointer maintains a reference count of owners sharing heap memory in C++?",
                    "type": "single", "a": "std::unique_ptr", "b": "std::shared_ptr", "c": "raw pointer", "d": "void*", "ans": "B",
                    "exp": "std::shared_ptr uses reference counter, deleting managed object when count reaches zero."
                },
                {
                    "q": "18. What issue occurs when two std::shared_ptr instances reference each other cyclically?",
                    "type": "single", "a": "Segmentation Fault", "b": "Cyclic Reference Memory Leak (Reference count never hits 0)", "c": "Stack Overflow", "d": "Compilation Error", "ans": "B",
                    "exp": "Cyclic references prevent reference count from reaching 0, causing memory leak. std::weak_ptr breaks cycles."
                },
                {
                    "q": "19. In array decay: when array name 'arr' is passed to a function void foo(int arr[]), what does 'arr' decay into inside foo?",
                    "type": "single", "a": "Full array copy", "b": "Pointer to first element int* arr", "c": "Reference to 2D matrix", "d": "Constant integer", "ans": "B",
                    "exp": "Arrays decay to pointer to first element when passed as function parameters, losing sizeof array length."
                },
                {
                    "q": "20. What is a 'Void Pointer' (void*) in C/C++?",
                    "type": "single", "a": "Pointer pointing to nothing", "b": "Generic pointer that can hold address of any data type without type information", "c": "Invalid pointer", "d": "Function pointer only", "ans": "B",
                    "exp": "void* is a generic raw address pointer; it must be type-cast before dereferencing."
                },
                {
                    "q": "21. What is the result of subtracting two pointers pointing to elements in the same array: (ptr2 - ptr1)?",
                    "type": "single", "a": "Difference in raw byte addresses", "b": "Number of elements between ptr1 and ptr2 (ptrdiff_t)", "c": "Product of addresses", "d": "Invalid operation", "ans": "B",
                    "exp": "Subtracting two pointers of same type returns the count of elements between them."
                },
                {
                    "q": "22. What does function pointer syntax int (*func_ptr)(int, int) declare?",
                    "type": "single", "a": "Function returning pointer to int", "b": "Pointer variable func_ptr to a function taking two ints and returning int", "c": "Array of functions", "d": "Macro definition", "ans": "B",
                    "exp": "int (*func_ptr)(int, int) declares pointer holding executable code address of function with matching signature."
                },
                {
                    "q": "23. In C++, what operator is used to allocate memory on heap and invoke constructor?",
                    "type": "single", "a": "malloc", "b": "new operator", "c": "calloc", "d": "alloc", "ans": "B",
                    "exp": "new operator allocates heap space and calls constructor; delete calls destructor and frees heap."
                },
                {
                    "q": "24. What happens when calling free(ptr) on a memory pointer that was ALREADY freed?",
                    "type": "single", "a": "Nothing happens", "b": "Double Free Vulnerability / Undefined Behavior crash", "c": "Reallocates memory", "d": "Clears stack", "ans": "B",
                    "exp": "Double freeing heap memory corrupts heap metadata allocator state, leading to crashes or security flaws."
                },
                {
                    "q": "25. Which memory area stores local function variables, parameter pointers, and return addresses?",
                    "type": "single", "a": "Heap Memory", "b": "Stack Memory", "c": "BSS Data Segment", "d": "Text Segment", "ans": "B",
                    "exp": "Stack memory manages local stack frames, automatically allocating on function entry and freeing on exit."
                }
            ]
        },
        {
            "topic": "Recursion",
            "title": "Recursion, Backtracking & Recurrence Relations Quiz",
            "description": "Master call stack frames, base cases, tail recursion, state space trees, divide and conquer, Master Theorem, and backtracking pruning.",
            "questions": [
                {
                    "q": "1. What mandatory component must every recursive function possess to prevent infinite execution?",
                    "type": "single", "a": "Loop counter", "b": "Base Case", "c": "Global variable", "d": "Pointer parameter", "ans": "B",
                    "exp": "The base case provides termination conditions where the function returns without making further recursive calls."
                },
                {
                    "q": "2. What error occurs when a recursive function lacks a valid base case or recurses too deeply?",
                    "type": "single", "a": "Segmentation Fault / Stack Overflow", "b": "Heap Leak", "c": "Deadlock", "d": "Null Pointer Exception", "ans": "A",
                    "exp": "Each recursive call consumes a call stack frame; exceeding stack limit causes Stack Overflow."
                },
                {
                    "q": "3. What is 'Tail Recursion'?",
                    "type": "single", "a": "Recursion inside a loop", "b": "Recursive call is the absolute final action performed in the function", "c": "Recursion with multiple base cases", "d": "Recursion returning void", "ans": "B",
                    "exp": "In tail recursion, no operations remain after the recursive call, allowing compilers to reuse stack frames."
                },
                {
                    "q": "4. Why is Tail Call Optimization (TCO) beneficial?",
                    "type": "single", "a": "Reduces time to O(1)", "b": "Reuses current stack frame, reducing auxiliary stack space from O(N) to O(1)", "c": "Eliminates variables", "d": "Prevents heap allocation", "ans": "B",
                    "exp": "TCO converts tail-recursive functions into iterative loops, avoiding call stack buildup."
                },
                {
                    "q": "5. What is the time complexity of naive recursive Fibonacci calc(N) = calc(N-1) + calc(N-2)?",
                    "type": "single", "a": "O(N)", "b": "O(N^2)", "c": "O(2^N) or O(1.618^N)", "d": "O(log N)", "ans": "C",
                    "exp": "Naive Fibonacci generates a binary call tree of height N, resulting in exponential O(2^N) calls due to redundant calculations."
                },
                {
                    "q": "6. What technique caches the results of expensive recursive calls to reduce time complexity from exponential to linear?",
                    "type": "single", "a": "Backtracking", "b": "Memoization (Top-Down Dynamic Programming)", "c": "Tail Call", "d": "Bit masking", "ans": "B",
                    "exp": "Memoization stores subproblem solutions in a hash map/array, reusing cached answers in O(1) time."
                },
                {
                    "q": "7. What recurrence relation T(N) = 2 T(N/2) + O(N) represents Merge Sort?",
                    "type": "single", "a": "T(N) = O(N)", "b": "T(N) = O(N log N)", "c": "T(N) = O(N^2)", "d": "T(N) = O(log N)", "ans": "B",
                    "exp": "By Master Theorem case 2, dividing into 2 halves with linear merge cost yields O(N log N) time."
                },
                {
                    "q": "8. In Master Theorem formula T(N) = a T(N/b) + f(N), what does 'a' represent?",
                    "type": "single", "a": "Size of subproblems", "b": "Number of recursive subproblems generated at each step", "c": "Base case constant", "d": "Stack depth", "ans": "B",
                    "exp": "'a' is the number of subproblems spawned in each recursive step (a >= 1)."
                },
                {
                    "q": "9. What is the space complexity due to call stack for depth-first recursion of max tree height H?",
                    "type": "single", "a": "O(1)", "b": "O(H)", "c": "O(2^H)", "d": "O(H^2)", "ans": "B",
                    "exp": "The call stack holds at most H stack frames simultaneously at any point along a branch path."
                },
                {
                    "q": "10. What is the general 3-step paradigm of Backtracking algorithms?",
                    "type": "single", "a": "Sort, Search, Output", "b": "Make Choice -> Recurse -> Undo Choice (Backtrack)", "c": "Push, Pop, Peek", "d": "Divide, Conquer, Combine", "ans": "B",
                    "exp": "Backtracking explores state space trees by choosing a path, recursing, and reverting state upon reaching dead ends."
                },
                {
                    "q": "11. How many total permutations are explored in brute force recursion for an array of size N?",
                    "type": "single", "a": "2^N", "b": "N!", "c": "N^2", "d": "N log N", "ans": "B",
                    "exp": "Placing N distinct elements in N slots generates N * (N-1) * ... * 1 = N! total permutations."
                },
                {
                    "q": "12. How many subsets (power set) exist for a set of size N?",
                    "type": "single", "a": "N!", "b": "2^N", "c": "N*(N+1)/2", "d": "N^2", "ans": "B",
                    "exp": "Each element has 2 options (include or exclude), yielding 2^N total subsets."
                },
                {
                    "q": "13. In N-Queens problem on N x N board, what technique prunes invalid search branches early?",
                    "type": "single", "a": "Column/Diagonal Collision Checking Sets", "b": "Full Board Sorting", "c": "Binary Search", "d": "BFS Queue", "ans": "A",
                    "exp": "Tracking occupied columns and diagonals in O(1) lookup sets prunes illegal queen placements immediately."
                },
                {
                    "q": "14. In Sudoku Solver algorithm, what type of search strategy is utilized?",
                    "type": "single", "a": "Breadth First Search", "b": "Depth-First Search with Backtracking", "c": "Greedy Choice", "d": "Binary Search", "ans": "B",
                    "exp": "DFS with Backtracking fills empty cells recursively, backspacing when digit conflicts occur."
                },
                {
                    "q": "15. What is the difference between Direct and Indirect Recursion?",
                    "type": "single", "a": "Direct calls itself; Indirect function A calls function B which calls A", "b": "Direct uses stack; Indirect uses heap", "c": "Direct is tail recursive", "d": "No difference", "ans": "A",
                    "exp": "Direct recursion invokes the same function; Indirect recursion forms a cycle of function calls (A -> B -> A)."
                },
                {
                    "q": "16. In Tower of Hanoi problem with N disks, what is the minimum number of moves required?",
                    "type": "single", "a": "2N", "b": "2^N - 1", "c": "N^2", "d": "N!", "ans": "B",
                    "exp": "The recurrence T(N) = 2 T(N-1) + 1 resolves to T(N) = 2^N - 1 total moves."
                },
                {
                    "q": "17. What is the time complexity of Quick Select algorithm (find Kth smallest element) on average?",
                    "type": "single", "a": "O(N^2)", "b": "O(N log N)", "c": "O(N)", "d": "O(log N)", "ans": "C",
                    "exp": "Recurrence T(N) = T(N/2) + O(N) sums N + N/2 + N/4 + ... = O(N) average time complexity."
                },
                {
                    "q": "18. How can any recursive algorithm be converted into an non-recursive iterative algorithm?",
                    "type": "single", "a": "Using an explicit Stack data structure to simulate function call frames", "b": "Using Queue only", "c": "By sorting input", "d": "It is impossible", "ans": "A",
                    "exp": "Simulating the call stack using a custom Stack data structure converts any recursion to an iterative loop."
                },
                {
                    "q": "19. In Subset Sum problem (find subset summing to K), what is the time complexity of naive recursive backtracking?",
                    "type": "single", "a": "O(N)", "b": "O(2^N)", "c": "O(N^2)", "d": "O(N!)", "ans": "B",
                    "exp": "Exploring include/exclude decisions for N elements forms a binary recursion tree of size 2^N."
                },
                {
                    "q": "20. What is 'Branch and Bound' in optimization problems?",
                    "type": "single", "a": "A sorting method", "b": "Backtracking enhanced with upper/lower heuristic bounds to prune non-optimal subtrees", "c": "Tail recursion", "d": "Binary search", "ans": "B",
                    "exp": "Branch & Bound calculates cost bounds for state nodes, abandoning branches that cannot beat current best solution."
                },
                {
                    "q": "21. What happens to local variables of a function when a recursive call is invoked?",
                    "type": "single", "a": "Overwritten immediately", "b": "Pushed onto stack in new stack frame, preserving caller variables independently", "c": "Copied to heap", "d": "Cleared to 0", "ans": "B",
                    "exp": "Every invocation receives a distinct stack frame storing its own independent copy of local variables."
                },
                {
                    "q": "22. In Combination Sum problem (reuse numbers allowed), how do you prevent duplicate combinations in output?",
                    "type": "single", "a": "Sort array and start inner recursive loop from current index i instead of 0", "b": "Use 2D array", "c": "Reverse input", "d": "Use FIFO queue", "ans": "A",
                    "exp": "Passing start index i prevents choosing previously considered elements, avoiding duplicate combinations."
                },
                {
                    "q": "23. What is the time complexity of Word Search grid puzzle (word len L on M x N grid)?",
                    "type": "single", "a": "O(M * N * 3^L)", "b": "O(M * N * L)", "c": "O((M*N)^L)", "d": "O(4^L)", "ans": "A",
                    "exp": "For each of M*N cells, exploring 3 direction branches up to depth L takes O(M * N * 3^L) worst case."
                },
                {
                    "q": "24. In recursive binary search T(N) = T(N/2) + O(1), what is the maximum call stack depth for N elements?",
                    "type": "single", "a": "N", "b": "floor(log2 N) + 1", "c": "N / 2", "d": "N^2", "ans": "B",
                    "exp": "Halving search space at each call limits stack depth to floor(log2 N) + 1 frames."
                },
                {
                    "q": "25. Which problem cannot be solved using simple divide-and-conquer without memoization/tabulation due to overlapping subproblems?",
                    "type": "single", "a": "Merge Sort", "b": "Longest Common Subsequence", "c": "Binary Search", "d": "Quick Sort", "ans": "B",
                    "exp": "LCS contains overlapping subproblems; pure divide-and-conquer leads to exponential re-computation without caching."
                }
            ]
        },
        {
            "topic": "LinkedList",
            "title": "Singly, Doubly & Circular Linked List Master Quiz",
            "description": "Master dynamic node pointers, 3-pointer reversals, Floyd's cycle detection, fast/slow middle pointer, skip lists, and memory fragmentation.",
            "questions": [
                {
                    "q": "1. What is the primary advantage of a Linked List over a static Array?",
                    "type": "single", "a": "O(1) Random Access", "b": "Dynamic size allocation without contiguous memory requirements", "c": "Better cache locality", "d": "Smaller memory per element", "ans": "B",
                    "exp": "Linked list nodes are allocated dynamically on heap; elements do not require contiguous memory blocks."
                },
                {
                    "q": "2. What is the time complexity to insert a new node at the HEAD of a Singly Linked List?",
                    "type": "single", "a": "O(N)", "b": "O(1)", "c": "O(log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "Updating new_node->next = head and head = new_node requires constant O(1) pointer updates."
                },
                {
                    "q": "3. What is the time complexity to access the K-th element in a Singly Linked List of N nodes?",
                    "type": "single", "a": "O(1)", "b": "O(K)", "c": "O(log K)", "d": "O(N^2)", "ans": "B",
                    "exp": "Linked lists lack index memory formulas; accessing index K requires traversing K pointers sequentially."
                },
                {
                    "q": "4. What pointers are stored in each node of a Doubly Linked List?",
                    "type": "single", "a": "next pointer only", "b": "next pointer and prev pointer", "c": "head pointer only", "d": "random pointer", "ans": "B",
                    "exp": "Doubly linked list nodes contain 'data', 'next' pointer (forward), and 'prev' pointer (backward)."
                },
                {
                    "q": "5. What algorithm reverses a Singly Linked List in-place in O(N) time and O(1) space?",
                    "type": "single", "a": "Three-Pointer Iteration (prev, curr, next)", "b": "Recursion only", "c": "Copying to array", "d": "Queue iteration", "ans": "A",
                    "exp": "Maintaining prev, curr, and next pointers redirects curr->next = prev in a single O(N) linear pass."
                },
                {
                    "q": "6. What is Floyd's Cycle Detection Algorithm (Tortoise & Hare)?",
                    "type": "single", "a": "Two pointers moving at same speed", "b": "Slow pointer (1 step) and Fast pointer (2 steps) detect loops if they meet", "c": "Sorting pointers", "d": "Hash table indexing", "ans": "B",
                    "exp": "If a cycle exists, fast pointer catches slow pointer inside the loop in O(N) time and O(1) space."
                },
                {
                    "q": "7. After Floyd's algorithm detects a cycle, how do you locate the EXACT START NODE of the cycle?",
                    "type": "single", "a": "Reset fast to Head, keep slow at meeting point, move both 1 step at a time until they collide", "b": "Reverse list", "c": "Count total nodes", "d": "Clear next pointers", "ans": "A",
                    "exp": "Distance from head to cycle start equals distance from meeting point to cycle start along loop path."
                },
                {
                    "q": "8. What is the purpose of a 'Dummy Head Node' in linked list operations?",
                    "type": "single", "a": "Saves memory", "b": "Simplifies boundary conditions when inserting/deleting list head", "c": "Accelerates search", "d": "Prevents memory leaks", "ans": "B",
                    "exp": "Dummy node eliminates special edge-case checks when head node is modified or deleted."
                },
                {
                    "q": "9. How do fast and slow pointers find the MIDDLE node of a linked list in one pass?",
                    "type": "single", "a": "Fast moves 1 step, slow moves 2 steps", "b": "Fast moves 2 steps, slow moves 1 step; when fast reaches end, slow is at middle", "c": "Count total nodes then loop", "d": "Reverse list first", "ans": "B",
                    "exp": "Because fast travels twice as fast, slow arrives at middle node when fast reaches the end."
                },
                {
                    "q": "10. What is the time and space complexity to find the K-th node from the END of a linked list using two pointers?",
                    "type": "single", "a": "O(N) time, O(1) space", "b": "O(N^2) time, O(N) space", "c": "O(N log N) time, O(1) space", "d": "O(1) time, O(N) space", "ans": "A",
                    "exp": "Advance pointer1 by K steps first, then advance pointer1 and pointer2 together until pointer1 reaches NULL."
                },
                {
                    "q": "11. How does a Circular Linked List differ from a standard Singly Linked List?",
                    "type": "single", "a": "Last node's next pointer points back to Head instead of NULL", "b": "Nodes are stored in array", "c": "Has no data field", "d": "Cannot be traversed", "ans": "A",
                    "exp": "In circular linked lists, tail->next points to head node, forming a continuous circular chain."
                },
                {
                    "q": "12. What is the time complexity to delete a node given ONLY a direct pointer 'node' to it in a Singly Linked List (not tail)?",
                    "type": "single", "a": "O(N)", "b": "O(1) by copying node->next data into node and deleting node->next", "c": "O(log N)", "d": "Impossible", "ans": "B",
                    "exp": "Copy next node's val into current node, then point node->next = node->next->next and delete node->next in O(1)."
                },
                {
                    "q": "13. What is the time complexity of Merge Sort on a Linked List of size N?",
                    "type": "single", "a": "O(N^2)", "b": "O(N log N)", "c": "O(N)", "d": "O(log N)", "ans": "B",
                    "exp": "Merge Sort splits list using middle pointer O(N) and merges sorted sublists in O(N log N) time & O(1) aux space."
                },
                {
                    "q": "14. Why is Quick Sort less preferred than Merge Sort for Singly Linked Lists?",
                    "type": "single", "a": "Quick sort requires random access indexing arr[i]", "b": "Linked lists cannot be partitioned", "c": "Merge sort requires O(N) extra array space", "d": "Quick sort takes O(N^3)", "ans": "A",
                    "exp": "Quick Sort relies on efficient random access pointer jumps; Merge Sort only requires sequential pointer relinking."
                },
                {
                    "q": "15. In LRU Cache implementation, why is a Doubly Linked List used alongside a Hash Map?",
                    "type": "single", "a": "Allows O(1) removal and node relocation to head upon access", "b": "Reduces memory", "c": "Sorts keys automatically", "d": "Prevents hash collisions", "ans": "A",
                    "exp": "Doubly linked list allows removing any node in O(1) given its pointer, enabling O(1) LRU updates."
                },
                {
                    "q": "16. What is a 'Skip List'?",
                    "type": "single", "a": "A linked list with missing nodes", "b": "Probabilistic data structure using multi-level pointer forward tracks to achieve O(log N) search/insert", "c": "Circular array", "d": "Binary search tree", "ans": "B",
                    "exp": "Skip List builds hierarchy of express lane linked lists, achieving O(log N) search, insert, and delete."
                },
                {
                    "q": "17. What is an 'XOR Doubly Linked List'?",
                    "type": "single", "a": "Memory-optimized doubly linked list storing XOR address (prev ^ next) in a single pointer field", "b": "List storing binary bits", "c": "List without pointers", "d": "Encrypting list", "ans": "A",
                    "exp": "Node stores pointer_diff = prev ^ next, saving half the pointer memory overhead per node."
                },
                {
                    "q": "18. What is the time complexity to check if a Singly Linked List is a Palindrome using fast/slow pointers and reversing second half?",
                    "type": "single", "a": "O(N) time, O(1) space", "b": "O(N^2) time, O(N) space", "c": "O(N log N) time, O(1) space", "d": "O(1) time", "ans": "A",
                    "exp": "Find middle (fast/slow), reverse second half, compare halves, and restore list in linear O(N) time & O(1) space."
                },
                {
                    "q": "19. How do you find the Intersection Node of two linked lists of lengths M and N in O(M+N) time and O(1) space?",
                    "type": "single", "a": "Hash table lookup", "b": "Two pointers pA and pB; when pA hits end jump to headB, when pB hits end jump to headA", "c": "Sort both lists", "d": "Nested loop search", "ans": "B",
                    "exp": "Traversing lenA + lenB equalizes path lengths, causing pointers to meet at intersection node in O(M+N)."
                },
                {
                    "q": "20. What is the time complexity of merging K sorted linked lists of total N nodes using Min-Heap?",
                    "type": "single", "a": "O(N * K)", "b": "O(N log K)", "c": "O(N^2)", "d": "O(K log K)", "ans": "B",
                    "exp": "Min-heap of size K extracts minimum node and inserts next node in O(log K) time per node across N nodes."
                },
                {
                    "q": "21. What happens if you fail to update tail->next = NULL when splitting a linked list into two sublists?",
                    "type": "single", "a": "List splits normally", "b": "Infinite loop / unexpected chain traversal", "c": "Compilation error", "d": "Memory freed automatically", "ans": "B",
                    "exp": "Failing to terminate sublist tail pointer with NULL leaves sublist linked to original list tail."
                },
                {
                    "q": "22. In Copy List with Random Pointer problem, how can you clone the list in O(N) time and O(1) auxiliary space?",
                    "type": "single", "a": "Interleave cloned nodes next to original nodes (A -> A' -> B -> B')", "b": "Use 2D matrix", "c": "Sort nodes by address", "d": "Recursion without pointers", "ans": "A",
                    "exp": "Interleaving cloned nodes allows setting clone->random = original->random->next without extra hash map."
                },
                {
                    "q": "23. Why do Linked Lists experience worse hardware performance than Arrays during sequential traversal?",
                    "type": "single", "a": "Pointers take more space", "b": "Heap memory fragmentation causes high CPU Cache Misses", "c": "Linked lists are non-linear", "d": "Traversal requires extra CPU cycles", "ans": "B",
                    "exp": "Scattered node pointers break spatial cache locality, requiring individual memory fetches on cache misses."
                },
                {
                    "q": "24. What is the time complexity of Flattening a Multi-Level Doubly Linked List containing child pointers?",
                    "type": "single", "a": "O(N) where N is total nodes", "b": "O(N^2)", "c": "O(2^N)", "d": "O(N log N)", "ans": "A",
                    "exp": "Using stack or tail pointer relinking, each node and child pointer is processed once in linear O(N) time."
                },
                {
                    "q": "25. How do Lock-Free Concurrent Linked Lists perform thread-safe insertions without global mutexes?",
                    "type": "single", "a": "Using Atomic Compare-And-Swap (CAS) hardware instructions", "b": "Disabling interrupts", "c": "Copying list on write", "d": "Using single thread", "ans": "A",
                    "exp": "Atomic CAS operations update node pointers atomically, retrying if concurrent threads modify target pointer."
                }
            ]
        },
        {
            "topic": "Stack",
            "title": "Stack Data Structure & Monotonic Stack Applications Quiz",
            "description": "Master LIFO invariants, call stack execution, expression evaluation (Shunting-Yard), monotonic stacks, min stack, and histogram area.",
            "questions": [
                {
                    "q": "1. What operational principle governs a Stack data structure?",
                    "type": "single", "a": "FIFO (First In First Out)", "b": "LIFO (Last In First Out)", "c": "LILO (Last In Last Out)", "d": "Random Access", "ans": "B",
                    "exp": "Stack enforces Last-In, First-Out: the most recently pushed element is the first element popped."
                },
                {
                    "q": "2. What is the time complexity of Push, Pop, and Top operations in a standard Stack?",
                    "type": "single", "a": "O(N)", "b": "O(1)", "c": "O(log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "All basic stack operations target the top element index/pointer, executing in constant O(1) time."
                },
                {
                    "q": "3. What condition occurs when attempting to POP an element from an EMPTY stack?",
                    "type": "single", "a": "Stack Overflow", "b": "Stack Underflow", "c": "Memory Leak", "d": "Segmentation Fault", "ans": "B",
                    "exp": "Popping or peeking from an empty stack triggers a Stack Underflow error."
                },
                {
                    "q": "4. What runtime environment structure tracks function calls, local variables, and return addresses?",
                    "type": "single", "a": "Heap Buffer", "b": "Call Stack / Execution Stack", "c": "Priority Queue", "d": "B-Tree", "ans": "B",
                    "exp": "The system call stack pushes frame on function invocation and pops frame upon return."
                },
                {
                    "q": "5. What algorithm converts Infix mathematical expressions (A + B) to Postfix (A B +)?",
                    "type": "single", "a": "Kadane's Algorithm", "b": "Dijkstra's Shunting-Yard Algorithm", "c": "KMP Algorithm", "d": "Floyd's Algorithm", "ans": "B",
                    "exp": "Dijkstra's Shunting-Yard algorithm uses an operator stack to parse infix expressions into postfix notation."
                },
                {
                    "q": "6. How is postfix expression '3 4 + 2 *' evaluated using a stack?",
                    "type": "single", "a": "Result = 14: push 3, 4; '+' pops 3+4=7, push 7; push 2; '*' pops 7*2=14", "b": "Result = 11", "c": "Result = 24", "d": "Result = 9", "ans": "A",
                    "exp": "Operands are pushed; operators pop 2 operands, calculate result, and push back. (3+4)*2 = 14."
                },
                {
                    "q": "7. How can you design a Min-Stack where getMin() runs in O(1) time?",
                    "type": "single", "a": "Sort stack on every push", "b": "Maintain auxiliary stack storing current minimum value at each depth", "c": "Scan stack in O(N)", "d": "Use binary search", "ans": "B",
                    "exp": "Auxiliary stack tracks min(val, auxStack.top()), enabling O(1) getMin() alongside standard stack operations."
                },
                {
                    "q": "8. What pattern uses a stack maintaining elements in strictly increasing/decreasing order to find Next Greater Element?",
                    "type": "single", "a": "Monotonic Stack Pattern", "b": "Segment Tree", "c": "Binary Heap", "d": "Sliding Window", "ans": "A",
                    "exp": "Monotonic stack pops smaller elements when encountering larger incoming element, solving Next Greater in O(N) time."
                },
                {
                    "q": "9. What is the time complexity to solve 'Next Greater Element' for all N array elements using a Monotonic Stack?",
                    "type": "single", "a": "O(N^2)", "b": "O(N)", "c": "O(N log N)", "d": "O(2^N)", "ans": "B",
                    "exp": "Each element is pushed once and popped at most once, taking amortized linear O(N) total time."
                },
                {
                    "q": "10. In 'Valid Parentheses' problem, what action is taken when encountering a closing bracket ')'?",
                    "type": "single", "a": "Push onto stack", "b": "Pop top element and check if it matches corresponding opening bracket '('", "c": "Clear stack", "d": "Ignore bracket", "ans": "B",
                    "exp": "Closing brackets must match the most recently pushed opening bracket at stack top."
                },
                {
                    "q": "11. What is the time complexity to calculate Largest Rectangle in Histogram using a Monotonic Stack?",
                    "type": "single", "a": "O(N^2)", "b": "O(N)", "c": "O(N log N)", "d": "O(N^3)", "ans": "B",
                    "exp": "Monotonic increasing stack determines left and right smaller boundary spans in linear O(N) time."
                },
                {
                    "q": "12. In Daily Temperatures problem (days until warmer temperature), what does the stack store?",
                    "type": "single", "a": "Raw temperature values only", "b": "Indices of array elements in monotonic decreasing temperature order", "c": "Difference of days", "d": "Average temperatures", "ans": "B",
                    "exp": "Storing indices allows computing day distance i - stack.pop() when warmer temperature arrives."
                },
                {
                    "q": "13. How can a Queue be implemented using TWO Stacks (inStack & outStack)?",
                    "type": "single", "a": "Enqueue pushes to inStack; Dequeue pops outStack (transferring inStack to outStack if empty)", "b": "Push to both stacks", "c": "Pop from both stacks", "d": "Impossible", "ans": "A",
                    "exp": "Transferring elements reverses stack order into FIFO order. Dequeue runs in amortized O(1) time."
                },
                {
                    "q": "14. What is the space complexity of an Array-based Stack of capacity C?",
                    "type": "single", "a": "O(C)", "b": "O(1)", "c": "O(C^2)", "d": "O(log C)", "ans": "A",
                    "exp": "Allocating contiguous array buffer of fixed size C consumes O(C) memory space."
                },
                {
                    "q": "15. What is the time complexity of reversing a string using a Stack?",
                    "type": "single", "a": "O(N^2)", "b": "O(N) time and O(N) space", "c": "O(1) time", "d": "O(N log N)", "ans": "B",
                    "exp": "Pushing all N characters then popping them back reverses string in linear O(N) time & space."
                },
                {
                    "q": "16. In expression parsing, prefix notation '+ A B' is also known as:",
                    "type": "single", "a": "Polish Notation", "b": "Reverse Polish Notation", "c": "Infix Notation", "d": "Binary Notation", "ans": "A",
                    "exp": "Prefix notation is called Polish Notation; Postfix notation is called Reverse Polish Notation (RPN)."
                },
                {
                    "q": "17. In Maximal Rectangle in 2D Binary Matrix problem, how is the problem transformed to use Histogram Stack algorithm?",
                    "type": "single", "a": "Treat each row as histogram base by accumulating consecutive 1s vertically", "b": "Sort matrix", "c": "Rotate matrix 90 degrees", "d": "Run BFS", "ans": "A",
                    "exp": "Updating running height array per row converts 2D matrix max rectangle into N subproblems of Histogram O(R * C)."
                },
                {
                    "q": "18. What stack state indicates that a string of brackets is valid after processing all characters?",
                    "type": "single", "a": "Stack has 1 element", "b": "Stack is completely empty", "c": "Stack contains numbers", "d": "Stack is full", "ans": "B",
                    "exp": "An empty stack confirms all opened brackets were successfully matched and closed in proper order."
                },
                {
                    "q": "19. In Asteroid Collision problem, when two asteroids meet (positive moving right, negative moving left), what determines which survives?",
                    "type": "single", "a": "Asteroid with larger absolute size survives; equal sizes explode both", "b": "Positive always wins", "c": "First asteroid wins", "d": "Random choice", "ans": "A",
                    "exp": "Top asteroid on stack collides with incoming asteroid until size comparison resolves or direction changes."
                },
                {
                    "q": "20. How do you implement stack using a SINGLE Queue recursively?",
                    "type": "single", "a": "On push(x), enqueue x, then dequeue and re-enqueue previous N-1 elements", "b": "Dequeue twice", "c": "Clear queue", "d": "Sort queue", "ans": "A",
                    "exp": "Rotating previous N-1 elements behind incoming element x moves x to queue front (LIFO ordering)."
                },
                {
                    "q": "21. What is the auxiliary space complexity of removing adjacent duplicates in a string using stack?",
                    "type": "single", "a": "O(1)", "b": "O(N)", "c": "O(N^2)", "d": "O(log N)", "ans": "B",
                    "exp": "Stack maintains non-duplicate character sequence of length up to N, consuming O(N) space."
                },
                {
                    "q": "22. In Decode String ('3[a2[c]]' -> 'accaccacc'), what data structure handles nested bracket expansion?",
                    "type": "single", "a": "Two Stacks (countStack and stringStack)", "b": "Queue", "c": "Binary Tree", "d": "Matrix", "ans": "A",
                    "exp": "Stacks save multiplier counts and current string prefixes when entering nested brackets '['."
                },
                {
                    "q": "23. In Simplify Path problem ('/a/./b/../../c/'), what does '..' command perform on path stack?",
                    "type": "single", "a": "Push '..'", "b": "Pop top directory from stack if stack non-empty", "c": "Clear entire stack", "d": "Ignore", "ans": "B",
                    "exp": "'..' represents parent directory, popping most recent directory from path stack."
                },
                {
                    "q": "24. What is the time complexity of evaluating an RPN (Reverse Polish Notation) expression array of length N?",
                    "type": "single", "a": "O(N)", "b": "O(N log N)", "c": "O(N^2)", "d": "O(2^N)", "ans": "A",
                    "exp": "Scanning array once while pushing operands and popping for operators executes in linear O(N) time."
                },
                {
                    "q": "25. Which OS memory segment grows downward towards lower memory addresses on x86 architectures?",
                    "type": "single", "a": "Heap Segment", "b": "Stack Segment", "c": "Data Segment", "d": "Code Segment", "ans": "B",
                    "exp": "The call stack segment conventionally grows downward from high memory addresses toward lower addresses."
                }
            ]
        },
        {
            "topic": "Queue",
            "title": "Queue, Circular Queue & Priority Queue Systems Quiz",
            "description": "Master FIFO scheduling buffers, circular modulo index arithmetic, priority queues, monotonic deques, double-ended queues, and multi-source BFS.",
            "questions": [
                {
                    "q": "1. What ordering invariant defines a Queue data structure?",
                    "type": "single", "a": "LIFO (Last In First Out)", "b": "FIFO (First In First Out)", "c": "Priority order only", "d": "Random order", "ans": "B",
                    "exp": "Queue operates under First-In, First-Out: elements are inserted at rear and removed from front."
                },
                {
                    "q": "2. What are the core operations of a Queue called?",
                    "type": "single", "a": "Push and Pop", "b": "Enqueue (insert rear) and Dequeue (remove front)", "c": "Insert and Delete", "d": "Add and Remove", "ans": "B",
                    "exp": "Enqueue adds elements to queue rear; Dequeue removes elements from queue front in O(1) time."
                },
                {
                    "q": "3. In a simple array-based queue without circular indexing, what is the drawback of Dequeue?",
                    "type": "single", "a": "Memory leak", "b": "Unused empty slots at front remain wasted unless elements shift in O(N) time", "c": "Stack underflow", "d": "Infinite loop", "ans": "B",
                    "exp": "Incrementing front pointer leaves front array slots empty and inaccessible unless elements shift (O(N))."
                },
                {
                    "q": "4. What formula updates the rear pointer in a Circular Queue of size N?",
                    "type": "single", "a": "rear = rear + 1", "b": "rear = (rear + 1) % N", "c": "rear = rear * 2", "d": "rear = (rear - 1) % N", "ans": "B",
                    "exp": "Modulo arithmetic wraps rear pointer back to index 0 when reaching array end."
                },
                {
                    "q": "5. How do you distinguish between EMPTY and FULL states in a Circular Queue of size N using front and rear?",
                    "type": "single", "a": "Empty: count == 0; Full: count == N (or maintain size counter)", "b": "Empty: front == rear + 1", "c": "Full: front == 0", "d": "No difference", "ans": "A",
                    "exp": "Tracking current element count variable distinguishes empty (count=0) from full (count=N) unequivocally."
                },
                {
                    "q": "6. What is a Deque (Double-Ended Queue)?",
                    "type": "single", "a": "Queue allowing insertion and deletion at BOTH front and rear ends in O(1)", "b": "Priority queue", "c": "Queue with 2 elements", "d": "Circular stack", "ans": "A",
                    "exp": "Deque supports push_front, push_back, pop_front, and pop_back all in constant O(1) time."
                },
                {
                    "q": "7. What graph traversal algorithm relies fundamentally on a Queue data structure?",
                    "type": "single", "a": "Depth-First Search (DFS)", "b": "Breadth-First Search (BFS)", "c": "Topological Sort DFS", "d": "Tarjan SCC", "ans": "B",
                    "exp": "BFS uses FIFO queue to explore graph vertices level-by-level in order of distance from source."
                },
                {
                    "q": "8. What data structure underpins a Priority Queue to achieve O(log N) insertion and extraction of min/max element?",
                    "type": "single", "a": "Linked List", "b": "Binary Heap (Min-Heap / Max-Heap)", "c": "Circular Array", "d": "Hash Map", "ans": "B",
                    "exp": "Binary Heap maintains heap-order property in tree structure, enabling O(log N) push and pop."
                },
                {
                    "q": "9. In Sliding Window Maximum problem (array size N, window K), what data structure achieves linear O(N) overall time?",
                    "type": "single", "a": "Priority Queue (Heap)", "b": "Monotonic Decreasing Deque storing element indices", "c": "Binary Search Tree", "d": "Standard FIFO Queue", "ans": "B",
                    "exp": "Monotonic Deque removes smaller elements from rear and outdated indices from front in O(N) total time."
                },
                {
                    "q": "10. How can a Stack be implemented using TWO Queues (q1 & q2)?",
                    "type": "single", "a": "Push to q2, transfer all elements from q1 to q2, swap q1 and q2 names", "b": "Enqueue to both queues", "c": "Dequeue from both queues", "d": "Impossible", "ans": "A",
                    "exp": "Re-queueing existing elements behind incoming element reverses FIFO order into LIFO order."
                },
                {
                    "q": "11. In Multi-Source BFS (e.g. Rotting Oranges), how is the Queue initialized before loop execution?",
                    "type": "single", "a": "Push single root node", "b": "Push ALL initial rotten orange coordinates into queue simultaneously at t=0", "c": "Push graph edges", "d": "Leave queue empty", "ans": "B",
                    "exp": "Enqueuing all starting points at level 0 expands distance frontiers simultaneously in parallel."
                },
                {
                    "q": "12. In OS CPU process scheduling, what queue mechanism prevents low-priority processes from starving?",
                    "type": "single", "a": "Single Priority Queue", "b": "Multilevel Feedback Queue with Aging (boosting priority over time)", "c": "LIFO Stack", "d": "Static Ring Buffer", "ans": "B",
                    "exp": "Multilevel feedback queues adjust priorities dynamically, aging waiting tasks to guarantee execution."
                },
                {
                    "q": "13. What is the time complexity to find Kth largest element in array using Min-Heap of size K?",
                    "type": "single", "a": "O(N log N)", "b": "O(N log K)", "c": "O(N^2)", "d": "O(K)", "ans": "B",
                    "exp": "Maintaining size-K min-heap takes O(log K) for each of N array insertions, yielding O(N log K)."
                },
                {
                    "q": "14. What is a 'Lock-Free SPSC Ring Buffer'?",
                    "type": "single", "a": "Single Producer Single Consumer circular queue using atomic atomic head/tail pointers without mutex locks", "b": "Stack buffer", "c": "Doubly linked queue", "d": "Heap tree", "ans": "A",
                    "exp": "SPSC ring buffer allows 1 thread writing and 1 thread reading without lock contention."
                },
                {
                    "q": "15. In Circular Tour / Gas Station problem, what is the time complexity to find starting station completing circuit?",
                    "type": "single", "a": "O(N^2)", "b": "O(N) time and O(1) space using running tank balance queue logic", "c": "O(N log N)", "d": "O(2^N)", "ans": "B",
                    "exp": "Single pass accumulating total gas vs cost finds starting gas station in linear O(N) time."
                },
                {
                    "q": "16. What is the time complexity of popping the highest priority element from an UNORDERED Array implementation of Priority Queue?",
                    "type": "single", "a": "O(1)", "b": "O(N) search for max element", "c": "O(log N)", "d": "O(N log N)", "ans": "B",
                    "exp": "Inserting takes O(1), but finding and removing maximum element from unsorted array requires scanning all N elements O(N)."
                },
                {
                    "q": "17. In standard C++ STL, what data structure underlies std::queue by default?",
                    "type": "single", "a": "std::vector", "b": "std::deque", "c": "std::list", "d": "std::set", "ans": "B",
                    "exp": "std::deque provides contiguous chunk memory with O(1) push/pop at both front and back."
                },
                {
                    "q": "18. What is the time complexity of building a Binary Heap from an array of N elements (Heapify)?",
                    "type": "single", "a": "O(N log N)", "b": "O(N)", "c": "O(N^2)", "d": "O(log N)", "ans": "B",
                    "exp": "Bottom-up heapify sums node heights sum(N / 2^(h+1) * h) = linear O(N) time."
                },
                {
                    "q": "19. In Task Scheduler problem (with cooling period CPU tasks), what data structures are optimal?",
                    "type": "single", "a": "Max-Heap for frequencies and Queue for cooling timer", "b": "Stack only", "c": "Binary Tree", "d": "Sorting array", "ans": "A",
                    "exp": "Max-heap picks highest frequency task; queue holds cooling tasks until ready time arrives."
                },
                {
                    "q": "20. What is the time complexity to peek front element in a Queue?",
                    "type": "single", "a": "O(N)", "b": "O(1)", "c": "O(log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "Peeking returns element at front pointer/index in constant O(1) time without modifying queue."
                },
                {
                    "q": "21. How do you implement a Stream Moving Average of last K integers?",
                    "type": "single", "a": "Queue of size K tracking running sum; subtract popped element when size exceeds K", "b": "Re-sum array every time", "c": "Sort list", "d": "Use stack", "ans": "A",
                    "exp": "Queue maintains latest K elements; running_sum += val - queue.dequeue() calculates average in O(1)."
                },
                {
                    "q": "22. In 0-1 BFS (graph edge weights 0 or 1), what data structure replaces Priority Queue to achieve O(V + E) time?",
                    "type": "single", "a": "Deque (push front weight 0, push back weight 1)", "b": "Stack", "c": "Binary Heap", "d": "Array", "ans": "A",
                    "exp": "Deque maintains sorted distance order by adding 0-weight edges at front and 1-weight edges at back in O(1)."
                },
                {
                    "q": "23. In Priority Queue, what operation decreases the key value of an existing node in Fibonacci Heap in amortized O(1) time?",
                    "type": "single", "a": "Decrease-Key", "b": "Heapify", "c": "Extract-Min", "d": "Build-Heap", "ans": "A",
                    "exp": "Fibonacci Heaps support amortized O(1) Decrease-Key, improving Dijkstra's algorithm to O(E + V log V)."
                },
                {
                    "q": "24. What happens when enqueueing to a Queue that has reached max capacity?",
                    "type": "single", "a": "Queue Underflow", "b": "Queue Overflow", "c": "Null Pointer", "d": "Memory Leak", "ans": "B",
                    "exp": "Attempting to push element into full queue triggers Queue Overflow error."
                },
                {
                    "q": "25. Which problem is solved in O(N) using Monotonic Queue of sliding window?",
                    "type": "single", "a": "Sliding Window Maximum / Minimum", "b": "2Sum problem", "c": "Graph Cycle Detection", "d": "Matrix Multiplication", "ans": "A",
                    "exp": "Monotonic Queue maintains window extremes in O(1) amortized time per element slide across array."
                }
            ]
        },
        {
            "topic": "Sliding Window",
            "title": "Sliding Window & Two Pointer Techniques Quiz",
            "description": "Master fixed vs dynamic window bounds, inward two pointers, fast/slow pointers, frequency map windows, and exact count reductions.",
            "questions": [
                {
                    "q": "1. What is the main advantage of Sliding Window technique over brute force nested loops?",
                    "type": "single", "a": "Reduces time complexity from O(N^2) or O(N^3) to linear O(N)", "b": "Reduces space to O(N^2)", "c": "Sorts array automatically", "d": "Prevents recursion", "ans": "A",
                    "exp": "Sliding window updates sub-segment state incrementally in O(1) instead of re-scanning window contents."
                },
                {
                    "q": "2. In Fixed-Size Sliding Window of length K, how is running window sum updated when moving window right by 1 step?",
                    "type": "single", "a": "Re-sum all K elements", "b": "new_sum = prev_sum + arr[right] - arr[left-1]", "c": "new_sum = prev_sum * arr[right]", "d": "new_sum = arr[right]", "ans": "B",
                    "exp": "Add entering right element and subtract leaving left element in constant O(1) time."
                },
                {
                    "q": "3. In Dynamic-Size Sliding Window (e.g. Max Subarray Sum <= Target with positive numbers), when do you expand right pointer R?",
                    "type": "single", "a": "When window condition is valid, expand R to find larger window", "b": "When window is invalid", "c": "Never", "d": "Always shrink L", "ans": "A",
                    "exp": "Expand R to test larger valid window bounds; shrink L when window constraint is violated."
                },
                {
                    "q": "4. What is the time complexity of processing an array of size N using Dynamic Sliding Window where left L and right R pointers move forward?",
                    "type": "single", "a": "O(N^2)", "b": "O(N) because L and R each advance at most N steps", "c": "O(N log N)", "d": "O(2^N)", "ans": "B",
                    "exp": "L and R pointers move monotonically forward from 0 to N; total operations bounded by 2N = O(N)."
                },
                {
                    "q": "5. In sorted array Two Pointer inward convergence (e.g. 2Sum), if arr[L] + arr[R] > Target, what action is taken?",
                    "type": "single", "a": "Increment L (L++)", "b": "Decrement R (R--)", "c": "Reset pointers", "d": "Return false", "ans": "B",
                    "exp": "Because array is sorted, decrementing R reduces total sum closer to target value."
                },
                {
                    "q": "6. Why can standard Sliding Window NOT be applied directly to solve Subarray Sum Equals K when array contains NEGATIVE numbers?",
                    "type": "single", "a": "Window sum is non-monotonic (expanding R may decrease sum, shrinking L may increase sum)", "b": "Negative numbers crash pointers", "c": "Array cannot be indexed", "d": "Requires 3 pointers", "ans": "A",
                    "exp": "Sliding window requires monotonicity (expanding increases sum). For negative numbers, Prefix Sum + Hash Map solves problem in O(N)."
                },
                {
                    "q": "7. What formula calculates exact count of subarrays with EXACTLY K distinct elements using At-Most helper function?",
                    "type": "single", "a": "Exact(K) = AtMost(K) - AtMost(K-1)", "b": "Exact(K) = AtMost(K) + AtMost(K-1)", "c": "Exact(K) = AtMost(K) * K", "d": "Exact(K) = AtMost(K) / 2", "ans": "A",
                    "exp": "Subarrays with at most K distinct minus subarrays with at most K-1 distinct leaves subarrays with exactly K distinct."
                },
                {
                    "q": "8. What is the time complexity of finding Longest Substring Without Repeating Characters using sliding window & hash map?",
                    "type": "single", "a": "O(N^2)", "b": "O(N)", "c": "O(N log N)", "d": "O(26)", "ans": "B",
                    "exp": "Updating character last-seen index map allows shrinking left boundary L in single pass linear O(N) time."
                },
                {
                    "q": "9. In Minimum Window Substring (string S len N, target T len M), what is the optimal overall time complexity?",
                    "type": "single", "a": "O(N * M)", "b": "O(N + M)", "c": "O(N^2)", "d": "O(2^M)", "ans": "B",
                    "exp": "Sliding window on S maintaining frequency count match of T processes each string character in O(N + M) time."
                },
                {
                    "q": "10. In Fruit Into Baskets problem (at most 2 distinct fruit types in window), what determines window shrinking trigger?",
                    "type": "single", "a": "When map size (distinct elements) exceeds 2", "b": "When basket is full", "c": "When arr[R] == 0", "d": "Every 2 steps", "ans": "A",
                    "exp": "Shrink left pointer L until distinct count in frequency map drops back to 2."
                },
                {
                    "q": "11. In Fast and Slow Pointers (Floyd's Tortoise & Hare) for array duplicate detection (Find Duplicate Number), why does it run in O(1) space?",
                    "type": "single", "a": "Array values act as next pointers arr[i]", "b": "Sorts array in place", "c": "Uses bitmask", "d": "Modifies array values", "ans": "A",
                    "exp": "Treating index i -> arr[i] as linked list node links forms a cycle containing the duplicate number."
                },
                {
                    "q": "12. In Container With Most Water problem (height array), how do you decide which pointer L or R to move inward?",
                    "type": "single", "a": "Move pointer with SMALLER height (height[L] < height[R] ? L++ : R--)", "b": "Move larger height pointer", "c": "Move both pointers", "d": "Random move", "ans": "A",
                    "exp": "Area is constrained by shorter line. Moving shorter line offers only opportunity to discover taller boundary."
                },
                {
                    "q": "13. In Max Consecutive Ones III (flip at most K zeros), what does window store?",
                    "type": "single", "a": "Running count of zeros inside window [L, R] <= K", "b": "Count of ones only", "c": "Sum of indices", "d": "XOR total", "ans": "A",
                    "exp": "Window expands R; when zero_count > K, advance L until zero_count <= K."
                },
                {
                    "q": "14. In 3Sum problem (find triplets sum to 0), why is array sorted first?",
                    "type": "single", "a": "Enables Two Pointer inward convergence and easy skip of duplicate elements", "b": "Required by binary search", "c": "Reduces space", "d": "Eliminates negative numbers", "ans": "A",
                    "exp": "Sorting array in O(N log N) allows 2 pointers per outer element and skipping duplicate values seamlessly."
                },
                {
                    "q": "15. What is the time complexity of 4Sum problem optimized with 2 outer loops and inner 2-pointer convergence?",
                    "type": "single", "a": "O(N^4)", "b": "O(N^3)", "c": "O(N^2 log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "Two nested loops take O(N^2); inner 2 pointers scan remaining range in O(N), yielding total O(N^3)."
                },
                {
                    "q": "16. In Subarrays with Bounded Maximum (max element between L and R), how is count accumulated?",
                    "type": "single", "a": "Track last valid element index within range [L, R]", "b": "Sort array", "c": "Use 2D matrix", "d": "Recursion tree", "ans": "A",
                    "exp": "Updating position indices of elements in range accumulated count in linear O(N) time."
                },
                {
                    "q": "17. In Minimum Size Subarray Sum (sum >= Target with positive numbers), what is updated upon finding a valid window sum?",
                    "type": "single", "a": "min_len = min(min_len, R - L + 1), then shrink L to test smaller window", "b": "Expand R", "c": "Break loop", "d": "Reset sum to 0", "ans": "A",
                    "exp": "Record minimum window length, then subtract arr[L] and increment L to seek shorter valid subarray."
                },
                {
                    "q": "18. How many total subarrays of window size K exist in array of size N?",
                    "type": "single", "a": "N - K + 1", "b": "N + K", "c": "N * K", "d": "N / K", "ans": "A",
                    "exp": "Window slides from starting index 0 up to index N - K, producing exactly N - K + 1 windows."
                },
                {
                    "q": "19. In Permutation in String problem (check if S1 permutation is substring of S2), what window size is maintained on S2?",
                    "type": "single", "a": "Fixed window of size equal to length of S1", "b": "Dynamic window", "c": "Size 1", "d": "Full length of S2", "ans": "A",
                    "exp": "Permutations have identical length; slide fixed window of size len(S1) across S2 comparing char frequencies."
                },
                {
                    "q": "20. In Trapping Rain Water problem using Two Pointers (left & right), what metric determines water trapped at index?",
                    "type": "single", "a": "min(left_max, right_max) - height[i]", "b": "left_max + right_max", "c": "max(left_max, right_max)", "d": "height[i] - min_height", "ans": "A",
                    "exp": "Water level at index i is bounded by minimum of tallest left and right walls minus current bar height."
                },
                {
                    "q": "21. In Move Zeroes to end in-place, how do slow and fast pointers operate?",
                    "type": "single", "a": "Fast scans array; when arr[fast] != 0, swap arr[slow] and arr[fast], increment slow", "b": "Slow moves back", "c": "Fast stays at 0", "d": "Sort array", "ans": "A",
                    "exp": "Slow pointer tracks target write position for non-zero numbers in single linear O(N) pass."
                },
                {
                    "q": "22. What is the space complexity of Two Pointer inward algorithm on sorted array?",
                    "type": "single", "a": "O(N)", "b": "O(1)", "c": "O(log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "Two pointer convergence uses only two integer index variables, requiring O(1) auxiliary space."
                },
                {
                    "q": "23. In Longest Repeating Character Replacement (replace at most K chars), window is valid if:",
                    "type": "single", "a": "(window_len - max_freq_char_in_window) <= K", "b": "window_len <= K", "c": "max_freq <= K", "d": "window_len == K", "ans": "A",
                    "exp": "Remaining characters to flip (window length minus most frequent character count) must not exceed K."
                },
                {
                    "q": "24. In Subarray Product Less Than K (positive integers), how many valid subarrays end at index R?",
                    "type": "single", "a": "R - L + 1", "b": "1", "c": "R * L", "d": "2^R", "ans": "A",
                    "exp": "For valid window [L, R], all contiguous subarrays ending at R (lengths 1 to R-L+1) are valid, adding R-L+1."
                },
                {
                    "q": "25. What is the optimal time complexity to find Partition Labels (partition string into max parts where char appears in 1 part)?",
                    "type": "single", "a": "O(N)", "b": "O(N^2)", "c": "O(N log N)", "d": "O(26^2)", "ans": "A",
                    "exp": "Record last occurrence index of each character, then expand window boundary max_last in single O(N) pass."
                }
            ]
        },
        {
            "topic": "Tree",
            "title": "General Trees & Tree Traversals Master Quiz",
            "description": "Master tree terminology, height vs depth, DFS (Inorder, Preorder, Postorder), BFS Level-Order, path sums, diameter, and tree construction.",
            "questions": [
                {
                    "q": "1. What is the defining topological property of a Tree with N vertices?",
                    "type": "single", "a": "Connected acyclic graph with exactly N - 1 edges", "b": "Complete graph with N^2 edges", "c": "Graph with cycles", "d": "Disconnected graph", "ans": "A",
                    "exp": "A tree is a connected acyclic graph containing exactly N vertices and N-1 edges."
                },
                {
                    "q": "2. What is the Depth of a node in a tree?",
                    "type": "single", "a": "Number of edges on the path from Root to that node", "b": "Number of edges on longest path from node to a leaf", "c": "Total nodes in tree", "d": "Number of children", "ans": "A",
                    "exp": "Depth measure distance from Root (depth 0) down to target node."
                },
                {
                    "q": "3. What is the Height of a tree?",
                    "type": "single", "a": "Number of edges on the longest path from Root to any Leaf node", "b": "Total nodes in tree", "c": "Depth of root", "d": "Max degree of root", "ans": "A",
                    "exp": "Height is maximum depth among all leaf nodes in the tree."
                },
                {
                    "q": "4. In binary tree Depth-First Search, what is the order of nodes visited in INORDER Traversal?",
                    "type": "single", "a": "Root -> Left -> Right", "b": "Left -> Root -> Right", "c": "Left -> Right -> Root", "d": "Root -> Right -> Left", "ans": "B",
                    "exp": "Inorder recursively visits Left Subtree, Root node, then Right Subtree."
                },
                {
                    "q": "5. In binary tree Depth-First Search, what is the order of nodes visited in PREORDER Traversal?",
                    "type": "single", "a": "Root -> Left -> Right", "b": "Left -> Root -> Right", "c": "Left -> Right -> Root", "d": "Right -> Left -> Root", "ans": "A",
                    "exp": "Preorder visits Root node first, then recursively Left Subtree, then Right Subtree."
                },
                {
                    "q": "6. In binary tree Depth-First Search, what is the order of nodes visited in POSTORDER Traversal?",
                    "type": "single", "a": "Root -> Left -> Right", "b": "Left -> Root -> Right", "c": "Left -> Right -> Root", "d": "Root -> Right -> Left", "ans": "C",
                    "exp": "Postorder recursively visits Left Subtree, Right Subtree, and finally Root node."
                },
                {
                    "q": "7. What data structure is used to perform Level-Order Traversal (BFS) of a tree?",
                    "type": "single", "a": "Stack", "b": "FIFO Queue", "c": "Min-Heap", "d": "Hash Map", "ans": "B",
                    "exp": "Level-order traversal uses a FIFO queue to visit nodes level-by-level top-to-bottom."
                },
                {
                    "q": "8. What is the maximum number of nodes in a Binary Tree of height H (where root height = 0)?",
                    "type": "single", "a": "2^(H+1) - 1", "b": "2^H", "c": "H^2", "d": "2*H", "ans": "A",
                    "exp": "Summing 1 + 2 + 4 + ... + 2^H geometric series yields 2^(H+1) - 1 maximum nodes."
                },
                {
                    "q": "9. What is a 'Full Binary Tree'?",
                    "type": "single", "a": "Tree where every node has either 0 or 2 children", "b": "Tree where all leaves are at same depth", "c": "Tree skewed to left", "d": "BST tree", "ans": "A",
                    "exp": "In a Full Binary Tree, no node has exactly 1 child (nodes have either 0 or 2 children)."
                },
                {
                    "q": "10. What is a 'Complete Binary Tree'?",
                    "type": "single", "a": "Binary tree where every level is completely filled except possibly last level, which is filled from left to right", "b": "Tree with N nodes", "c": "BST with no duplicate values", "d": "Tree of height N", "ans": "A",
                    "exp": "Complete binary trees fill levels left-to-right, making them ideal for array representation in heaps."
                },
                {
                    "q": "11. What is the Diameter of a Binary Tree?",
                    "type": "single", "a": "Length of longest path between ANY two nodes in the tree (may or may not pass through root)", "b": "Height of root", "c": "Total leaf nodes", "d": "Max degree", "ans": "A",
                    "exp": "Diameter is max(left_height + right_height) evaluated at every node in postorder traversal."
                },
                {
                    "q": "12. What pair of tree traversals is required to UNLEASH unique reconstruction of a general Binary Tree?",
                    "type": "single", "a": "Preorder + Inorder (or Postorder + Inorder)", "b": "Preorder + Postorder", "c": "Level-order only", "d": "Preorder only", "ans": "A",
                    "exp": "Inorder traversal is essential because it splits nodes into left and right subtrees around root node identified by Preorder/Postorder."
                },
                {
                    "q": "13. What is the time complexity to check if a binary tree is Symmetric (mirror image of itself)?",
                    "type": "single", "a": "O(N)", "b": "O(N^2)", "c": "O(log N)", "d": "O(2^N)", "ans": "A",
                    "exp": "Recursive DFS comparing left.left vs right.right and left.right vs right.left visits each node once in O(N)."
                },
                {
                    "q": "14. In Binary Tree Maximum Path Sum problem, what does a node return to its parent during postorder recursion?",
                    "type": "single", "a": "node.val + max(0, max(left_branch, right_branch))", "b": "node.val + left + right", "c": "0", "d": "max_sum", "ans": "A",
                    "exp": "Parent can choose at most ONE child branch path to extend; returning max non-negative branch path allows parent path continuation."
                },
                {
                    "q": "15. What is Lowest Common Ancestor (LCA) of two nodes P and Q in a general binary tree?",
                    "type": "single", "a": "Deepest node that has both P and Q as descendants", "b": "Root of tree always", "c": "Node P always", "d": "Node Q always", "ans": "A",
                    "exp": "LCA is the deepest shared ancestor node along paths from root to P and root to Q."
                },
                {
                    "q": "16. What is the time complexity of finding LCA in a balanced Binary Tree of N nodes?",
                    "type": "single", "a": "O(N)", "b": "O(log N)", "c": "O(N^2)", "d": "O(1)", "ans": "A",
                    "exp": "Recursive DFS visiting nodes to locate P and Q scans up to N nodes in O(N) worst case."
                },
                {
                    "q": "17. What is Morris Inorder Traversal?",
                    "type": "single", "a": "Inorder traversal achieving O(N) time and O(1) auxiliary space using threaded temporary links to predecessor", "b": "Queue traversal", "c": "Stack traversal", "d": "Heap traversal", "ans": "A",
                    "exp": "Morris traversal creates temporary threads from rightmost child of left subtree back to current root node, avoiding call stack."
                },
                {
                    "q": "18. What is the space complexity of recursive DFS traversal on a SKEWED tree of N nodes?",
                    "type": "single", "a": "O(1)", "b": "O(N) stack frames", "c": "O(log N)", "d": "O(N^2)", "ans": "B",
                    "exp": "A degenerate line tree of height N creates N recursive call stack frames."
                },
                {
                    "q": "19. In Zigzag Level-Order Traversal (Spiral Order), how are level node values accumulated?",
                    "type": "single", "a": "Alternate left-to-right and right-to-left insertion direction per level", "b": "Reverse root", "c": "Sort each level", "d": "Use max heap", "ans": "A",
                    "exp": "Flips insertion order (normal vs reversed) on alternating level indices."
                },
                {
                    "q": "20. How do you serialize a binary tree into a string for storage?",
                    "type": "single", "a": "Preorder traversal inserting null markers '#' for missing child pointers", "b": "Store leaf nodes only", "c": "Sort node values", "d": "Store height only", "ans": "A",
                    "exp": "Preorder with null markers unambiguously encodes tree structure for exact deserialization."
                },
                {
                    "q": "21. What is the maximum number of leaf nodes in a Full Binary Tree with L leaves?",
                    "type": "single", "a": "Total nodes N = 2L - 1", "b": "N = L^2", "c": "N = 2^L", "d": "N = L + 1", "ans": "A",
                    "exp": "In full binary trees, internal nodes I = L - 1, so total nodes N = I + L = 2L - 1."
                },
                {
                    "q": "22. In Path Sum III (count paths summing to Target, path does not need to start at root), what optimal data structure is used during DFS?",
                    "type": "single", "a": "Prefix Sum Hash Map", "b": "2D Matrix", "c": "Priority Queue", "d": "Graph Matrix", "ans": "A",
                    "exp": "Tracking running root-to-node prefix sum counts in hash map finds valid sub-paths in O(N) time."
                },
                {
                    "q": "23. In Subtree of Another Tree problem, what is the worst-case time complexity comparing tree S (N nodes) and T (M nodes)?",
                    "type": "single", "a": "O(N * M)", "b": "O(N + M)", "c": "O(N^2)", "d": "O(2^N)", "ans": "A",
                    "exp": "Comparing subtree structure at each of N nodes takes O(M), giving O(N * M) worst case."
                },
                {
                    "q": "24. What is the time complexity to flatten a binary tree into a linked list in-place using right pointer chaining?",
                    "type": "single", "a": "O(N)", "b": "O(N^2)", "c": "O(N log N)", "d": "O(2^N)", "ans": "A",
                    "exp": "Re-linking left subtree between root and right subtree processes each node in linear O(N) time."
                },
                {
                    "q": "25. Which traversal visits all leaf nodes from left to right in a standard binary tree?",
                    "type": "single", "a": "Inorder, Preorder, and Postorder all visit leaves in left-to-right relative order", "b": "Level order only", "c": "Postorder only", "d": "Preorder only", "ans": "A",
                    "exp": "DFS traversals preserve left-to-right child exploration priority, visiting leaf nodes in left-to-right order."
                }
            ]
        },
        {
            "topic": "Binary Tree",
            "title": "Binary Tree Architecture & Properties Quiz",
            "description": "Master binary tree properties, complete vs full vs perfect trees, vertical order, top/bottom views, LCA, and subtree invariants.",
            "questions": [
                {
                    "q": "1. What is the defining constraint of a Binary Tree?",
                    "type": "single", "a": "Every node has at most 2 children (left child and right child)", "b": "Values must be sorted", "c": "Tree height must be log N", "d": "Nodes must have 2 children", "ans": "A",
                    "exp": "Binary tree degree is bounded by 2: each node has 0, 1, or 2 children."
                },
                {
                    "q": "2. What is a 'Perfect Binary Tree'?",
                    "type": "single", "a": "Binary tree where all internal nodes have 2 children AND all leaf nodes are at identical depth", "b": "Tree with 1 node", "c": "Skewed tree", "d": "Heap tree", "ans": "A",
                    "exp": "Perfect binary trees are completely filled across all levels with total nodes = 2^(H+1) - 1."
                },
                {
                    "q": "3. In an array representation of a Complete Binary Tree (1-based indexing), what is the index of the LEFT child of node at index i?",
                    "type": "single", "a": "2 * i", "b": "2 * i + 1", "c": "i / 2", "d": "i + 1", "ans": "A",
                    "exp": "1-based array heap indexing maps left child to 2*i, right child to 2*i + 1, parent to i // 2."
                },
                {
                    "q": "4. In 0-based array indexing of a Complete Binary Tree, what is the index of the RIGHT child of node at index i?",
                    "type": "single", "a": "2 * i + 1", "b": "2 * i + 2", "c": "(i - 1) / 2", "d": "2 * i", "ans": "B",
                    "exp": "0-based indexing maps left child = 2*i + 1, right child = 2*i + 2, parent = (i - 1) // 2."
                },
                {
                    "q": "5. What algorithm calculates Vertical Order Traversal of a Binary Tree?",
                    "type": "single", "a": "BFS Level-Order maintaining horizontal distance HD (left HD-1, right HD+1) in Map", "b": "Inorder traversal only", "c": "Preorder traversal only", "d": "Postorder traversal only", "ans": "A",
                    "exp": "Assigning HD column coordinates and grouping node values by HD column via BFS computes vertical view."
                },
                {
                    "q": "6. In Top View of a Binary Tree, which node is visible for each vertical column HD?",
                    "type": "single", "a": "The FIRST node encountered at column HD during BFS level-order traversal", "b": "The last node at HD", "c": "The root node", "d": "Leaf node only", "ans": "A",
                    "exp": "Top view retains the highest level (first seen) node for each horizontal distance coordinate HD."
                },
                {
                    "q": "7. In Bottom View of a Binary Tree, which node is visible for each vertical column HD?",
                    "type": "single", "a": "The LAST node encountered at column HD during BFS level-order traversal", "b": "First node at HD", "c": "Root node", "d": "Middle node", "ans": "A",
                    "exp": "Bottom view overwrites map entry so the lowest level (last seen) node per column HD remains."
                },
                {
                    "q": "8. In Left View of a Binary Tree, which nodes are visible?",
                    "type": "single", "a": "The first node encountered at each level depth during BFS level-order", "b": "All left child nodes", "c": "Leaf nodes only", "d": "Root only", "ans": "A",
                    "exp": "Left view captures the leftmost node (first node processed per level during BFS)."
                },
                {
                    "q": "9. In Right View of a Binary Tree, which nodes are visible?",
                    "type": "single", "a": "The last node encountered at each level depth during BFS level-order", "b": "All right child nodes", "c": "Root node only", "d": "Leaf nodes only", "ans": "A",
                    "exp": "Right view captures the rightmost node (last node processed per level depth during BFS)."
                },
                {
                    "q": "10. What is the time complexity to check if a binary tree is Height-Balanced (AVL balanced property |left_h - right_h| <= 1)?",
                    "type": "single", "a": "O(N) using bottom-up postorder returning height or -1 if unbalanced", "b": "O(N^2)", "c": "O(log N)", "d": "O(2^N)", "ans": "A",
                    "exp": "Bottom-up postorder computes height and short-circuits with -1 if balance factor fails, taking O(N)."
                },
                {
                    "q": "11. What is the Maximum Width of a Binary Tree?",
                    "type": "single", "a": "Maximum width among all levels, measured as positional distance between leftmost and rightmost non-null nodes in level", "b": "Total leaves", "c": "Height of tree", "d": "Max degree", "ans": "A",
                    "exp": "Width uses positional heap indexing per level: (rightmost_index - leftmost_index + 1)."
                },
                {
                    "q": "12. In Invert/Flip Binary Tree (mirror image), what operation is performed at each node?",
                    "type": "single", "a": "Swap node.left and node.right pointers recursively", "b": "Sort values", "c": "Delete left child", "d": "Reverse values", "ans": "A",
                    "exp": "Swapping left and right child pointers at every node mirrors the tree structure in O(N) time."
                },
                {
                    "q": "13. What is the total number of structurally unique Binary Trees that can be formed with N unlabeled nodes?",
                    "type": "single", "a": "Catalan Number C_n = (1 / (n + 1)) * (2n choose n)", "b": "N!", "c": "2^N", "d": "N^2", "ans": "A",
                    "exp": "The N-th Catalan number C_n counts structurally unique unlabeled binary tree topologies."
                },
                {
                    "q": "14. How many structurally unique Binary Search Trees can be formed with N distinct key values?",
                    "type": "single", "a": "Catalan Number C_n", "b": "N!", "c": "2^N - 1", "d": "N^2", "ans": "A",
                    "exp": "With keys sorted, choosing root i leaves C_(i-1) left subtrees and C_(n-i) right subtrees, producing C_n total BSTs."
                },
                {
                    "q": "15. In Boundary Traversal of a Binary Tree, in what order are boundary nodes collected?",
                    "type": "single", "a": "Root -> Left Boundary (excluding leaves) -> All Leaf Nodes -> Right Boundary in Reverse (excluding leaves)", "b": "Level order", "c": "Inorder traversal", "d": "Right boundary first", "ans": "A",
                    "exp": "Boundary traversal collects outer perimeter nodes counter-clockwise: Root, Left edge, Leaves, Right edge reverse."
                },
                {
                    "q": "16. What is the time complexity of Boundary Traversal on a tree of N nodes?",
                    "type": "single", "a": "O(N)", "b": "O(N^2)", "c": "O(log N)", "d": "O(H^2)", "ans": "A",
                    "exp": "Left boundary O(H), leaves DFS O(N), and right boundary O(H) combine to linear O(N) time."
                },
                {
                    "q": "17. What is an 'Expression Tree'?",
                    "type": "single", "a": "Binary tree where internal nodes are operators (+, -, *, /) and leaves are operands", "b": "BST tree", "c": "Heap tree", "d": "Trie tree", "ans": "A",
                    "exp": "Inorder traversal of expression tree yields infix math statement; Postorder yields postfix RPN."
                },
                {
                    "q": "18. In Construct Binary Tree from Preorder and Postorder Traversal, when is construction unique?",
                    "type": "single", "a": "Only if the binary tree is FULL (every node has 0 or 2 children)", "b": "Always unique", "c": "Never unique", "d": "Only for BST", "ans": "A",
                    "exp": "Single-child nodes create ambiguity between preorder/postorder; unique construction requires full binary trees."
                },
                {
                    "q": "19. What is the auxiliary space complexity of Level-Order Traversal on a Perfect Binary Tree of height H (N nodes)?",
                    "type": "single", "a": "O(N) queue memory (max level contains ~N/2 leaf nodes)", "b": "O(1)", "c": "O(log N)", "d": "O(H^2)", "ans": "A",
                    "exp": "The bottom leaf level holds N/2 nodes simultaneously in the BFS queue, requiring O(N) space."
                },
                {
                    "q": "20. How do you find the All Nodes Distance K from Target Node in Binary Tree?",
                    "type": "single", "a": "Build parent pointer graph links during DFS, then run BFS outwards from target node up to distance K", "b": "Sort nodes", "c": "Inorder traversal", "d": "Postorder only", "ans": "A",
                    "exp": "Mapping parent links converts binary tree into undirected graph; BFS expands distance K layer by layer."
                },
                {
                    "q": "21. What is the Maximum Path Sum between any two leaves in a binary tree?",
                    "type": "single", "a": "Postorder tracking max(max_leaf_path, left_path + right_path + node.val)", "b": "Root to leaf sum", "c": "Total sum", "d": "Leaf count", "ans": "A",
                    "exp": "Postorder recursion evaluates sum of left and right leaf paths passing through current node."
                },
                {
                    "q": "22. In Cousin Nodes in Binary Tree (same depth, different parents), how is relationship validated?",
                    "type": "single", "a": "Nodes P and Q have identical depth level AND node1.parent != node2.parent", "b": "Same parent", "c": "Different depth", "d": "Leaf nodes", "ans": "A",
                    "exp": "Cousins share the same depth level in tree hierarchy but possess distinct parent nodes."
                },
                {
                    "q": "23. In Population of Next Right Pointers in Each Node (Perfect Binary Tree), what pointer link is added?",
                    "type": "single", "a": "node.left.next = node.right and node.right.next = node.next.left", "b": "node.next = parent", "c": "node.next = left", "d": "node.next = root", "ans": "A",
                    "exp": "Leveraging existing next pointers connects level sibling nodes in O(1) extra space."
                },
                {
                    "q": "24. What is the time complexity to Count Complete Tree Nodes in less than O(N) time?",
                    "type": "single", "a": "O((log N)^2) by comparing left and right subtree heights to binary search complete level", "b": "O(N)", "c": "O(N^2)", "d": "O(1)", "ans": "A",
                    "exp": "If left_h == right_h, left subtree is perfect (2^h - 1 nodes); recurse right. Runs in O((log N)^2) time."
                },
                {
                    "q": "25. Which tree property guarantees that simple array 2*i and 2*i+1 indexing stores nodes compactly without empty slot gaps?",
                    "type": "single", "a": "Complete Binary Tree property", "b": "Skewed Tree property", "c": "BST property", "d": "Full Tree property", "ans": "A",
                    "exp": "Complete binary trees fill levels left-to-right, ensuring array indices 0..N-1 are densely packed."
                }
            ]
        },
        {
            "topic": "Binary Search Tree (BST)",
            "title": "Binary Search Tree Invariants & Operations Quiz",
            "description": "Master BST search, insert, delete (3 cases), inorder sorting property, BST validation, LCA in BST, floor/ceil, and Kth smallest element.",
            "questions": [
                {
                    "q": "1. What is the structural ordering invariant of a Binary Search Tree (BST)?",
                    "type": "single", "a": "Left Subtree values < Root value < Right Subtree values for EVERY node", "b": "Root value is always maximum", "c": "Left subtree height == Right subtree height", "d": "Nodes ordered by insertion order", "ans": "A",
                    "exp": "Every node in a BST strictly satisfies: all left descendants < node.val < all right descendants."
                },
                {
                    "q": "2. What tree traversal on a BST produces node key values in STRICTLY SORTED ascending order?",
                    "type": "single", "a": "Preorder Traversal", "b": "Inorder Traversal", "c": "Postorder Traversal", "d": "Level-order Traversal", "ans": "B",
                    "exp": "Inorder traversal (Left, Root, Right) processes BST keys in monotonically increasing sorted order."
                },
                {
                    "q": "3. What is the time complexity of Search, Insert, and Delete in a BALANCED BST of N nodes?",
                    "type": "single", "a": "O(N)", "b": "O(log N)", "c": "O(1)", "d": "O(N log N)", "ans": "B",
                    "exp": "When tree height H = O(log N), binary decisions eliminate half the remaining tree at each step."
                },
                {
                    "q": "4. What is the WORST-CASE time complexity of searching in a SKEWED (degenerate) BST of N nodes?",
                    "type": "single", "a": "O(log N)", "b": "O(N)", "c": "O(1)", "d": "O(N^2)", "ans": "B",
                    "exp": "Inserting sorted elements into un-balanced BST builds a linear chain of height N, degrading operations to O(N)."
                },
                {
                    "q": "5. In BST node DELETION, what replaces a deleted node that has TWO children?",
                    "type": "single", "a": "Inorder Successor (smallest node in right subtree) OR Inorder Predecessor (largest in left subtree)", "b": "Root of tree", "c": "NULL pointer", "d": "Random leaf", "ans": "A",
                    "exp": "Replacing with Inorder Successor preserves the BST ordering invariant without breaking subtrees."
                },
                {
                    "q": "6. How do you locate the MINIMUM key value in a BST?",
                    "type": "single", "a": "Traverse left pointers starting from Root until node.left is NULL", "b": "Traverse right pointers", "c": "Check root node", "d": "Inorder traversal to end", "ans": "A",
                    "exp": "The minimum value resides at the leftmost node of the BST."
                },
                {
                    "q": "7. How do you locate the MAXIMUM key value in a BST?",
                    "type": "single", "a": "Traverse right pointers starting from Root until node.right is NULL", "b": "Traverse left pointers", "c": "Check root node", "d": "Postorder traversal", "ans": "A",
                    "exp": "The maximum value resides at the rightmost node of the BST."
                },
                {
                    "q": "8. How can you validate if a Binary Tree is a VALID BST in linear O(N) time?",
                    "type": "single", "a": "DFS passing valid range bounds (min_val, max_val) down to children", "b": "Check node.left < node < node.right locally only", "c": "Check root only", "d": "Count nodes", "ans": "A",
                    "exp": "Local checks fail for deep illegal descendants. DFS must enforce global range (min_val < node.val < max_val)."
                },
                {
                    "q": "9. What is the time complexity to find K-th Smallest Element in a BST using Inorder Traversal?",
                    "type": "single", "a": "O(H + K) time, O(H) stack space", "b": "O(N^2)", "c": "O(1)", "d": "O(N log N)", "ans": "A",
                    "exp": "Iterative Inorder traversal stops as soon as K nodes are visited, taking O(H + K) time."
                },
                {
                    "q": "10. In BST, how is Lowest Common Ancestor (LCA) of nodes P and Q located efficiently in O(H) time?",
                    "type": "single", "a": "Starting from Root: if P and Q < curr, move left; if P and Q > curr, move right; else curr is LCA", "b": "Full DFS traversal", "c": "Level order search", "d": "Compare height", "ans": "A",
                    "exp": "The first node where P and Q split into left and right subtrees (or match curr) is the LCA in BST."
                },
                {
                    "q": "11. What is the FLOOR value of Key X in a BST?",
                    "type": "single", "a": "The largest key value in the BST that is <= X", "b": "The smallest key >= X", "c": "Key X minus 1", "d": "Root value", "ans": "A",
                    "exp": "Floor is the maximum node key smaller than or equal to target X."
                },
                {
                    "q": "12. What is the CEIL value of Key X in a BST?",
                    "type": "single", "a": "The smallest key value in the BST that is >= X", "b": "The largest key <= X", "c": "Key X plus 1", "d": "Leaf node", "ans": "A",
                    "exp": "Ceil is the minimum node key greater than or equal to target X."
                },
                {
                    "q": "13. How do you convert a Sorted Array into a Height-Balanced BST in O(N) time?",
                    "type": "single", "a": "Pick middle element arr[mid] as Root, recursively build left subtree from left half, right subtree from right half", "b": "Insert elements 1 by 1", "c": "Reverse array first", "d": "Use max heap", "ans": "A",
                    "exp": "Picking mid element divides array evenly, creating an optimal AVL-balanced BST of height O(log N)."
                },
                {
                    "q": "14. How do you convert a Sorted Doubly Linked List into a Balanced BST in-place in O(N) time?",
                    "type": "single", "a": "Bottom-up Inorder simulation advancing list head pointer as nodes are built", "b": "Top-down searching", "c": "Copying to array", "d": "Quick sort", "ans": "A",
                    "exp": "Bottom-up construction builds left subtree, assigns curr list head as root, and builds right subtree in linear O(N)."
                },
                {
                    "q": "15. In Two Sum IV - Input is a BST (find 2 nodes summing to Target), what space-efficient technique runs in O(N) time and O(H) space?",
                    "type": "single", "a": "Two BST Iterators (1 normal Inorder, 1 Reverse Inorder)", "b": "Array sorting", "c": "Nested loops", "d": "Matrix search", "ans": "A",
                    "exp": "Two iterators act like two pointers L and R on sorted array, requiring only O(H) stack memory."
                },
                {
                    "q": "16. What algorithm restores a BST where EXACTLY TWO nodes were swapped accidentally (Recover BST)?",
                    "type": "single", "a": "Inorder traversal tracking prev node; detect 1st swap (prev > curr) and 2nd swap (prev > curr), then swap back values", "b": "Rebuild tree from scratch", "c": "Delete root", "d": "Rotate tree", "ans": "A",
                    "exp": "Inorder traversal on BST is strictly sorted. Swapped nodes create 1 or 2 inverted adjacent pairs in O(N) time & O(1) space."
                },
                {
                    "q": "17. What is the time complexity to Construct a BST from a Given Preorder Traversal array of size N?",
                    "type": "single", "a": "O(N) passing upper bound constraint down recursive calls", "b": "O(N^2)", "c": "O(N log N)", "d": "O(2^N)", "ans": "A",
                    "exp": "Using upper bound constraint checks whether next preorder value belongs to current subtree in linear O(N) time."
                },
                {
                    "q": "18. What is the Range Sum of BST (sum of node values in range [Low, High]) time complexity?",
                    "type": "single", "a": "O(N) worst case, pruned branches skip subtrees out of range", "b": "O(N^2)", "c": "O(1)", "d": "O(2^N)", "ans": "A",
                    "exp": "Pruning subtrees where root < Low (skip left) or root > High (skip right) optimizes search traversal."
                },
                {
                    "q": "19. What data structure maintains dynamic median of data stream in O(log N) insert time?",
                    "type": "single", "a": "Self-Balancing BST (or Dual Heaps: Max-Heap for left half, Min-Heap for right half)", "b": "Single Stack", "c": "Circular Queue", "d": "Unsorted Array", "ans": "A",
                    "exp": "Dual heaps or balanced BST keep sizes equalized, yielding stream median in O(1) access and O(log N) insertion."
                },
                {
                    "q": "20. In BST Inorder Successor search without parent pointers, what node is tracked when moving LEFT?",
                    "type": "single", "a": "Current node is candidate successor (successor = curr)", "b": "Predecessor node", "c": "Root node", "d": "NULL", "ans": "A",
                    "exp": "When moving left, current root is larger than target, so it becomes potential candidate successor."
                },
                {
                    "q": "21. What is the Largest BST Subtree in Binary Tree algorithm time complexity?",
                    "type": "single", "a": "O(N) bottom-up returning (is_bst, size, min_val, max_val)", "b": "O(N^2)", "c": "O(N log N)", "d": "O(2^N)", "ans": "A",
                    "exp": "Bottom-up postorder aggregates subtree range bounds and node count, verifying BST status in linear O(N) time."
                },
                {
                    "q": "22. Why does a standard BST fail to guarantee O(log N) operational performance in real-world applications?",
                    "type": "single", "a": "Sorted or semi-sorted insertion sequences cause tree height to degrade to O(N)", "b": "BST cannot store integers", "c": "Pointers leak memory", "d": "Nodes take too much memory", "ans": "A",
                    "exp": "Without self-balancing mechanisms, sequential inserts build skewed line trees of height N."
                },
                {
                    "q": "23. In BST insertion, where is a new unique key inserted?",
                    "type": "single", "a": "Always as a NEW LEAF node at appropriate NULL pointer position", "b": "At root position", "c": "As middle node", "d": "In place of existing key", "ans": "A",
                    "exp": "Standard BST insertion traverses down search path until reaching NULL leaf position where node is attached."
                },
                {
                    "q": "24. In BST, what is the Inorder Predecessor of a node X with a LEFT child?",
                    "type": "single", "a": "The MAXIMUM key node in X's LEFT subtree (rightmost node of left child)", "b": "Minimum in right subtree", "c": "Parent node", "d": "Root node", "ans": "A",
                    "exp": "Inorder predecessor is the largest value smaller than X, located at rightmost node of left subtree."
                },
                {
                    "q": "25. What property distinguishes BST from a Binary Heap?",
                    "type": "single", "a": "BST enforces Left < Root < Right order; Heap enforces Parent >= Child (Max-Heap) across both children", "b": "Heap is sorted inorder", "c": "BST is array based", "d": "Heap has height N", "ans": "A",
                    "exp": "BST maintains horizontal search ordering; Binary Heap maintains vertical priority parent-child ordering."
                }
            ]
        },
        {
            "topic": "AVL Tree",
            "title": "AVL Trees & Self-Balancing Rotations Quiz",
            "description": "Master balance factor invariant (-1, 0, 1), single rotations (LL, RR), double rotations (LR, RL), insertion/deletion rebalancing, and AVL height bounds.",
            "questions": [
                {
                    "q": "1. What is an AVL Tree?",
                    "type": "single", "a": "Self-balancing Binary Search Tree where height difference between left and right subtrees of EVERY node is at most 1", "b": "Complete binary tree heap", "c": "Unsorted binary tree", "d": "B-Tree of order 5", "ans": "A",
                    "exp": "AVL tree is the first self-balancing BST; height balance factor is strictly restricted to {-1, 0, +1}."
                },
                {
                    "q": "2. How is the Balance Factor (BF) of a node calculated in an AVL Tree?",
                    "type": "single", "a": "BF(node) = Height(Left Subtree) - Height(Right Subtree)", "b": "BF(node) = Left nodes + Right nodes", "c": "BF(node) = node.val / 2", "d": "BF(node) = Height / N", "ans": "A",
                    "exp": "Balance factor equals height of left child minus height of right child."
                },
                {
                    "q": "3. What values of Balance Factor indicate that an AVL tree node is OUT OF BALANCE and requires rotation?",
                    "type": "single", "a": "BF > 1 or BF < -1 (i.e. BF = +2 or BF = -2)", "b": "BF == 0", "c": "BF == 1", "d": "BF == -1", "ans": "A",
                    "exp": "Valid balance factors are -1, 0, +1. Any value outside this range (e.g. +2 or -2) triggers rebalancing rotations."
                },
                {
                    "q": "4. What is the MAXIMUM height H of an AVL tree containing N nodes?",
                    "type": "single", "a": "H <= 1.44 * log2(N)", "b": "H = N", "c": "H = N / 2", "d": "H = N^2", "ans": "A",
                    "exp": "AVL trees strictly guarantee height H < 1.44 log2 N, assuring O(log N) worst-case search time."
                },
                {
                    "q": "5. What rotation rebalances a Left-Left (LL) imbalance (node BF = +2, left child BF = +1)?",
                    "type": "single", "a": "Single Right Rotation (Rotate Right around unbalanced node)", "b": "Single Left Rotation", "c": "Left-Right Rotation", "d": "Right-Left Rotation", "ans": "A",
                    "exp": "LL imbalance (heavy left-left branch) is resolved by a single Right Rotation."
                },
                {
                    "q": "6. What rotation rebalances a Right-Right (RR) imbalance (node BF = -2, right child BF = -1)?",
                    "type": "single", "a": "Single Left Rotation (Rotate Left around unbalanced node)", "b": "Single Right Rotation", "c": "Right-Left Rotation", "d": "Left-Right Rotation", "ans": "A",
                    "exp": "RR imbalance (heavy right-right branch) is resolved by a single Left Rotation."
                },
                {
                    "q": "7. What rotations rebalance a Left-Right (LR) imbalance (node BF = +2, left child BF = -1)?",
                    "type": "single", "a": "Left Rotation on Left Child, followed by Right Rotation on Unbalanced Node", "b": "Single Right Rotation", "c": "Single Left Rotation", "d": "Two Right Rotations", "ans": "A",
                    "exp": "LR double rotation first turns left child into LL shape (Left Rotate), then Right Rotates unbalanced root."
                },
                {
                    "q": "8. What rotations rebalance a Right-Left (RL) imbalance (node BF = -2, right child BF = +1)?",
                    "type": "single", "a": "Right Rotation on Right Child, followed by Left Rotation on Unbalanced Node", "b": "Single Left Rotation", "c": "Single Right Rotation", "d": "Two Left Rotations", "ans": "A",
                    "exp": "RL double rotation converts right child to RR shape (Right Rotate), then Left Rotates unbalanced root."
                },
                {
                    "q": "9. What is the time complexity of a single tree rotation (Left or Right)?",
                    "type": "single", "a": "O(1)", "b": "O(log N)", "c": "O(N)", "d": "O(N^2)", "ans": "A",
                    "exp": "Tree rotation only updates 3 pointer references and height numbers, running in constant O(1) time."
                },
                {
                    "q": "10. During INSERTION in an AVL tree, what is the maximum number of rotations required to restore balance to the entire tree?",
                    "type": "single", "a": "At most 1 single or 1 double rotation (at most 2 pointer rotations total)", "b": "O(N) rotations", "c": "O(log N) rotations", "d": "N rotations", "ans": "A",
                    "exp": "After inserting a node, rebalancing at the lowest unbalanced ancestor restores height across the whole tree."
                },
                {
                    "q": "11. During DELETION in an AVL tree, what is the maximum number of rotations required to restore balance?",
                    "type": "single", "a": "Up to O(log N) rotations (rebalancing may propagate up ancestors to root)", "b": "At most 1 rotation", "c": "0 rotations", "d": "O(N) rotations", "ans": "A",
                    "exp": "Node deletion can shorten subtrees, causing height balance fixes to ripple up to log N ancestors."
                },
                {
                    "q": "12. What is the worst-case time complexity for Search, Insert, and Delete in an AVL tree of N nodes?",
                    "type": "single", "a": "O(log N) for all three operations", "b": "O(N) for delete", "c": "O(1) for search", "d": "O(N log N)", "ans": "A",
                    "exp": "Strict height balance H = O(log N) guarantees O(log N) worst-case time for search, insert, and delete."
                },
                {
                    "q": "13. How does an AVL Tree compare with a Red-Black Tree in terms of search speed vs insertion/deletion overhead?",
                    "type": "single", "a": "AVL is more strictly balanced (faster searches), but requires more rotations during frequent insertions/deletions", "b": "Red-Black is faster for searches", "c": "AVL requires no rotations", "d": "Red-Black has height N", "ans": "A",
                    "exp": "AVL maintains tighter height bounds (log2 N vs 2 log2 N for Red-Black), yielding faster lookups but higher rebalancing cost."
                },
                {
                    "q": "14. What minimum number of nodes N(H) is required to construct an AVL tree of height H?",
                    "type": "single", "a": "N(H) = N(H-1) + N(H-2) + 1 (Fibonacci-like tree recurrence)", "b": "2^H - 1", "c": "H + 1", "d": "H^2", "ans": "A",
                    "exp": "Minimal AVL trees (Fibonacci Trees) satisfy N(H) = N(H-1) + N(H-2) + 1 with base cases N(0)=1, N(1)=2."
                },
                {
                    "q": "15. In Right Rotation around node Z (with left child Y and Y's right child T2), where does T2 attach after rotation?",
                    "type": "single", "a": "T2 becomes the LEFT child of node Z", "b": "T2 becomes right child of Y", "c": "T2 becomes root", "d": "T2 is deleted", "ans": "A",
                    "exp": "Right rotation sets Y->right = Z and Z->left = T2, preserving BST order since T2 values lie between Y and Z."
                },
                {
                    "q": "16. In Left Rotation around node X (with right child Y and Y's left child T2), where does T2 attach after rotation?",
                    "type": "single", "a": "T2 becomes the RIGHT child of node X", "b": "T2 becomes left child of Y", "c": "T2 becomes root", "d": "T2 is deleted", "ans": "A",
                    "exp": "Left rotation sets Y->left = X and X->right = T2, preserving BST ordering."
                },
                {
                    "q": "17. What extra data field must every node in an AVL tree store?",
                    "type": "single", "a": "Height of the node (or Balance Factor)", "b": "Parent pointer only", "c": "Color bit", "d": "Degree count", "ans": "A",
                    "exp": "AVL nodes maintain an integer 'height' field to compute balance factor during bottom-up recursion."
                },
                {
                    "q": "18. What is the space complexity of storing an AVL tree of N nodes?",
                    "type": "single", "a": "O(N) memory for nodes and height fields", "b": "O(N log N)", "c": "O(N^2)", "d": "O(1)", "ans": "A",
                    "exp": "N nodes with pointers, keys, and integer height fields consume linear O(N) memory."
                },
                {
                    "q": "19. If an AVL tree node has height 0 (leaf), what is its height after inserting a single child?",
                    "type": "single", "a": "1", "b": "2", "c": "0", "d": "-1", "ans": "A",
                    "exp": "Height = 1 + max(left_height, right_height). Parent of leaf has height 1."
                },
                {
                    "q": "20. What is the height of an empty (NULL) subtree in AVL balance factor calculations?",
                    "type": "single", "a": "-1 (or 0 depending on convention)", "b": "1", "c": "100", "d": "Undefined", "ans": "A",
                    "exp": "NULL subtree height is treated as -1, so a leaf node with two NULL children has height 1 + max(-1, -1) = 0."
                },
                {
                    "q": "21. Why are AVL trees preferred over Red-Black trees in lookup-heavy database index applications?",
                    "type": "single", "a": "Stricter balance factor guarantees shorter tree height, minimizing disk read / pointer traversal operations", "b": "AVL uses less memory", "c": "AVL has no pointers", "d": "Red-Black cannot be searched", "ans": "A",
                    "exp": "Shallow height minimizes comparison steps, making AVL optimal for read-intensive databases."
                },
                {
                    "q": "22. In AVL tree rebalancing after insertion, how do you determine whether an imbalance at node Z is LL vs LR?",
                    "type": "single", "a": "Check left child Y: if inserted key < Y.key it is LL; if inserted key > Y.key it is LR", "b": "Check root key", "c": "Check height", "d": "Random check", "ans": "A",
                    "exp": "Key comparison identifies whether inserted node fell into left child's left subtree (LL) or right subtree (LR)."
                },
                {
                    "q": "23. In an AVL tree with 1 node, what is the tree height (using 0-based root convention)?",
                    "type": "single", "a": "0", "b": "1", "c": "2", "d": "-1", "ans": "A",
                    "exp": "Single root node tree has height 0 under standard edge-count height convention."
                },
                {
                    "q": "24. What happens if you attempt to insert a duplicate key into a standard AVL Tree?",
                    "type": "single", "a": "Duplicates are rejected/ignored OR stored in node frequency counter", "b": "Duplicates crash tree", "c": "Tree height becomes N", "d": "Replaces root", "ans": "A",
                    "exp": "Standard BSTs ignore duplicate keys or maintain a frequency count field in existing node."
                },
                {
                    "q": "25. Who invented the AVL Tree data structure in 1962?",
                    "type": "single", "a": "Adelson-Velsky and Landis", "b": "Algorithm, Vector & Logic", "c": "Alan Turing & Von Neumann", "d": "Dijkstra & Knuth", "ans": "A",
                    "exp": "AVL tree was invented in 1962 by Soviet mathematicians Georgy Adelson-Velsky and Evgenii Landis."
                }
            ]
        },
        {
            "topic": "Heap",
            "title": "Min-Heap, Max-Heap & Priority Queue Operations Quiz",
            "description": "Master heap invariants (Min-Heap, Max-Heap), array representation, Heapify (O(N)), Heap Sort, Priority Queues, K-way merges, and median streams.",
            "questions": [
                {
                    "q": "1. What ordering property defines a MAX-HEAP?",
                    "type": "single", "a": "Every parent node key is GREATER than or equal to its children keys (Root is Maximum)", "b": "Left child < Root < Right child", "c": "Root is minimum", "d": "Leaf nodes are maximum", "ans": "A",
                    "exp": "Max-Heap property enforces parent key >= children keys; max element always resides at root."
                },
                {
                    "q": "2. What ordering property defines a MIN-HEAP?",
                    "type": "single", "a": "Every parent node key is LESS than or equal to its children keys (Root is Minimum)", "b": "Root is maximum", "c": "Sorted left to right", "d": "Leaves are minimum", "ans": "A",
                    "exp": "Min-Heap property enforces parent key <= children keys; min element always resides at root."
                },
                {
                    "q": "3. What structural property must every Binary Heap satisfy?",
                    "type": "single", "a": "Must be a Complete Binary Tree (all levels filled except possibly last, filled left-to-right)", "b": "Must be AVL balanced", "c": "Must be skewed", "d": "Full tree", "ans": "A",
                    "exp": "Complete binary tree property allows storing heaps compactly in arrays without empty slot gaps."
                },
                {
                    "q": "4. In 0-based array heap representation, given parent index i, what are the left child, right child, and parent indices?",
                    "type": "single", "a": "left = 2*i + 1, right = 2*i + 2, parent = (i - 1) // 2", "b": "left = 2*i, right = 2*i + 1, parent = i / 2", "c": "left = i + 1, right = i + 2, parent = i - 1", "d": "left = i * 2, right = i * 4, parent = i / 4", "ans": "A",
                    "exp": "0-based array index arithmetic maps left child = 2i + 1, right child = 2i + 2, parent = (i - 1) // 2."
                },
                {
                    "q": "5. What is the time complexity to INSERT a new element into a Binary Heap of N elements?",
                    "type": "single", "a": "O(log N) using Percolate Up / Bubble Up", "b": "O(N)", "c": "O(1)", "d": "O(N log N)", "ans": "A",
                    "exp": "Append to array end, then bubble up along tree height O(log N) to restore heap property."
                },
                {
                    "q": "6. What is the time complexity to EXTRACT MAX / MIN (pop root) from a Binary Heap of N elements?",
                    "type": "single", "a": "O(log N) using Percolate Down / Heapify", "b": "O(1)", "c": "O(N)", "d": "O(N^2)", "ans": "A",
                    "exp": "Swap root with last leaf element, remove last element, and percolate down root in O(log N) time."
                },
                {
                    "q": "7. What is the time complexity to BUILD A HEAP (Heapify) from an unsorted array of N elements?",
                    "type": "single", "a": "O(N) bottom-up heapify", "b": "O(N log N)", "c": "O(N^2)", "d": "O(log N)", "ans": "A",
                    "exp": "Bottom-up heapify calling percolate_down from non-leaf nodes N/2 down to 0 sums to O(N) linear time."
                },
                {
                    "q": "8. What is the worst-case time complexity of HEAP SORT on an array of N elements?",
                    "type": "single", "a": "O(N log N) time and O(1) auxiliary space", "b": "O(N^2) time", "c": "O(N) time", "d": "O(2^N)", "ans": "A",
                    "exp": "Build Max-Heap O(N), then repeatedly extract max and swap with end N times (N * log N = O(N log N) in-place)."
                },
                {
                    "q": "9. Is Heap Sort a STABLE sorting algorithm?",
                    "type": "single", "a": "No, non-adjacent element swaps break relative order of equal keys", "b": "Yes, always stable", "c": "Stable only for integers", "d": "Stable for strings", "ans": "A",
                    "exp": "Heap sift-down swaps distant elements, making Heap Sort unstable."
                },
                {
                    "q": "10. In array of size N representing Max-Heap, at what index do LEAF nodes start (0-based indexing)?",
                    "type": "single", "a": "Index floor(N / 2)", "b": "Index 0", "c": "Index N - 1", "d": "Index floor(N / 4)", "ans": "A",
                    "exp": "Nodes from floor(N/2) to N-1 are leaf nodes with no children, requiring no heapify."
                },
                {
                    "q": "11. What is the time complexity to find the MINIMUM element in a MAX-HEAP of N elements?",
                    "type": "single", "a": "O(N) search among leaf nodes floor(N/2)..N-1", "b": "O(1)", "c": "O(log N)", "d": "O(N log N)", "ans": "A",
                    "exp": "In Max-Heap, minimum element can be any leaf node; searching N/2 leaves takes linear O(N) time."
                },
                {
                    "q": "12. In K-th Largest Element in an Array problem, what heap size should be maintained to achieve O(N log K) time?",
                    "type": "single", "a": "Min-Heap of size K (root holds K-th largest element)", "b": "Max-Heap of size N", "c": "Min-Heap of size N", "d": "Max-Heap of size K", "ans": "A",
                    "exp": "Maintaining size-K Min-Heap evicts smaller elements, leaving K largest elements with minimum at root."
                },
                {
                    "q": "13. In Find Median from Data Stream, what two heaps are used?",
                    "type": "single", "a": "Max-Heap for lower half of numbers, Min-Heap for upper half of numbers", "b": "Two Min-Heaps", "c": "Two Max-Heaps", "d": "Single Heap", "ans": "A",
                    "exp": "Max-Heap (lower half) top and Min-Heap (upper half) top yield median in O(1) time."
                },
                {
                    "q": "14. What is the time complexity of Merging K Sorted Lists of total N elements using Min-Heap?",
                    "type": "single", "a": "O(N log K)", "b": "O(N * K)", "c": "O(N^2)", "d": "O(K log N)", "ans": "A",
                    "exp": "Min-heap holds first element from each of K lists; extracting min and pushing next element takes O(N log K)."
                },
                {
                    "q": "15. What is a 'd-ary Heap'?",
                    "type": "single", "a": "Heap where each non-leaf node has d children instead of 2", "b": "Heap with d levels", "c": "Dual heap", "d": "Dynamic heap", "ans": "A",
                    "exp": "d-ary heap increases fan-out: decrease-key runs faster O(log_d N), while extract-min takes O(d log_d N)."
                },
                {
                    "q": "16. In Fibonacci Heap, what is the amortized time complexity of Insert, Find-Min, and Decrease-Key operations?",
                    "type": "single", "a": "O(1) amortized time for Insert, Find-Min, and Decrease-Key", "b": "O(log N)", "c": "O(N)", "d": "O(N^2)", "ans": "A",
                    "exp": "Fibonacci Heap achieves O(1) amortized for insert, find-min, decrease-key (Extract-Min remains O(log N))."
                },
                {
                    "q": "17. What graph shortest path algorithm benefits directly from Fibonacci Heap's O(1) Decrease-Key performance?",
                    "type": "single", "a": "Dijkstra's Algorithm (improves time from O(E log V) to O(E + V log V))", "b": "Bellman-Ford", "c": "Floyd-Warshall", "d": "Kruskal MST", "ans": "A",
                    "exp": "O(1) decrease-key lowers edge relaxations cost to O(E), improving total time to O(E + V log V)."
                },
                {
                    "q": "18. What heap operation is used in Priority Queue to change an element's value and fix heap order?",
                    "type": "single", "a": "Decrease-Key / Increase-Key (percolate up if smaller in Min-Heap, down if larger)", "b": "Sort heap", "c": "Clear heap", "d": "Reverse array", "ans": "A",
                    "exp": "Updating value and calling bubble-up or sift-down restores heap property in O(log N) time."
                },
                {
                    "q": "19. In Top K Frequent Elements problem (array of N numbers), how can you solve it in O(N log K) time?",
                    "type": "single", "a": "Count frequencies using Hash Map, then maintain Min-Heap of size K based on frequency", "b": "Sort array", "c": "Max-Heap of size N", "d": "2D Matrix", "ans": "A",
                    "exp": "Min-Heap of size K retains K highest frequency entries, taking O(N log K) overall time."
                },
                {
                    "q": "20. How do you implement a Max-Heap in Python's heapq module (which only provides Min-Heap by default)?",
                    "type": "single", "a": "Multiply numerical values by -1 before push and after pop", "b": "Reverse array", "c": "Pass custom comparator function", "d": "Python cannot handle Max-Heap", "ans": "A",
                    "exp": "Negating numbers flips inequality sign, allowing heapq min-heap to function as max-heap."
                },
                {
                    "q": "21. What is the space complexity of storing a Binary Heap of N elements in an array?",
                    "type": "single", "a": "O(N) contiguous array memory", "b": "O(N log N)", "c": "O(N^2)", "d": "O(1)", "ans": "A",
                    "exp": "Binary heap uses array buffer of size N without extra pointer overhead."
                },
                {
                    "q": "22. In Reorganize String problem (rearrange so no adjacent identical chars), what heap strategy is used?",
                    "type": "single", "a": "Max-Heap of character frequencies; pop top 2 most frequent characters per step", "b": "Min-Heap", "c": "Stack", "d": "Sort string", "ans": "A",
                    "exp": "Popping top 2 distinct characters guarantees adjacent characters differ while exhausting high frequencies."
                },
                {
                    "q": "23. What is the time complexity to Peek the Root element of a Min-Heap?",
                    "type": "single", "a": "O(1)", "b": "O(log N)", "c": "O(N)", "d": "O(N log N)", "ans": "A",
                    "exp": "Root element resides at array index 0; peeking accesses heap[0] in constant O(1) time."
                },
                {
                    "q": "24. In Minimum Cost to Connect Ropes problem, what heap strategy minimizes total cost?",
                    "type": "single", "a": "Min-Heap: repeatedly pop 2 smallest ropes, add sum to cost, push sum back to Min-Heap", "b": "Max-Heap", "c": "Sort once", "d": "Stack", "ans": "A",
                    "exp": "Greedy choice combining two shortest ropes at each step minimizes accumulated connection cost (Huffman coding)."
                },
                {
                    "q": "25. Which heap type supports O(1) Meld (merge two heaps) operation?",
                    "type": "single", "a": "Pairing Heap / Fibonacci Heap / Binomial Heap", "b": "Standard Binary Heap", "c": "Static Array Heap", "d": "B-Tree", "ans": "A",
                    "exp": "Mergeable heaps (Binomial, Fibonacci, Pairing) support uniting two heaps efficiently."
                }
            ]
        },
        {
            "topic": "Graph",
            "title": "Graph Algorithms, Shortest Paths & Topological Sort Quiz",
            "description": "Master Adjacency List/Matrix, BFS, DFS, Cycle Detection, Topological Sort (Kahn's), Dijkstra, Bellman-Ford, Kruskal/Prim MST, and Tarjan SCC.",
            "questions": [
                {
                    "q": "1. What is the space complexity of storing a Graph G(V, E) using an Adjacency Matrix vs Adjacency List?",
                    "type": "single", "a": "Adjacency Matrix: O(V^2); Adjacency List: O(V + E)", "b": "Matrix: O(V+E); List: O(V^2)", "c": "Matrix: O(E); List: O(V)", "d": "Both are O(V*E)", "ans": "A",
                    "exp": "Adjacency matrix allocates V x V grid O(V^2); Adjacency list stores only actual edges O(V + E)."
                },
                {
                    "q": "2. What graph traversal algorithm uses a FIFO Queue and finds Shortest Path in UNWEIGHTED graphs?",
                    "type": "single", "a": "Breadth-First Search (BFS)", "b": "Depth-First Search (DFS)", "c": "Dijkstra's Algorithm", "d": "Floyd-Warshall", "ans": "A",
                    "exp": "BFS explores graph level-by-level, guaranteeing shortest path in unweighted graphs in O(V + E) time."
                },
                {
                    "q": "3. What graph traversal uses a Call Stack / Recursion and explores deep along edges before backtracking?",
                    "type": "single", "a": "Depth-First Search (DFS)", "b": "Breadth-First Search (BFS)", "c": "Kahn's Algorithm", "d": "Prim's Algorithm", "ans": "A",
                    "exp": "DFS traverses deeply down path branches until hitting dead ends, then backtracks."
                },
                {
                    "q": "4. What is the time complexity of BFS and DFS traversals on a graph represented as an Adjacency List?",
                    "type": "single", "a": "O(V + E)", "b": "O(V * E)", "c": "O(V^2)", "d": "O(E log V)", "ans": "A",
                    "exp": "Every vertex and edge is visited a constant number of times, yielding linear O(V + E) complexity."
                },
                {
                    "q": "5. How do you detect a Cycle in an UNDIRECTED Graph using Disjoint Set Union (DSU)?",
                    "type": "single", "a": "If find(u) == find(v) for edge (u, v), a cycle exists", "b": "If degree(u) > 2", "c": "If V > E", "d": "If indegree == 0", "ans": "A",
                    "exp": "If two endpoints of an edge already belong to the same connected component set, adding the edge forms a cycle."
                },
                {
                    "q": "6. How do you detect a Cycle in a DIRECTED Graph using DFS?",
                    "type": "single", "a": "Track visit states: Unvisited (0), Visiting/Active in Call Stack (1), Visited (2). Encountering state 1 indicates back-edge cycle", "b": "Check indegrees", "c": "Count edges", "d": "Check connected components", "ans": "A",
                    "exp": "Re-encountering a node currently in active recursion stack (state 1) identifies a directed back-edge cycle."
                },
                {
                    "q": "7. What is Topological Sort?",
                    "type": "single", "a": "Linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u -> v, u comes before v", "b": "Sorting graph vertices alphabetically", "c": "Finding shortest path", "d": "BFS on undirected graph", "ans": "A",
                    "exp": "Topological sort orders DAG dependencies (e.g. course prerequisites) in linear O(V + E) time."
                },
                {
                    "q": "8. What algorithm uses In-Degree counting and a Queue to perform Topological Sort (Kahn's Algorithm)?",
                    "type": "single", "a": "Kahn's Algorithm: enqueue 0-indegree nodes, pop node, decrement neighbor indegrees, enqueue new 0-indegree nodes", "b": "Dijkstra's Algorithm", "c": "Kosaraju's Algorithm", "d": "Tarjan's Algorithm", "ans": "A",
                    "exp": "Kahn's algorithm processes 0-indegree nodes sequentially. If processed nodes < V, graph has a cycle."
                },
                {
                    "q": "9. What shortest path algorithm finds single-source shortest paths in NON-NEGATIVE weighted graphs using Min-Priority Queue?",
                    "type": "single", "a": "Dijkstra's Algorithm", "b": "Bellman-Ford Algorithm", "c": "Floyd-Warshall Algorithm", "d": "Kruskal's Algorithm", "ans": "A",
                    "exp": "Greedy choice using Min-PQ relaxes shortest distance estimates in O((V + E) log V) time."
                },
                {
                    "q": "10. Why does Dijkstra's Algorithm FAIL or enter infinite loops on graphs with NEGATIVE edge weights?",
                    "type": "single", "a": "Greedy assumption breaks (visited distance can be re-shortened by negative edge), causing incorrect distances or infinite loops in negative cycles", "b": "Priority queue crashes", "c": "Memory leak", "d": "Graph becomes disconnected", "ans": "A",
                    "exp": "Dijkstra assumes distance estimates never decrease once popped. Negative edges violate this greedy principle."
                },
                {
                    "q": "11. What algorithm computes single-source shortest paths on graphs with NEGATIVE edge weights and detects negative weight cycles?",
                    "type": "single", "a": "Bellman-Ford Algorithm", "b": "Dijkstra's Algorithm", "c": "Kahn's Algorithm", "d": "Prim's Algorithm", "ans": "A",
                    "exp": "Bellman-Ford relaxes all E edges V-1 times. A 16th relaxation loop detecting distance decreases confirms a negative cycle."
                },
                {
                    "q": "12. What is the time complexity of Bellman-Ford Algorithm on graph G(V, E)?",
                    "type": "single", "a": "O(V * E)", "b": "O((V + E) log V)", "c": "O(V^3)", "d": "O(V + E)", "ans": "A",
                    "exp": "V-1 iterations scanning all E edges yields O(V * E) time complexity."
                },
                {
                    "q": "13. What algorithm computes ALL-PAIRS shortest paths between every pair of vertices in O(V^3) time?",
                    "type": "single", "a": "Floyd-Warshall Algorithm", "b": "Dijkstra's Algorithm", "c": "Bellman-Ford Algorithm", "d": "Tarjan's Algorithm", "ans": "A",
                    "exp": "Dynamic programming matrix update dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) across 3 nested loops V times."
                },
                {
                    "q": "14. What is a Minimum Spanning Tree (MST)?",
                    "type": "single", "a": "Subset of edges connecting all V vertices in a weighted connected graph without cycles, with MINIMUM total edge weight", "b": "Shortest path tree from root", "c": "Graph with max edges", "d": "Directed graph component", "ans": "A",
                    "exp": "MST spans all V vertices using V-1 edges with smallest cumulative weight sum."
                },
                {
                    "q": "15. How does Kruskal's Algorithm build a Minimum Spanning Tree?",
                    "type": "single", "a": "Sort all E edges by weight, iterate sorted edges, add edge to MST if DSU find(u) != find(v)", "b": "Grow tree from single root using PQ", "c": "DFS traversal", "d": "Topological sort", "ans": "A",
                    "exp": "Greedy edge choice combined with Disjoint Set Union (DSU) cycle prevention runs in O(E log E) time."
                },
                {
                    "q": "16. How does Prim's Algorithm build a Minimum Spanning Tree?",
                    "type": "single", "a": "Start from arbitrary vertex, maintain Min-PQ of edges connected to visited tree, greedily pick smallest edge to unvisited node", "b": "Sort all edges first", "c": "Use Bellman-Ford", "d": "Matrix multiplication", "ans": "A",
                    "exp": "Prim's grows a single connected component tree out from start vertex in O(E log V) time."
                },
                {
                    "q": "17. What is a Bipartite Graph?",
                    "type": "single", "a": "Graph whose vertices can be divided into 2 disjoint sets U and V such that every edge connects a vertex in U to a vertex in V", "b": "Graph with 2 edges", "c": "Complete graph", "d": "Tree of degree 2", "ans": "A",
                    "exp": "Graph is bipartite if and only if it contains NO odd-length cycles (validated via 2-coloring BFS/DFS)."
                },
                {
                    "q": "18. What is a Strongly Connected Component (SCC) in a Directed Graph?",
                    "type": "single", "a": "Maximal subgraph where EVERY vertex is reachable from every other vertex in the subgraph", "b": "Connected component in undirected graph", "c": "A cyclic path", "d": "Tree component", "ans": "A",
                    "exp": "SCC represents maximal vertex sets with mutual reachability u -> v and v -> u."
                },
                {
                    "q": "19. What algorithm finds all Strongly Connected Components in a Directed Graph in linear O(V + E) time using low-link values?",
                    "type": "single", "a": "Tarjan's SCC Algorithm (or Kosaraju's Algorithm)", "b": "Dijkstra's Algorithm", "c": "Kruskal's Algorithm", "d": "Floyd-Warshall", "ans": "A",
                    "exp": "Tarjan's algorithm uses DFS discovery times and low-link values on a stack to extract SCCs in O(V + E)."
                },
                {
                    "q": "20. What is an Articulation Point (Cut Vertex) in a graph?",
                    "type": "single", "a": "A vertex whose removal increases the number of connected components (disconnects the graph)", "b": "Leaf vertex", "c": "Root vertex", "d": "Vertex with max degree", "ans": "A",
                    "exp": "Cut vertices are critical nodes whose failure fractures the graph network into isolated sub-graphs."
                },
                {
                    "q": "21. What condition identifies a Bridge (Cut Edge) in graph DFS low-link calculation for edge u -> v?",
                    "type": "single", "a": "low[v] > disc[u]", "b": "low[v] == disc[u]", "c": "disc[v] < disc[u]", "d": "degree[u] == 1", "ans": "A",
                    "exp": "If lowest discovery time reachable from v is strictly greater than u's discovery time, edge (u, v) is a Bridge."
                },
                {
                    "q": "22. In Network Flow, what theorem states that Maximum Flow through a network equals Minimum Capacity Cut?",
                    "type": "single", "a": "Max-Flow Min-Cut Theorem (Ford-Fulkerson Algorithm)", "b": "Master Theorem", "c": "Euler's Theorem", "d": "Handshaking Lemma", "ans": "A",
                    "exp": "Max-Flow Min-Cut theorem establishes duality between maximum flow and minimum bottleneck cut capacity."
                },
                {
                    "q": "23. What is an Eulerian Path in a graph?",
                    "type": "single", "a": "Path that visits EVERY EDGE in the graph exactly once", "b": "Path visiting every vertex once", "c": "Shortest path", "d": "Cycle path", "ans": "A",
                    "exp": "Eulerian path traverses every edge once. Exists if connected graph has 0 or 2 vertices of odd degree."
                },
                {
                    "q": "24. What is a Hamiltonian Path in a graph?",
                    "type": "single", "a": "Path that visits EVERY VERTEX in the graph exactly once", "b": "Path visiting every edge once", "c": "Minimum spanning tree", "d": "BFS path", "ans": "A",
                    "exp": "Hamiltonian path visits every vertex once (NP-complete problem solved via backtracking / Bitmask DP)."
                },
                {
                    "q": "25. What is the Handshaking Lemma for undirected graphs?",
                    "type": "single", "a": "Sum of degrees of all vertices equals 2 * |E|", "b": "Sum of degrees == |V|", "c": "|V| == |E| + 1", "d": "Degree of root == 2", "ans": "A",
                    "exp": "Because every undirected edge contributes 1 to the degree of two endpoints, total degree sum = 2 * |E|."
                }
            ]
        },
        {
            "topic": "Dynamic Programming (DP)",
            "title": "Dynamic Programming (DP) & State Transitions Quiz",
            "description": "Master optimal substructure, overlapping subproblems, top-down memoization, bottom-up tabulation, 1D/2D DP, Knapsack variants, LCS, and Bitmask DP.",
            "questions": [
                {
                    "q": "1. What TWO core properties must a problem satisfy to be solvable using Dynamic Programming?",
                    "type": "single", "a": "Optimal Substructure and Overlapping Subproblems", "b": "Greedy Choice and Divide & Conquer", "c": "Sorted Input and Monotonicity", "d": "Graph DAG and Binary Search", "ans": "A",
                    "exp": "DP applies when optimal solution is built from optimal subproblems AND identical subproblems recur multiple times."
                },
                {
                    "q": "2. What is Top-Down Dynamic Programming?",
                    "type": "single", "a": "Recursion combined with Memoization table/hash map to cache calculated state results", "b": "Iterative matrix filling", "c": "Greedy choice", "d": "Binary search", "ans": "A",
                    "exp": "Top-down starts from original problem target and recurses downwards, caching subproblem solutions."
                },
                {
                    "q": "3. What is Bottom-Up Dynamic Programming?",
                    "type": "single", "a": "Iterative Tabulation filling DP table starting from Base Cases up to Target state", "b": "Recursion with call stack", "c": "Divide & conquer", "d": "Backtracking", "ans": "A",
                    "exp": "Bottom-up solves smallest subproblems first, building state transitions iteratively without call stack."
                },
                {
                    "q": "4. What is the time & space complexity of calculating N-th Fibonacci number using DP Tabulation with 2 variables?",
                    "type": "single", "a": "O(N) time and O(1) auxiliary space", "b": "O(2^N) time, O(N) space", "c": "O(N^2) time", "d": "O(log N) space", "ans": "A",
                    "exp": "Maintaining prev1 and prev2 updates fibonacci state in linear O(N) time and constant O(1) space."
                },
                {
                    "q": "5. In 0/1 Knapsack Problem (N items, Weight W), what choices are available for each item?",
                    "type": "single", "a": "Include item at most ONCE or Exclude item", "b": "Reuse item infinite times", "c": "Fractional items allowed", "d": "Sort items by weight", "ans": "A",
                    "exp": "0/1 Knapsack restricts each item to 0 (exclude) or 1 (include) decision."
                },
                {
                    "q": "6. What is the time and space complexity of standard 2D DP for 0/1 Knapsack (N items, capacity W)?",
                    "type": "single", "a": "O(N * W) time and O(N * W) space (reducible to O(W) space)", "b": "O(2^N) time", "c": "O(N log W) time", "d": "O(N + W) time", "ans": "A",
                    "exp": "DP table of size (N+1) x (W+1) fills each entry in O(1) time. Space compresses to 1D array O(W)."
                },
                {
                    "q": "7. How does Unbounded Knapsack differ from 0/1 Knapsack?",
                    "type": "single", "a": "Items can be chosen and reused an INFINITE number of times", "b": "Weight limit is infinite", "c": "Items are fractional", "d": "Items must be sorted", "ans": "A",
                    "exp": "Unbounded knapsack allows unlimited copies of each item (e.g. Coin Change problem)."
                },
                {
                    "q": "8. What state transition equation defines Longest Common Subsequence (LCS) for S1[i-1] == S2[j-1]?",
                    "type": "single", "a": "dp[i][j] = 1 + dp[i-1][j-1]", "b": "dp[i][j] = max(dp[i-1][j], dp[i][j-1])", "c": "dp[i][j] = dp[i-1][j-1]", "d": "dp[i][j] = 0", "ans": "A",
                    "exp": "Matching characters extend previous diagonal common subsequence dp[i-1][j-1] by 1."
                },
                {
                    "q": "9. What state transition equation defines LCS when S1[i-1] != S2[j-1]?",
                    "type": "single", "a": "dp[i][j] = max(dp[i-1][j], dp[i][j-1])", "b": "dp[i][j] = 1 + dp[i-1][j-1]", "c": "dp[i][j] = dp[i-1][j-1] - 1", "d": "dp[i][j] = 0", "ans": "A",
                    "exp": "Non-matching characters take maximum of skipping char from S1 vs skipping char from S2."
                },
                {
                    "q": "10. In Coin Change Problem (minimum coins to make amount A), what is the state transition for dp[i]?",
                    "type": "single", "a": "dp[i] = min(dp[i], 1 + dp[i - coin]) for all coins <= i", "b": "dp[i] = sum(dp[i - coin])", "c": "dp[i] = max(dp[i - coin])", "d": "dp[i] = dp[i - 1] + 1", "ans": "A",
                    "exp": "Taking coin adds 1 coin to subproblem dp[i - coin], minimizing across all valid coin choices."
                },
                {
                    "q": "11. In Coin Change 2 Problem (total UNIQUE COMBINATIONS to make amount A), what is the loop order?",
                    "type": "single", "a": "Outer loop over coins, inner loop over amounts from coin to A", "b": "Outer loop over amounts, inner loop over coins", "c": "Both work identically", "d": "Sort coins in descending order", "ans": "A",
                    "exp": "Outer coin loop ensures coins are considered in fixed order, counting combinations (unordered) rather than permutations."
                },
                {
                    "q": "12. What is the time complexity to find Longest Increasing Subsequence (LIS) of length N using DP + Binary Search (Patience Sorting)?",
                    "type": "single", "a": "O(N log N)", "b": "O(N^2)", "c": "O(2^N)", "d": "O(N)", "ans": "A",
                    "exp": "Maintaining tail array and using std::lower_bound binary search runs in O(N log N) time & O(N) space."
                },
                {
                    "q": "13. In Edit Distance (Levenshtein) between S1 (len M) and S2 (len N), what is the transition when S1[i-1] != S2[j-1]?",
                    "type": "single", "a": "dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) (Delete, Insert, Replace)", "b": "dp[i][j] = 1 + dp[i-1][j-1]", "c": "dp[i][j] = 0", "d": "dp[i][j] = max(dp[i-1][j], dp[i][j-1])", "ans": "A",
                    "exp": "Min cost takes 1 + minimum of Delete dp[i-1][j], Insert dp[i][j-1], or Replace dp[i-1][j-1]."
                },
                {
                    "q": "14. In Partition Equal Subset Sum (can array sum S be split into 2 equal halves S/2), what DP variant does this reduce to?",
                    "type": "single", "a": "0/1 Knapsack Subset Sum with target capacity = TotalSum / 2", "b": "Unbounded Knapsack", "c": "LCS", "d": "LIS", "ans": "A",
                    "exp": "If TotalSum is even, check if subset exists with sum equal to TotalSum / 2 using 0/1 Knapsack."
                },
                {
                    "q": "15. In Matrix Chain Multiplication (find min scalar multiplications to multiply N matrices), what DP pattern is used?",
                    "type": "single", "a": "Interval / Range Dynamic Programming dp[i][j] for subsegment range [i..j]", "b": "1D State DP", "c": "Bitmask DP", "d": "Tree DP", "ans": "A",
                    "exp": "Interval DP evaluates splitting range [i..j] at partition k (i <= k < j), minimizing dp[i][k] + dp[k+1][j] + cost."
                },
                {
                    "q": "16. What is the time complexity of Matrix Chain Multiplication for N matrices using Interval DP?",
                    "type": "single", "a": "O(N^3)", "b": "O(N^2)", "c": "O(2^N)", "d": "O(N log N)", "ans": "A",
                    "exp": "Length loop O(N), start loop O(N), and split point k loop O(N) multiply to O(N^3) total operations."
                },
                {
                    "q": "17. What is Bitmask Dynamic Programming?",
                    "type": "single", "a": "Using integer bitmask (e.g. 0 to 2^N - 1) to represent subset state of visited elements in NP-hard problems", "b": "Bitwise XOR sum", "c": "Binary search DP", "d": "1D array DP", "ans": "A",
                    "exp": "Bitmasks represent subset combinations as binary integers, optimizing state space for N <= 20."
                },
                {
                    "q": "18. What is the time complexity of Traveling Salesperson Problem (TSP) using Bitmask DP (Held-Karp Algorithm) for N cities?",
                    "type": "single", "a": "O(N^2 * 2^N) time, reduced from brute force O(N!)", "b": "O(N!)", "c": "O(N^3)", "d": "O(2^N)", "ans": "A",
                    "exp": "State dp(mask, u) has 2^N * N states; transitioning across N neighbors takes O(N^2 * 2^N) time."
                },
                {
                    "q": "19. In Palindromic Partitioning II (min cuts to partition string into palindromes), what is optimal time complexity?",
                    "type": "single", "a": "O(N^2) by precomputing palindrome matrix then 1D DP min cut", "b": "O(N^3)", "c": "O(2^N)", "d": "O(N log N)", "ans": "A",
                    "exp": "Expand around center precomputes palindrome table in O(N^2); 1D DP calculates min cuts in O(N^2)."
                },
                {
                    "q": "20. In House Robber II (houses arranged in a CIRCLE), how is circular constraint handled?",
                    "type": "single", "a": "Run 1D DP twice: once for range [0..N-2] (skip last), once for range [1..N-1] (skip first), take max", "b": "Run DP once", "c": "Sort house values", "d": "Use 2D matrix", "ans": "A",
                    "exp": "Because house 0 and house N-1 cannot both be robbed, running 1D DP on both linear subranges solves problem."
                },
                {
                    "q": "21. What optimization technique reduces DP transitions from O(N) to O(1) in convex DP recurrence functions?",
                    "type": "single", "a": "Convex Hull Trick (CHT) / Monotonic Queue Optimization", "b": "Bitmasking", "c": "Matrix Exponentiation", "d": "Binary Search", "ans": "A",
                    "exp": "Convex Hull Trick maintains linear convex functions envelope, reducing DP state transitions to O(1) or O(log N)."
                },
                {
                    "q": "22. In N-th Fibonacci number using Matrix Exponentiation, what is the time complexity?",
                    "type": "single", "a": "O(log N) using binary matrix power", "b": "O(N)", "c": "O(N^2)", "d": "O(1)", "ans": "A",
                    "exp": "Raising transition matrix [[1,1],[1,0]] to power N using binary exponentiation takes O(log N) time."
                },
                {
                    "q": "23. In Word Break Problem (dict of words, check if S can be segmented), what is time complexity using 1D DP?",
                    "type": "single", "a": "O(N^2 * L) where N is len(S) and L is max word len in dict", "b": "O(2^N)", "c": "O(N log N)", "d": "O(N)", "ans": "A",
                    "exp": "dp[i] is true if dp[j] is true AND S[j..i] exists in dictionary set for j < i."
                },
                {
                    "q": "24. In Wildcard Matching ('?' matches 1 char, '*' matches any sequence), what is 2D DP matrix transition for '*'?",
                    "type": "single", "a": "dp[i][j] = dp[i-1][j] (match 1+ chars) OR dp[i][j-1] (match empty sequence)", "b": "dp[i][j] = dp[i-1][j-1]", "c": "dp[i][j] = false", "d": "dp[i][j] = 0", "ans": "A",
                    "exp": "'*' can either absorb current text character dp[i-1][j] or act as empty string dp[i][j-1]."
                },
                {
                    "q": "25. Why is Space Optimization possible in many 2D DP problems (e.g. 0/1 Knapsack, Unique Paths)?",
                    "type": "single", "a": "State dp[i][j] depends ONLY on previous row dp[i-1], allowing rolling array of 1 or 2 rows", "b": "DP matrix can be deleted", "c": "Values are small", "d": "Columns are fixed", "ans": "A",
                    "exp": "When transition only references row i-1, keeping 1D rolling array reduces auxiliary space from O(R*C) to O(C)."
                }
            ]
        }
    ]

    print(f"Seeding {len(quiz_data)} DSA Quiz topics...")
    Quiz.objects.all().delete() # Clean previous test quizzes

    created_quizzes_count = 0
    created_questions_count = 0

    for item in quiz_data:
        quiz = Quiz.objects.create(
            title=item["title"],
            topic=item["topic"],
            difficulty="Basic to Advanced",
            description=item["description"],
            start_time=start_time,
            end_time=end_time,
            is_live=True,
            total_xp=250
        )
        created_quizzes_count += 1

        for q_data in item["questions"]:
            QuizQuestion.objects.create(
                quiz=quiz,
                question_text=q_data["q"],
                question_type=q_data.get("type", "single"),
                option_a=q_data.get("a", ""),
                option_b=q_data.get("b", ""),
                option_c=q_data.get("c", ""),
                option_d=q_data.get("d", ""),
                correct_answer=q_data.get("ans", "A"),
                explanation=q_data.get("exp", ""),
                points=10
            )
            created_questions_count += 1

    print(f"Successfully seeded {created_quizzes_count} Quizzes and {created_questions_count} Questions!")

if __name__ == '__main__':
    seed_quizzes()
