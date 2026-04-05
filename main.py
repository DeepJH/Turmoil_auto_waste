#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turmoil 自动浪费钱设施脚本

功能:
- 自动借贷
- 自动放置钻机
- 自动建造和升级管道

注意: 此脚本仅适用于 2560*1440 分辨率
"""

import pyautogui
from time import sleep

def show_mouse_position():
    """显示鼠标当前位置（调试用）"""
    while 1:
        x, y = pyautogui.position()
        print(x, y)

def borrow_money():
    """自动借贷操作"""
    pyautogui.press('f')
    pyautogui.moveTo(1520, 766)
    for _ in range(110):
        pyautogui.click()
    pyautogui.moveTo(1707, 262)
    pyautogui.click()
    pyautogui.moveTo(1287, 765)
    pyautogui.click()

def put_drill_rigs():
    """自动放置16个钻机"""
    y = 893
    x = 197
    step = 136
    for _ in range(16):
        pyautogui.press('r')
        pyautogui.moveTo(x, y)
        pyautogui.click()
        x += step

def build_pipe(move_x, move_y):
    """建造单段管道"""
    pyautogui.mouseDown()
    pyautogui.moveRel(move_x, move_y)
    pyautogui.mouseUp()

def build_pipe_single(start_x, start_y, step_x, step_y, moves):
    """建造连续管道网络"""
    pyautogui.moveTo(start_x, start_y)
    for _ in range(moves):
        build_pipe(step_x, step_y)
        build_pipe(step_x, -step_y)
        pyautogui.moveRel(step_x * 2, 0)

def enhance_pipe_single(start_x, start_y, step_x, step_y, moves):
    """升级管道"""
    sleep(8 // moves)
    pyautogui.moveTo(start_x, start_y)
    pyautogui.moveRel(step_x // 2, step_y // 2)
    for _ in range(moves):
        pyautogui.click()
        pyautogui.moveRel(step_x, 0)
        pyautogui.click()
        pyautogui.moveRel(step_x * 3, 0)

def make_pipe_all(enhance = 0, round = 0):
    """建造所有管道网络
    
    Args:
        enhance: 是否升级模式 (0=建造, 1=升级)
        round: 轮次参数，用于调整坐标偏移
    """
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
    """执行全部操作流程"""
    borrow_money()
    put_drill_rigs()
    make_pipe_all()
    # for _ in range(3):
    #     make_pipe_all(1)


if __name__ == "__main__":
    print("Turmoil 自动浪费钱设施脚本")
    print("=" * 40)
    print("请确保:")
    print("1. 游戏已启动并处于窗口模式")
    print("2. 屏幕分辨率为 2560x1440")
    print("3. 3秒后自动开始执行...")
    print()
    
    sleep(3)
    
    # show_mouse_position()  # 取消注释以调试获取坐标
    run_all()
    
    print("\n执行完成!")