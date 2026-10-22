import pygame
import time
import random
import sys
import os
from pygame.math import Vector2

# --- XÁC ĐỊNH THƯ MỤC GỐC CHỨA FILE CODE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPHICS_DIR = os.path.join(BASE_DIR, 'Graphics')
SOUND_DIR = os.path.join(BASE_DIR, 'Sound') 

# Khởi động pygame và hệ thống âm thanh
pygame.init()
pygame.mixer.init() 

# --- KHAI BÁO ĐƯỜNG DẪN NHẠC NỀN VÀ ÂM THANH ---

MENU_BGM = os.path.join(SOUND_DIR, "menu.wav")     
EASY_BGM = os.path.join(SOUND_DIR, "ez_mode.wav")     
NORMAL_BGM = os.path.join(SOUND_DIR, "nomal_mode.wav")   
HARD_BGM = os.path.join(SOUND_DIR, "hard_mode.mp3")     
GAME_OVER_SOUND = os.path.join(SOUND_DIR, "smal_explosion.wav") 

EAT_APPLE_SOUND = os.path.join(SOUND_DIR, "crunch.wav")  
EAT_ITEM_SOUND = os.path.join(SOUND_DIR, "power_up.wav")   

SELECT_MODE_SOUND = os.path.join(SOUND_DIR, "beep.wav") 
WALL_BREAK_SOUND = os.path.join(SOUND_DIR, "mecha_explosion.wav") 

# Khởi tạo đối tượng âm thanh Game Over
game_over_sfx = None
if GAME_OVER_SOUND and os.path.exists(GAME_OVER_SOUND):
    try:
        game_over_sfx = pygame.mixer.Sound(GAME_OVER_SOUND)
        game_over_sfx.set_volume(0.8) 
    except Exception as e:
        print(f"Warning: Không thể tải âm thanh game over. Lỗi: {e}")

# Khởi tạo đối tượng âm thanh Ăn Táo
eat_apple_sfx = None
if EAT_APPLE_SOUND and os.path.exists(EAT_APPLE_SOUND):
    try:
        eat_apple_sfx = pygame.mixer.Sound(EAT_APPLE_SOUND)
        eat_apple_sfx.set_volume(0.8) 
    except Exception as e:
        print(f"Warning: Không thể tải âm thanh ăn táo. Lỗi: {e}")

# Khởi tạo đối tượng âm thanh Ăn Vật Phẩm
eat_item_sfx = None
if EAT_ITEM_SOUND and os.path.exists(EAT_ITEM_SOUND):
    try:
        eat_item_sfx = pygame.mixer.Sound(EAT_ITEM_SOUND)
        eat_item_sfx.set_volume(0.8) 
    except Exception as e:
        print(f"Warning: Không thể tải âm thanh ăn vật phẩm. Lỗi: {e}")

# Khởi tạo đối tượng âm thanh Chọn Mode
select_mode_sfx = None
if SELECT_MODE_SOUND and os.path.exists(SELECT_MODE_SOUND):
    try:
        select_mode_sfx = pygame.mixer.Sound(SELECT_MODE_SOUND)
        select_mode_sfx.set_volume(0.8) 
    except Exception as e:
        print(f"Warning: Không thể tải âm thanh chọn mode. Lỗi: {e}")

# Khởi tạo đối tượng âm thanh Phá Tường
wall_break_sfx = None
if WALL_BREAK_SOUND and os.path.exists(WALL_BREAK_SOUND):
    try:
        wall_break_sfx = pygame.mixer.Sound(WALL_BREAK_SOUND)
        wall_break_sfx.set_volume(0.8) 
    except Exception as e:
        print(f"Warning: Không thể tải âm thanh phá tường. Lỗi: {e}")


# Hàm hỗ trợ phát nhạc nền
def play_bgm(bgm_path):
    if bgm_path and os.path.exists(bgm_path):
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.set_volume(0.8) 
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Warning: Không thể phát nhạc nền. Lỗi: {e}")
    else:
        pygame.mixer.music.stop()

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
DARK_PANEL = (30, 40, 60)
GHOST_SNAKE = (150, 255, 200) 
DARK_GREEN = (34, 139, 34) 
PORTAL_COLOR1 = (138, 43, 226) 
PORTAL_COLOR2 = (0, 255, 255)  
POISON_COLOR = (255, 0, 255) 

# Mảng màu nền thay đổi theo Level
LEVEL_BGS = [
    (50, 153, 213), (40, 110, 160), (60, 80, 130), 
    (80, 50, 100), (100, 40, 60), (40, 40, 40)
]

# Kích thước màn hình
TOTAL_WIDTH = 1300
HEIGHT = 720
GAME_WIDTH = 1000 

screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
pygame.display.set_caption('Ultimate Snake Game - Boss Level & Breaker Item')
clock = pygame.time.Clock()

# Fonts chữ
font_style = pygame.font.SysFont("bahnschrift", 40)
score_font = pygame.font.SysFont("comicsansms", 40)
panel_title_font = pygame.font.SysFont("bahnschrift", 30)
timer_font = pygame.font.SysFont("bahnschrift", 22) 
menu_font = pygame.font.SysFont("bahnschrift", 35)

# --- LOAD ĐỒ HỌA ---
try:
    head_up = pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_up.png')).convert_alpha()
    head_down = pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_down.png')).convert_alpha()
    head_right = pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_right.png')).convert_alpha()
    head_left = pygame.image.load(os.path.join(GRAPHICS_DIR, 'head_left.png')).convert_alpha()
    
    tail_up = pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_up.png')).convert_alpha()
    tail_down = pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_down.png')).convert_alpha()
    tail_right = pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_right.png')).convert_alpha()
    tail_left = pygame.image.load(os.path.join(GRAPHICS_DIR, 'tail_left.png')).convert_alpha()

    body_vertical = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_vertical.png')).convert_alpha()
    body_horizontal = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_horizontal.png')).convert_alpha()

    body_tr = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_tr.png')).convert_alpha()
    body_tl = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_tl.png')).convert_alpha()
    body_br = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_br.png')).convert_alpha()
    body_bl = pygame.image.load(os.path.join(GRAPHICS_DIR, 'body_bl.png')).convert_alpha()
    
    apple_img = pygame.image.load(os.path.join(GRAPHICS_DIR, 'apple.png')).convert_alpha()
    
    poison_apple_img = apple_img.copy()
    poison_apple_img.fill((0, 0, 255), special_flags=pygame.BLEND_RGB_ADD)
    
    SNAKE_IMAGES_LOADED = True
except:
    print("Warning: Graphics not loaded successfully. Running in fallback mode.")
    SNAKE_IMAGES_LOADED = False 

def show_score_level(score, level):
    val_score = score_font.render(f"Score: {score}", True, YELLOW)
    val_level = score_font.render(f"Level: {level}", True, WHITE)
    screen.blit(val_score, [10, 10])
    screen.blit(val_level, [10, 60])

def update_head_graphics(snake_list, snake_block):
    if len(snake_list) < 2:
        return head_up 
    
    head = Vector2(snake_list[0][0], snake_list[0][1])
    second = Vector2(snake_list[1][0], snake_list[1][1])
    head_relation = (second - head) / snake_block
    
    if head_relation == Vector2(1, 0): return head_left
    elif head_relation == Vector2(-1, 0): return head_right
    elif head_relation == Vector2(0, 1): return head_up
    elif head_relation == Vector2(0, -1): return head_down
    return head_up

def update_tail_graphics(snake_list, snake_block):
    if len(snake_list) < 2:
        return tail_up
        
    tail = Vector2(snake_list[-1][0], snake_list[-1][1])
    before_tail = Vector2(snake_list[-2][0], snake_list[-2][1])
    tail_relation = (before_tail - tail) / snake_block
    
    if tail_relation == Vector2(1, 0): return tail_left
    elif tail_relation == Vector2(-1, 0): return tail_right
    elif tail_relation == Vector2(0, 1): return tail_up
    elif tail_relation == Vector2(0, -1): return tail_down
    return tail_up

def draw_snake(snake_block, snake_list, is_ghost, is_breaker):
    if is_ghost or is_breaker:
        if (pygame.time.get_ticks() // 150) % 2 == 0:
            color = GHOST_SNAKE if is_ghost else ORANGE
            for x in snake_list:
                pygame.draw.rect(screen, color, [x[0], x[1], snake_block, snake_block])
                pygame.draw.rect(screen, BLACK, [x[0], x[1], snake_block, snake_block], 1)
            return 

    if not SNAKE_IMAGES_LOADED:
        color = GREEN
        for x in snake_list:
            pygame.draw.rect(screen, color, [x[0], x[1], snake_block, snake_block])
            pygame.draw.rect(screen, BLACK, [x[0], x[1], snake_block, snake_block], 1)
        return

    def scale_img(img):
        return pygame.transform.scale(img, (int(snake_block), int(snake_block)))

    current_head = scale_img(update_head_graphics(snake_list, snake_block))
    current_tail = scale_img(update_tail_graphics(snake_list, snake_block))
    b_vert = scale_img(body_vertical)
    b_horiz = scale_img(body_horizontal)
    b_tr = scale_img(body_tr)
    b_tl = scale_img(body_tl)
    b_br = scale_img(body_br)
    b_bl = scale_img(body_bl)

    for index, block in enumerate(snake_list):
        x_pos = int(block[0])
        y_pos = int(block[1])
        block_rect = pygame.Rect(x_pos, y_pos, snake_block, snake_block)

        if index == 0:
            screen.blit(current_head, block_rect)
        elif index == len(snake_list) - 1:
            screen.blit(current_tail, block_rect)
        else:
            previous_block = Vector2(snake_list[index + 1][0], snake_list[index + 1][1]) - Vector2(block[0], block[1])
            previous_block = Vector2(previous_block.x / snake_block, previous_block.y / snake_block)
            
            next_block = Vector2(snake_list[index - 1][0], snake_list[index - 1][1]) - Vector2(block[0], block[1])
            next_block = Vector2(next_block.x / snake_block, next_block.y / snake_block)

            if previous_block.x == next_block.x:
                screen.blit(b_vert, block_rect)
            elif previous_block.y == next_block.y:
                screen.blit(b_horiz, block_rect)
            else:
                if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                    screen.blit(b_tl, block_rect)
                elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                    screen.blit(b_bl, block_rect)
                elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                    screen.blit(b_tr, block_rect)
                elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                    screen.blit(b_br, block_rect)

def draw_walls(snake_block, wall_clusters, snake_head=None):
    for cluster in wall_clusters:
        is_invisible = cluster.get('invisible', False)
        show_cluster = not is_invisible
        
        # Nếu tường có thuộc tính tàng hình, kiểm tra khoảng cách đến đầu rắn
        if is_invisible and snake_head:
            for b in cluster['blocks']:
                # Tính khoảng cách theo số ô (Chebyshev distance)
                dist_x = abs(snake_head[0] - b[0])
                dist_y = abs(snake_head[1] - b[1])
                
                # Nếu có bất kỳ block nào của cụm tường lọt vào phạm vi 4 ô
                if max(dist_x, dist_y) <= 4 * snake_block:
                    show_cluster = True
                    break
                    
        # Chỉ vẽ tường nếu nó không tàng hình hoặc rắn đã ở đủ gần
        if show_cluster:
            for b in cluster['blocks']:
                pygame.draw.rect(screen, BROWN, [b[0], b[1], snake_block, snake_block])
                pygame.draw.rect(screen, BLACK, [b[0], b[1], snake_block, snake_block], 1)

def draw_apple(x, y, block):
    if SNAKE_IMAGES_LOADED:
        scaled_apple = pygame.transform.scale(apple_img, (int(block), int(block)))
        screen.blit(scaled_apple, (x, y))
    else:
        center_x, center_y = x + block // 2, y + block // 2
        pygame.draw.circle(screen, RED, (center_x, center_y), block // 2)
        pygame.draw.rect(screen, DARK_GREEN, [x + block // 2 - 2, y - max(1, block//4), 4, block // 2])

def draw_poison_apple(x, y, block):
    if SNAKE_IMAGES_LOADED:
        scaled_poison = pygame.transform.scale(poison_apple_img, (int(block), int(block)))
        screen.blit(scaled_poison, (x, y))
    else:
        center_x, center_y = x + block // 2, y + block // 2
        pygame.draw.circle(screen, POISON_COLOR, (center_x, center_y), block // 2)
        pygame.draw.rect(screen, DARK_GREEN, [x + block // 2 - 2, y - max(1, block//4), 4, block // 2])

def draw_white_item(x, y, block):
    center_x, center_y = x + block // 2, y + block // 2
    pygame.draw.circle(screen, WHITE, (center_x, center_y), block // 2 - 1)
    pygame.draw.circle(screen, BLUE, (center_x, center_y), max(1, block // 2 - 5))

def draw_portal(x, y, block):
    center_x, center_y = x + block // 2, y + block // 2
    pygame.draw.circle(screen, PORTAL_COLOR1, (center_x, center_y), block // 2)
    pygame.draw.circle(screen, PORTAL_COLOR2, (center_x, center_y), max(2, block // 2 - 3))

def draw_breaker_item(x, y, block):
    cx, cy = x + block // 2, y + block // 2
    pygame.draw.polygon(screen, ORANGE, [(cx, y), (x + block, cy), (cx, y + block), (x, cy)])
    pygame.draw.circle(screen, YELLOW, (cx, cy), max(2, block // 4))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [GAME_WIDTH / 10, HEIGHT / 3])

def get_valid_coord(snake_block, width, height, occupied_positions):
    while True:
        x = round(random.randrange(0, width - snake_block) / float(snake_block)) * float(snake_block)
        y = round(random.randrange(0, height - snake_block) / float(snake_block)) * float(snake_block)
        if [x, y] not in occupied_positions:
            return x, y

def generate_wall_clusters(num_clusters, snake_block, width, height, exclude_area, current_walls=[], min_len=2, max_len=4):
    clusters = []
    existing_blocks = [b for c in current_walls for b in c['blocks']] 
    
    for _ in range(num_clusters):
        wall_length = random.randint(min_len, max_len)
        direction_build = random.randint(0, 1)
        
        while True:
            start_x = round(random.randrange(0, width - snake_block * wall_length) / float(snake_block)) * float(snake_block)
            start_y = round(random.randrange(0, height - snake_block * wall_length) / float(snake_block)) * float(snake_block)
            
            if (abs(start_x - exclude_area[0]) > snake_block * 5) or (abs(start_y - exclude_area[1]) > snake_block * 5):
                temp_walls = []
                conflict = False
                for i in range(wall_length):
                    if direction_build == 0:
                        current_x, current_y = start_x + (i * snake_block), start_y
                    else:
                        current_x, current_y = start_x, start_y + (i * snake_block)
                    
                    if [current_x, current_y] in existing_blocks:
                        conflict = True
                        break
                    temp_walls.append([current_x, current_y])
                
                if not conflict:
                    move_axis = 'x' if random.randint(0, 1) == 0 else 'y'
                    move_dir = 1 if random.randint(0, 1) == 0 else -1
                    clusters.append({'blocks': temp_walls, 'axis': move_axis, 'dir': move_dir})
                    existing_blocks.extend(temp_walls)
                    break
    return clusters

def get_all_wall_blocks(clusters):
    return [block for cluster in clusters for block in cluster['blocks']]

def draw_ui_panel(current_speed, ghost_mode, time_left_ghost, breaker_mode, time_left_breaker, mode, level, player_name):
    ui_x = GAME_WIDTH
    ui_y = 0
    
    pygame.draw.rect(screen, DARK_PANEL, [ui_x, ui_y, TOTAL_WIDTH - GAME_WIDTH, HEIGHT])
    pygame.draw.line(screen, WHITE, (GAME_WIDTH, 0), (GAME_WIDTH, HEIGHT), 3)

    title = panel_title_font.render(f"MODE: {mode}", True, YELLOW)
    screen.blit(title, [ui_x + 20, 20])
    
    name_txt = timer_font.render(f"PLAYER: {player_name}", True, GREEN)
    screen.blit(name_txt, [ui_x + 20, 55])

    draw_y = 90
    LEGEND_BLOCK = 20

    draw_apple(ui_x + 20, draw_y, LEGEND_BLOCK) 
    screen.blit(timer_font.render("Food (+1 Pts)", True, WHITE), [ui_x + 50, draw_y - 2])

    if mode != 'EASY':
        draw_y += 35
        pygame.draw.rect(screen, BROWN, [ui_x + 20, draw_y, LEGEND_BLOCK, LEGEND_BLOCK])
        screen.blit(timer_font.render("Moving Wall (Obstacle)", True, WHITE), [ui_x + 50, draw_y - 2])

    if mode == 'HARD':
        draw_y += 35
        draw_poison_apple(ui_x + 20, draw_y, LEGEND_BLOCK)
        screen.blit(timer_font.render("Purple Apple (Speed -2)", True, POISON_COLOR), [ui_x + 50, draw_y - 2])

        draw_y += 35
        draw_white_item(ui_x + 20, draw_y, LEGEND_BLOCK)
        screen.blit(timer_font.render("Orb (Ghost Mode)", True, WHITE), [ui_x + 50, draw_y - 2])

        draw_y += 35
        draw_portal(ui_x + 20, draw_y, LEGEND_BLOCK)
        screen.blit(timer_font.render("Portal (Teleport)", True, WHITE), [ui_x + 50, draw_y - 2])

        draw_y += 35
        draw_breaker_item(ui_x + 20, draw_y, LEGEND_BLOCK)
        screen.blit(timer_font.render("Diamond (Destroy Wall)", True, WHITE), [ui_x + 50, draw_y - 2])

    pygame.draw.line(screen, WHITE, (GAME_WIDTH + 20, draw_y + 40), (TOTAL_WIDTH - 20, draw_y + 40), 1)
    
    screen.blit(timer_font.render(f"SPEED: {current_speed}", True, YELLOW), [ui_x + 20, draw_y + 60])
    screen.blit(timer_font.render(f"LEVEL: {level}", True, PORTAL_COLOR2), [ui_x + 20, draw_y + 90])

    if ghost_mode:
        screen.blit(timer_font.render(f"GHOST MODE: {time_left_ghost}s", True, GHOST_SNAKE), [ui_x + 20, draw_y + 130])
    
    if breaker_mode:
        screen.blit(timer_font.render(f"BREAKER MODE: {time_left_breaker}s", True, ORANGE), [ui_x + 20, draw_y + 160])


def gameLoop(mode, player_name):
    # --- THÊM DANH SÁCH NHẠC VÀ BIẾN THEO DÕI ---
    bgm_list = [EASY_BGM, NORMAL_BGM, HARD_BGM]
    current_bgm = None
    # --------------------------------------------

    if mode == 'EASY':
        snake_block = 40; base_speed = 9; base_walls = 0; items_enabled = False
        current_bgm = EASY_BGM
        play_bgm(current_bgm)
    elif mode == 'NORMAL':
        snake_block = 40; base_speed = 11; base_walls = 6; items_enabled = False
        current_bgm = NORMAL_BGM
        play_bgm(current_bgm)
    elif mode == 'HARD':
        snake_block = 20; base_speed = 12; base_walls = 12; items_enabled = True
        current_bgm = HARD_BGM
        play_bgm(current_bgm)

    game_over = False; game_close = False
    x1 = round(GAME_WIDTH / 2 / float(snake_block)) * float(snake_block)
    y1 = round(HEIGHT / 2 / float(snake_block)) * float(snake_block)
    x1_change, y1_change = 0, 0
    
    snake_list = [
        [x1, y1], 
        [x1 - snake_block, y1], 
        [x1 - (2 * snake_block), y1]
    ]
    length_of_snake = 3
    level = 1
    current_speed = base_speed
    
    wall_clusters = generate_wall_clusters(base_walls, snake_block, GAME_WIDTH, HEIGHT, (x1, y1))
    
    # THÊM MỚI: Chọn ngẫu nhiên 1-3 bức tường làm tường tàng hình ở chế độ HARD
    if mode == 'HARD' and len(wall_clusters) > 0:
        num_invisible = random.randint(1, min(3, len(wall_clusters)))
        for cluster in random.sample(wall_clusters, num_invisible):
            cluster['invisible'] = True
            
    wall_move_timer = 0

    apple_active = False; apple_x, apple_y = -100, -100
    white_active = False; white_x, white_y = -100, -100
    portal_active = False; portal_x, portal_y = -100, -100
    breaker_item_active = False; breaker_x, breaker_y = -100, -100

    ghost_mode = False; ghost_start_time = 0; time_left_ghost = 0
    breaker_mode = False; breaker_start_time = 0; time_left_breaker = 0

    played_game_over_sound = False 

    flat_walls = get_all_wall_blocks(wall_clusters)
    occupied = flat_walls + snake_list
    foodx, foody = get_valid_coord(snake_block, GAME_WIDTH, HEIGHT, occupied)

    while not game_over:
        bg_color_index = min(level - 1, len(LEVEL_BGS) - 1)
        current_bg = LEVEL_BGS[bg_color_index]

        while game_close:
            
            if not played_game_over_sound:
                pygame.mixer.music.stop() 
                if game_over_sfx:
                    game_over_sfx.play() 
                played_game_over_sound = True 

            screen.fill(current_bg)
            draw_ui_panel(current_speed, ghost_mode, time_left_ghost, breaker_mode, time_left_breaker, mode, level, player_name)
            message("GAME OVER! C: Again | M: Menu | Q: Quit", RED)
            show_score_level(length_of_snake - 3, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if event.key == pygame.K_c:
                        gameLoop(mode, player_name)
                    if event.key == pygame.K_m:
                        show_menu(player_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    if [x1 - snake_block, y1] != snake_list[1]:
                        x1_change = -snake_block; y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    if [x1 + snake_block, y1] != snake_list[1]:
                        x1_change = snake_block; y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    if [x1, y1 - snake_block] != snake_list[1]:
                        y1_change = -snake_block; x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    if [x1, y1 + snake_block] != snake_list[1]:
                        y1_change = snake_block; x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if level >= 2 and mode != 'EASY':
            wall_move_timer += 1
            threshold = max(2, 10 - (level - 2) * 2) 
            if wall_move_timer >= threshold:
                wall_move_timer = 0
                for cluster in wall_clusters:
                    hit_bound = False
                    for b in cluster['blocks']:
                        nx = b[0] + (snake_block * cluster['dir'] if cluster['axis'] == 'x' else 0)
                        ny = b[1] + (snake_block * cluster['dir'] if cluster['axis'] == 'y' else 0)
                        if nx < 0 or nx >= GAME_WIDTH or ny < 0 or ny >= HEIGHT:
                            hit_bound = True; break
                    
                    if hit_bound: cluster['dir'] *= -1
                    else:
                        for b in cluster['blocks']:
                            if cluster['axis'] == 'x': b[0] += snake_block * cluster['dir']
                            if cluster['axis'] == 'y': b[1] += snake_block * cluster['dir']
                flat_walls = get_all_wall_blocks(wall_clusters)

        if ghost_mode:
            time_left_ghost = 10 - int(time.time() - ghost_start_time)
            if time_left_ghost <= 0: ghost_mode = False 
            
        if breaker_mode:
            time_left_breaker = 10 - int(time.time() - breaker_start_time)
            if time_left_breaker <= 0: breaker_mode = False 

        # Kiểm tra ăn cổng dịch chuyển
        if items_enabled and portal_active and x1 == portal_x and y1 == portal_y:
            if eat_item_sfx:                   
                eat_item_sfx.play()
            x1, y1 = foodx, foody
            portal_active = False

        if ghost_mode:
            if x1 >= GAME_WIDTH: x1 = 0
            elif x1 < 0: x1 = GAME_WIDTH - snake_block
            if y1 >= HEIGHT: y1 = 0
            elif y1 < 0: y1 = HEIGHT - snake_block
        else:
            if x1 >= GAME_WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
                game_close = True

        snake_head = [x1, y1]
        hit_cluster_idx = -1
        for idx, cluster in enumerate(wall_clusters):
            if snake_head in cluster['blocks']:
                hit_cluster_idx = idx
                break

        if hit_cluster_idx != -1:
            if breaker_mode:
                # --- PHÁT ÂM THANH KHI PHÁ TƯỜNG ---
                if wall_break_sfx:
                    wall_break_sfx.play()
                    
                wall_clusters.pop(hit_cluster_idx)
                flat_walls = get_all_wall_blocks(wall_clusters)
            elif not ghost_mode:
                game_close = True

        screen.fill(current_bg)
        
        occupied = flat_walls + snake_list + [[foodx, foody]]
        if apple_active: occupied.append([apple_x, apple_y])
        if white_active: occupied.append([white_x, white_y])
        if portal_active: occupied.append([portal_x, portal_y])
        if breaker_item_active: occupied.append([breaker_x, breaker_y])

        # SỬA: Cập nhật hàm vẽ tường để truyền thêm snake_head
        draw_walls(snake_block, wall_clusters, snake_head)
        draw_apple(foodx, foody, snake_block)
        
        if items_enabled:
            if apple_active: draw_poison_apple(apple_x, apple_y, snake_block)
            if white_active: draw_white_item(white_x, white_y, snake_block)
            if portal_active: draw_portal(portal_x, portal_y, snake_block)
            if breaker_item_active: draw_breaker_item(breaker_x, breaker_y, snake_block)

        if x1_change != 0 or y1_change != 0:
            snake_list.insert(0, snake_head)
            # Rắn ăn được thức ăn (Táo thường)
            if x1 == foodx and y1 == foody:
                if eat_apple_sfx:              
                    eat_apple_sfx.play()
                
                length_of_snake += 1
                score = length_of_snake - 3
                foodx, foody = get_valid_coord(snake_block, GAME_WIDTH, HEIGHT, occupied)
                
                new_level = (score // 10) + 1
                if new_level > level:
                    level = new_level
                    current_speed = base_speed + (level * 1.5) 
                    
                    # --- CHUYỂN NHẠC KHI TĂNG LEVEL ---
                    available_bgms = [bgm for bgm in bgm_list if bgm != current_bgm]
                    current_bgm = random.choice(available_bgms)
                    play_bgm(current_bgm)
                    # -----------------------------------
                    
                    if mode != 'EASY':
                        min_w, max_w = (4, 6) if (mode == 'HARD' and level >= 20) else (2, 4)
                        new_walls = generate_wall_clusters(2, snake_block, GAME_WIDTH, HEIGHT, (x1, y1), wall_clusters, min_len=min_w, max_len=max_w)
                        
                        # THÊM MỚI: Tường mới sinh ra trong HARD mode có 30% tỷ lệ bị tàng hình
                        if mode == 'HARD':
                            for nw in new_walls:
                                if random.random() < 0.3:
                                    nw['invisible'] = True
                                    
                        wall_clusters.extend(new_walls)
                        flat_walls = get_all_wall_blocks(wall_clusters)

                if mode == 'HARD' and level >= 20 and score % 3 == 0:
                    new_walls = generate_wall_clusters(1, snake_block, GAME_WIDTH, HEIGHT, (x1, y1), wall_clusters, min_len=4, max_len=6)
                    
                    # THÊM MỚI: Tường mới sinh ra trong HARD mode có 30% tỷ lệ bị tàng hình
                    for nw in new_walls:
                        if random.random() < 0.3:
                            nw['invisible'] = True
                            
                    wall_clusters.extend(new_walls)
                    flat_walls = get_all_wall_blocks(wall_clusters)

                if items_enabled:
                    if score in [10, 30, 60, 90] and not apple_active:
                        apple_x, apple_y = get_valid_coord(snake_block, GAME_WIDTH, HEIGHT, occupied)
                        apple_active = True
                    if score >= 5 and (score - 5) % 10 == 0 and not white_active and not ghost_mode:
                        white_x, white_y = get_valid_coord(snake_block, GAME_WIDTH, HEIGHT, occupied)
                        white_active = True
                    if score > 0 and random.random() < 0.25 and not portal_active:
                        portal_x, portal_y = get_valid_coord(snake_block, GAME_WIDTH, HEIGHT, occupied)
                        portal_active = True
                    if score > 0 and random.random() < 0.25 and not breaker_item_active:
                        breaker_x, breaker_y = get_valid_coord(snake_block, GAME_WIDTH, HEIGHT, occupied)
                        breaker_item_active = True
            else:
                snake_list.pop()

        if not ghost_mode and (x1_change != 0 or y1_change != 0):
            for x in snake_list[1:]:
                if x == snake_head:
                    game_close = True

        draw_snake(snake_block, snake_list, ghost_mode, breaker_mode)
        
        score = length_of_snake - 3
        show_score_level(score, level)
        draw_ui_panel(current_speed, ghost_mode, time_left_ghost, breaker_mode, time_left_breaker, mode, level, player_name)
        pygame.display.update()

        # Kiểm tra ăn các vật phẩm khác
        if items_enabled:
            if apple_active and x1 == apple_x and y1 == apple_y:
                if eat_item_sfx: eat_item_sfx.play()  
                current_speed = max(6, current_speed - 2)
                apple_active = False
            if white_active and x1 == white_x and y1 == white_y:
                if eat_item_sfx: eat_item_sfx.play()  
                ghost_mode = True; ghost_start_time = time.time()
                white_active = False
            if breaker_item_active and x1 == breaker_x and y1 == breaker_y:
                if eat_item_sfx: eat_item_sfx.play()  
                breaker_mode = True; breaker_start_time = time.time()
                breaker_item_active = False

        clock.tick(current_speed)

def get_player_name():
    name = ""
    input_active = True
    while input_active:
        screen.fill(DARK_PANEL)
        title = score_font.render("WELCOME TO ULTIMATE SNAKE", True, YELLOW)
        screen.blit(title, [TOTAL_WIDTH // 2 - 300, HEIGHT // 4 - 50])
        prompt = panel_title_font.render("Enter your name:", True, WHITE)
        screen.blit(prompt, [TOTAL_WIDTH // 2 - 120, HEIGHT // 2 - 60])
        
        pygame.draw.rect(screen, WHITE, [TOTAL_WIDTH // 2 - 150, HEIGHT // 2, 300, 50], 2)
        name_surface = menu_font.render(name, True, GREEN)
        screen.blit(name_surface, [TOTAL_WIDTH // 2 - 140, HEIGHT // 2 + 5])
        
        inst = timer_font.render("Press ENTER to continue", True, BLUE)
        screen.blit(inst, [TOTAL_WIDTH // 2 - 110, HEIGHT // 2 + 70])
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "": name = "Guest"
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode
    return name

def show_menu(player_name):
    play_bgm(MENU_BGM)

    menu = True
    try:
        bg_image_path = os.path.join(BASE_DIR, "snakebackground.jpg")
        bg_image = pygame.image.load(bg_image_path)
        bg_image = pygame.transform.scale(bg_image, (TOTAL_WIDTH, HEIGHT))
    except:
        bg_image = pygame.Surface((TOTAL_WIDTH, HEIGHT))
        bg_image.fill(DARK_PANEL)

    overlay = pygame.Surface((TOTAL_WIDTH, HEIGHT))
    overlay.set_alpha(160) 
    overlay.fill(BLACK)

    while menu:
        screen.blit(bg_image, (0, 0))
        screen.blit(overlay, (0, 0))
        
        title = score_font.render("ULTIMATE SNAKE GAME", True, YELLOW)
        screen.blit(title, [TOTAL_WIDTH // 2 - 220, HEIGHT // 4 - 50])
        
        greeting = timer_font.render(f"Ready, {player_name}? Select your difficulty:", True, WHITE)
        screen.blit(greeting, [TOTAL_WIDTH // 2 - 170, HEIGHT // 4 + 30])

        easy_txt = menu_font.render("Press 1 : CLASSIC MODE   (Speed 9, No Obstacles)", True, GREEN)
        norm_txt = menu_font.render("Press 2 : TACTICIAN MODE (Speed 11, Moving Walls, Levels)", True, BLUE)
        hard_txt = menu_font.render("Press 3 : LEGEND MODE   (Giant Map, Magic Items & Breaker)", True, RED)

        screen.blit(easy_txt, [TOTAL_WIDTH // 2 - 380, HEIGHT // 2 - 20])
        screen.blit(norm_txt, [TOTAL_WIDTH // 2 - 380, HEIGHT // 2 + 40])
        screen.blit(hard_txt, [TOTAL_WIDTH // 2 - 380, HEIGHT // 2 + 100])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    if select_mode_sfx:
                        select_mode_sfx.play()

                if event.key == pygame.K_1: gameLoop('EASY', player_name)
                if event.key == pygame.K_2: gameLoop('NORMAL', player_name)
                if event.key == pygame.K_3: gameLoop('HARD', player_name)

current_player = get_player_name()
show_menu(current_player)