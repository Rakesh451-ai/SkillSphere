import os
import random
import datetime
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
django.setup()

from accounts.models import User
from skills.models import Skill
from studylogs.models import StudyLog
from goals.models import Goal

USERS_DATA = [
    {
        "username": "alex_coder",
        "email": "alex.coder@example.com",
        "first_name": "Alex",
        "last_name": "Morgan",
        "college": "MIT",
        "branch": "Computer Science & Engineering",
        "year": "3",
        "bio": "Passionate full-stack developer working on distributed systems and AI applications.",
        "skills_list": "Python, React, Django, Docker, PostgreSQL",
        "github_link": "https://github.com/alexcoder",
        "linkedin_link": "https://linkedin.com/in/alexcoder",
        "xp_points": 2450,
        "current_streak": 14,
        "longest_streak": 30,
        "game_typer_level": 5,
        "game_bug_level": 4,
        "game_complexity_level": 3,
        "game_parsons_level": 6,
        "game_predictor_level": 4,
        "leetcode_username": "alex_m",
        "leetcode_easy_solved": 85,
        "leetcode_medium_solved": 64,
        "leetcode_hard_solved": 12,
        "skills": [
            ("Python Development", "WEBDEV", 120.5, "advanced", 90),
            ("React & Redux", "WEBDEV", 85.0, "intermediate", 75),
            ("Data Structures", "DSA", 150.0, "advanced", 95),
        ],
        "logs": [
            ("Mastering Dynamic Programming", 3.5, 9, "DSA", "Solved 4 hard DP problems on LeetCode."),
            ("Building REST APIs with Django", 4.0, 8, "WEBDEV", "Implemented JWT authentication and rate limiting."),
        ],
        "goals": [
            ("Solve 200 LeetCode Problems", "Complete 200 problems across topics by end of month.", "monthly", "in_progress", 80, 15),
            ("Build Portfolio Website", "Launch responsive portfolio with Next.js.", "weekly", "completed", 100, 3),
        ]
    },
    {
        "username": "priya_sharma",
        "email": "priya.sharma@example.com",
        "first_name": "Priya",
        "last_name": "Sharma",
        "college": "IIT Bombay",
        "branch": "Artificial Intelligence & Data Science",
        "year": "4",
        "bio": "AI enthusiast researching deep learning models, Computer Vision, and PyTorch.",
        "skills_list": "Python, PyTorch, Machine Learning, Data Structures, SQL",
        "github_link": "https://github.com/priyasharma-ai",
        "linkedin_link": "https://linkedin.com/in/priyasharma-ai",
        "xp_points": 3100,
        "current_streak": 21,
        "longest_streak": 45,
        "game_typer_level": 8,
        "game_bug_level": 7,
        "game_complexity_level": 6,
        "game_parsons_level": 8,
        "game_predictor_level": 7,
        "leetcode_username": "priya_ai",
        "leetcode_easy_solved": 110,
        "leetcode_medium_solved": 95,
        "leetcode_hard_solved": 25,
        "skills": [
            ("Machine Learning", "AIML", 210.0, "advanced", 95),
            ("PyTorch & Computer Vision", "AIML", 140.0, "advanced", 88),
            ("Aptitude & Reasoning", "APT", 60.0, "intermediate", 70),
        ],
        "logs": [
            ("Fine-tuning Transformer Models", 5.0, 10, "AIML", "Trained BERT model on custom classification dataset."),
            ("Graph Neural Networks Overview", 2.5, 7, "AIML", "Read research paper and implemented GCN in PyTorch."),
        ],
        "goals": [
            ("Publish Machine Learning Paper", "Draft paper on vision transformers for conference submission.", "monthly", "in_progress", 65, 30),
            ("Daily 2 ML coding drills", "Practice PyTorch tensor operations every day.", "daily", "in_progress", 90, 1),
        ]
    },
    {
        "username": "marcus_v",
        "email": "marcus.v@example.com",
        "first_name": "Marcus",
        "last_name": "Vance",
        "college": "Stanford University",
        "branch": "Information Technology",
        "year": "2",
        "bio": "Frontend wizard obsessed with UI design, smooth micro-interactions, and WebGL.",
        "skills_list": "JavaScript, TypeScript, React, TailwindCSS, Three.js",
        "github_link": "https://github.com/marcusvance",
        "linkedin_link": "https://linkedin.com/in/marcusvance",
        "xp_points": 1850,
        "current_streak": 8,
        "longest_streak": 18,
        "game_typer_level": 6,
        "game_bug_level": 3,
        "game_complexity_level": 2,
        "game_parsons_level": 4,
        "game_predictor_level": 3,
        "leetcode_username": "marcus_ui",
        "leetcode_easy_solved": 60,
        "leetcode_medium_solved": 30,
        "leetcode_hard_solved": 5,
        "skills": [
            ("Frontend UI Design", "WEBDEV", 160.0, "advanced", 92),
            ("TypeScript Mastery", "WEBDEV", 75.0, "intermediate", 68),
        ],
        "logs": [
            ("Three.js 3D Canvas Animations", 4.0, 9, "WEBDEV", "Created interactive 3D particle sphere."),
            ("CSS Grid & Layout Math", 2.0, 8, "WEBDEV", "Built responsive dashboard grid system."),
        ],
        "goals": [
            ("Design UI Component Library", "Build reusable React components with Tailwind.", "weekly", "in_progress", 50, 7),
        ]
    },
    {
        "username": "sophia_chen",
        "email": "sophia.chen@example.com",
        "first_name": "Sophia",
        "last_name": "Chen",
        "college": "UC Berkeley",
        "branch": "Computer Science",
        "year": "3",
        "bio": "Competitive programmer and algorithms enthusiast. Target: Codeforces Candidate Master.",
        "skills_list": "C++, Data Structures, Algorithms, Graph Theory, System Design",
        "github_link": "https://github.com/sophiachen",
        "linkedin_link": "https://linkedin.com/in/sophiachen",
        "xp_points": 3800,
        "current_streak": 30,
        "longest_streak": 60,
        "game_typer_level": 10,
        "game_bug_level": 9,
        "game_complexity_level": 8,
        "game_parsons_level": 9,
        "game_predictor_level": 9,
        "leetcode_username": "sophia_algo",
        "leetcode_easy_solved": 150,
        "leetcode_medium_solved": 180,
        "leetcode_hard_solved": 65,
        "skills": [
            ("Advanced Algorithms", "DSA", 320.0, "advanced", 98),
            ("System Design", "CORE", 90.0, "intermediate", 72),
        ],
        "logs": [
            ("Segment Trees & Lazy Propagation", 3.0, 10, "DSA", "Solved 5 range query problems."),
            ("System Design: Distributed Caching", 3.5, 9, "CORE", "Studied Redis clustering and cache invalidation strategies."),
        ],
        "goals": [
            ("Reach 2000 Codeforces Rating", "Compete in all Div 2 rounds and upsolve problems.", "monthly", "in_progress", 75, 20),
        ]
    },
    {
        "username": "rohan_gupta",
        "email": "rohan.gupta@example.com",
        "first_name": "Rohan",
        "last_name": "Gupta",
        "college": "BITS Pilani",
        "branch": "Electrical & Electronics Engineering",
        "year": "1",
        "bio": "First-year engineering student exploring Python, Web Development, and Core CS fundamentals.",
        "skills_list": "Python, HTML/CSS, C Programming, Git",
        "github_link": "https://github.com/rohangupta",
        "linkedin_link": "https://linkedin.com/in/rohangupta",
        "xp_points": 920,
        "current_streak": 5,
        "longest_streak": 12,
        "game_typer_level": 3,
        "game_bug_level": 2,
        "game_complexity_level": 2,
        "game_parsons_level": 3,
        "game_predictor_level": 2,
        "leetcode_username": "rohan_1styear",
        "leetcode_easy_solved": 35,
        "leetcode_medium_solved": 10,
        "leetcode_hard_solved": 1,
        "skills": [
            ("Python Basics", "WEBDEV", 45.0, "intermediate", 60),
            ("Aptitude Preparation", "APT", 30.0, "beginner", 40),
        ],
        "logs": [
            ("Python OOP Fundamentals", 2.0, 7, "WEBDEV", "Learned classes, inheritance, and encapsulation."),
            ("Quantitative Aptitude Practice", 1.5, 8, "APT", "Solved 25 speed & distance problems."),
        ],
        "goals": [
            ("Complete Python Bootcamp", "Finish all modules in Python fundamentals course.", "weekly", "in_progress", 40, 5),
        ]
    },
    {
        "username": "elena_rostova",
        "email": "elena.rostova@example.com",
        "first_name": "Elena",
        "last_name": "Rostova",
        "college": "ETH Zurich",
        "branch": "Cybersecurity & Networks",
        "year": "4",
        "bio": "Cybersecurity researcher focused on cloud security, cryptography, and network protocols.",
        "skills_list": "Python, Linux, Cryptography, Network Security, Bash",
        "github_link": "https://github.com/elenarostova",
        "linkedin_link": "https://linkedin.com/in/elenarostova",
        "xp_points": 2750,
        "current_streak": 17,
        "longest_streak": 28,
        "game_typer_level": 7,
        "game_bug_level": 6,
        "game_complexity_level": 5,
        "game_parsons_level": 7,
        "game_predictor_level": 6,
        "leetcode_username": "elena_sec",
        "leetcode_easy_solved": 90,
        "leetcode_medium_solved": 70,
        "leetcode_hard_solved": 18,
        "skills": [
            ("Network Security", "CORE", 180.0, "advanced", 90),
            ("Applied Cryptography", "CORE", 110.0, "advanced", 82),
        ],
        "logs": [
            ("TLS 1.3 Protocol Analysis", 4.0, 9, "CORE", "Analyzed handshake packets in Wireshark."),
            ("CTF Web Security Challenges", 3.0, 8, "OTHER", "Completed 3 web exploitation challenges."),
        ],
        "goals": [
            ("Obtain Security+ Certification", "Review all 6 domain areas and practice exam questions.", "monthly", "in_progress", 85, 14),
        ]
    }
]

def create_users():
    today = datetime.date.today()
    created_count = 0
    
    for udata in USERS_DATA:
        username = udata["username"]
        user, created = User.objects.get_or_create(username=username, defaults={
            "email": udata["email"],
            "first_name": udata["first_name"],
            "last_name": udata["last_name"],
            "college": udata["college"],
            "branch": udata["branch"],
            "year": udata["year"],
            "bio": udata["bio"],
            "skills_list": udata["skills_list"],
            "github_link": udata["github_link"],
            "linkedin_link": udata["linkedin_link"],
            "xp_points": udata["xp_points"],
            "current_streak": udata["current_streak"],
            "longest_streak": udata["longest_streak"],
            "last_activity_date": today,
            "game_typer_level": udata["game_typer_level"],
            "game_bug_level": udata["game_bug_level"],
            "game_complexity_level": udata["game_complexity_level"],
            "game_parsons_level": udata["game_parsons_level"],
            "game_predictor_level": udata["game_predictor_level"],
            "leetcode_username": udata["leetcode_username"],
            "leetcode_easy_solved": udata["leetcode_easy_solved"],
            "leetcode_medium_solved": udata["leetcode_medium_solved"],
            "leetcode_hard_solved": udata["leetcode_hard_solved"],
        })
        
        # Set password
        user.set_password("password123")
        
        # Update user attributes if existed
        user.email = udata["email"]
        user.first_name = udata["first_name"]
        user.last_name = udata["last_name"]
        user.college = udata["college"]
        user.branch = udata["branch"]
        user.year = udata["year"]
        user.bio = udata["bio"]
        user.skills_list = udata["skills_list"]
        user.github_link = udata["github_link"]
        user.linkedin_link = udata["linkedin_link"]
        user.xp_points = udata["xp_points"]
        user.current_streak = udata["current_streak"]
        user.longest_streak = udata["longest_streak"]
        user.last_activity_date = today
        user.game_typer_level = udata["game_typer_level"]
        user.game_bug_level = udata["game_bug_level"]
        user.game_complexity_level = udata["game_complexity_level"]
        user.game_parsons_level = udata["game_parsons_level"]
        user.game_predictor_level = udata["game_predictor_level"]
        user.leetcode_username = udata["leetcode_username"]
        user.leetcode_easy_solved = udata["leetcode_easy_solved"]
        user.leetcode_medium_solved = udata["leetcode_medium_solved"]
        user.leetcode_hard_solved = udata["leetcode_hard_solved"]
        user.save()
        
        created_count += 1
        print(f"[{'Created' if created else 'Updated'}] User: {user.username} ({user.display_name}) - {user.college}")

        # Add Skills
        for sk in udata.get("skills", []):
            Skill.objects.update_or_create(
                user=user,
                skill_name=sk[0],
                defaults={
                    "category": sk[1],
                    "hours_practiced": sk[2],
                    "level": sk[3],
                    "progress": sk[4],
                }
            )

        # Add Study Logs
        for idx, log in enumerate(udata.get("logs", [])):
            log_date = today - datetime.timedelta(days=idx + 1)
            StudyLog.objects.get_or_create(
                user=user,
                topic=log[0],
                date=log_date,
                defaults={
                    "hours": log[1],
                    "productivity": log[2],
                    "category": log[3],
                    "notes": log[4],
                }
            )

        # Add Goals
        for goal in udata.get("goals", []):
            deadline_date = today + datetime.timedelta(days=goal[5])
            Goal.objects.get_or_create(
                user=user,
                title=goal[0],
                defaults={
                    "description": goal[1],
                    "goal_type": goal[2],
                    "status": goal[3],
                    "progress": goal[4],
                    "deadline": deadline_date,
                }
            )

    print(f"\nSuccessfully processed {created_count} random users with full details, skills, study logs, and goals!")

if __name__ == '__main__':
    create_users()
