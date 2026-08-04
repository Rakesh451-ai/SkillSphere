import sys
import re

file_path = '/home/rakesh/SkillSphere/templates/dashboard/cpp_calculator.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We will add language switcher logic right before SPEED_TYPER_LEVELS definition.

lang_switcher_code = """
// ====================================================
// MULTI-LANGUAGE ENGINE FOR CODING GAMES ARCADE
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

let SPEED_TYPER_LEVELS = SPEED_TYPER_LEVELS_BY_LANG[currentSelectedLanguage] || SPEED_TYPER_LEVELS_BY_LANG['cpp'];

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

    if (typeof populateTyperSelect === 'function') populateTyperSelect();
    if (typeof initTyperGame === 'function') initTyperGame(0);
}

document.addEventListener('DOMContentLoaded', () => {
    switchGameLanguage(currentSelectedLanguage);
});
"""

if 'const SPEED_TYPER_LEVELS = [' in content:
    content = content.replace('const SPEED_TYPER_LEVELS = [', lang_switcher_code + '\n// Original fallback dataset\nconst ORIGINAL_TYPER_LEVELS = [')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Multi-language engine successfully integrated!")
else:
    print("Target string not found!")
