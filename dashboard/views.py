import json
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg, Count
from django.shortcuts import render, redirect
from django.utils import timezone

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

    # Sync Leetcode stats if user has linked their account
    if user.leetcode_username:
        if not user.leetcode_last_sync or now - user.leetcode_last_sync > timezone.timedelta(minutes=10):
            try:
                from accounts.leetcode import sync_leetcode_stats
                sync_leetcode_stats(user)
            except Exception:
                pass

    # DSA Sheet progress
    from .views import DSA_SHEET
    completed_dsa = user.completed_dsa_problems or []
    total_dsa_problems = sum(len(problems) for problems in DSA_SHEET.values())
    completed_dsa_count = len(completed_dsa)
    dsa_rate = round((completed_dsa_count / total_dsa_problems * 100)) if total_dsa_problems > 0 else 0

    # Placement readiness
    placement_score = calculate_placement_readiness(user)

    # Recent recommendations
    recommendations = Recommendation.objects.filter(user=user)
    if not recommendations.exists():
        from recommendations.engine import generate_recommendations
        generate_recommendations(user)
        recommendations = Recommendation.objects.filter(user=user)
    recommendations = recommendations[:3]

    # Games max level sum
    total_game_level = (
        user.game_typer_level + user.game_bug_level +
        user.game_complexity_level + user.game_parsons_level +
        user.game_predictor_level
    )

    context = {
        'current_streak': user.current_streak,
        'placement_score': placement_score,
        'completed_dsa_count': completed_dsa_count,
        'total_dsa_problems': total_dsa_problems,
        'dsa_rate': dsa_rate,
        'total_game_level': total_game_level,
        'recommendations': recommendations,
        'xp_points': user.xp_points,
    }
    return render(request, 'dashboard/home.html', context)


def calculate_placement_readiness(user):
    score = 0
    max_score = 100

    # LeetCode Solved (35 points)
    total_leetcode = user.leetcode_total_solved
    score += min(int(total_leetcode * 0.7), 35)

    # Study consistency / Streak (25 points)
    if user.current_streak >= 14:
        score += 25
    elif user.current_streak >= 7:
        score += 18
    elif user.current_streak >= 3:
        score += 12
    elif user.current_streak >= 1:
        score += 6

    # Games Levels (20 points)
    total_game_level = (
        user.game_typer_level + user.game_bug_level +
        user.game_complexity_level + user.game_parsons_level +
        user.game_predictor_level
    )
    score += min(int(total_game_level * 1.5), 20)

    # Resume quality (20 points)
    from resumeanalyzer.models import ResumeAnalysis
    latest_resume = ResumeAnalysis.objects.filter(user=user).first()
    if latest_resume:
        score += int(latest_resume.score * 0.20)

    return min(score, max_score)


from .models import GameHistory


@login_required
def cpp_calculator(request):
    user = request.user
    game_histories = GameHistory.objects.filter(user=user).order_by('-played_at')[:50]
    total_games_played = GameHistory.objects.filter(user=user).count()
    context = {
        'typer_level': user.game_typer_level,
        'bug_level': user.game_bug_level,
        'complexity_level': user.game_complexity_level,
        'parsons_level': user.game_parsons_level,
        'predictor_level': user.game_predictor_level,
        'game_histories': game_histories,
        'total_games_played': total_games_played,
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

            # Record Game History entry
            history_entry = GameHistory.objects.create(
                user=user,
                game_type=game_type,
                level=level,
                score=score,
            )
            
            return JsonResponse({
                'status': 'success', 
                'xp_points': user.xp_points,
                'typer_level': user.game_typer_level,
                'bug_level': user.game_bug_level,
                'complexity_level': user.game_complexity_level,
                'parsons_level': user.game_parsons_level,
                'predictor_level': user.game_predictor_level,
                'history_item': {
                    'game_type': history_entry.game_type,
                    'game_display_name': history_entry.game_display_name,
                    'level': history_entry.level,
                    'score': history_entry.score,
                    'played_at': history_entry.played_at.strftime('%b %d, %Y %I:%M %p'),
                }
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


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from accounts.models import User


def staff_required(view_func):
    def check_user(user):
        return user.is_authenticated and (user.is_staff or user.is_superuser)
    return user_passes_test(check_user, login_url='landing')(view_func)


@staff_required
def admin_user_dashboard(request):
    q = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', 'all')
    status_filter = request.GET.get('status', 'all')

    users = User.objects.all().order_by('-date_joined')

    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(college__icontains=q) |
            Q(branch__icontains=q)
        )

    if role_filter == 'admin':
        users = users.filter(Q(is_staff=True) | Q(is_superuser=True))
    elif role_filter == 'student':
        users = users.filter(is_staff=False, is_superuser=False)

    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)

    total_users_count = User.objects.count()
    staff_users_count = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    active_users_count = User.objects.filter(is_active=True).count()
    inactive_users_count = User.objects.filter(is_active=False).count()
    total_xp_sum = User.objects.aggregate(tot=Sum('xp_points'))['tot'] or 0

    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    from notifications.models import Notification
    recent_notifications = Notification.objects.select_related('user').order_by('-created_at')[:10]
    total_notifications_sent = Notification.objects.count()

    context = {
        'page_obj': page_obj,
        'q': q,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'total_users_count': total_users_count,
        'staff_users_count': staff_users_count,
        'active_users_count': active_users_count,
        'inactive_users_count': inactive_users_count,
        'total_xp_sum': total_xp_sum,
        'year_choices': User.YEAR_CHOICES,
        'recent_notifications': recent_notifications,
        'total_notifications_sent': total_notifications_sent,
        'notification_type_choices': Notification.TYPE_CHOICES,
    }
    return render(request, 'dashboard/admin_user_dashboard.html', context)


@staff_required
def admin_send_broadcast_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        message = request.POST.get('message', '').strip()
        notification_type = request.POST.get('notification_type', 'system')
        target_group = request.POST.get('target_group', 'all')
        target_user_id = request.POST.get('target_user_id')

        if not title or not message:
            messages.error(request, 'Title and Message are required.')
            return redirect('dashboard:admin_user_dashboard')

        if target_group == 'single' and target_user_id:
            target_users = User.objects.filter(id=target_user_id)
        elif target_group == 'active':
            target_users = User.objects.filter(is_active=True)
        elif target_group == 'students':
            target_users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)
        elif target_group == 'staff':
            target_users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True), is_active=True)
        else:
            target_users = User.objects.all()

        user_count = target_users.count()
        if user_count == 0:
            messages.warning(request, 'No users found for selected audience.')
            return redirect('dashboard:admin_user_dashboard')

        from notifications.models import Notification
        notifications_to_create = [
            Notification(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type
            )
            for user in target_users
        ]
        
        Notification.objects.bulk_create(notifications_to_create)
        
        if target_group == 'single' and target_users.first():
            recipient_name = f"@{target_users.first().username}"
            messages.success(request, f'Notification sent to {recipient_name}.')
        else:
            messages.success(request, f'Notification sent to {user_count} user(s).')

    return redirect('dashboard:admin_user_dashboard')



@staff_required
def admin_user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        college = request.POST.get('college', '').strip()
        branch = request.POST.get('branch', '').strip()
        year = request.POST.get('year', '')
        xp_points = request.POST.get('xp_points', 0)
        is_staff = request.POST.get('is_staff') == 'on'

        if not username or not password:
            messages.error(request, 'Username and Password are required.')
            return redirect('dashboard:admin_user_dashboard')

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return redirect('dashboard:admin_user_dashboard')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                college=college,
                branch=branch,
                year=year,
                is_staff=is_staff,
            )
            if xp_points:
                user.xp_points = int(xp_points)
                user.save()
            messages.success(request, f'User "{username}" created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')

    return redirect('dashboard:admin_user_dashboard')


@staff_required
def admin_user_edit(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        college = request.POST.get('college', '').strip()
        branch = request.POST.get('branch', '').strip()
        year = request.POST.get('year', '')
        xp_points = request.POST.get('xp_points', target_user.xp_points)
        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'

        if target_user == request.user and not is_active:
            messages.warning(request, "You cannot set your own account to inactive.")
            is_active = True

        target_user.email = email
        target_user.first_name = first_name
        target_user.last_name = last_name
        target_user.college = college
        target_user.branch = branch
        target_user.year = year
        target_user.is_staff = is_staff
        target_user.is_active = is_active
        try:
            target_user.xp_points = int(xp_points)
        except ValueError:
            pass

        target_user.save()
        messages.success(request, f'User details for "{target_user.username}" updated successfully!')

    return redirect('dashboard:admin_user_dashboard')


@staff_required
def admin_user_toggle_status(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if target_user == request.user:
            messages.warning(request, "You cannot modify your own administrative or active status.")
            return redirect('dashboard:admin_user_dashboard')

        if action == 'toggle_active':
            target_user.is_active = not target_user.is_active
            target_user.save()
            status_str = "activated" if target_user.is_active else "deactivated (suspended)"
            messages.success(request, f'User "{target_user.username}" was successfully {status_str}.')
        elif action == 'toggle_staff':
            target_user.is_staff = not target_user.is_staff
            target_user.save()
            role_str = "promoted to Staff" if target_user.is_staff else "demoted from Staff"
            messages.success(request, f'User "{target_user.username}" was {role_str}.')

    return redirect('dashboard:admin_user_dashboard')


@staff_required
def admin_user_delete(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot delete your own account from the admin panel.")
        return redirect('dashboard:admin_user_dashboard')

    username = target_user.username
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # Clean up all user relations before deleting target user
            cursor.execute("DELETE FROM dashboard_gamehistory WHERE user_id = %s", [user_id])
            cursor.execute("DELETE FROM leaderboard_userbadge WHERE user_id = %s", [user_id])
            cursor.execute("DELETE FROM leaderboard_achievement WHERE user_id = %s", [user_id])
            cursor.execute("DELETE FROM notifications_notification WHERE user_id = %s", [user_id])
            cursor.execute("DELETE FROM recommendations_recommendation WHERE user_id = %s", [user_id])
            cursor.execute("DELETE FROM resumeanalyzer_resumeanalysis WHERE user_id = %s", [user_id])

        target_user.delete()
        messages.success(request, f'User account "@{username}" has been deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting user account "@{username}": {str(e)}')

    return redirect('dashboard:admin_user_dashboard')


from .models import DiscussionPost, DiscussionReply


@login_required
def discussions_list(request):
    q = request.GET.get('q', '').strip()
    post_type = request.GET.get('type', 'all')
    category = request.GET.get('category', 'all')

    posts = DiscussionPost.objects.all().select_related('user').prefetch_related('replies', 'upvoted_users')

    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(code_snippet__icontains=q) |
            Q(user__username__icontains=q)
        )

    if post_type != 'all':
        posts = posts.filter(post_type=post_type)

    if category != 'all':
        posts = posts.filter(category__iexact=category)

    # Pre-seed default discussions if none exist
    if not DiscussionPost.objects.exists():
        admin_user = User.objects.filter(is_staff=True).first() or request.user
        p1 = DiscussionPost.objects.create(
            user=admin_user,
            title="Welcome to SkillSphere Discussion & Problem Sharing Hub!",
            content="Use this hub to ask questions, discuss algorithm solutions, share code snippets, or chat directly with peers and administrators.",
            post_type="announcement",
            category="General"
        )
        p2 = DiscussionPost.objects.create(
            user=admin_user,
            title="Problem: Two Sum with O(n) Time Complexity",
            content="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. Share your optimal HashMap solution below!",
            code_snippet="vector<int> twoSum(vector<int>& nums, int target) {\n    unordered_map<int, int> mp;\n    for(int i=0; i<nums.size(); i++) {\n        int complement = target - nums[i];\n        if(mp.count(complement)) return {mp[complement], i};\n        mp[nums[i]] = i;\n    }\n    return {};\n}",
            post_type="problem",
            category="DSA"
        )
        DiscussionReply.objects.create(
            post=p2,
            user=request.user,
            content="Here is the C++ solution using Hash Table for O(N) time and O(N) space complexity.",
            code_solution="// Time: O(N), Space: O(N)\n// Hash table lookup takes O(1) average time.",
            is_solution=True
        )
    # Load chat messages for the live chat panel
    if not ChatMessage.objects.exists():
        admin_user = User.objects.filter(is_staff=True).first() or request.user
        ChatMessage.objects.create(
            user=admin_user,
            message="Welcome to the General Community Chat! Connect with peers and administrators here."
        )

    chat_messages = list(ChatMessage.objects.all().select_related('user').order_by('created_at')[:100])
    last_chat_id = chat_messages[-1].id if chat_messages else 0

    context = {
        'posts': posts,
        'chat_messages': chat_messages,
        'last_chat_id': last_chat_id,
        'q': q,
        'post_type': post_type,
        'category': category,
        'type_choices': DiscussionPost.POST_TYPES,
    }
    return render(request, 'dashboard/discussions.html', context)


@login_required
def discussion_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        code_snippet = request.POST.get('code_snippet', '').strip()
        post_type = request.POST.get('post_type', 'problem')
        category = request.POST.get('category', 'General').strip()

        if title and content:
            if post_type == 'announcement' and not (request.user.is_staff or request.user.is_superuser):
                post_type = 'chat'

            post = DiscussionPost.objects.create(
                user=request.user,
                title=title,
                content=content,
                code_snippet=code_snippet if code_snippet else None,
                post_type=post_type,
                category=category if category else 'General',
            )

            request.user.xp_points += 15
            request.user.save()
            messages.success(request, 'Your post has been published successfully! (+15 XP awarded)')
        else:
            messages.error(request, 'Please provide both a title and content for your post.')

    return redirect('dashboard:discussions')


@login_required
def discussion_detail(request, post_id):
    post = get_object_or_404(DiscussionPost.objects.select_related('user'), id=post_id)
    replies = post.replies.select_related('user').all()
    context = {
        'post': post,
        'replies': replies,
    }
    return render(request, 'dashboard/discussion_detail.html', context)


@login_required
def discussion_reply(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        code_solution = request.POST.get('code_solution', '').strip()
        is_solution = request.POST.get('is_solution') == 'on'

        if content:
            reply = DiscussionReply.objects.create(
                post=post,
                user=request.user,
                content=content,
                code_solution=code_solution if code_solution else None,
                is_solution=is_solution if (request.user == post.user or request.user.is_staff) else False
            )
            request.user.xp_points += 10
            request.user.save()
            messages.success(request, 'Reply submitted! (+10 XP awarded)')
        else:
            messages.error(request, 'Reply content cannot be empty.')

    return redirect('dashboard:discussions')


@login_required
def discussion_upvote(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.user in post.upvoted_users.all():
        post.upvoted_users.remove(request.user)
        post.upvotes = max(0, post.upvotes - 1)
        post.save()
        messages.info(request, 'Upvote removed.')
    else:
        post.upvoted_users.add(request.user)
        post.upvotes += 1
        post.save()
        messages.success(request, 'Post upvoted!')

    return redirect('dashboard:discussions')


@login_required
def discussion_delete(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if post.user == request.user or request.user.is_staff or request.user.is_superuser:
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this post.')

    return redirect('dashboard:discussions')


from .models import ChatMessage
from django.http import JsonResponse


@login_required
def general_chat(request):
    if not ChatMessage.objects.exists():
        admin_user = User.objects.filter(is_staff=True).first() or request.user
        ChatMessage.objects.create(
            user=admin_user,
            message="Welcome to the General Chat Room! Feel free to talk about projects, ask quick questions, or say hello to fellow developers."
        )
        ChatMessage.objects.create(
            user=request.user,
            message="Hey everyone! Excited to connect and collaborate here."
        )

    messages_list = ChatMessage.objects.all().select_related('user').order_by('created_at')[:100]
    return render(request, 'dashboard/general_chat.html', {'chat_messages': messages_list})


@login_required
def chat_api_messages(request):
    last_id = request.GET.get('last_id', 0)
    try:
        last_id = int(last_id)
    except ValueError:
        last_id = 0

    messages_qs = ChatMessage.objects.filter(id__gt=last_id).select_related('user').order_by('created_at')[:100]
    data = []
    for msg in messages_qs:
        data.append({
            'id': msg.id,
            'username': msg.user.username,
            'display_name': msg.user.display_name,
            'is_staff': msg.user.is_staff or msg.user.is_superuser,
            'is_self': msg.user == request.user,
            'avatar_letter': msg.user.username[:1].upper(),
            'message': msg.message,
            'code_snippet': msg.code_snippet,
            'timestamp': msg.created_at.strftime('%I:%M %p'),
        })

    return JsonResponse({'status': 'success', 'messages': data})


@login_required
def chat_api_send(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            msg_text = body.get('message', '').strip()
            code_snippet = body.get('code_snippet', '').strip()
        except Exception:
            msg_text = request.POST.get('message', '').strip()
            code_snippet = request.POST.get('code_snippet', '').strip()

        if msg_text:
            msg = ChatMessage.objects.create(
                user=request.user,
                message=msg_text,
                code_snippet=code_snippet if code_snippet else None,
            )
            request.user.xp_points += 2
            request.user.save()

            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': msg.id,
                    'username': msg.user.username,
                    'display_name': msg.user.display_name,
                    'is_staff': msg.user.is_staff or msg.user.is_superuser,
                    'is_self': True,
                    'avatar_letter': msg.user.username[:1].upper(),
                    'message': msg.message,
                    'code_snippet': msg.code_snippet,
                    'timestamp': msg.created_at.strftime('%I:%M %p'),
                }
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid message content'}, status=400)


@login_required
def chat_message_delete(request, message_id):
    msg = get_object_or_404(ChatMessage, id=message_id)
    if msg.user == request.user or request.user.is_staff or request.user.is_superuser:
        msg.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)


from .models import Quiz, QuizQuestion, QuizSubmission
from django.utils.dateparse import parse_datetime


@login_required
def quiz_list(request):
    if Quiz.objects.count() < 15:
        try:
            from create_dsa_quizzes import seed_quizzes
            seed_quizzes(force=False)
        except Exception:
            pass

    quizzes = Quiz.objects.all().prefetch_related('questions', 'submissions')
    user_submissions = {s.quiz_id: s for s in QuizSubmission.objects.filter(user=request.user)}

    context = {
        'quizzes': quizzes,
        'user_submissions': user_submissions,
    }
    return render(request, 'dashboard/quiz_list.html', context)


@login_required
def quiz_take(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions'), id=quiz_id)

    submission = QuizSubmission.objects.filter(quiz=quiz, user=request.user).first()
    if submission:
        return redirect('dashboard:quiz_result', quiz_id=quiz.id)

    if quiz.status != 'live':
        messages.error(request, f"This quiz is currently {quiz.status_display}. You cannot take it at this time.")
        return redirect('dashboard:quiz_list')

    context = {
        'quiz': quiz,
        'questions': quiz.questions.all(),
    }
    return render(request, 'dashboard/quiz_take.html', context)


@login_required
def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions'), id=quiz_id)

    existing = QuizSubmission.objects.filter(quiz=quiz, user=request.user).first()
    if existing:
        return redirect('dashboard:quiz_result', quiz_id=quiz.id)

    if request.method == 'POST':
        score = 0
        total_possible = 0
        questions = quiz.questions.all()

        for q in questions:
            total_possible += q.points
            if q.question_type == 'single':
                ans = request.POST.get(f'q_{q.id}', '').strip().upper()
                if ans == q.correct_answer.strip().upper():
                    score += q.points
            elif q.question_type == 'multiple':
                ans_list = request.POST.getlist(f'q_{q.id}')
                user_ans = ','.join(sorted([a.strip().upper() for a in ans_list]))
                correct_ans = ','.join(sorted([c.strip().upper() for c in q.correct_answer.split(',')]))
                if user_ans == correct_ans:
                    score += q.points
            elif q.question_type == 'text':
                user_text = request.POST.get(f'q_{q.id}', '').strip().lower()
                correct_text = q.correct_answer.strip().lower()
                acceptable = [k.strip() for k in correct_text.replace('|', ',').split(',')]
                if user_text in acceptable or any(k in user_text for k in acceptable if k):
                    score += q.points

        pct = (score / total_possible) if total_possible > 0 else 0
        earned_xp = int(quiz.total_xp * pct)

        submission = QuizSubmission.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            total_possible=total_possible,
            xp_awarded=earned_xp
        )

        request.user.xp_points += earned_xp
        request.user.save()

        messages.success(request, f'Quiz submitted! Score: {score}/{total_possible} (+{earned_xp} XP awarded)')
        return redirect('dashboard:quiz_result', quiz_id=quiz.id)

    return redirect('dashboard:quiz_list')


@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions'), id=quiz_id)
    submission = get_object_or_404(QuizSubmission, quiz=quiz, user=request.user)
    all_submissions = quiz.submissions.select_related('user').all()[:20]

    context = {
        'quiz': quiz,
        'submission': submission,
        'all_submissions': all_submissions,
        'questions': quiz.questions.all(),
    }
    return render(request, 'dashboard/quiz_result.html', context)


# Admin Quiz Management Views
@staff_required
def admin_quiz_list(request):
    quizzes = Quiz.objects.all().prefetch_related('questions', 'submissions')
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'dashboard/admin_quiz_list.html', context)


@staff_required
def admin_quiz_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        total_xp = request.POST.get('total_xp', 100)
        is_live = request.POST.get('is_live') == 'on'

        start_time = parse_datetime(start_time_str) if start_time_str else timezone.now()
        end_time = parse_datetime(end_time_str) if end_time_str else (timezone.now() + timezone.timedelta(days=1))

        if title:
            quiz = Quiz.objects.create(
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                total_xp=int(total_xp),
                is_live=is_live
            )
            messages.success(request, f'Quiz "{title}" created! Now add questions to the quiz.')
            return redirect('dashboard:admin_quiz_edit', quiz_id=quiz.id)
        else:
            messages.error(request, 'Quiz title is required.')

    return redirect('dashboard:admin_quiz_list')


@staff_required
def admin_quiz_edit(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions', 'submissions'), id=quiz_id)

    if request.method == 'POST':
        quiz.title = request.POST.get('title', quiz.title).strip()
        quiz.description = request.POST.get('description', quiz.description).strip()
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        if start_time_str: quiz.start_time = parse_datetime(start_time_str) or quiz.start_time
        if end_time_str: quiz.end_time = parse_datetime(end_time_str) or quiz.end_time
        quiz.total_xp = int(request.POST.get('total_xp', quiz.total_xp))
        quiz.is_live = request.POST.get('is_live') == 'on'
        quiz.save()
        messages.success(request, 'Quiz details updated successfully.')
        return redirect('dashboard:admin_quiz_edit', quiz_id=quiz.id)

    context = {
        'quiz': quiz,
        'questions': quiz.questions.all(),
        'submissions': quiz.submissions.select_related('user').all(),
    }
    return render(request, 'dashboard/admin_quiz_edit.html', context)


@staff_required
def admin_quiz_add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        question_type = request.POST.get('question_type', 'single')
        option_a = request.POST.get('option_a', '').strip()
        option_b = request.POST.get('option_b', '').strip()
        option_c = request.POST.get('option_c', '').strip()
        option_d = request.POST.get('option_d', '').strip()
        correct_answer = request.POST.get('correct_answer', '').strip()
        explanation = request.POST.get('explanation', '').strip()
        points = request.POST.get('points', 10)

        if question_text and correct_answer:
            QuizQuestion.objects.create(
                quiz=quiz,
                question_text=question_text,
                question_type=question_type,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer,
                explanation=explanation,
                points=int(points)
            )
            messages.success(request, 'Question added to quiz!')
        else:
            messages.error(request, 'Please provide question text and correct answer.')

    return redirect('dashboard:admin_quiz_edit', quiz_id=quiz.id)


@staff_required
def admin_quiz_delete_question(request, question_id):
    q = get_object_or_404(QuizQuestion, id=question_id)
    quiz_id = q.quiz_id
    q.delete()
    messages.success(request, 'Question deleted successfully.')
    return redirect('dashboard:admin_quiz_edit', quiz_id=quiz_id)


@staff_required
def admin_quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    title = quiz.title
    quiz.delete()
    messages.success(request, f'Quiz "{title}" deleted.')
    return redirect('dashboard:admin_quiz_list')


@login_required
def dsa_visualizer(request):
    return render(request, 'dashboard/dsa_visualizer.html')

