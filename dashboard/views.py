import json
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg, Count
from django.shortcuts import render, redirect
from django.utils import timezone

from goals.models import Goal
from skills.models import Skill
from studylogs.models import StudyLog
from recommendations.models import Recommendation


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


@login_required
def home(request):
    user = request.user
    now = timezone.now()
    today = now.date()

    # Sync Leetcode stats if user has linked their account
    if user.leetcode_username:
        if not user.leetcode_last_sync or now - user.leetcode_last_sync > timezone.timedelta(minutes=10):
            try:
                from accounts.leetcode import sync_leetcode_stats
                sync_leetcode_stats(user)
            except Exception:
                pass

    # Study stats
    all_logs = StudyLog.objects.filter(user=user)
    total_hours = all_logs.aggregate(total=Sum('hours'))['total'] or 0

    # Weekly data (last 7 days)
    weekly_data = []
    weekly_labels = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_hours = all_logs.filter(date=day).aggregate(total=Sum('hours'))['total'] or 0
        weekly_data.append(float(day_hours))
        weekly_labels.append(day.strftime('%a'))

    # Skill data
    skills = Skill.objects.filter(user=user)
    skill_names = [s.skill_name[:15] for s in skills[:8]]
    skill_hours = [float(s.hours_practiced) for s in skills[:8]]

    # Goals stats
    goals = Goal.objects.filter(user=user)
    completed_goals = goals.filter(status='completed').count()
    total_goals = goals.count()

    # Productivity data (last 7 days)
    productivity_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        avg_prod = all_logs.filter(date=day).aggregate(avg=Avg('productivity'))['avg'] or 0
        productivity_data.append(round(float(avg_prod), 1))

    # Monthly analytics (last 4 weeks)
    monthly_labels = []
    monthly_hours = []
    for i in range(3, -1, -1):
        week_start = today - timedelta(weeks=i + 1)
        week_end = today - timedelta(weeks=i)
        hours = all_logs.filter(date__gte=week_start, date__lt=week_end).aggregate(
            total=Sum('hours'))['total'] or 0
        monthly_labels.append(f'Week {4 - i}')
        monthly_hours.append(float(hours))

    # Placement readiness
    placement_score = calculate_placement_readiness(user)

    # Productivity score
    recent_logs = all_logs.filter(date__gte=today - timedelta(days=7))
    productivity_score = recent_logs.aggregate(avg=Avg('productivity'))['avg'] or 0
    productivity_score = round(float(productivity_score) * 10, 1)

    # Most improved and weakest skills
    most_improved = skills.order_by('-hours_practiced').first()
    weakest = skills.order_by('hours_practiced').first()

    # Recent recommendations
    recommendations = Recommendation.objects.filter(user=user)
    if not recommendations.exists():
        from recommendations.engine import generate_recommendations
        generate_recommendations(user)
        recommendations = Recommendation.objects.filter(user=user)
    recommendations = recommendations[:3]

    context = {
        'total_hours': float(total_hours),
        'current_streak': user.current_streak,
        'placement_score': placement_score,
        'completed_goals': completed_goals,
        'total_goals': total_goals,
        'productivity_score': productivity_score,
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_data': json.dumps(weekly_data),
        'skill_names': json.dumps(skill_names),
        'skill_hours': json.dumps(skill_hours),
        'productivity_data': json.dumps(productivity_data),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_hours': json.dumps(monthly_hours),
        'most_improved': most_improved,
        'weakest': weakest,
        'recommendations': recommendations,
        'xp_points': user.xp_points,
    }
    return render(request, 'dashboard/home.html', context)


def calculate_placement_readiness(user):
    score = 0
    max_score = 100

    # Skill levels (30 points)
    skills = Skill.objects.filter(user=user)
    if skills.exists():
        advanced = skills.filter(level='advanced').count()
        intermediate = skills.filter(level='intermediate').count()
        skill_score = min((advanced * 10 + intermediate * 5), 30)
        score += skill_score

    # Study consistency (20 points)
    if user.current_streak >= 14:
        score += 20
    elif user.current_streak >= 7:
        score += 15
    elif user.current_streak >= 3:
        score += 10
    elif user.current_streak >= 1:
        score += 5

    # Goal completion (20 points)
    goals = Goal.objects.filter(user=user)
    if goals.exists():
        completed = goals.filter(status='completed').count()
        total = goals.count()
        score += int((completed / total) * 20)

    # Resume quality (15 points)
    from resumeanalyzer.models import ResumeAnalysis
    latest_resume = ResumeAnalysis.objects.filter(user=user).first()
    if latest_resume:
        score += int(latest_resume.score * 0.15)

    # Study hours (15 points)
    total_hours = StudyLog.objects.filter(user=user).aggregate(
        total=Sum('hours'))['total'] or 0
    if total_hours >= 200:
        score += 15
    elif total_hours >= 100:
        score += 10
    elif total_hours >= 50:
        score += 7
    elif total_hours >= 20:
        score += 4

    return min(score, max_score)


@login_required
def analytics(request):
    user = request.user
    today = timezone.now().date()
    all_logs = StudyLog.objects.filter(user=user)

    # Category distribution
    category_data = {}
    for log in all_logs:
        cat = log.get_category_display()
        category_data[cat] = category_data.get(cat, 0) + float(log.hours)

    # Daily heatmap data (last 30 days)
    heatmap_data = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        hours = all_logs.filter(date=day).aggregate(total=Sum('hours'))['total'] or 0
        heatmap_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'day_name': day.strftime('%a'),
            'hours': float(hours),
        })

    # Goal completion rate by type
    goals = Goal.objects.filter(user=user)
    goal_stats = {}
    for goal_type, label in Goal.TYPE_CHOICES:
        type_goals = goals.filter(goal_type=goal_type)
        total = type_goals.count()
        completed = type_goals.filter(status='completed').count()
        goal_stats[label] = {
            'total': total,
            'completed': completed,
            'rate': round(completed / total * 100) if total > 0 else 0,
        }

    context = {
        'category_labels': json.dumps(list(category_data.keys())),
        'category_data': json.dumps(list(category_data.values())),
        'heatmap_data': json.dumps(heatmap_data),
        'goal_stats': goal_stats,
    }
    return render(request, 'dashboard/analytics.html', context)


@login_required
def cpp_calculator(request):
    user = request.user
    context = {
        'typer_level': user.game_typer_level,
        'bug_level': user.game_bug_level,
        'complexity_level': user.game_complexity_level,
        'parsons_level': user.game_parsons_level,
        'predictor_level': user.game_predictor_level,
    }
    return render(request, 'dashboard/cpp_calculator.html', context)


@login_required
def update_game_progress(request):
    import json
    from django.http import JsonResponse
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_type = data.get('game_type')  # 'typer', 'bug', 'complexity', 'parsons', 'predictor'
            level = data.get('level')
            score = data.get('score', 0)
            
            if not game_type or level is None:
                return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)
                
            user = request.user
            if game_type == 'typer':
                user.game_typer_level = max(user.game_typer_level, level)
            elif game_type == 'bug':
                user.game_bug_level = max(user.game_bug_level, level)
            elif game_type == 'complexity':
                user.game_complexity_level = max(user.game_complexity_level, level)
            elif game_type == 'parsons':
                user.game_parsons_level = max(user.game_parsons_level, level)
            elif game_type == 'predictor':
                user.game_predictor_level = max(user.game_predictor_level, level)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid game type'}, status=400)
                
            # Award XP points
            user.xp_points += score
            user.save()
            
            return JsonResponse({
                'status': 'success', 
                'xp_points': user.xp_points,
                'typer_level': user.game_typer_level,
                'bug_level': user.game_bug_level,
                'complexity_level': user.game_complexity_level,
                'parsons_level': user.game_parsons_level,
                'predictor_level': user.game_predictor_level,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


DSA_SHEET = {
    'Arrays': [
        {'title': 'Two Sum', 'slug': 'two-sum', 'difficulty': 'Easy'},
        {'title': 'Best Time to Buy and Sell Stock', 'slug': 'best-time-to-buy-and-sell-stock', 'difficulty': 'Easy'},
        {'title': 'Contains Duplicate', 'slug': 'contains-duplicate', 'difficulty': 'Easy'},
        {'title': 'Product of Array Except Self', 'slug': 'product-of-array-except-self', 'difficulty': 'Medium'},
        {'title': 'Maximum Subarray', 'slug': 'maximum-subarray', 'difficulty': 'Medium'},
        {'title': '3Sum', 'slug': '3sum', 'difficulty': 'Medium'},
        {'title': 'Merge Intervals', 'slug': 'merge-intervals', 'difficulty': 'Medium'},
        {'title': 'Insert Interval', 'slug': 'insert-interval', 'difficulty': 'Medium'},
        {'title': 'Container With Most Water', 'slug': 'container-with-most-water', 'difficulty': 'Medium'},
        {'title': 'Spiral Matrix', 'slug': 'spiral-matrix', 'difficulty': 'Medium'},
    ],
    'Strings': [
        {'title': 'Valid Anagram', 'slug': 'valid-anagram', 'difficulty': 'Easy'},
        {'title': 'Valid Palindrome', 'slug': 'valid-palindrome', 'difficulty': 'Easy'},
        {'title': 'Longest Substring Without Repeating Characters', 'slug': 'longest-substring-without-repeating-characters', 'difficulty': 'Medium'},
        {'title': 'Longest Repeating Character Replacement', 'slug': 'longest-repeating-character-replacement', 'difficulty': 'Medium'},
        {'title': 'Minimum Window Substring', 'slug': 'minimum-window-substring', 'difficulty': 'Hard'},
        {'title': 'Group Anagrams', 'slug': 'group-anagrams', 'difficulty': 'Medium'},
        {'title': 'Valid Parentheses', 'slug': 'valid-parentheses', 'difficulty': 'Easy'},
        {'title': 'Longest Common Prefix', 'slug': 'longest-common-prefix', 'difficulty': 'Easy'},
    ],
    'Two Pointers & Sliding Window': [
        {'title': 'Two Sum II - Input Array Is Sorted', 'slug': 'two-sum-ii-input-array-is-sorted', 'difficulty': 'Medium'},
        {'title': 'Trapping Rain Water', 'slug': 'trapping-rain-water', 'difficulty': 'Hard'},
        {'title': 'Minimum Size Subarray Sum', 'slug': 'minimum-size-subarray-sum', 'difficulty': 'Medium'},
        {'title': 'Permutation in String', 'slug': 'permutation-in-string', 'difficulty': 'Medium'},
    ],
    'Linked List': [
        {'title': 'Reverse Linked List', 'slug': 'reverse-linked-list', 'difficulty': 'Easy'},
        {'title': 'Merge Two Sorted Lists', 'slug': 'merge-two-sorted-lists', 'difficulty': 'Easy'},
        {'title': 'Linked List Cycle', 'slug': 'linked-list-cycle', 'difficulty': 'Easy'},
        {'title': 'Reorder List', 'slug': 'reorder-list', 'difficulty': 'Medium'},
        {'title': 'Remove Nth Node From End of List', 'slug': 'remove-nth-node-from-end-of-list', 'difficulty': 'Medium'},
        {'title': 'Copy List with Random Pointer', 'slug': 'copy-list-with-random-pointer', 'difficulty': 'Medium'},
        {'title': 'Add Two Numbers', 'slug': 'add-two-numbers', 'difficulty': 'Medium'},
        {'title': 'Merge k Sorted Lists', 'slug': 'merge-k-sorted-lists', 'difficulty': 'Hard'},
    ],
    'Binary Search': [
        {'title': 'Binary Search', 'slug': 'binary-search', 'difficulty': 'Easy'},
        {'title': 'Search a 2D Matrix', 'slug': 'search-a-2d-matrix', 'difficulty': 'Medium'},
        {'title': 'Koko Eating Bananas', 'slug': 'koko-eating-bananas', 'difficulty': 'Medium'},
        {'title': 'Search in Rotated Sorted Array', 'slug': 'search-in-rotated-sorted-array', 'difficulty': 'Medium'},
        {'title': 'Find Minimum in Rotated Sorted Array', 'slug': 'find-minimum-in-rotated-sorted-array', 'difficulty': 'Medium'},
        {'title': 'Median of Two Sorted Arrays', 'slug': 'median-of-two-sorted-arrays', 'difficulty': 'Hard'},
    ],
    'Stack & Queue': [
        {'title': 'Min Stack', 'slug': 'min-stack', 'difficulty': 'Medium'},
        {'title': 'Evaluate Reverse Polish Notation', 'slug': 'evaluate-reverse-polish-notation', 'difficulty': 'Medium'},
        {'title': 'Generate Parentheses', 'slug': 'generate-parentheses', 'difficulty': 'Medium'},
        {'title': 'Daily Temperatures', 'slug': 'daily-temperatures', 'difficulty': 'Medium'},
        {'title': 'Largest Rectangle in Histogram', 'slug': 'largest-rectangle-in-histogram', 'difficulty': 'Hard'},
    ],
    'Trees & BST': [
        {'title': 'Invert Binary Tree', 'slug': 'invert-binary-tree', 'difficulty': 'Easy'},
        {'title': 'Maximum Depth of Binary Tree', 'slug': 'maximum-depth-of-binary-tree', 'difficulty': 'Easy'},
        {'title': 'Same Tree', 'slug': 'same-tree', 'difficulty': 'Easy'},
        {'title': 'Subtree of Another Tree', 'slug': 'subtree-of-another-tree', 'difficulty': 'Easy'},
        {'title': 'Lowest Common Ancestor of a BST', 'slug': 'lowest-common-ancestor-of-a-binary-search-tree', 'difficulty': 'Medium'},
        {'title': 'Binary Tree Level Order Traversal', 'slug': 'binary-tree-level-order-traversal', 'difficulty': 'Medium'},
        {'title': 'Validate Binary Search Tree', 'slug': 'validate-binary-search-tree', 'difficulty': 'Medium'},
        {'title': 'Kth Smallest Element in a BST', 'slug': 'kth-smallest-element-in-a-bst', 'difficulty': 'Medium'},
        {'title': 'Binary Tree Maximum Path Sum', 'slug': 'binary-tree-maximum-path-sum', 'difficulty': 'Hard'},
        {'title': 'Serialize and Deserialize Binary Tree', 'slug': 'serialize-and-deserialize-binary-tree', 'difficulty': 'Hard'},
    ],
    'Graphs': [
        {'title': 'Number of Islands', 'slug': 'number-of-islands', 'difficulty': 'Medium'},
        {'title': 'Clone Graph', 'slug': 'clone-graph', 'difficulty': 'Medium'},
        {'title': 'Course Schedule', 'slug': 'course-schedule', 'difficulty': 'Medium'},
        {'title': 'Pacific Atlantic Water Flow', 'slug': 'pacific-atlantic-water-flow', 'difficulty': 'Medium'},
        {'title': 'Redundant Connection', 'slug': 'redundant-connection', 'difficulty': 'Medium'},
        {'title': 'Word Ladder', 'slug': 'word-ladder', 'difficulty': 'Hard'},
        {'title': 'Network Delay Time', 'slug': 'network-delay-time', 'difficulty': 'Medium'},
    ],
    'Heap / Priority Queue': [
        {'title': 'Kth Largest Element in a Stream', 'slug': 'kth-largest-element-in-a-stream', 'difficulty': 'Easy'},
        {'title': 'Last Stone Weight', 'slug': 'last-stone-weight', 'difficulty': 'Easy'},
        {'title': 'K Closest Points to Origin', 'slug': 'k-closest-points-to-origin', 'difficulty': 'Medium'},
        {'title': 'Kth Largest Element in an Array', 'slug': 'kth-largest-element-in-an-array', 'difficulty': 'Medium'},
        {'title': 'Find Median from Data Stream', 'slug': 'find-median-from-data-stream', 'difficulty': 'Hard'},
    ],
    'Recursion & Backtracking': [
        {'title': 'Subsets', 'slug': 'subsets', 'difficulty': 'Medium'},
        {'title': 'Combination Sum', 'slug': 'combination-sum', 'difficulty': 'Medium'},
        {'title': 'Permutations', 'slug': 'permutations', 'difficulty': 'Medium'},
        {'title': 'Word Search', 'slug': 'word-search', 'difficulty': 'Medium'},
        {'title': 'N-Queens', 'slug': 'n-queens', 'difficulty': 'Hard'},
        {'title': 'Letter Combinations of a Phone Number', 'slug': 'letter-combinations-of-a-phone-number', 'difficulty': 'Medium'},
    ],
    'Dynamic Programming': [
        {'title': 'Climbing Stairs', 'slug': 'climbing-stairs', 'difficulty': 'Easy'},
        {'title': 'Min Cost Climbing Stairs', 'slug': 'min-cost-climbing-stairs', 'difficulty': 'Easy'},
        {'title': 'House Robber', 'slug': 'house-robber', 'difficulty': 'Medium'},
        {'title': 'Longest Palindromic Substring', 'slug': 'longest-palindromic-substring', 'difficulty': 'Medium'},
        {'title': 'Unique Paths', 'slug': 'unique-paths', 'difficulty': 'Medium'},
        {'title': 'Coin Change', 'slug': 'coin-change', 'difficulty': 'Medium'},
        {'title': 'Longest Increasing Subsequence', 'slug': 'longest-increasing-subsequence', 'difficulty': 'Medium'},
        {'title': 'Edit Distance', 'slug': 'edit-distance', 'difficulty': 'Medium'},
        {'title': 'Partition Equal Subset Sum', 'slug': 'partition-equal-subset-sum', 'difficulty': 'Medium'},
    ],
    'Greedy': [
        {'title': 'Jump Game', 'slug': 'jump-game', 'difficulty': 'Medium'},
        {'title': 'Jump Game II', 'slug': 'jump-game-ii', 'difficulty': 'Medium'},
        {'title': 'Gas Station', 'slug': 'gas-station', 'difficulty': 'Medium'},
        {'title': 'Hand of Straights', 'slug': 'hand-of-straights', 'difficulty': 'Medium'},
        {'title': 'Merge Triplets to Form Target Triplet', 'slug': 'merge-triplets-to-form-target-triplet', 'difficulty': 'Medium'},
    ]
}


@login_required
def study_materials(request):
    logged_in_user = request.user
    view_username = request.GET.get('username')
    
    is_own_sheet = True
    user = logged_in_user
    
    if view_username and view_username != logged_in_user.username:
        from accounts.models import User
        try:
            user = User.objects.get(username=view_username)
            is_own_sheet = False
        except User.DoesNotExist:
            user = logged_in_user

    if request.GET.get('sync') == '1':
        if is_own_sheet:
            if user.leetcode_username:
                try:
                    from accounts.leetcode import sync_leetcode_stats
                    success = sync_leetcode_stats(user)
                    if success:
                        messages.success(request, f"Successfully synced LeetCode stats for {user.leetcode_username}!")
                    else:
                        messages.error(request, f"Failed to sync LeetCode stats. Please verify that the username '{user.leetcode_username}' is correct and public on LeetCode.")
                except Exception as e:
                    messages.error(request, f"Error syncing LeetCode stats: {str(e)}")
            else:
                messages.error(request, "No LeetCode username configured. Please update your profile to link your LeetCode account.")
            return redirect('dashboard:study_materials')
        else:
            messages.error(request, "You cannot sync another user's LeetCode statistics.")
            return redirect(f'/dashboard/study/?username={user.username}')

    completed_problems = user.completed_dsa_problems
    if not isinstance(completed_problems, list):
        completed_problems = []

    dsa_categories = []
    total_problems = 0
    completed_problems_count = 0

    for category, problems in DSA_SHEET.items():
        cat_total = len(problems)
        cat_completed = 0
        cat_problems = []
        for p in problems:
            is_done = p['slug'] in completed_problems
            cat_problems.append({
                'title': p['title'],
                'slug': p['slug'],
                'difficulty': p['difficulty'],
                'completed': is_done
            })
            if is_done:
                cat_completed += 1
                completed_problems_count += 1
            total_problems += 1
            
        dsa_categories.append({
            'name': category,
            'slug': category.lower().replace(' ', '-').replace('&', 'and').replace('/', '-'),
            'problems': cat_problems,
            'total': cat_total,
            'completed': cat_completed,
            'percentage': int((cat_completed / cat_total) * 100) if cat_total > 0 else 0
        })

    overall_percentage = int((completed_problems_count / total_problems) * 100) if total_problems > 0 else 0

    context = {
        'dsa_categories': dsa_categories,
        'overall_total': total_problems,
        'overall_completed': completed_problems_count,
        'overall_percentage': overall_percentage,
        'viewed_user': user,
        'is_own_sheet': is_own_sheet,
    }
    return render(request, 'dashboard/study_materials.html', context)


@login_required
def toggle_dsa_problem(request):
    import json
    from django.http import JsonResponse
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            problem_slug = data.get('problem_slug')
            if not problem_slug:
                return JsonResponse({'status': 'error', 'message': 'No problem slug provided'}, status=400)
            
            user = request.user
            completed = user.completed_dsa_problems
            if not isinstance(completed, list):
                completed = []
                
            if problem_slug in completed:
                completed.remove(problem_slug)
                status = 'removed'
            else:
                completed.append(problem_slug)
                status = 'added'
                
            user.completed_dsa_problems = completed
            user.save()
            return JsonResponse({'status': 'success', 'action': status})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
