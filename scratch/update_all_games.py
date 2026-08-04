import sys
import re

file_path = '/home/rakesh/SkillSphere/templates/dashboard/cpp_calculator.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define language datasets
multi_lang_datasets = """
// ====================================================
// FULL MULTI-LANGUAGE ENGINE FOR ALL CODING GAMES
// ====================================================
let currentSelectedLanguage = localStorage.getItem('arcade_selected_lang') || 'cpp';

const SPEED_TYPER_LEVELS_BY_LANG = {
    cpp: [
        { lang: 'C++', file: 'binary_search.cpp', code: `int binarySearch(vector<int>& nums, int target) {\\n    int low = 0, high = nums.size() - 1;\\n    while (low <= high) {\\n        int mid = low + (high - low) / 2;\\n        if (nums[mid] == target) return mid;\\n        if (nums[mid] < target) low = mid + 1;\\n        else high = mid - 1;\\n    }\\n    return -1;\\n}` },
        { lang: 'C++', file: 'reverse_list.cpp', code: `ListNode* reverseList(ListNode* head) {\\n    ListNode *prev = nullptr, *curr = head;\\n    while (curr != nullptr) {\\n        ListNode* nextNode = curr->next;\\n        curr->next = prev;\\n        prev = curr;\\n        curr = nextNode;\\n    }\\n    return prev;\\n}` },
        { lang: 'C++', file: 'two_sum.cpp', code: `vector<int> twoSum(vector<int>& nums, int target) {\\n    unordered_map<int, int> mp;\\n    for (int i = 0; i < nums.size(); i++) {\\n        int comp = target - nums[i];\\n        if (mp.count(comp)) return {mp[comp], i};\\n        mp[nums[i]] = i;\\n    }\\n    return {};\\n}` },
        { lang: 'C++', file: 'lru_cache.cpp', code: `class LRUCache {\\n    int capacity;\\n    list<pair<int, int>> cache;\\n    unordered_map<int, list<pair<int, int>>::iterator> map;\\npublic:\\n    LRUCache(int cap) : capacity(cap) {}\\n    int get(int key) {\\n        if (!map.count(key)) return -1;\\n        cache.splice(cache.begin(), cache, map[key]);\\n        return map[key]->second;\\n    }\\n};` },
        { lang: 'C++', file: 'quick_sort.cpp', code: `int partition(vector<int>& arr, int low, int high) {\\n    int pivot = arr[high], i = low - 1;\\n    for (int j = low; j < high; j++) {\\n        if (arr[j] < pivot) swap(arr[++i], arr[j]);\\n    }\\n    swap(arr[i + 1], arr[high]);\\n    return i + 1;\\n}` }
    ],
    python: [
        { lang: 'Python', file: 'binary_search.py', code: `def search(arr, target):\\n    low, high = 0, len(arr) - 1\\n    while low <= high:\\n        mid = (low + high) // 2\\n        if arr[mid] == target:\\n            return mid\\n        elif arr[mid] < target:\\n            low = mid + 1\\n        else:\\n            high = mid - 1\\n    return -1` },
        { lang: 'Python', file: 'reverse_list.py', code: `def reverse_list(head):\\n    prev, curr = None, head\\n    while curr:\\n        nxt = curr.next\\n        curr.next = prev\\n        prev = curr\\n        curr = nxt\\n    return prev` },
        { lang: 'Python', file: 'two_sum.py', code: `def two_sum(nums, target):\\n    seen = {}\\n    for i, num in enumerate(nums):\\n        diff = target - num\\n        if diff in seen:\\n            return [seen[diff], i]\\n        seen[num] = i\\n    return []` },
        { lang: 'Python', file: 'lru_cache.py', code: `from collections import OrderedDict\\n\\nclass LRUCache:\\n    def __init__(self, capacity: int):\\n        self.cache = OrderedDict()\\n        self.cap = capacity\\n\\n    def get(self, key: int) -> int:\\n        if key not in self.cache:\\n            return -1\\n        self.cache.move_to_end(key)\\n        return self.cache[key]` },
        { lang: 'Python', file: 'quick_sort.py', code: `def quicksort(arr):\\n    if len(arr) <= 1:\\n        return arr\\n    pivot = arr[len(arr) // 2]\\n    left = [x for x in arr if x < pivot]\\n    middle = [x for x in arr if x == pivot]\\n    right = [x for x in arr if x > pivot]\\n    return quicksort(left) + middle + quicksort(right)` }
    ],
    java: [
        { lang: 'Java', file: 'BinarySearch.java', code: `public static int binarySearch(int[] nums, int target) {\\n    int low = 0, high = nums.length - 1;\\n    while (low <= high) {\\n        int mid = low + (high - low) / 2;\\n        if (nums[mid] == target) return mid;\\n        if (nums[mid] < target) low = mid + 1;\\n        else high = mid - 1;\\n    }\\n    return -1;\\n}` },
        { lang: 'Java', file: 'ReverseList.java', code: `public ListNode reverseList(ListNode head) {\\n    ListNode prev = null, curr = head;\\n    while (curr != null) {\\n        ListNode nextNode = curr.next;\\n        curr.next = prev;\\n        prev = curr;\\n        curr = nextNode;\\n    }\\n    return prev;\\n}` },
        { lang: 'Java', file: 'TwoSum.java', code: `public int[] twoSum(int[] nums, int target) {\\n    Map<Integer, Integer> map = new HashMap<>();\\n    for (int i = 0; i < nums.length; i++) {\\n        int comp = target - nums[i];\\n        if (map.containsKey(comp)) return new int[] { map.get(comp), i };\\n        map.put(nums[i], i);\\n    }\\n    return new int[]{};\\n}` },
        { lang: 'Java', file: 'LRUCache.java', code: `class LRUCache extends LinkedHashMap<Integer, Integer> {\\n    private int capacity;\\n    public LRUCache(int capacity) {\\n        super(capacity, 0.75f, true);\\n        this.capacity = capacity;\\n    }\\n    public int get(int key) {\\n        return super.getOrDefault(key, -1);\\n    }\\n}` },
        { lang: 'Java', file: 'QuickSort.java', code: `public static void quickSort(int[] arr, int low, int high) {\\n    if (low < high) {\\n        int pi = partition(arr, low, high);\\n        quickSort(arr, low, pi - 1);\\n        quickSort(arr, pi + 1, high);\\n    }\\n}` }
    ],
    javascript: [
        { lang: 'JavaScript', file: 'binarySearch.js', code: `function binarySearch(nums, target) {\\n  let low = 0, high = nums.length - 1;\\n  while (low <= high) {\\n    let mid = Math.floor((low + high) / 2);\\n    if (nums[mid] === target) return mid;\\n    if (nums[mid] < target) low = mid + 1;\\n    else high = mid - 1;\\n  }\\n  return -1;\\n}` },
        { lang: 'JavaScript', file: 'reverseList.js', code: `function reverseList(head) {\\n  let prev = null, curr = head;\\n  while (curr !== null) {\\n    let nextNode = curr.next;\\n    curr.next = prev;\\n    prev = curr;\\n    curr = nextNode;\\n  }\\n  return prev;\\n}` },
        { lang: 'JavaScript', file: 'twoSum.js', code: `function twoSum(nums, target) {\\n  const map = new Map();\\n  for (let i = 0; i < nums.length; i++) {\\n    let comp = target - nums[i];\\n    if (map.has(comp)) return [map.get(comp), i];\\n    map.set(nums[i], i);\\n  }\\n  return [];\\n}` },
        { lang: 'JavaScript', file: 'debounce.js', code: `function debounce(func, delay) {\\n  let timer;\\n  return function(...args) {\\n    clearTimeout(timer);\\n    timer = setTimeout(() => {\\n      func.apply(this, args);\\n    }, delay);\\n  };\\n}` },
        { lang: 'JavaScript', file: 'quickSort.js', code: `function quickSort(arr) {\\n  if (arr.length <= 1) return arr;\\n  const pivot = arr[Math.floor(arr.length / 2)];\\n  const left = arr.filter(x => x < pivot);\\n  const middle = arr.filter(x => x === pivot);\\n  const right = arr.filter(x => x > pivot);\\n  return [...quickSort(left), ...middle, ...quickSort(right)];\\n}` }
    ]
};

const BUG_HUNTER_PUZZLES_BY_LANG = {
    cpp: [
        {
            lang: 'C++',
            code: `int& getVal() {\\n    int x = 10;\\n    return x; // Bug!\\n}`,
            question: 'What memory issue occurs when calling getVal()?',
            options: [
                'Functions cannot return reference types in C++.',
                'Returning reference to local stack variable (dangling reference).',
                'Memory leak because x is allocated on heap.',
                'Variable x is not initialized.'
            ],
            correct: 1,
            explanation: 'Returning a reference to a local variable x results in a dangling reference because x is destroyed when getVal() finishes execution.'
        },
        {
            lang: 'C++',
            code: `class Vector {\\n    int* data;\\npublic:\\n    Vector(int size) { data = new int[size]; }\\n    ~Vector() { delete data; } // Bug!\\n};`,
            question: 'Identify the deletion syntax bug:',
            options: [
                'delete must be written as free(data).',
                'Array memory allocated with new[] must be freed with delete[] data.',
                'Destructors cannot free pointer variables.',
                'Vectors require smart pointers.'
            ],
            correct: 1,
            explanation: 'Allocations made with new[] require delete[] data to destruct all elements and avoid undefined memory behavior.'
        }
    ],
    python: [
        {
            lang: 'Python',
            code: `def append_to(element, target=[]):\\n    target.append(element)\\n    return target\\n\\nprint(append_to(1)) # -> [1]\\nprint(append_to(2)) # -> [1, 2] (Bug!)`,
            question: 'Why does the list accumulate elements across multiple calls in Python?',
            options: [
                'Lists are immutable in Python.',
                'Default arguments are evaluated once at function definition, sharing the list instance.',
                'Function scope variables resolve globally.',
                'The print function caches return values.'
            ],
            correct: 1,
            explanation: 'In Python, default parameter values are evaluated once when the function is defined. Use target=None inside the function.'
        },
        {
            lang: 'Python',
            code: `d = {[1, 2]: "numbers"} # TypeError!`,
            question: 'Why does dict key creation fail in Python?',
            options: [
                'Lists are mutable and unhashable, so they cannot be used as dict keys.',
                'Dict values cannot be strings in Python.',
                'Dict keys must be integers.',
                'Brace syntax is invalid.'
            ],
            correct: 0,
            explanation: 'Python dictionary keys must be immutable and hashable. Use tuples (1, 2) instead of mutable lists [1, 2].'
        }
    ],
    java: [
        {
            lang: 'Java',
            code: `String res = "";\\nfor (int i = 0; i < 1000; i++) {\\n    res += i; // Bug!\\n}`,
            question: 'Why is string concatenation inside a loop inefficient in Java?',
            options: [
                'Integers take 32 bits.',
                'String is immutable, so += continuously allocates new String objects and copies memory.',
                'For loops run sequentially.',
                'Java prohibits string concatenation.'
            ],
            correct: 1,
            explanation: 'Because String objects in Java are immutable, concatenation in a loop allocates new objects repeatedly. Use StringBuilder.'
        },
        {
            lang: 'Java',
            code: `List<Integer> list = new ArrayList<>();\\nfor (Integer x : list) {\\n    list.remove(x); // Bug!\\n}`,
            question: 'What exception occurs when modifying a collection inside a foreach loop in Java?',
            options: [
                'ConcurrentModificationException.',
                'NullPointerException.',
                'IndexOutOfBoundsException.',
                'ArrayStoreException.'
            ],
            correct: 0,
            explanation: 'Modifying a collection while iterating over it via foreach triggers a ConcurrentModificationException. Use Iterator.remove().'
        }
    ],
    javascript: [
        {
            lang: 'JavaScript',
            code: `const obj = {\\n  name: "SkillSphere",\\n  greet: function() {\\n    setTimeout(function() {\\n      console.log(this.name);\\n    }, 500);\\n  }\\n};\\nobj.greet(); // outputs undefined (Bug!)`,
            question: 'Why does "this.name" output undefined in JS?',
            options: [
                'setTimeout is asynchronous.',
                'The standard callback function rebinds "this" to the global/window context.',
                'const objects cannot be read.',
                'Objects cannot hold functions.'
            ],
            correct: 1,
            explanation: 'Standard callbacks rebind "this". Using an arrow function () => { console.log(this.name); } preserves the parent lexical scope.'
        },
        {
            lang: 'JavaScript',
            code: `function test() {\\n  console.log(a); // outputs undefined\\n  var a = 10;\\n}`,
            question: 'Why does console.log(a) print undefined instead of throwing a ReferenceError?',
            options: [
                'var has no lexical scope.',
                'Variable hoisting moves the "var a" declaration to the top of the function scope.',
                'console.log is asynchronous.',
                'Function parameters default to window.'
            ],
            correct: 1,
            explanation: 'JS hoists var declarations to the top of the function scope as "var a;", leaving assignment "a = 10" below.'
        }
    ]
};

const REPAIR_SHOP_PUZZLES_BY_LANG = {
    cpp: [
        {
            title: 'Binary Search (C++)',
            desc: 'Reorder C++ binary search algorithm.',
            lines: [
                { id: 0, text: 'int bSearch(int arr[], int n, int k) {', targetIndent: 0 },
                { id: 1, text: '    int l = 0, r = n - 1;', targetIndent: 1 },
                { id: 2, text: '    while (l <= r) {', targetIndent: 1 },
                { id: 3, text: '        int m = l + (r - l) / 2;', targetIndent: 2 },
                { id: 4, text: '        if (arr[m] == k) return m;', targetIndent: 2 },
                { id: 5, text: '        if (arr[m] < k) l = m + 1;', targetIndent: 2 },
                { id: 6, text: '        else r = m - 1;', targetIndent: 2 },
                { id: 7, text: '    }', targetIndent: 1 },
                { id: 8, text: '    return -1;', targetIndent: 1 },
                { id: 9, text: '}', targetIndent: 0 }
            ],
            explanation: 'Initialize left & right pointers, check middle node matches, adapt bounds, return -1 if unfound.'
        }
    ],
    python: [
        {
            title: 'Reverse String (Python)',
            desc: 'Reorder and indent the lines to reverse a string inside reverse(s).',
            lines: [
                { id: 0, text: 'def reverse(s):', targetIndent: 0 },
                { id: 1, text: '    res = ""', targetIndent: 1 },
                { id: 2, text: '    for char in s:', targetIndent: 1 },
                { id: 3, text: '        res = char + res', targetIndent: 2 },
                { id: 4, text: '    return res', targetIndent: 1 }
            ],
            explanation: 'Initializes accumulator, loops over s prepending characters, and returns the accumulated reverse string.'
        }
    ],
    java: [
        {
            title: 'Sum Array (Java)',
            desc: 'Reorder lines to sum elements of an array in Java.',
            lines: [
                { id: 0, text: 'public static int sumArray(int[] arr) {', targetIndent: 0 },
                { id: 1, text: '    int sum = 0;', targetIndent: 1 },
                { id: 2, text: '    for (int num : arr) {', targetIndent: 1 },
                { id: 3, text: '        sum += num;', targetIndent: 2 },
                { id: 4, text: '    }', targetIndent: 1 },
                { id: 5, text: '    return sum;', targetIndent: 1 },
                { id: 6, text: '}', targetIndent: 0 }
            ],
            explanation: 'Iterate over array elements accumulating sum, then return total.'
        }
    ],
    javascript: [
        {
            title: 'Is Prime Verification (JavaScript)',
            desc: 'Arrange blocks to check if a number is prime.',
            lines: [
                { id: 0, text: 'function isPrime(n) {', targetIndent: 0 },
                { id: 1, text: '  if (n <= 1) return false;', targetIndent: 1 },
                { id: 2, text: '  for (let i = 2; i * i <= n; i++) {', targetIndent: 1 },
                { id: 3, text: '    if (n % i === 0) return false;', targetIndent: 2 },
                { id: 4, text: '  }', targetIndent: 1 },
                { id: 5, text: '  return true;', targetIndent: 1 },
                { id: 6, text: '}', targetIndent: 0 }
            ],
            explanation: 'Check edge cases, search factors up to sqrt(n), return false on division match, else true.'
        }
    ]
};

let SPEED_TYPER_LEVELS = SPEED_TYPER_LEVELS_BY_LANG[currentSelectedLanguage] || SPEED_TYPER_LEVELS_BY_LANG['cpp'];
let BUG_HUNTER_PUZZLES = BUG_HUNTER_PUZZLES_BY_LANG[currentSelectedLanguage] || BUG_HUNTER_PUZZLES_BY_LANG['cpp'];
let REPAIR_SHOP_PUZZLES = REPAIR_SHOP_PUZZLES_BY_LANG[currentSelectedLanguage] || REPAIR_SHOP_PUZZLES_BY_LANG['cpp'];

function switchGameLanguage(lang) {
    currentSelectedLanguage = lang;
    localStorage.setItem('arcade_selected_lang', lang);

    document.querySelectorAll('.lang-btn').forEach(btn => {
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active', 'btn-info', 'text-dark');
            btn.classList.remove('btn-outline-secondary', 'text-white');
        } else {
            btn.classList.remove('active', 'btn-info', 'text-dark');
            btn.classList.add('btn-outline-secondary', 'text-white');
        }
    });

    SPEED_TYPER_LEVELS = SPEED_TYPER_LEVELS_BY_LANG[lang] || SPEED_TYPER_LEVELS_BY_LANG['cpp'];
    BUG_HUNTER_PUZZLES = BUG_HUNTER_PUZZLES_BY_LANG[lang] || BUG_HUNTER_PUZZLES_BY_LANG['cpp'];
    REPAIR_SHOP_PUZZLES = REPAIR_SHOP_PUZZLES_BY_LANG[lang] || REPAIR_SHOP_PUZZLES_BY_LANG['cpp'];

    if (typeof populateTyperSelect === 'function') populateTyperSelect();
    if (typeof initTyperGame === 'function') initTyperGame(0);
    if (typeof initBugGame === 'function') initBugGame();
    if (typeof initParsonsGame === 'function') initParsonsGame();
}

document.addEventListener('DOMContentLoaded', () => {
    switchGameLanguage(currentSelectedLanguage);
});
"""

# Replace in content
if '// ====================================================\n// MULTI-LANGUAGE ENGINE FOR CODING GAMES ARCADE' in content:
    idx = content.find('// ====================================================\n// MULTI-LANGUAGE ENGINE FOR CODING GAMES ARCADE')
    end_idx = content.find('// ----------------------------------------------------\n// GAME 1: SPEED TYPER LOGIC', idx)
    if end_idx != -1:
        content = content[:idx] + multi_lang_datasets + '\n\n' + content[end_idx:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated multi-language datasets for ALL games successfully!")
    else:
        print("End marker not found!")
else:
    print("Multi-language engine marker not found!")
