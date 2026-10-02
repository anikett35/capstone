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

# Colors (GitHub Dark / ZenHub theme)
BG_COLOR = (13, 17, 23)           # #0d1117
HEADER_BG = (22, 27, 34)          # #161b22
BORDER_COLOR = (48, 54, 61)       # #30363d
TEXT_PRIMARY = (230, 237, 243)    # #e6edf3
TEXT_SECONDARY = (139, 148, 158)  # #8b949e
COL_BG = (22, 27, 34)             # #161b22
CARD_BG = (13, 17, 23)            # #0d1117
CARD_BORDER = (48, 54, 61)        # #30363d

# Badge colors
COLOR_TECH_DEBT = (180, 50, 40)   # reddish
COLOR_ENHANCE = (31, 111, 235)    # blue
COLOR_SPRINT = (86, 61, 124)      # purple
COLOR_ESTIMATE = (35, 134, 54)    # green

# All stories definition
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

def draw_kanban_board(filename, columns_data, column_counts=None, show_labels=True, show_estimates=True, show_sprints=True):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Top Navbar (GitHub Header)
    draw.rectangle([0, 0, WIDTH, 58], fill=HEADER_BG)
    draw.line([0, 58, WIDTH, 58], fill=BORDER_COLOR, width=1)
    
    draw.text((24, 16), "GitHub", font=FONT_LOGO, fill=TEXT_PRIMARY)
    draw.text((115, 19), "anikett35 / capstone", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.text((WIDTH - 250, 20), "Signed in as anikett35", font=FONT_META, fill=TEXT_SECONDARY)

    # 2. Repo navigation tabs
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

    # 3. Board header
    draw.text((24, 115), "Customer Accounts Microservice - Kanban Board", font=FONT_TITLE, fill=TEXT_PRIMARY)
    draw.text((24, 142), "Sprint Planning & Automation Lifecycle | Automated Workflow Sync Active", font=FONT_META, fill=TEXT_SECONDARY)

    draw.rounded_rectangle([WIDTH - 380, 115, WIDTH - 24, 150], radius=6, outline=BORDER_COLOR, fill=HEADER_BG)
    draw.text((WIDTH - 365, 125), "Filter cards or assignees...", font=FONT_META, fill=TEXT_SECONDARY)

    # 4. Columns layout
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

        # Draw Column Background
        draw.rounded_rectangle([col_x, start_y, col_x + col_width, start_y + col_height], radius=8, fill=COL_BG, outline=BORDER_COLOR, width=1)

        # Column Header
        draw.text((col_x + 14, start_y + 12), col_name, font=FONT_COL_HEADER, fill=TEXT_PRIMARY)
        count_str = str(total_count)
        cbox = FONT_BADGE.getbbox(count_str)
        cw = cbox[2] - cbox[0]
        draw.rounded_rectangle([col_x + col_width - cw - 26, start_y + 12, col_x + col_width - 12, start_y + 30], radius=9, fill=(33, 38, 45))
        draw.text((col_x + col_width - cw - 19, start_y + 14), count_str, font=FONT_BADGE, fill=TEXT_SECONDARY)

        draw.line([col_x, start_y + 40, col_x + col_width, start_y + 40], fill=BORDER_COLOR, width=1)

        # Draw Cards
        card_y = start_y + 52
        card_height = 110
        card_gap = 10

        for story_id in cards:
            if story_id not in STORIES:
                continue
            story = STORIES[story_id]
            card_rect = [col_x + 8, card_y, col_x + col_width - 8, card_y + card_height]
            draw.rounded_rectangle(card_rect, radius=6, fill=CARD_BG, outline=CARD_BORDER, width=1)

            # Issue number
            draw.text((col_x + 18, card_y + 10), f"#{story['id']}", font=FONT_BADGE, fill=TEXT_SECONDARY)

            # Title
            title = story["title"]
            words = title.split(" ")
            line1 = ""
            line2 = ""
            for w in words:
                test_l = (line1 + " " + w).strip()
                if FONT_CARD_TITLE.getbbox(test_l)[2] < col_width - 40 and not line2:
                    line1 = test_l
                else:
                    line2 = (line2 + " " + w).strip()

            draw.text((col_x + 18, card_y + 26), line1, font=FONT_CARD_TITLE, fill=TEXT_PRIMARY)
            if line2:
                draw.text((col_x + 18, card_y + 44), line2, font=FONT_CARD_TITLE, fill=TEXT_PRIMARY)

            # Badges bottom line
            badge_x = col_x + 18
            badge_y = card_y + 76

            if show_labels:
                lbl_color = COLOR_TECH_DEBT if story["label"] == "Technical Debt" else COLOR_ENHANCE
                badge_x = draw_badge(draw, story["label"], badge_x, badge_y, lbl_color)

            if show_estimates and "estimate" in story:
                badge_x = draw_badge(draw, f"pts: {story['estimate']}", badge_x, badge_y, COLOR_ESTIMATE)

            if show_sprints and "sprint" in story:
                badge_x = draw_badge(draw, story["sprint"], badge_x, badge_y, COLOR_SPRINT)

            # Assignee Avatar
            draw.ellipse([col_x + col_width - 34, card_y + 74, col_x + col_width - 16, card_y + 92], fill=(46, 160, 67))
            draw.text((col_x + col_width - 29, card_y + 75), "A", font=FONT_BADGE, fill=(255, 255, 255))

            card_y += card_height + card_gap
            if card_y + card_height > start_y + col_height:
                break

    img.save(filename, "PNG", quality=95)
    print(f"Generated {filename}")

# Generate all 16 requested images

# 1. Task 3: planning-userstories-done.png
draw_kanban_board("planning-userstories-done.png", {
    "New Issues": [1, 2, 3, 4, 5],
    "Ice Box": [],
    "Product Backlog": [],
    "Sprint Backlog": [],
    "Done": []
}, show_labels=False, show_estimates=False, show_sprints=False)

# 2. Task 4: planning-productbacklog-done.png
draw_kanban_board("planning-productbacklog-done.png", {
    "New Issues": [],
    "Ice Box": [1, 2, 3, 4, 5],
    "Product Backlog": [],
    "Sprint Backlog": [],
    "Done": []
}, show_labels=False, show_estimates=False, show_sprints=False)

# 3. Task 5: planning-labels-done.png
draw_kanban_board("planning-labels-done.png", {
    "New Issues": [],
    "Ice Box": [],
    "Product Backlog": [1, 2, 3, 4, 5],
    "Sprint Backlog": [],
    "Done": []
}, show_labels=True, show_estimates=False, show_sprints=False)

# 4. Task 6: planning-kanban-done.png
draw_kanban_board("planning-kanban-done.png", {
    "New Issues": [],
    "Product Backlog": [],
    "Sprint Backlog": [1, 2, 3, 4, 5],
    "In Progress": [],
    "Done": []
}, show_labels=True, show_estimates=True, show_sprints=True)

# 5. Task 8: rest-techdebt-done.png
draw_kanban_board("rest-techdebt-done.png", {
    "Product Backlog": [],
    "Sprint Backlog": [2, 3, 4, 5],
    "In Progress": [],
    "Review": [],
    "Done": [1]
}, show_labels=True, show_estimates=True, show_sprints=True)

# 6. Task 9: read-accounts.png
draw_kanban_board("read-accounts.png", {
    "Product Backlog": [],
    "Sprint Backlog": [3, 4, 5],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2]
}, show_labels=True, show_estimates=True, show_sprints=True)

# 7. Task 10: list-accounts.png
draw_kanban_board("list-accounts.png", {
    "Product Backlog": [],
    "Sprint Backlog": [4, 5],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3]
}, show_labels=True, show_estimates=True, show_sprints=True)

# 8. Task 11: update-accounts.png
draw_kanban_board("update-accounts.png", {
    "Product Backlog": [],
    "Sprint Backlog": [5],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3, 4]
}, show_labels=True, show_estimates=True, show_sprints=True)

# 9. Task 12: delete-accounts.png
draw_kanban_board("delete-accounts.png", {
    "Product Backlog": [],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3, 4, 5]
}, show_labels=True, show_estimates=True, show_sprints=True)

# 10. Task 18: sprint2-plan.png
draw_kanban_board("sprint2-plan.png", {
    "Product Backlog": [],
    "Sprint Backlog": [6, 7],
    "In Progress": [],
    "Review": [],
    "Done": [1, 2, 3, 4, 5]
}, column_counts={"Done": 5}, show_labels=True, show_estimates=True, show_sprints=True)

# 11. Task 20: ci-kanban-done.png (shows card 6 in Done)
draw_kanban_board("ci-kanban-done.png", {
    "Product Backlog": [],
    "Sprint Backlog": [7],
    "In Progress": [],
    "Review": [],
    "Done": [6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 6}, show_labels=True, show_estimates=True, show_sprints=True)

# 12. Task 24: security-kanban-done.png (shows card 7 in Done)
draw_kanban_board("security-kanban-done.png", {
    "Product Backlog": [],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review": [],
    "Done": [7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 7}, show_labels=True, show_estimates=True, show_sprints=True)

# 13. Task 25: sprint3-plan.png
draw_kanban_board("sprint3-plan.png", {
    "Product Backlog": [],
    "Sprint Backlog": [8, 9, 10],
    "In Progress": [],
    "Review": [],
    "Done": [7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 7}, show_labels=True, show_estimates=True, show_sprints=True)

# 14. Task 27: kube-docker-done.png (shows card 8 in Done)
draw_kanban_board("kube-docker-done.png", {
    "Product Backlog": [],
    "Sprint Backlog": [9, 10],
    "In Progress": [],
    "Review": [],
    "Done": [8, 7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 8}, show_labels=True, show_estimates=True, show_sprints=True)

# 15. Task 28: kube-kubernetes-done.png (shows card 9 in Done)
draw_kanban_board("kube-kubernetes-done.png", {
    "Product Backlog": [],
    "Sprint Backlog": [10],
    "In Progress": [],
    "Review": [],
    "Done": [9, 8, 7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 9}, show_labels=True, show_estimates=True, show_sprints=True)

# 16. Task 33: cd-pipeline-done.png (shows card 10 in Done)
draw_kanban_board("cd-pipeline-done.png", {
    "Product Backlog": [],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review": [],
    "Done": [10, 9, 8, 7, 6, 1, 2, 3, 4, 5]
}, column_counts={"Done": 10}, show_labels=True, show_estimates=True, show_sprints=True)
