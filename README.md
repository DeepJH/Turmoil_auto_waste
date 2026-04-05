# Turmoil 自动浪费钱设施脚本

> 为 [Turmoil](https://store.steampowered.com/app/361280/Turmoil/) 游戏设计的自动化脚本，用于快速搭建浪费钱的设施。

<video src="./demo.mp4" width="100%" controls>
  您的浏览器不支持 video 标签。
</video>

## ⚠️ 免责声明

此脚本仅用于学习和个人娱乐目的。使用此脚本可能违反游戏规则，请在使用前了解相关规则并自行承担风险。

## 📋 功能特性

- 💰 自动借贷功能
- 🔧 自动放置钻机
- 🛠️ 自动建造和升级管道
- ⚡ 一键执行所有操作
- 📝 完善的日志输出
- ⚙️ 灵活的配置管理
- 🛡️ 故障安全保护

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Windows 操作系统
- 游戏 Turmoil（以窗口模式运行）

### 安装

1. 克隆或下载本项目

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 🎮 使用方法

### 准备工作

1. 启动 Turmoil 游戏
2. 确保游戏窗口处于**窗口模式**（非全屏）
3. 确保屏幕分辨率为 **2560*1440**（脚本使用硬编码坐标）

### 运行脚本

```bash
python main.py
```

运行后脚本会根据 `config.json` 中的配置等待指定时间后自动执行，请及时切换到游戏窗口。

### 执行流程

脚本将自动完成以下操作：

1. **借贷** (`borrow_money`)
   - 按 `F` 键打开借贷界面
   - 自动点击完成借贷操作

2. **放置钻机** (`put_drill_rigs`)
   - 按 `R` 键选择钻机
   - 在预设位置自动放置 16 个钻机

3. **建造管道** (`make_pipe_all`)
   - 自动建造多层管道网络
   - 支持管道升级功能

## ⚙️ 配置说明

所有配置项都在 `config.json` 文件中：

```json
{
    "resolution": {
        "width": 2560,
        "height": 1440
    },
    "borrow_money": {
        "keys": ["f"],
        "clicks": [
            {"x": 1520, "y": 766, "count": 110},
            {"x": 1707, "y": 262, "count": 1},
            {"x": 1287, "y": 765, "count": 1}
        ]
    },
    "drill_rigs": {
        "key": "r",
        "count": 16,
        "start_x": 197,
        "start_y": 893,
        "step": 136
    },
    "pipes": {
        "layers": 3,
        "start_x": 197,
        "start_y": 889,
        "step_x": 68,
        "step_y": 15,
        "initial_moves": 8,
        "offset_per_round": 20
    },
    "delays": {
        "start_delay": 3,
        "enhance_delay_per_move": 8
    }
}
```

### 主要配置项

| 配置项 | 说明 |
|--------|------|
| `resolution` | 屏幕分辨率设置 |
| `borrow_money` | 借贷相关配置（按键和点击坐标） |
| `drill_rigs` | 钻机放置配置（起始位置、数量、间距） |
| `pipes` | 管道建造配置（层数、步长、移动次数） |
| `delays` | 延迟设置（启动延迟、升级延迟） |

### 调试模式

运行以下命令可以获取鼠标实时坐标：

```python
from main import TurmoilConfig, TurmoilBot

config = TurmoilConfig()
bot = TurmoilBot(config)
bot.show_mouse_position()
```

## 📁 项目结构

```
Turmoil_auto_waste/
├── main.py              # 主脚本文件
├── config.json          # 配置文件
├── requirements.txt     # Python 依赖
├── LICENSE             # MIT 许可证
└── README.md           # 项目说明文档
```

## 🏗️ 架构设计

### 核心类

| 类名 | 功能描述 |
|------|----------|
| `TurmoilConfig` | 配置管理，从 JSON 文件加载和管理所有配置项 |
| `TurmoilBot` | 游戏自动化机器人，实现所有游戏操作 |

### 主要方法

| 方法名 | 功能描述 |
|--------|----------|
| `show_mouse_position()` | 显示鼠标当前位置（调试用） |
| `borrow_money()` | 自动借贷 |
| `put_drill_rigs()` | 放置钻机 |
| `build_pipe()` | 建造单段管道 |
| `build_pipe_single()` | 建造连续管道 |
| `enhance_pipe_single()` | 升级管道 |
| `make_pipe_all()` | 建造所有管道网络 |
| `run_all()` | 执行全部操作 |

## ⚠️ 注意事项

1. **分辨率依赖**: 脚本使用硬编码坐标，仅支持 2560x1440 分辨率
2. **窗口模式**: 游戏必须以窗口模式运行
3. **执行时机**: 运行脚本后有准备时间（可在 config.json 中调整）
4. **故障保护**: 将鼠标快速移到屏幕左上角可立即中止脚本
5. **风险自负**: 自动化操作可能违反游戏规则，请谨慎使用

## 🛠️ 常见问题

### Q: 坐标不准确怎么办？

A: 不同分辨率或窗口位置会导致坐标偏移。请确保：
- 使用 2560*1440 分辨率
- 游戏窗口位置固定
- 或使用 `show_mouse_position()` 重新获取坐标并更新 `config.json`

### Q: 脚本执行失败？

A: 检查以下事项：
- 是否以管理员权限运行
- 游戏是否处于正确状态
- 依赖是否正确安装
- 配置文件格式是否正确

### Q: 如何调整操作速度？

A: 在 `config.json` 中修改 `delays` 相关配置：
- `start_delay`: 启动前的等待时间
- `enhance_delay_per_move`: 管道升级时的延迟

## 🔄 更新日志

### v2.0 (当前版本)
- ✨ 使用面向对象重构代码
- ✨ 添加 JSON 配置文件支持
- ✨ 完善日志输出系统
- ✨ 添加类型注解
- ✨ 改进错误处理
- ✨ 添加故障安全保护

### v1.0
- 🎉 初始版本发布
- 基础自动化功能

## 📝 许可证

本项目采用 [MIT License](LICENSE)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
