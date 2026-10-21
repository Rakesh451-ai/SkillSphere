import sys

file_path = '/home/rakesh/SkillSphere/templates/dashboard/cpp_calculator.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace dataset names to ALL_BUG_HUNTER_PUZZLES, ALL_REPAIR_SHOP_PUZZLES, etc.
content = content.replace('const BUG_HUNTER_PUZZLES = [', 'const ALL_BUG_HUNTER_PUZZLES = [\n')
content = content.replace('const REPAIR_SHOP_PUZZLES = [', 'const ALL_REPAIR_SHOP_PUZZLES = [\n')

# Define updated switchGameLanguage
new_switch_func = """
let BUG_HUNTER_PUZZLES = [];
let REPAIR_SHOP_PUZZLES = [];

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

    const searchLang = (lang === 'cpp') ? 'c++' : (lang === 'javascript') ? 'javascript' : (lang === 'java') ? 'java' : 'python';

    SPEED_TYPER_LEVELS = SPEED_TYPER_LEVELS_BY_LANG[lang] || SPEED_TYPER_LEVELS_BY_LANG['cpp'];

    if (typeof ALL_BUG_HUNTER_PUZZLES !== 'undefined') {
        let filtered = ALL_BUG_HUNTER_PUZZLES.filter(p => p.lang && p.lang.toLowerCase().includes(searchLang));
        BUG_HUNTER_PUZZLES = filtered.length > 0 ? filtered : ALL_BUG_HUNTER_PUZZLES;
    }

    if (typeof ALL_REPAIR_SHOP_PUZZLES !== 'undefined') {
        let filtered = ALL_REPAIR_SHOP_PUZZLES.filter(p => p.title && p.title.toLowerCase().includes(searchLang));
        REPAIR_SHOP_PUZZLES = filtered.length > 0 ? filtered : ALL_REPAIR_SHOP_PUZZLES;
    }

    if (typeof populateTyperSelect === 'function') populateTyperSelect();
    if (typeof initTyperGame === 'function') initTyperGame(0);
    if (typeof initBugGame === 'function') initBugGame();
    if (typeof initParsonsGame === 'function') initParsonsGame();
}
"""

# Replace switchGameLanguage in content
pattern = r'function switchGameLanguage\(lang\) \{.*?\n\}'
import re
content = re.sub(r'function switchGameLanguage\(lang\) \{[\s\S]*?\n\}', new_switch_func, content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated game filtering per language successfully!")
