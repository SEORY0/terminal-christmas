import time
import random
import os
import sys

# 터미널 색상 코드 (ANSI escape codes)
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BROWN = '\033[33m'  

    ORNAMENTS = [RED, BLUE, MAGENTA, CYAN, YELLOW, WHITE]

def hide_cursor():
    sys.stdout.write("\033[?25l")

def show_cursor():
    sys.stdout.write("\033[?25h")

def move_cursor_home():
    sys.stdout.write("\033[H")

def draw_tree(height, width, snowflakes):

    canvas = [[' ' for _ in range(width)] for _ in range(height + 3)]
    
    # 1. 트리 그리기
    tree_width = height * 2 - 1
    start_col = (width - tree_width) // 2
    
    # 별 (꼭대기)
    star_pos = width // 2
    canvas[0][star_pos] = f"{Colors.YELLOW}★{Colors.RESET}"

    # 나무 몸통
    for i in range(1, height):
        row_width = i * 2 + 1
        row_start = star_pos - i
        
        for j in range(row_width):
            # 80% 확률로 초록 잎, 20% 확률로 알록달록 장식
            if random.random() > 0.2:
                char = "*"
                color = Colors.GREEN
            else:
                char = "o" # 장식 모양
                color = random.choice(Colors.ORNAMENTS)
            
            canvas[i][row_start + j] = f"{color}{char}{Colors.RESET}"

    # 나무 기둥
    trunk_height = 2
    trunk_width = 3
    for i in range(trunk_height):
        for j in range(trunk_width):
            canvas[height + i][star_pos - 1 + j] = f"{Colors.BROWN}#{Colors.RESET}"

    # 2. 눈 내리기 효과 적용
    # 눈송이 위치 업데이트 및 그리기
    new_snowflakes = []
    for x, y in snowflakes:
        # 캔버스 범위 내이고, 트리가 그려진 곳이 아닌 경우(빈 공간)에만 눈을 그림
        if 0 <= y < len(canvas) and 0 <= x < width:
            # 현재 위치에 다른 문자가 없으면(트리가 아니면) 눈 표시
            # 색상 코드가 포함된 문자열 길이를 체크하기 어려우므로 간단히 길이 체크
            if len(canvas[y][x]) == 1: 
                canvas[y][x] = f"{Colors.WHITE}.{Colors.RESET}"
        
        # 눈송이 아래로 이동
        if y < len(canvas) - 1:
            new_snowflakes.append((x, y + 1))
            
    # 새로운 눈송이 생성 (랜덤 위치)
    if random.random() > 0.6: # 눈 내리는 빈도
        new_snowflakes.append((random.randint(0, width - 1), 0))
        
    return canvas, new_snowflakes

def main():
    tree_height = 10  # 트리의 높이 (작고 귀여운 사이즈)
    canvas_width = 40 # 전체 화면 너비
    
    snowflakes = []
    
    # 터미널 화면 깨끗하게 비우기
    os.system('cls' if os.name == 'nt' else 'clear')
    hide_cursor()
    
    print(f"{Colors.YELLOW}🎄 크리스마스 트리를 준비 중입니다... (종료하려면 Ctrl+C) 🎄{Colors.RESET}")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        while True:
            move_cursor_home() # 커서를 맨 위로
            
            # 프레임 생성
            canvas, snowflakes = draw_tree(tree_height, canvas_width, snowflakes)
            
            # 출력
            output = []
            output.append("\n") 
            for row in canvas:
                output.append("".join(row))
            output.append(f"\n      {Colors.RED}Merry Christmas!{Colors.RESET}")
            
            sys.stdout.write("\n".join(output))
            sys.stdout.flush()
            
            time.sleep(0.2) # 애니메이션 속도 조절

    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_cursor()
        print(f"\n{Colors.GREEN}Merry Christmas! 🎅{Colors.RESET}")

if __name__ == "__main__":
    main()