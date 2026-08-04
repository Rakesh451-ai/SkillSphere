import os
import sys
import django

sys.path.append('/home/rakesh/SkillSphere')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
django.setup()

from dashboard.models import Quiz, QuizQuestion
from django.utils import timezone
import datetime

# Create 6 PM to 7 PM datetime for today (2026-08-02)
# Using timezone aware datetimes
now = timezone.now()
start_dt = timezone.make_aware(datetime.datetime(2026, 8, 2, 18, 0, 0))
end_dt = timezone.make_aware(datetime.datetime(2026, 8, 2, 19, 0, 0))

# Create or Update Linked List Quiz
quiz, created = Quiz.objects.get_or_create(
    title="Linked List Mastery & Logic Challenge",
    defaults={
        "description": "Exclusive 1-Hour Live Quiz on Linked List Data Structure. Test pointer manipulation, cycle detection, and space-time optimizations!",
        "start_time": start_dt,
        "end_time": end_dt,
        "is_live": True,
        "total_xp": 200
    }
)

if not created:
    quiz.description = "Exclusive 1-Hour Live Quiz on Linked List Data Structure. Test pointer manipulation, cycle detection, and space-time optimizations!"
    quiz.start_time = start_dt
    quiz.end_time = end_dt
    quiz.is_live = True
    quiz.total_xp = 200
    quiz.save()
    quiz.questions.all().delete()

questions_data = [
    {
        "question_text": "In Floyd's Cycle-Finding Algorithm (Tortoise and Hare), if the slow pointer moves 1 step and the fast pointer moves 2 steps in a Linked List with a loop, why are they guaranteed to meet?",
        "option_a": "The relative distance between them decreases by 1 node in each iteration once inside the loop.",
        "option_b": "Fast pointer automatically resets to head whenever it reaches the end node.",
        "option_c": "Memory addresses overlap after 2N iterations.",
        "option_d": "Linked list nodes are stored contiguously in CPU L1 cache.",
        "correct_answer": "A",
        "explanation": "Inside a loop of length L, the relative speed of the fast pointer relative to the slow pointer is (2 - 1) = 1 step per iteration. Therefore, the gap between them decreases by exactly 1 in each step until it becomes 0, guaranteeing a collision.",
        "points": 10
    },
    {
        "question_text": "When finding the middle node of a singly linked list using two pointers (slow moving 1 step, fast moving 2 steps), what is the stopping condition for the fast pointer to handle both even and odd node counts safely?",
        "option_a": "fast == nullptr",
        "option_b": "fast->next == nullptr",
        "option_c": "fast == nullptr || fast->next == nullptr",
        "option_d": "slow == fast",
        "correct_answer": "C",
        "explanation": "For odd list lengths, fast->next == nullptr terminates the loop at the last node. For even list lengths, fast == nullptr terminates the loop past the end. Checking fast == nullptr || fast->next == nullptr handles both without null pointer dereferences.",
        "points": 10
    },
    {
        "question_text": "What is the optimal time and auxiliary space complexity to reverse a Singly Linked List in-place iteratively?",
        "option_a": "Time: O(N), Space: O(N)",
        "option_b": "Time: O(N), Space: O(1)",
        "option_c": "Time: O(N log N), Space: O(1)",
        "option_d": "Time: O(N^2), Space: O(1)",
        "correct_answer": "B",
        "explanation": "Iterative reversal using three pointers (prev, curr, next) traverses the list exactly once in linear O(N) time while utilizing constant O(1) auxiliary pointer memory.",
        "points": 10
    },
    {
        "question_text": "Given a pointer to a specific intermediate node in a Doubly Linked List vs a Singly Linked List (without head pointer access), what is the time complexity to delete that node?",
        "option_a": "O(1) for Doubly Linked List, and O(N) for Singly Linked List (or O(1) value-copy trick)",
        "option_b": "O(N) for both Doubly and Singly Linked Lists",
        "option_c": "O(1) for both Doubly and Singly Linked Lists under all conditions",
        "option_d": "O(log N) for Doubly Linked List, O(N) for Singly Linked List",
        "correct_answer": "A",
        "explanation": "In a Doubly Linked List, node->prev and node->next allow direct O(1) unlinking. In a Singly Linked List, you must traverse from head (O(N)) to locate predecessor, unless you copy next node's value into current node and delete next (O(1) trick, which fails for tail node).",
        "points": 10
    },
    {
        "question_text": "After detecting a cycle in a Linked List using slow and fast pointers, you reset the slow pointer back to the head and move both slow and fast pointers 1 step at a time. Where will they meet?",
        "option_a": "At the tail node of the linked list",
        "option_b": "At the exact start node (entry point) of the cycle",
        "option_c": "At the exact middle node of the linked list",
        "option_d": "They will continue infinitely without meeting again",
        "correct_answer": "B",
        "explanation": "By mathematical proof (distance from head to cycle start equals distance from meeting point to cycle start along loop), advancing both pointers 1 step at a time brings them together precisely at the cycle entry node.",
        "points": 10
    },
    {
        "question_text": "Why does retrieving the K-th element in a Singly Linked List take O(K) time, whereas in an Array / Vector it takes O(1) time?",
        "option_a": "Array elements are non-contiguous, while Linked List nodes are contiguous.",
        "option_b": "Linked List nodes are scattered across non-contiguous heap memory, requiring sequential pointer traversal.",
        "option_c": "Linked Lists use bitwise shifting for indexing.",
        "option_d": "Array indexing requires pointer dereferencing at each index offset.",
        "correct_answer": "B",
        "explanation": "Arrays provide O(1) random index access because elements reside in contiguous memory (base_address + k * item_size). Linked List nodes reside in arbitrary heap locations, requiring sequential pointer hops from head.",
        "points": 10
    },
    {
        "question_text": "Two Singly Linked Lists merge at a common node. What is an optimal algorithm to find the intersection node in O(M + N) time and O(1) auxiliary space?",
        "option_a": "Store node memory addresses of list 1 in a Hash Set and check list 2.",
        "option_b": "Calculate lengths len1 & len2, advance pointer of longer list by |len1 - len2|, then traverse both together until matching.",
        "option_c": "Sort both linked lists first and compare corresponding elements.",
        "option_d": "Reverse both linked lists and inspect the final matching element.",
        "correct_answer": "B",
        "explanation": "Calculating lengths len1 & len2 allows aligning start positions by advancing the longer list by length difference |len1 - len2|. Moving both in sync finds the intersection node in O(M+N) time and O(1) space.",
        "points": 10
    },
    {
        "question_text": "What is the primary architectural benefit of using a Sentinel (Dummy Head) node in Linked List algorithms (e.g. merging two sorted lists)?",
        "option_a": "It reduces overall memory footprint by half.",
        "option_b": "It eliminates special edge-case checks when inserting or deleting at the head of the list.",
        "option_c": "It automatically sorts the linked list elements.",
        "option_d": "It converts a singly linked list into a doubly linked list.",
        "correct_answer": "B",
        "explanation": "A Sentinel / Dummy Head node provides a persistent non-null anchor. This unifies logic so head operations are identical to internal node insertions/deletions, eliminating verbose null check branches.",
        "points": 10
    },
    {
        "question_text": "To verify if a Singly Linked List is a Palindrome in O(N) time and O(1) auxiliary space, which combination of steps is required?",
        "option_a": "Copy list into dynamic array and perform two-pointer checks.",
        "option_b": "Find middle using fast/slow pointer, reverse second half in-place, compare first and second halves node-by-node, then restore list.",
        "option_c": "Sort the linked list and compare with original.",
        "option_d": "Use recursive stack traversal with deep node copies.",
        "correct_answer": "B",
        "explanation": "Locating middle via fast/slow pointers, reversing the second half in-place, and comparing nodes yields O(N) time and O(1) space without allocating extra memory buffer structures.",
        "points": 10
    },
    {
        "question_text": "Why is a Doubly Linked List combined with a Hash Map to implement an LRU (Least Recently Used) Cache with O(1) get and put operations?",
        "option_a": "Hash Map provides O(1) node lookup by key, and Doubly Linked List enables O(1) node removal and insertion at the head.",
        "option_b": "Doubly Linked List provides O(1) key search, and Hash Map maintains sorting order.",
        "option_c": "Singly Linked List does not support String keys.",
        "option_d": "Arrays cannot store pointer references.",
        "correct_answer": "A",
        "explanation": "Hash Map maps keys directly to Doubly Linked List node addresses in O(1) time. Doubly Linked List enables unlinking any intermediate node in O(1) and moving it to the head as the most recently used item.",
        "points": 10
    }
]

for q_item in questions_data:
    QuizQuestion.objects.create(
        quiz=quiz,
        question_text=q_item["question_text"],
        question_type="single",
        option_a=q_item["option_a"],
        option_b=q_item["option_b"],
        option_c=q_item["option_c"],
        option_d=q_item["option_d"],
        correct_answer=q_item["correct_answer"],
        explanation=q_item["explanation"],
        points=q_item["points"]
    )

print(f"Quiz '{quiz.title}' populated with {quiz.questions.count()} single choice questions successfully!")
print(f"Schedule: {quiz.start_time.strftime('%Y-%m-%d %H:%M:%S %Z')} to {quiz.end_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
