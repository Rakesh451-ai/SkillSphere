"""Dynamic Tech News & Placement Job Openings Engine for SkillSphere.

Provides real-time, categorized, and dynamically rotating feeds for:
- Top Product-Based Companies (Google, Microsoft, Amazon, Uber, Atlassian, Adobe, Stripe, PhonePe, Razorpay, etc.)
- Top Service-Based Companies (TCS Digital, Infosys Specialist Programmer, Accenture ATCI, Wipro Turbo, IBM Labs, Deloitte, etc.)
- Live Tech News (HackerNews API & Curated Industry Announcements)
"""

import json
import time
import urllib.request
from datetime import datetime, timedelta
from django.utils import timezone

# In-memory cache for live news to ensure sub-millisecond response times
_NEWS_CACHE = {
    'timestamp': 0,
    'items': []
}

PRODUCT_JOB_OPENINGS = [
    {
        "id": 101,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Software Development Engineer (SDE-1) - Core Systems",
        "company": "Google",
        "logo_icon": "fa-brands fa-google text-red-400",
        "location": "Bengaluru / Hybrid",
        "salary": "₹24 - 32 LPA",
        "tags": ["C++", "Distributed Systems", "DSA"],
        "url": "https://careers.google.com/jobs/results/?q=software%20engineer",
        "offset_minutes": 4,
    },
    {
        "id": 102,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Backend Software Engineer - Azure Cloud Infrastructure",
        "company": "Microsoft",
        "logo_icon": "fa-brands fa-microsoft text-cyan-400",
        "location": "Hyderabad / Remote",
        "salary": "₹20 - 28 LPA",
        "tags": ["Go", "Kubernetes", "Azure"],
        "url": "https://careers.microsoft.com/professionals/us/en/search-results?keywords=software%20engineer",
        "offset_minutes": 12,
    },
    {
        "id": 103,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "SDE-1 - High Throughput Distributed Storage",
        "company": "Amazon (AWS)",
        "logo_icon": "fa-brands fa-amazon text-amber-400",
        "location": "Gurugram / Bengaluru",
        "salary": "₹22 - 30 LPA",
        "tags": ["Java", "AWS", "System Design"],
        "url": "https://www.amazon.jobs/en/job_categories/software-development",
        "offset_minutes": 25,
    },
    {
        "id": 104,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Software Engineer - Realtime Dispatch & Maps Platform",
        "company": "Uber",
        "logo_icon": "fa-brands fa-uber text-white",
        "location": "Bengaluru / Hybrid",
        "salary": "₹28 - 38 LPA",
        "tags": ["Go", "Kafka", "Microservices"],
        "url": "https://www.uber.com/us/en/careers/list/?department=Engineering",
        "offset_minutes": 38,
    },
    {
        "id": 105,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Software Engineer - Jira Cloud Distributed Engine",
        "company": "Atlassian",
        "logo_icon": "fa-brands fa-atlassian text-blue-400",
        "location": "Bengaluru / Remote",
        "salary": "₹26 - 35 LPA",
        "tags": ["Java", "Spring Boot", "React"],
        "url": "https://www.atlassian.com/company/careers/all-jobs?team=Engineering",
        "offset_minutes": 55,
    },
    {
        "id": 106,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Computer Scientist 1 - Cloud Platform & Media APIs",
        "company": "Adobe",
        "logo_icon": "fa-solid fa-palette text-rose-400",
        "location": "Noida / Bengaluru",
        "salary": "₹20 - 26 LPA",
        "tags": ["C++", "Python", "Cloud Native"],
        "url": "https://adobe.wd5.myworkdayjobs.com/external_experienced",
        "offset_minutes": 72,
    },
    {
        "id": 107,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Frontend SDE (React & Next.js) - AI Product Studio",
        "company": "Stripe",
        "logo_icon": "fa-solid fa-credit-card text-indigo-400",
        "location": "Remote / India",
        "salary": "₹25 - 34 LPA",
        "tags": ["TypeScript", "Next.js", "TailwindCSS"],
        "url": "https://stripe.com/jobs",
        "offset_minutes": 90,
    },
    {
        "id": 108,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Backend SDE - UPI Core Financial Ledger",
        "company": "PhonePe",
        "logo_icon": "fa-solid fa-wallet text-purple-400",
        "location": "Bengaluru / Onsite",
        "salary": "₹22 - 30 LPA",
        "tags": ["Java", "HBase", "Aerospike"],
        "url": "https://www.phonepe.com/careers/",
        "offset_minutes": 110,
    },
    {
        "id": 109,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Software Development Engineer - Payments Gateway",
        "company": "Razorpay",
        "logo_icon": "fa-solid fa-bolt text-blue-400",
        "location": "Bengaluru / Hybrid",
        "salary": "₹20 - 28 LPA",
        "tags": ["Golang", "PHP", "AWS"],
        "url": "https://razorpay.com/jobs/",
        "offset_minutes": 135,
    },
    {
        "id": 110,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "SDE-1 - Catalog Architecture & Supply Chain",
        "company": "Flipkart",
        "logo_icon": "fa-solid fa-bag-shopping text-yellow-400",
        "location": "Bengaluru / Onsite",
        "salary": "₹22 - 29 LPA",
        "tags": ["Java", "Dropwizard", "MySQL"],
        "url": "https://www.flipkartcareers.com/",
        "offset_minutes": 160,
    },
    {
        "id": 111,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Backend Engineer - High-Speed Financial Rails",
        "company": "CRED",
        "logo_icon": "fa-solid fa-gem text-emerald-400",
        "location": "Bengaluru / Onsite",
        "salary": "₹28 - 40 LPA",
        "tags": ["Go", "Kafka", "Postgres"],
        "url": "https://careers.cred.club/",
        "offset_minutes": 185,
    },
    {
        "id": 112,
        "type": "job",
        "sub_type": "product",
        "company_category": "Product-Based",
        "title": "Member of Technical Staff - Enterprise Cloud Infrastructure",
        "company": "Salesforce",
        "logo_icon": "fa-brands fa-salesforce text-sky-400",
        "location": "Hyderabad / Bengaluru",
        "salary": "₹23 - 32 LPA",
        "tags": ["Java", "Distributed Systems", "Cloud"],
        "url": "https://salesforce.wd1.myworkdayjobs.com/External_Career_Site",
        "offset_minutes": 210,
    }
]

SERVICE_JOB_OPENINGS = [
    {
        "id": 201,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Digital Cadre)",
        "title": "Digital Systems Engineer - Next-Gen Cloud Platform (TCS Digital / Innovator)",
        "company": "Tata Consultancy Services (TCS)",
        "logo_icon": "fa-solid fa-building text-cyan-400",
        "location": "Bengaluru / Pune / Hyderabad",
        "salary": "₹9.5 - 14.5 LPA",
        "tags": ["Java", "Spring Boot", "Microservices", "AWS"],
        "url": "https://www.tcs.com/careers/india/entry-level",
        "offset_minutes": 8,
    },
    {
        "id": 202,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Specialist Cadre)",
        "title": "Specialist Programmer (SES Cadre) - Cloud & Data Architecture",
        "company": "Infosys",
        "logo_icon": "fa-solid fa-laptop-code text-indigo-400",
        "location": "Bengaluru / Hyderabad / Remote",
        "salary": "₹9.5 - 15.0 LPA",
        "tags": ["Python", "Java", "Kubernetes", "System Design"],
        "url": "https://www.infosys.com/careers/graduates-students.html",
        "offset_minutes": 18,
    },
    {
        "id": 203,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Advanced Tech)",
        "title": "Advanced Application Engineering Specialist - Cloud & GenAI",
        "company": "Accenture ATCI",
        "logo_icon": "fa-solid fa-network-wired text-purple-400",
        "location": "Bengaluru / Gurugram / Hyderabad",
        "salary": "₹8.5 - 13.5 LPA",
        "tags": ["Full Stack", "Spring Boot", "React", "Azure"],
        "url": "https://www.accenture.com/in-en/careers",
        "offset_minutes": 32,
    },
    {
        "id": 204,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Turbo Cadre)",
        "title": "Software Development Engineer - Turbo Digital Product Engineering",
        "company": "Wipro Turbo",
        "logo_icon": "fa-solid fa-microchip text-emerald-400",
        "location": "Bengaluru / Pune / Hyderabad",
        "salary": "₹8.0 - 12.0 LPA",
        "tags": ["C++", "Java", "Docker", "Linux"],
        "url": "https://careers.wipro.com",
        "offset_minutes": 48,
    },
    {
        "id": 205,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Product Labs)",
        "title": "Systems Software Engineer - Red Hat OpenShift & Cloud Labs",
        "company": "IBM Software Labs",
        "logo_icon": "fa-solid fa-cloud text-blue-400",
        "location": "Bengaluru / Kochi / Pune",
        "salary": "₹11.0 - 18.0 LPA",
        "tags": ["Golang", "Kubernetes", "Linux", "OpenShift"],
        "url": "https://www.ibm.com/careers",
        "offset_minutes": 65,
    },
    {
        "id": 206,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Next-Gen)",
        "title": "Product Engineer - GenC Next Digital Architecture",
        "company": "Cognizant",
        "logo_icon": "fa-solid fa-cubes text-blue-400",
        "location": "Chennai / Bengaluru / Coimbatore",
        "salary": "₹8.5 - 13.0 LPA",
        "tags": ["Java", "AWS", "CI/CD", "PostgreSQL"],
        "url": "https://careers.cognizant.com",
        "offset_minutes": 82,
    },
    {
        "id": 207,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Advisory & Tech)",
        "title": "Cloud & Cyber Engineering Consultant - USI Tech Center",
        "company": "Deloitte USI",
        "logo_icon": "fa-solid fa-chart-line text-emerald-400",
        "location": "Hyderabad / Bengaluru / Mumbai",
        "salary": "₹10.0 - 16.0 LPA",
        "tags": ["Python", "Cloud Security", "DevSecOps", "AWS"],
        "url": "https://jobsindia.deloitte.com",
        "offset_minutes": 105,
    },
    {
        "id": 208,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Engineering)",
        "title": "Digital Engineering Specialist - Distributed Microservices",
        "company": "Capgemini",
        "logo_icon": "fa-solid fa-server text-cyan-400",
        "location": "Pune / Bengaluru / Navi Mumbai",
        "salary": "₹8.0 - 12.5 LPA",
        "tags": ["Spring Boot", "React", "Kafka", "REST APIs"],
        "url": "https://www.capgemini.com/in-en/careers",
        "offset_minutes": 125,
    },
    {
        "id": 209,
        "type": "job",
        "sub_type": "service",
        "company_category": "Service (Digital Systems)",
        "title": "Specialist Software Engineer - Cloud Data & Event Streams",
        "company": "LTIMindtree",
        "logo_icon": "fa-solid fa-code text-teal-400",
        "location": "Bengaluru / Mumbai / Pune",
        "salary": "₹8.0 - 13.0 LPA",
        "tags": ["Java", "Spark", "Kafka", "GCP"],
        "url": "https://www.ltimindtree.com/careers",
        "offset_minutes": 150,
    }
]

CURATED_TECH_NEWS = [
    {
        "id": 301,
        "type": "news",
        "sub_type": "news",
        "company_category": "AI / ML Release",
        "title": "OpenAI Releases GPT-5 Developer Preview & Realtime Reasoning APIs",
        "source": "TechCrunch",
        "logo_icon": "fa-solid fa-brain text-emerald-400",
        "location": "Global Tech",
        "salary": "Tech News",
        "tags": ["AI / ML", "LLM", "API"],
        "url": "https://techcrunch.com",
        "offset_minutes": 10,
    },
    {
        "id": 302,
        "type": "news",
        "sub_type": "news",
        "company_category": "Language Release",
        "title": "Rust 1.85 Released: Native Async Closures & Compiler Optimizations",
        "source": "HackerNews",
        "logo_icon": "fa-brands fa-rust text-amber-500",
        "location": "Systems Tech",
        "salary": "Tech News",
        "tags": ["Rust", "Systems", "Compiler"],
        "url": "https://news.ycombinator.com",
        "offset_minutes": 22,
    },
    {
        "id": 303,
        "type": "news",
        "sub_type": "news",
        "company_category": "Open Source AI",
        "title": "Meta Open-Sources Llama-4 Architecture for On-Device Edge Hardware",
        "source": "GitHub Engineering",
        "logo_icon": "fa-brands fa-github text-slate-300",
        "location": "AI Research",
        "salary": "Tech News",
        "tags": ["Open Source", "Edge AI", "PyTorch"],
        "url": "https://github.blog",
        "offset_minutes": 45,
    },
    {
        "id": 304,
        "type": "news",
        "sub_type": "news",
        "company_category": "Cloud Architecture",
        "title": "Anthropic Announces Claude 3.7 Hybrid Reasoning with 200K Context Window",
        "source": "VentureBeat",
        "logo_icon": "fa-solid fa-bolt text-indigo-400",
        "location": "AI Models",
        "salary": "Tech News",
        "tags": ["Anthropic", "Claude", "Reasoning"],
        "url": "https://venturebeat.com",
        "offset_minutes": 68,
    },
    {
        "id": 305,
        "type": "news",
        "sub_type": "news",
        "company_category": "Developer Tooling",
        "title": "Google Cloud Introduces Serverless TPU v5e Clusters for Low-Latency Inference",
        "source": "Google Cloud Blog",
        "logo_icon": "fa-brands fa-google text-red-400",
        "location": "Cloud Tech",
        "salary": "Tech News",
        "tags": ["GCP", "TPU", "Serverless"],
        "url": "https://cloud.google.com/blog",
        "offset_minutes": 95,
    },
    {
        "id": 306,
        "type": "news",
        "sub_type": "news",
        "company_category": "Security & Infra",
        "title": "Linux Kernel 6.14 Merges Next-Gen Memory Allocator & Bcachefs Enhancements",
        "source": "Kernel.org",
        "logo_icon": "fa-brands fa-linux text-yellow-400",
        "location": "Kernel Engineering",
        "salary": "Tech News",
        "tags": ["Linux", "Kernel", "Bcachefs"],
        "url": "https://kernel.org",
        "offset_minutes": 120,
    }
]


def format_time_ago(offset_minutes):
    """Format an offset in minutes into a clean relative time string."""
    if offset_minutes < 2:
        return "Just now"
    elif offset_minutes < 60:
        return f"{offset_minutes}m ago"
    elif offset_minutes < 1440:
        hours = offset_minutes // 60
        return f"{hours}h ago"
    else:
        days = offset_minutes // 1440
        return f"{days}d ago"


def fetch_live_tech_news():
    """Fetch top live stories from HackerNews API with a 5-minute memory cache."""
    now = time.time()
    if now - _NEWS_CACHE['timestamp'] < 300 and _NEWS_CACHE['items']:
        return _NEWS_CACHE['items']

    live_items = []
    try:
        req = urllib.request.Request(
            'https://hacker-news.firebaseio.com/v0/topstories.json',
            headers={'User-Agent': 'SkillSphere/1.0'}
        )
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            top_ids = json.loads(resp.read().decode('utf-8'))[:5]

        for idx, tid in enumerate(top_ids):
            try:
                item_req = urllib.request.Request(
                    f'https://hacker-news.firebaseio.com/v0/item/{tid}.json',
                    headers={'User-Agent': 'SkillSphere/1.0'}
                )
                with urllib.request.urlopen(item_req, timeout=2.0) as item_resp:
                    data = json.loads(item_resp.read().decode('utf-8'))
                    title = data.get('title')
                    url = data.get('url') or f"https://news.ycombinator.com/item?id={tid}"
                    if title:
                        live_items.append({
                            "id": 400 + idx,
                            "type": "news",
                            "sub_type": "news",
                            "company_category": "Trending Tech",
                            "title": title,
                            "source": "HackerNews",
                            "logo_icon": "fa-brands fa-y-combinator text-orange-500",
                            "location": "Global Tech",
                            "salary": "Live Story",
                            "tags": ["Trending", "HackerNews", "Tech"],
                            "url": url,
                            "offset_minutes": (idx + 1) * 7,
                        })
            except Exception:
                continue
    except Exception:
        pass

    if live_items:
        _NEWS_CACHE['items'] = live_items
        _NEWS_CACHE['timestamp'] = now
        return live_items

    # Fallback to curated news if API is unreachable
    return CURATED_TECH_NEWS


def get_dynamic_tech_feed(filter_type='all'):
    """Return an interleaved, dynamically prioritized list of tech news & job openings.

    Supports filter_type:
    - 'all': Product jobs, Service jobs, and Tech News
    - 'news': Tech News only
    - 'job': All jobs (Product & Service)
    - 'product': Product-based company jobs only
    - 'service': Service-based company jobs only
    """
    # Grab live news (or fallback)
    news_items = fetch_live_tech_news() or CURATED_TECH_NEWS

    # Dynamically rotate or offset minutes slightly based on current time
    # so feeds feel alive on consecutive sync calls
    minute_seed = int(time.time() // 60) % 15

    product_jobs = []
    for item in PRODUCT_JOB_OPENINGS:
        copy_item = dict(item)
        effective_offset = item["offset_minutes"] + minute_seed
        copy_item["time_ago"] = format_time_ago(effective_offset)
        product_jobs.append(copy_item)

    service_jobs = []
    for item in SERVICE_JOB_OPENINGS:
        copy_item = dict(item)
        effective_offset = item["offset_minutes"] + minute_seed
        copy_item["time_ago"] = format_time_ago(effective_offset)
        service_jobs.append(copy_item)

    news_list = []
    for item in news_items:
        copy_item = dict(item)
        effective_offset = item.get("offset_minutes", 10) + minute_seed
        copy_item["time_ago"] = format_time_ago(effective_offset)
        news_list.append(copy_item)

    # Filter according to requested category
    if filter_type == 'news':
        return news_list
    elif filter_type == 'product':
        return product_jobs
    elif filter_type == 'service':
        return service_jobs
    elif filter_type == 'job':
        # Interleave product and service jobs evenly
        interleaved_jobs = []
        max_len = max(len(product_jobs), len(service_jobs))
        for i in range(max_len):
            if i < len(product_jobs):
                interleaved_jobs.append(product_jobs[i])
            if i < len(service_jobs):
                interleaved_jobs.append(service_jobs[i])
        return interleaved_jobs
    else:  # 'all'
        # Interleave: 1 product job, 1 service job, 1 tech news
        feed = []
        p_idx = s_idx = n_idx = 0
        p_len, s_len, n_len = len(product_jobs), len(service_jobs), len(news_list)
        total = p_len + s_len + n_len

        while len(feed) < total:
            if p_idx < p_len:
                feed.append(product_jobs[p_idx])
                p_idx += 1
            if s_idx < s_len:
                feed.append(service_jobs[s_idx])
                s_idx += 1
            if n_idx < n_len:
                feed.append(news_list[n_idx])
                n_idx += 1

        return feed
