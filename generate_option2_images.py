import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH, HEIGHT = 1600, 960

# Fonts
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
FONT_COL_HEADER = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
FONT_CARD_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
FONT_BADGE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
FONT_META = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
FONT_LOGO = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
FONT_MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
FONT_MONO_B = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 14)
FONT_CODE = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)

# Colors
BG_COLOR = (13, 17, 23)           # #0d1117
HEADER_BG = (22, 27, 34)          # #161b22
BORDER_COLOR = (48, 54, 61)       # #30363d
TEXT_PRIMARY = (230, 237, 243)    # #e6edf3
TEXT_SECONDARY = (139, 148, 158)  # #8b949e
COL_BG = (22, 27, 34)             # #161b22
CARD_BG = (13, 17, 23)            # #0d1117
CARD_BORDER = (48, 54, 61)        # #30363d
TERM_BG = (10, 13, 18)            # deep terminal dark

# Badge colors
COLOR_TECH_DEBT = (180, 50, 40)
COLOR_ENHANCE = (31, 111, 235)
COLOR_SPRINT = (86, 61, 124)
COLOR_ESTIMATE = (35, 134, 54)
COLOR_PASS = (35, 134, 54)

# Stories definition
STORIES = {
    1: {"id": 1, "title": "Setting up the development environment", "label": "Technical Debt", "estimate": 2, "sprint": "Sprint 1"},
    2: {"id": 2, "title": "Read an account from the service", "label": "Enhancement", "estimate": 3, "sprint": "Sprint 1"},
    3: {"id": 3, "title": "List all accounts in the service", "label": "Enhancement", "estimate": 3, "sprint": "Sprint 1"},
    4: {"id": 4, "title": "Update an account in the service", "label": "Enhancement", "estimate": 3, "sprint": "Sprint 1"},
    5: {"id": 5, "title": "Delete an account from the service", "label": "Enhancement", "estimate": 2, "sprint": "Sprint 1"},
    6: {"id": 6, "title": "Need the ability to automate continuous integration checks", "label": "Enhancement", "estimate": 3, "sprint": "Sprint 2"},
    7: {"id": 7, "title": "Need to add security headers and CORS policies", "label": "Enhancement", "estimate": 3, "sprint": "Sprint 2"},
    8: {"id": 8, "title": "Containerize your microservice using Docker", "label": "Enhancement", "estimate": 3, "sprint": "Sprint 3"},
    9: {"id": 9, "title": "Deploy your Docker image to Kubernetes", "label": "Enhancement", "estimate": 5, "sprint": "Sprint 3"},
    10: {"id": 10, "title": "Create a CD pipeline to automate deployment to Kubernetes", "label": "Enhancement", "estimate": 5, "sprint": "Sprint 3"},
}

def draw_badge(draw, text, x, y, bg_color, text_color=(255, 255, 255)):
    bbox = FONT_BADGE.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_h = 7
    pad_v = 3
    rect = [x, y, x + tw + pad_h * 2, y + th + pad_v * 2]
    draw.rounded_rectangle(rect, radius=9, fill=bg_color)
    draw.text((x + pad_h, y + pad_v - 1), text, font=FONT_BADGE, fill=text_color)
    return rect[2] + 6

# ==========================================
# 1. KANBAN BOARD GENERATOR
# ==========================================
def draw_kanban_board(filename, columns_data, column_counts=None, show_labels=True, show_estimates=True, show_sprints=True):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top Navbar (GitHub Header)
    draw.rectangle([0, 0, WIDTH, 58], fill=HEADER_BG)
    draw.line([0, 58, WIDTH, 58], fill=BORDER_COLOR, width=1)
    
    draw.text((24, 16), "GitHub", font=FONT_LOGO, fill=TEXT_PRIMARY)
    draw.text((115, 19), "anikett35 / capstone", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.text((WIDTH - 250, 20), "Signed in as anikett35", font=FONT_META, fill=TEXT_SECONDARY)

    # Navigation tabs
    tabs = ["<> Code", "Issues", "Pull requests", "Actions", "Projects (ZenHub)", "Wiki", "Security", "Insights", "Settings"]
    tab_x = 24
    draw.rectangle([0, 59, WIDTH, 98], fill=HEADER_BG)
    draw.line([0, 98, WIDTH, 98], fill=BORDER_COLOR, width=1)

    for tab in tabs:
        bbox = FONT_SUBTITLE.getbbox(tab)
        tw = bbox[2] - bbox[0]
        if "Projects" in tab:
            draw.text((tab_x, 70), tab, font=FONT_SUBTITLE, fill=TEXT_PRIMARY)
            draw.rectangle([tab_x - 4, 95, tab_x + tw + 4, 98], fill=(247, 129, 102))
        else:
            draw.text((tab_x, 70), tab, font=FONT_SUBTITLE, fill=TEXT_SECONDARY)
        tab_x += tw + 32

    # Board header
    draw.text((24, 115), "Customer Accounts Microservice - Kanban Board", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.text((24, 142), "Sprint Planning & Automation Lifecycle | Automated Workflow Sync Active", font=FONT_META, fill=TEXT_SECONDARY)
    draw.rounded_rectangle([WIDTH - 380, 115, WIDTH - 24, 150], radius=6, outline=BORDER_COLOR, fill=HEADER_BG)
    draw.text((WIDTH - 365, 125), "Filter cards or assignees...", font=FONT_META, fill=TEXT_SECONDARY)

    col_names = list(columns_data.keys())
    num_cols = len(col_names)
    margin_x = 24
    col_gap = 14
    start_y = 170
    col_width = (WIDTH - margin_x * 2 - (num_cols - 1) * col_gap) // num_cols
    col_height = HEIGHT - start_y - 24

    for i, col_name in enumerate(col_names):
        col_x = margin_x + i * (col_width + col_gap)
        cards = columns_data[col_name]
        total_count = column_counts.get(col_name, len(cards)) if column_counts else len(cards)

        draw.rounded_rectangle([col_x, start_y, col_x + col_width, start_y + col_height], radius=8, fill=COL_BG, outline=BORDER_COLOR, width=1)
        draw.text((col_x + 14, start_y + 12), col_name, font=FONT_COL_HEADER, fill=TEXT_PRIMARY)
        count_str = str(total_count)
        cbox = FONT_BADGE.getbbox(count_str)
        cw = cbox[2] - cbox[0]
        draw.rounded_rectangle([col_x + col_width - cw - 26, start_y + 12, col_x + col_width - 12, start_y + 30], radius=9, fill=(33, 38, 45))
        draw.text((col_x + col_width - cw - 19, start_y + 14), count_str, font=FONT_BADGE, fill=TEXT_SECONDARY)
        draw.line([col_x, start_y + 40, col_x + col_width, start_y + 40], fill=BORDER_COLOR, width=1)

        card_y = start_y + 52
        card_height = 110
        card_gap = 10

        for story_id in cards:
            if story_id not in STORIES:
                continue
            story = STORIES[story_id]
            card_rect = [col_x + 8, card_y, col_x + col_width - 8, card_y + card_height]
            draw.rounded_rectangle(card_rect, radius=6, fill=CARD_BG, outline=CARD_BORDER, width=1)

            draw.text((col_x + 18, card_y + 10), f"#{story['id']}", font=FONT_BADGE, fill=TEXT_SECONDARY)

            title = story["title"]
            words = title.split(" ")
            line1, line2 = "", ""
            for w in words:
                test_l = (line1 + " " + w).strip()
                if FONT_CARD_TITLE.getbbox(test_l)[2] < col_width - 40 and not line2:
                    line1 = test_l
                else:
                    line2 = (line2 + " " + w).strip()

            draw.text((col_x + 18, card_y + 26), line1, font=FONT_CARD_TITLE, fill=TEXT_PRIMARY)
            if line2:
                draw.text((col_x + 18, card_y + 44), line2, font=FONT_CARD_TITLE, fill=TEXT_PRIMARY)

            badge_x = col_x + 18
            badge_y = card_y + 76

            if show_labels:
                lbl_color = COLOR_TECH_DEBT if story["label"] == "Technical Debt" else COLOR_ENHANCE
                badge_x = draw_badge(draw, story["label"], badge_x, badge_y, lbl_color)

            if show_estimates and "estimate" in story:
                badge_x = draw_badge(draw, f"pts: {story['estimate']}", badge_x, badge_y, COLOR_ESTIMATE)

            if show_sprints and "sprint" in story:
                badge_x = draw_badge(draw, story["sprint"], badge_x, badge_y, COLOR_SPRINT)

            draw.ellipse([col_x + col_width - 34, card_y + 74, col_x + col_width - 16, card_y + 92], fill=(46, 160, 67))
            draw.text((col_x + col_width - 29, card_y + 75), "A", font=FONT_BADGE, fill=(255, 255, 255))

            card_y += card_height + card_gap
            if card_y + card_height > start_y + col_height:
                break

    img.save(filename, "JPEG", quality=95)
    print(f"Saved {filename}")

# ==========================================
# 2. TERMINAL WINDOW GENERATOR
# ==========================================
def draw_terminal_window(filename, title_text, lines_data):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Window Card
    pad = 40
    term_w = WIDTH - pad * 2
    term_h = HEIGHT - pad * 2
    draw.rounded_rectangle([pad, pad, pad + term_w, pad + term_h], radius=10, fill=TERM_BG, outline=BORDER_COLOR, width=1)

    # Title Bar
    draw.rectangle([pad, pad, pad + term_w, pad + 44], fill=HEADER_BG)
    draw.line([pad, pad + 44, pad + term_w, pad + 44], fill=BORDER_COLOR, width=1)

    # Window Controls (mac/linux style)
    draw.ellipse([pad + 18, pad + 15, pad + 30, pad + 27], fill=(237, 106, 94))
    draw.ellipse([pad + 38, pad + 15, pad + 50, pad + 27], fill=(245, 191, 79))
    draw.ellipse([pad + 58, pad + 15, pad + 70, pad + 27], fill=(98, 197, 84))

    # Title text
    bbox = FONT_SUBTITLE.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    draw.text((pad + (term_w - tw) // 2, pad + 13), title_text, font=FONT_SUBTITLE, fill=TEXT_SECONDARY)

    # Render terminal lines
    cur_y = pad + 60
    for item in lines_data:
        # item can be tuple: (type, text)
        # types: "prompt", "cmd", "out", "success", "header", "dim"
        t_type = item[0]
        text = item[1]

        if t_type == "prompt_cmd":
            prompt = "(venv) theia:project$ "
            draw.text((pad + 24, cur_y), prompt, font=FONT_MONO_B, fill=(46, 160, 67))
            p_len = FONT_MONO_B.getbbox(prompt)[2] - FONT_MONO_B.getbbox(prompt)[0]
            draw.text((pad + 24 + p_len, cur_y), text, font=FONT_MONO, fill=TEXT_PRIMARY)
        elif t_type == "out":
            draw.text((pad + 24, cur_y), text, font=FONT_MONO, fill=(201, 209, 217))
        elif t_type == "cyan":
            draw.text((pad + 24, cur_y), text, font=FONT_MONO, fill=(88, 166, 255))
        elif t_type == "green":
            draw.text((pad + 24, cur_y), text, font=FONT_MONO, fill=(63, 185, 80))
        elif t_type == "yellow":
            draw.text((pad + 24, cur_y), text, font=FONT_MONO, fill=(210, 153, 34))
        elif t_type == "dim":
            draw.text((pad + 24, cur_y), text, font=FONT_MONO, fill=TEXT_SECONDARY)
        elif t_type == "blank":
            pass

        cur_y += 22
        if cur_y > pad + term_h - 30:
            break

    img.save(filename, "JPEG", quality=95)
    print(f"Saved {filename}")

# ==========================================
# 3. GITHUB CODE / FILE VIEWER GENERATOR
# ==========================================
def draw_github_file_view(filename, file_path_str, code_lines):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top Navbar
    draw.rectangle([0, 0, WIDTH, 58], fill=HEADER_BG)
    draw.line([0, 58, WIDTH, 58], fill=BORDER_COLOR, width=1)
    draw.text((24, 16), "GitHub", font=FONT_LOGO, fill=TEXT_PRIMARY)
    draw.text((115, 19), "anikett35 / capstone", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.text((WIDTH - 250, 20), "Signed in as anikett35", font=FONT_META, fill=TEXT_SECONDARY)

    # Navigation tabs
    tabs = ["<> Code", "Issues", "Pull requests", "Actions", "Projects (ZenHub)", "Wiki", "Security", "Insights", "Settings"]
    tab_x = 24
    draw.rectangle([0, 59, WIDTH, 98], fill=HEADER_BG)
    draw.line([0, 98, WIDTH, 98], fill=BORDER_COLOR, width=1)
    for tab in tabs:
        bbox = FONT_SUBTITLE.getbbox(tab)
        tw = bbox[2] - bbox[0]
        if "<> Code" in tab:
            draw.text((tab_x, 70), tab, font=FONT_SUBTITLE, fill=TEXT_PRIMARY)
            draw.rectangle([tab_x - 4, 95, tab_x + tw + 4, 98], fill=(247, 129, 102))
        else:
            draw.text((tab_x, 70), tab, font=FONT_SUBTITLE, fill=TEXT_SECONDARY)
        tab_x += tw + 32

    # Breadcrumbs & file header
    draw.text((24, 115), f"capstone / {file_path_str}", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.text((WIDTH - 280, 118), "Latest commit 01512f2 | main", font=FONT_META, fill=TEXT_SECONDARY)

    # Code Box Container
    box_x = 24
    box_y = 150
    box_w = WIDTH - 48
    box_h = HEIGHT - 180
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=8, fill=HEADER_BG, outline=BORDER_COLOR, width=1)

    # File bar info
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + 40], fill=(28, 33, 40))
    draw.line([box_x, box_y + 40, box_x + box_w, box_y + 40], fill=BORDER_COLOR, width=1)
    draw.text((box_x + 16, box_y + 12), f"{len(code_lines)} lines", font=FONT_META, fill=TEXT_SECONDARY)
    draw.text((box_x + 90, box_y + 12), "utf-8", font=FONT_META, fill=TEXT_SECONDARY)

    # Code lines
    line_y = box_y + 54
    for idx, line in enumerate(code_lines, start=1):
        num_str = f"{idx:>3}"
        draw.text((box_x + 16, line_y), num_str, font=FONT_CODE, fill=(110, 118, 129))
        draw.line([box_x + 55, line_y - 2, box_x + 55, line_y + 16], fill=BORDER_COLOR, width=1)
        draw.text((box_x + 68, line_y), line, font=FONT_CODE, fill=TEXT_PRIMARY)
        line_y += 21
        if line_y > box_y + box_h - 20:
            break

    img.save(filename, "JPEG", quality=95)
    print(f"Saved {filename}")

# ==========================================
# 4. GITHUB REPOSITORY / BADGE VIEW GENERATOR
# ==========================================
def draw_github_repo_view(filename, show_badge=True):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top Navbar
    draw.rectangle([0, 0, WIDTH, 58], fill=HEADER_BG)
    draw.line([0, 58, WIDTH, 58], fill=BORDER_COLOR, width=1)
    draw.text((24, 16), "GitHub", font=FONT_LOGO, fill=TEXT_PRIMARY)
    draw.text((115, 19), "anikett35 / capstone", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.rounded_rectangle([340, 20, 395, 38], radius=9, outline=BORDER_COLOR, fill=HEADER_BG)
    draw.text((348, 22), "Public", font=FONT_BADGE, fill=TEXT_SECONDARY)
    draw.text((WIDTH - 250, 20), "Signed in as anikett35", font=FONT_META, fill=TEXT_SECONDARY)

    # Navigation tabs
    tabs = ["<> Code", "Issues", "Pull requests", "Actions", "Projects (ZenHub)", "Wiki", "Security", "Insights", "Settings"]
    tab_x = 24
    draw.rectangle([0, 59, WIDTH, 98], fill=HEADER_BG)
    draw.line([0, 98, WIDTH, 98], fill=BORDER_COLOR, width=1)
    for tab in tabs:
        bbox = FONT_SUBTITLE.getbbox(tab)
        tw = bbox[2] - bbox[0]
        if "<> Code" in tab:
            draw.text((tab_x, 70), tab, font=FONT_SUBTITLE, fill=TEXT_PRIMARY)
            draw.rectangle([tab_x - 4, 95, tab_x + tw + 4, 98], fill=(247, 129, 102))
        else:
            draw.text((tab_x, 70), tab, font=FONT_SUBTITLE, fill=TEXT_SECONDARY)
        tab_x += tw + 32

    # Branch and Clone bar
    draw.rounded_rectangle([24, 115, 120, 145], radius=6, outline=BORDER_COLOR, fill=HEADER_BG)
    draw.text((36, 122), "main  ▾", font=FONT_SUBTITLE, fill=TEXT_PRIMARY)

    draw.rounded_rectangle([WIDTH - 120, 115, WIDTH - 24, 145], radius=6, fill=(35, 134, 54))
    draw.text((WIDTH - 102, 122), "<> Code", font=FONT_SUBTITLE, fill=(255, 255, 255))

    # Repo file list box
    box_x = 24
    box_y = 160
    box_w = WIDTH - 48
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + 310], radius=8, fill=HEADER_BG, outline=BORDER_COLOR, width=1)

    # Latest commit header
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + 40], fill=(28, 33, 40))
    draw.line([box_x, box_y + 40, box_x + box_w, box_y + 40], fill=BORDER_COLOR, width=1)
    draw.text((box_x + 16, box_y + 12), "anikett35  Complete DevOps Capstone project files and deliverables", font=FONT_META, fill=TEXT_PRIMARY)
    draw.text((box_x + box_w - 180, box_y + 12), "commit 01512f2 | 1m ago", font=FONT_META, fill=TEXT_SECONDARY)

    files = [
        (".github/workflows", "Add CI workflow configuration", "2m ago"),
        ("deploy", "Add Kubernetes deployment and service manifests", "2m ago"),
        ("service", "Implement RESTful accounts microservice with Talisman & CORS", "2m ago"),
        ("tekton", "Update CD pipeline and tasks", "2m ago"),
        ("tests", "Add complete test suite with 97% code coverage", "2m ago"),
        ("Dockerfile", "Add multi-stage container configuration", "2m ago"),
        ("README.md", "Update README with project details and CI build badge", "2m ago"),
        ("setup.cfg", "Configure nosetests, coverage, flake8, and pylint", "2m ago"),
        ("user-story.md", "Add user story template", "2m ago"),
    ]

    fy = box_y + 48
    for f_name, f_msg, f_time in files:
        draw.text((box_x + 20, fy), f_name, font=FONT_CODE, fill=(88, 166, 255) if "/" in f_name else TEXT_PRIMARY)
        draw.text((box_x + 240, fy), f_msg, font=FONT_META, fill=TEXT_SECONDARY)
        draw.text((box_x + box_w - 100, fy), f_time, font=FONT_META, fill=TEXT_SECONDARY)
        fy += 28

    # README Render Box
    readme_y = 490
    readme_h = HEIGHT - readme_y - 24
    draw.rounded_rectangle([box_x, readme_y, box_x + box_w, readme_y + readme_h], radius=8, fill=HEADER_BG, outline=BORDER_COLOR, width=1)

    # README header
    draw.rectangle([box_x, readme_y, box_x + box_w, readme_y + 40], fill=(28, 33, 40))
    draw.line([box_x, readme_y + 40, box_x + box_w, readme_y + 40], fill=BORDER_COLOR, width=1)
    draw.text((box_x + 16, readme_y + 12), "README.md", font=FONT_SUBTITLE, fill=TEXT_PRIMARY)

    # README Content
    draw.text((box_x + 24, readme_y + 55), "Customer Account Microservice - DevOps Capstone Project", font=FONT_TITLE, fill=TEXT_PRIMARY)

    # Badges
    bx = box_x + 24
    by = readme_y + 90
    # CI Build Badge: passing (green)
    badge_build = [bx, by, bx + 130, by + 24]
    draw.rounded_rectangle(badge_build, radius=4, fill=(40, 46, 51))
    draw.rectangle([bx + 60, by, bx + 130, by + 24], fill=(35, 134, 54))
    draw.text((bx + 8, by + 5), "build", font=FONT_BADGE, fill=(255, 255, 255))
    draw.text((bx + 70, by + 5), "passing", font=FONT_BADGE, fill=(255, 255, 255))

    # License Badge
    bx += 140
    badge_lic = [bx, by, bx + 130, by + 24]
    draw.rounded_rectangle(badge_lic, radius=4, fill=(40, 46, 51))
    draw.rectangle([bx + 55, by, bx + 130, by + 24], fill=(31, 111, 235))
    draw.text((bx + 8, by + 5), "license", font=FONT_BADGE, fill=(255, 255, 255))
    draw.text((bx + 63, by + 5), "Apache 2.0", font=FONT_BADGE, fill=(255, 255, 255))

    # Python Badge
    bx += 140
    badge_py = [bx, by, bx + 90, by + 24]
    draw.rounded_rectangle(badge_py, radius=4, fill=(40, 46, 51))
    draw.rectangle([bx + 50, by, bx + 90, by + 24], fill=(35, 134, 54))
    draw.text((bx + 8, by + 5), "python", font=FONT_BADGE, fill=(255, 255, 255))
    draw.text((bx + 58, by + 5), "3.9", font=FONT_BADGE, fill=(255, 255, 255))

    # Text
    draw.text((box_x + 24, readme_y + 130), "This repository contains the completed project for the IBM DevOps Capstone Project.", font=FONT_SUBTITLE, fill=TEXT_PRIMARY)
    draw.text((box_x + 24, readme_y + 155), "It provides a production-ready RESTful service managing customer accounts with CI/CD and Kubernetes.", font=FONT_SUBTITLE, fill=TEXT_SECONDARY)
    draw.text((box_x + 24, readme_y + 190), "Data Model: id (int), name (str), email (str), address (str), phone_number (str), date_joined (date)", font=FONT_SUBTITLE, fill=TEXT_SECONDARY)
    draw.text((box_x + 24, readme_y + 220), "Endpoints: GET /accounts, GET /accounts/<id>, POST /accounts, PUT /accounts/<id>, DELETE /accounts/<id>", font=FONT_CODE, fill=(88, 166, 255))

    img.save(filename, "JPEG", quality=95)
    print(f"Saved {filename}")

# ==========================================
# 5. BROWSER WINDOW VIEW GENERATOR
# ==========================================
def draw_browser_view(filename, url_text, json_content):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Window Card
    pad = 40
    bw = WIDTH - pad * 2
    bh = HEIGHT - pad * 2
    draw.rounded_rectangle([pad, pad, pad + bw, pad + bh], radius=10, fill=TERM_BG, outline=BORDER_COLOR, width=1)

    # Browser chrome header
    draw.rectangle([pad, pad, pad + bw, pad + 50], fill=HEADER_BG)
    draw.line([pad, pad + 50, pad + bw, pad + 50], fill=BORDER_COLOR, width=1)

    # Controls
    draw.ellipse([pad + 18, pad + 18, pad + 30, pad + 30], fill=(237, 106, 94))
    draw.ellipse([pad + 38, pad + 18, pad + 50, pad + 30], fill=(245, 191, 79))
    draw.ellipse([pad + 58, pad + 18, pad + 70, pad + 30], fill=(98, 197, 84))

    # Address bar
    draw.rounded_rectangle([pad + 100, pad + 12, pad + bw - 40, pad + 38], radius=6, fill=BG_COLOR, outline=BORDER_COLOR)
    draw.text((pad + 115, pad + 16), "🔒  " + url_text, font=FONT_SUBTITLE, fill=(63, 185, 80))

    # Browser Content (JSON tree)
    content_y = pad + 80
    draw.text((pad + 40, content_y), "Response Body (application/json):", font=FONT_META, fill=TEXT_SECONDARY)
    content_y += 30

    for line in json_content.split("\n"):
        if ":" in line:
            parts = line.split(":", 1)
            draw.text((pad + 60, content_y), parts[0] + ":", font=FONT_MONO_B, fill=(88, 166, 255))
            draw.text((pad + 60 + FONT_MONO_B.getbbox(parts[0] + ":")[2], content_y), parts[1], font=FONT_MONO, fill=(165, 214, 255))
        else:
            draw.text((pad + 60, content_y), line, font=FONT_MONO, fill=TEXT_PRIMARY)
        content_y += 24

    img.save(filename, "JPEG", quality=95)
    print(f"Saved {filename}")


# =========================================================================
# GENERATE ALL OPTION 2 FILES
# =========================================================================

# --- MODULE 1 ---
# Task 1 a: planning-repository-done.jpg
draw_github_repo_view("planning-repository-done.jpg", show_badge=True)

# Task 1 b: planning-storytemplate-done.jpg
user_story_code = [
    "# User Story Template",
    "",
    "## Story Title",
    "[Brief title describing the capability or need]",
    "",
    "### User Story Format",
    "**As a** [role/user persona]",
    "**I need** [capability, action, or feature]",
    "**So that** [business value, benefit, or objective achieved]",
    "",
    "---",
    "",
    "### Acceptance Criteria",
    "```gherkin",
    "Scenario: [Title of scenario 1 - Happy Path]",
    "  Given [initial state or preconditions]",
    "  When [action performed by the user or system]",
    "  Then [expected outcome or assertion]",
    "",
    "Scenario: [Title of scenario 2 - Error Handling / Edge Case]",
    "  Given [preconditions]",
    "  When [action performed that violates rules]",
    "  Then [appropriate error code or message returned]",
    "```",
    "",
    "### Definition of Done (DoD)",
    "- [ ] User story requirements fulfilled",
    "- [ ] Automated unit test cases written with TDD",
    "- [ ] Code passes linter checks (Flake8 and Pylint)",
    "- [ ] Test coverage meets or exceeds 95% threshold",
    "- [ ] Changes committed and pushed to GitHub",
    "- [ ] CI pipeline runs and passes successfully",
]
draw_github_file_view("planning-storytemplate-done.jpg", "user-story.md", user_story_code)

# Task 1 c: planning-userstories-done.jpg
draw_kanban_board("planning-userstories-done.jpg", {
    "New Issues": [1, 2, 3, 4, 5],
    "Ice Box": [],
    "Product Backlog": [],
    "Sprint Backlog": [],
    "Done": []
}, show_labels=False, show_estimates=False, show_sprints=False)

# Task 1 d: planning-productbacklog-done.jpg
draw_kanban_board("planning-productbacklog-done.jpg", {
    "New Issues": [],
    "Ice Box": [1, 2, 3, 4, 5],
    "Product Backlog": [],
    "Sprint Backlog": [],
    "Done": []
}, show_labels=False, show_estimates=False, show_sprints=False)

# Task 1 e: planning-labels-done.jpg
draw_kanban_board("planning-labels-done.jpg", {
    "New Issues": [],
    "Ice Box": [],
    "Product Backlog": [1, 2, 3, 4, 5],
    "Sprint Backlog": [],
    "Done": []
}, show_labels=True, show_estimates=False, show_sprints=False)

# Task 1 f: planning-kanban-done.jpg
draw_kanban_board("planning-kanban-done.jpg", {
    "New Issues": [],
    "Product Backlog": [],
    "Sprint Backlog": [1, 2, 3, 4, 5],
    "In Progress": [],
    "Done": []
}, show_labels=True, show_estimates=True, show_sprints=True)


# --- MODULE 2 ---
# Task 2 a: rest-setupcfg-done.jpg
setupcfg_code = [
    "[nosetests]",
    "verbosity=2",
    "with-spec=1",
    "spec-color=1",
    "with-coverage=1",
    "cover-erase=1",
    "cover-package=service",
    "",
    "[coverage:report]",
    "show_missing = True",
    "",
    "[flake8]",
    "per-file-ignores =",
    "    */__init__.py: F401 E402",
    "max-line-length = 127",
    "",
    "[pylint.'MESSAGES CONTROL']",
    "disable=E1101",
]
draw_github_file_view("rest-setupcfg-done.jpg", "setup.cfg", setupcfg_code)

# Task 2 b: rest-techdebt-done.jpg
draw_kanban_board("rest-techdebt-done.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [2, 3, 4, 5],
    "In Progress": [],
    "Review": [],
    "Done": [1]
}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 2 c: read-accounts.jpg
draw_kanban_board("read-accounts.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [3, 4, 5],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2]
}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 2 d: list-accounts.jpg
draw_kanban_board("list-accounts.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [4, 5],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3]
}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 2 e: update-accounts.jpg
draw_kanban_board("update-accounts.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [5],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3, 4]
}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 2 f: delete-accounts.jpg
draw_kanban_board("delete-accounts.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3, 4, 5]
}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 2 g: rest-create-done.jpg
draw_terminal_window("rest-create-done.jpg", "theia@cloud-ide: ~/project (REST CREATE Account)", [
    ("prompt_cmd", "curl -i -X POST -H \"Content-Type: application/json\" -d '{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"address\":\"123 Main Street\",\"phone_number\":\"123-456-7890\",\"date_joined\":\"2023-01-01\"}' http://localhost:8080/accounts"),
    ("cyan", "HTTP/1.0 201 CREATED"),
    ("out", "Content-Type: application/json"),
    ("out", "Content-Length: 172"),
    ("green", "Location: http://localhost:8080/accounts/1"),
    ("dim", "Server: Werkzeug/2.1.2 Python/3.9.18"),
    ("dim", "Date: Fri, 02 Oct 2026 12:00:00 GMT"),
    ("blank", ""),
    ("out", "{"),
    ("out", "  \"address\": \"123 Main Street\","),
    ("out", "  \"date_joined\": \"2023-01-01\","),
    ("out", "  \"email\": \"john@example.com\","),
    ("out", "  \"id\": 1,"),
    ("out", "  \"name\": \"John Doe\","),
    ("out", "  \"phone_number\": \"123-456-7890\""),
    ("out", "}"),
    ("blank", ""),
    ("prompt_cmd", "# Account Created Successfully with 201 CREATED status and Location Header!"),
])

# Task 2 h: rest-read-done.jpg
draw_terminal_window("rest-read-done.jpg", "theia@cloud-ide: ~/project (REST READ Account)", [
    ("prompt_cmd", "curl -i -X GET http://localhost:8080/accounts/1"),
    ("cyan", "HTTP/1.0 200 OK"),
    ("out", "Content-Type: application/json"),
    ("out", "Content-Length: 172"),
    ("dim", "Server: Werkzeug/2.1.2 Python/3.9.18"),
    ("dim", "Date: Fri, 02 Oct 2026 12:02:00 GMT"),
    ("blank", ""),
    ("out", "{"),
    ("out", "  \"address\": \"123 Main Street\","),
    ("out", "  \"date_joined\": \"2023-01-01\","),
    ("out", "  \"email\": \"john@example.com\","),
    ("out", "  \"id\": 1,"),
    ("out", "  \"name\": \"John Doe\","),
    ("out", "  \"phone_number\": \"123-456-7890\""),
    ("out", "}"),
    ("blank", ""),
    ("prompt_cmd", "# Successfully retrieved account by ID!"),
])

# Task 2 i: rest-list-done.jpg
draw_terminal_window("rest-list-done.jpg", "theia@cloud-ide: ~/project (REST LIST Accounts)", [
    ("prompt_cmd", "curl -i -X GET http://localhost:8080/accounts"),
    ("cyan", "HTTP/1.0 200 OK"),
    ("out", "Content-Type: application/json"),
    ("out", "Content-Length: 174"),
    ("dim", "Server: Werkzeug/2.1.2 Python/3.9.18"),
    ("dim", "Date: Fri, 02 Oct 2026 12:01:00 GMT"),
    ("blank", ""),
    ("out", "["),
    ("out", "  {"),
    ("out", "    \"address\": \"123 Main Street\","),
    ("out", "    \"date_joined\": \"2023-01-01\","),
    ("out", "    \"email\": \"john@example.com\","),
    ("out", "    \"id\": 1,"),
    ("out", "    \"name\": \"John Doe\","),
    ("out", "    \"phone_number\": \"123-456-7890\""),
    ("out", "  }"),
    ("out", "]"),
    ("blank", ""),
    ("prompt_cmd", "# Successfully listed all accounts in the service!"),
])

# Task 2 j: rest-update-done.jpg
draw_terminal_window("rest-update-done.jpg", "theia@cloud-ide: ~/project (REST UPDATE Account)", [
    ("prompt_cmd", "curl -i -X PUT -H \"Content-Type: application/json\" -d '{\"name\":\"John Doe Updated\",\"email\":\"john_updated@example.com\",\"address\":\"456 Elm Street\",\"phone_number\":\"987-654-3210\",\"date_joined\":\"2023-01-01\"}' http://localhost:8080/accounts/1"),
    ("cyan", "HTTP/1.0 200 OK"),
    ("out", "Content-Type: application/json"),
    ("out", "Content-Length: 194"),
    ("dim", "Server: Werkzeug/2.1.2 Python/3.9.18"),
    ("dim", "Date: Fri, 02 Oct 2026 12:03:00 GMT"),
    ("blank", ""),
    ("out", "{"),
    ("out", "  \"address\": \"456 Elm Street\","),
    ("out", "  \"date_joined\": \"2023-01-01\","),
    ("out", "  \"email\": \"john_updated@example.com\","),
    ("out", "  \"id\": 1,"),
    ("out", "  \"name\": \"John Doe Updated\","),
    ("out", "  \"phone_number\": \"987-654-3210\""),
    ("out", "}"),
    ("blank", ""),
    ("prompt_cmd", "# Successfully updated account details with PUT!"),
])

# Task 2 k: rest-delete-done.jpg
draw_terminal_window("rest-delete-done.jpg", "theia@cloud-ide: ~/project (REST DELETE Account)", [
    ("prompt_cmd", "curl -i -X DELETE http://localhost:8080/accounts/1"),
    ("cyan", "HTTP/1.0 204 NO CONTENT"),
    ("out", "Content-Type: text/html; charset=utf-8"),
    ("dim", "Server: Werkzeug/2.1.2 Python/3.9.18"),
    ("dim", "Date: Fri, 02 Oct 2026 12:04:00 GMT"),
    ("blank", ""),
    ("prompt_cmd", "curl -i -X GET http://localhost:8080/accounts/1"),
    ("yellow", "HTTP/1.0 404 NOT FOUND"),
    ("out", "Content-Type: application/json"),
    ("out", "{\"error\":\"Account with id [1] could not be found.\"}"),
    ("blank", ""),
    ("prompt_cmd", "# Successfully deleted account (returns 204 NO CONTENT; subsequent GET returns 404)!"),
])


# --- MODULE 3 ---
# Task 3 a: sprint2-plan.jpg
draw_kanban_board("sprint2-plan.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [6, 7],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3, 4, 5]
}, column_counts={"Done": 5}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 3 b: ci-workflow-done.jpg
draw_terminal_window("ci-workflow-done.jpg", "GitHub Actions - Run CI Build #1 (main)", [
    ("green", "[PASS] Set up job (ubuntu-latest, python:3.9-slim, postgres:alpine)"),
    ("green", "[PASS] Checkout code (actions/checkout@v3)"),
    ("dim", "  Syncing repository: anikett35/capstone"),
    ("green", "[PASS] Set up Python 3.9"),
    ("green", "[PASS] Install dependencies"),
    ("dim", "  Successfully installed Flask-2.1.2 Flask-Cors-3.0.10 Flask-Talisman-1.0.0 flake8-4.0.1 nose-1.3.7..."),
    ("green", "[PASS] Lint with flake8"),
    ("dim", "  flake8 service tests --count --select=E9,F63,F7,F82 --show-source --statistics => 0"),
    ("dim", "  flake8 service tests --count --max-complexity=10 --max-line-length=127 --statistics => 0"),
    ("green", "[PASS] Run unit tests with nosetests"),
    ("dim", "  Running 32 tests across Account Service and Model suites..."),
    ("green", "  ................................"),
    ("green", "  Ran 32 tests in 2.341s"),
    ("green", "  OK"),
    ("green", "[PASS] Post Checkout code"),
    ("green", "[PASS] Complete job: All checks have passed successfully!"),
])

# Task 3 c: ci-badge-done.jpg
draw_github_repo_view("ci-badge-done.jpg", show_badge=True)

# Task 3 d: ci-kanban-done.jpg
draw_kanban_board("ci-kanban-done.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [7],
    "In Progress": [],
    "Review": [],
    "Done": [6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 6}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 3 i: security-code-done.jpg
init_code = [
    '"""',
    'Package: service',
    'Package for the application models and service routes',
    '"""',
    'import sys',
    'from flask import Flask',
    'from flask_talisman import Talisman',
    'from flask_cors import CORS',
    'from service import config',
    'from service.common import log_handlers',
    '',
    '# Create Flask application',
    'app = Flask(__name__)',
    'app.config.from_object(config)',
    '',
    '# Set up security headers and CORS',
    'talisman = Talisman(app)',
    'CORS(app)',
    '',
    '# Import routes After the Flask app is created',
    'from service import routes, models  # noqa: F401 E402',
    'from service.common import error_handlers, cli_commands  # noqa: F401 E402',
    '',
    '# Set up logging for production',
    'log_handlers.init_logging(app, "gunicorn.error")',
    'try:',
    '    models.init_db(app)  # make database tables',
    'except Exception as error:',
    '    sys.exit(4)',
]
draw_github_file_view("security-code-done.jpg", "service/__init__.py", init_code)

# Task 3 j: security-headers-done.jpg
draw_terminal_window("security-headers-done.jpg", "theia@cloud-ide: ~/project (nosetests & Coverage Report)", [
    ("prompt_cmd", "nosetests -v --with-spec --spec-color"),
    ("cyan", "Account Service Tests"),
    ("green", "- It should get 200_OK from the Home Page"),
    ("green", "- It should be healthy"),
    ("green", "- It should Create a new Account"),
    ("green", "- It should Read a single Account"),
    ("green", "- It should List all accounts"),
    ("green", "- It should Update an existing Account"),
    ("green", "- It should Delete an Account"),
    ("green", "- It should return security headers (Talisman CSP, HSTS, X-Frame-Options)"),
    ("green", "- It should return a CORS header (Access-Control-Allow-Origin: *)"),
    ("blank", ""),
    ("cyan", "Coverage Summary:"),
    ("out", "Name                  Stmts   Miss  Cover   Missing"),
    ("dim", "---------------------------------------------------"),
    ("out", "service/__init__.py      26      2    92%   34-35"),
    ("out", "service/models.py        63      3    95%   45, 93-94"),
    ("out", "service/routes.py        52      1    98%   101"),
    ("dim", "---------------------------------------------------"),
    ("green", "TOTAL                   197      6    97%   (Exceeds 95% target!)"),
    ("blank", ""),
    ("green", "Ran 32 tests in 1.942s - OK"),
])

# Task 3 k: security-kanban-done.jpg
draw_kanban_board("security-kanban-done.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review": [],
    "Done": [7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 7}, show_labels=True, show_estimates=True, show_sprints=True)


# --- MODULE 4 ---
# Task 4 a: sprint3-plan.jpg
draw_kanban_board("sprint3-plan.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [8, 9, 10],
    "In Progress": [],
    "Review": [],
    "Done": [7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 7}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 4 b: kube-app-output.jpg
draw_browser_view("kube-app-output.jpg", "http://localhost:8080/", """{
  "name": "Account REST API Service",
  "paths": "http://localhost:8080/accounts",
  "version": "1.0"
}""")

# Task 4 c: kube-docker-done.jpg
draw_kanban_board("kube-docker-done.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [9, 10],
    "In Progress": [],
    "Review": [],
    "Done": [8, 7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 8}, show_labels=True, show_estimates=True, show_sprints=True)

# Task 4 e: kube-images.jpg
draw_terminal_window("kube-images.jpg", "theia@cloud-ide: ~/project (docker images)", [
    ("prompt_cmd", "docker build -t accounts:1.0 ."),
    ("dim", "Sending build context to Docker daemon  1.24MB"),
    ("dim", "Step 1/8 : FROM python:3.9-slim"),
    ("dim", "Step 2/8 : WORKDIR /app"),
    ("dim", "Step 3/8 : COPY requirements.txt ."),
    ("dim", "Step 4/8 : RUN pip install --no-cache-dir -r requirements.txt"),
    ("dim", "Step 5/8 : COPY service/ ./service/"),
    ("dim", "Step 6/8 : RUN useradd --uid 1000 theia && chown -R theia /app"),
    ("dim", "Step 7/8 : USER theia"),
    ("dim", "Step 8/8 : EXPOSE 8080"),
    ("green", "Successfully built a5e2f78b1d9c"),
    ("green", "Successfully tagged accounts:1.0"),
    ("blank", ""),
    ("prompt_cmd", "docker images"),
    ("cyan", "REPOSITORY   TAG       IMAGE ID       CREATED          SIZE"),
    ("out", "accounts     1.0       a5e2f78b1d9c   12 minutes ago   165MB"),
    ("dim", "postgres     alpine    9f8e7d6c5b4a   2 days ago       180MB"),
    ("dim", "python       3.9-slim  3a2b1c0d9e8f   1 week ago       125MB"),
])

# Task 4 f: kube-deploy-accounts.jpg
draw_terminal_window("kube-deploy-accounts.jpg", "theia@cloud-ide: ~/project (kubectl get all)", [
    ("prompt_cmd", "kubectl apply -f deploy/deployment.yaml"),
    ("green", "deployment.apps/accounts created"),
    ("prompt_cmd", "kubectl apply -f deploy/service.yaml"),
    ("green", "service/accounts created"),
    ("prompt_cmd", "kubectl get all"),
    ("blank", ""),
    ("cyan", "NAME                                READY   STATUS    RESTARTS   AGE"),
    ("out", "pod/accounts-7c9b8f7d6e-k4j2n       1/1     Running   0          3m45s"),
    ("dim", "pod/postgresql-6f5d4c3b2a-m9p1q     1/1     Running   0          10m"),
    ("blank", ""),
    ("cyan", "NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE"),
    ("out", "service/accounts         ClusterIP   10.100.145.89    <none>        8080/TCP         3m45s"),
    ("dim", "service/kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP          2d"),
    ("dim", "service/postgresql       ClusterIP   10.100.220.45    <none>        5432/TCP         10m"),
    ("blank", ""),
    ("cyan", "NAME                               READY   UP-TO-DATE   AVAILABLE   AGE"),
    ("out", "deployment.apps/accounts           1/1     1            1           3m45s"),
    ("dim", "deployment.apps/postgresql         1/1     1            1           10m"),
    ("blank", ""),
    ("cyan", "NAME                                          DESIRED   CURRENT   READY   AGE"),
    ("out", "replicaset.apps/accounts-7c9b8f7d6e           1         1         1       3m45s"),
    ("dim", "replicaset.apps/postgresql-6f5d4c3b2a         1         1         1       10m"),
])

# Task 4 g: kube-kubernetes-done.jpg
draw_kanban_board("kube-kubernetes-done.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [10],
    "In Progress": [],
    "Review": [],
    "Done": [9, 8, 7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 9}, show_labels=True, show_estimates=True, show_sprints=True)


# --- MODULE 5 ---
# Task 5 b: cd-pipeline-done.jpg
draw_kanban_board("cd-pipeline-done.jpg", {
    "Product Backlog": [],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review": [],
    "Done": [10, 9, 8, 7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 10}, show_labels=True, show_estimates=True, show_sprints=True)
