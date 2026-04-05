import pyautogui
from time import sleep

def show_mouse_position():
    while 1:
        x, y = pyautogui.position()
        print(x, y)

def borrow_money():
    pyautogui.press('f')
    pyautogui.moveTo(1520, 766)
    for _ in range(110):
        pyautogui.click()
    pyautogui.moveTo(1707, 262)
    pyautogui.click()
    pyautogui.moveTo(1287, 765)
    pyautogui.click()

def put_drill_rigs():
    y = 893
    x = 197
    step = 136
    for _ in range(16):
        pyautogui.press('r')
        pyautogui.moveTo(x, y)
        pyautogui.click()
        x += step

def build_pipe(move_x, move_y):
    pyautogui.mouseDown()
    pyautogui.moveRel(move_x, move_y)
    pyautogui.mouseUp()

def build_pipe_single(start_x, start_y, step_x, step_y, moves):
    pyautogui.moveTo(start_x, start_y)
    for _ in range(moves):
        build_pipe(step_x, step_y)
        build_pipe(step_x, -step_y)
        pyautogui.moveRel(step_x * 2, 0)

def enhance_pipe_single(start_x, start_y, step_x, step_y, moves):
    sleep(8 // moves)
    pyautogui.moveTo(start_x, start_y)
    pyautogui.moveRel(step_x // 2, step_y // 2)
    for _ in range(moves):
        pyautogui.click()
        pyautogui.moveRel(step_x, 0)
        pyautogui.click()
        pyautogui.moveRel(step_x * 3, 0)

def make_pipe_all(enhance = 0, round = 0):
    start_y = 889
    start_x = 197
    step_x = 68
    step_y = 15
    moves = 8
    for _ in range(3):
        if not enhance:
            build_pipe_single(start_x, start_y, step_x, step_y, moves)
        else:
            enhance_pipe_single(start_x + round * 20, start_y + round * 20, step_x, step_y, moves)
        start_y += step_y
        start_x += step_x
        step_x *= 2
        step_y *= 1
        moves //= 2
    if not enhance:
        build_pipe_single(start_x, start_y, step_x, step_y, moves)
    else:
        enhance_pipe_single(start_x + round * 20, start_y + round * 20, step_x, step_y, moves)

def run_all():
    borrow_money()
    put_drill_rigs()
    make_pipe_all()
    # for _ in range(3):
    #     make_pipe_all(1)

sleep(3)

# show_mouse_position()
run_all()