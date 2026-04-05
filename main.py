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
import json
import logging
import sys
from pathlib import Path
from time import sleep
from typing import Tuple, List, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TurmoilConfig:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_file.exists():
            logger.error(f"配置文件 {self.config_file} 不存在")
            raise FileNotFoundError(f"配置文件 {self.config_file} 不存在")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @property
    def resolution(self) -> Tuple[int, int]:
        return (self.config['resolution']['width'], self.config['resolution']['height'])
    
    @property
    def borrow_config(self) -> Dict[str, Any]:
        return self.config['borrow_money']
    
    @property
    def drill_config(self) -> Dict[str, Any]:
        return self.config['drill_rigs']
    
    @property
    def pipe_config(self) -> Dict[str, Any]:
        return self.config['pipes']
    
    @property
    def delay_config(self) -> Dict[str, Any]:
        return self.config['delays']


class TurmoilBot:
    """Turmoil 游戏自动化机器人"""
    
    def __init__(self, config: TurmoilConfig):
        self.config = config
        self._setup_pyautogui()
    
    def _setup_pyautogui(self):
        """配置 pyautogui 参数"""
        pyautogui.FAILSAFE = True  # 启用故障保护（将鼠标移到左上角可中止）
        pyautogui.PAUSE = 0.1  # 每次操作后暂停 0.1 秒
    
    @staticmethod
    def show_mouse_position():
        """显示鼠标当前位置（调试用）"""
        logger.info("移动鼠标以获取坐标，按 Ctrl+C 退出")
        try:
            while True:
                x, y = pyautogui.position()
                print(f"\r当前坐标: ({x}, {y})", end='', flush=True)
                sleep(0.1)
        except KeyboardInterrupt:
            print()
            logger.info("坐标获取结束")
    
    def click_multiple(self, x: int, y: int, count: int, description: str = ""):
        """多次点击指定位置"""
        desc = f" - {description}" if description else ""
        logger.info(f"点击 ({x}, {y}) {count} 次{desc}")
        pyautogui.moveTo(x, y)
        for _ in range(count):
            pyautogui.click()
    
    def borrow_money(self):
        """自动借贷操作"""
        logger.info("开始执行借贷操作")
        borrow_config = self.config.borrow_config
        
        # 按指定键
        for key in borrow_config.get('keys', []):
            logger.info(f"按键: {key}")
            pyautogui.press(key)
            sleep(0.5)
        
        # 执行点击操作
        for click in borrow_config.get('clicks', []):
            self.click_multiple(click['x'], click['y'], click['count'])
            sleep(0.3)
        
        logger.info("借贷操作完成")
    
    def put_drill_rigs(self):
        """自动放置钻机"""
        logger.info("开始放置钻机")
        drill_config = self.config.drill_config
        
        key = drill_config['key']
        count = drill_config['count']
        x = drill_config['start_x']
        y = drill_config['start_y']
        step = drill_config['step']
        
        for i in range(count):
            logger.info(f"放置第 {i + 1}/{count} 个钻机")
            pyautogui.press(key)
            pyautogui.moveTo(x, y)
            pyautogui.click()
            x += step
            sleep(0.2)
        
        logger.info("钻机放置完成")
    
    def build_pipe(self, move_x: int, move_y: int):
        """建造单段管道"""
        pyautogui.mouseDown()
        pyautogui.moveRel(move_x, move_y)
        pyautogui.mouseUp()
    
    def build_pipe_single(self, start_x: int, start_y: int, step_x: int, step_y: int, moves: int):
        """建造连续管道网络"""
        logger.info(f"建造管道: 起点({start_x}, {start_y}), 步数: {moves}")
        pyautogui.moveTo(start_x, start_y)
        for _ in range(moves):
            self.build_pipe(step_x, step_y)
            self.build_pipe(step_x, -step_y)
            pyautogui.moveRel(step_x * 2, 0)
    
    def enhance_pipe_single(self, start_x: int, start_y: int, step_x: int, step_y: int, moves: int):
        """升级管道"""
        delay = self.config.delay_config['enhance_delay_per_move'] // max(moves, 1)
        sleep(delay)
        
        logger.info(f"升级管道: 起点({start_x}, {start_y}), 步数: {moves}")
        pyautogui.moveTo(start_x, start_y)
        pyautogui.moveRel(step_x // 2, step_y // 2)
        for _ in range(moves):
            pyautogui.click()
            pyautogui.moveRel(step_x, 0)
            pyautogui.click()
            pyautogui.moveRel(step_x * 3, 0)
    
    def make_pipe_all(self, enhance: bool = False, round: int = 0):
        """建造所有管道网络

        Args:
            enhance: 是否为升级模式
            round: 轮次参数，用于调整坐标偏移
        """
        logger.info(f"开始建造管道网络 (升级模式: {enhance}, 轮次: {round})")
        pipe_config = self.config.pipe_config
        
        start_y = pipe_config['start_y']
        start_x = pipe_config['start_x']
        step_x = pipe_config['step_x']
        step_y = pipe_config['step_y']
        moves = pipe_config['initial_moves']
        offset = pipe_config['offset_per_round'] * round
        
        layers = pipe_config['layers']
        for layer in range(layers):
            current_x = start_x + offset
            current_y = start_y + offset
            
            if not enhance:
                self.build_pipe_single(current_x, current_y, step_x, step_y, moves)
            else:
                self.enhance_pipe_single(current_x, current_y, step_x, step_y, moves)
            
            start_y += step_y
            start_x += step_x
            step_x *= 2
            moves //= 2
        
        # 最后一层
        current_x = start_x + offset
        current_y = start_y + offset
        if not enhance:
            self.build_pipe_single(current_x, current_y, step_x, step_y, moves)
        else:
            self.enhance_pipe_single(current_x, current_y, step_x, step_y, moves)
        
        logger.info("管道网络建造完成")
    
    def run_all(self, enhance_pipe: bool = False, rounds: int = 0):
        """执行全部操作流程"""
        logger.info("=" * 50)
        logger.info("开始执行自动化流程")
        logger.info("=" * 50)
        
        try:
            # 1. 借贷
            self.borrow_money()
            sleep(1)
            
            # 2. 放置钻机
            self.put_drill_rigs()
            sleep(1)
            
            # 3. 建造管道
            self.make_pipe_all(enhance=enhance_pipe, round=rounds)
            
            # 4. 可选：管道升级
            if enhance_pipe and rounds > 0:
                for i in range(rounds):
                    logger.info(f"执行第 {i + 1} 轮管道升级")
                    self.make_pipe_all(enhance=True, round=i + 1)
                    sleep(1)
            
            logger.info("=" * 50)
            logger.info("自动化流程执行完成!")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"执行过程中出错: {e}", exc_info=True)
            raise


def main():
    """主函数"""
    print("=" * 50)
    print("Turmoil 自动浪费钱设施脚本")
    print("=" * 50)
    print("请确保:")
    print("1. 游戏已启动并处于窗口模式")
    print("2. 屏幕分辨率为 2560x1440")
    print(f"3. {CONFIG['delays']['start_delay']} 秒后自动开始执行...")
    print()
    
    # 等待指定时间
    sleep(CONFIG['delays']['start_delay'])
    
    try:
        # 加载配置
        turmoil_config = TurmoilConfig()
        
        # 创建机器人实例
        bot = TurmoilBot(turmoil_config)
        
        # 执行所有操作
        bot.run_all()
        
    except KeyboardInterrupt:
        logger.info("\n用户中断执行")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序执行失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    with open("config.json", 'r', encoding='utf-8') as f:
        CONFIG = json.load(f)
    main()