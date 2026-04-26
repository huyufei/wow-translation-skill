# WoW Translation Skill

魔兽世界英文翻译技能，用于翻译英文攻略、字幕等内容为中文。

## 项目结构

项目源码位于 `wow-translation/` 目录：

```
wow-translation/
├── README.md           # 详细使用说明
├── SKILL.md            # 核心 Skill 定义文件
├── LICENSE             # MIT 协议
├── references/         # 术语数据库 (~13000+ 条)
│   ├── abilities_translation.json
│   ├── trees_translation.json
│   ├── pvp_translation.json
│   └── wow_slang.json
├── scripts/            # 辅助脚本
│   ├── preprocess_srt.py
│   └── validate_srt.py
└── assets/samples/     # 翻译样例
    ├── cn0.srt, en0.srt
    └── ...
```

## 快速开始

进入项目目录查看详细说明：

```bash
cd wow-translation/
cat README.md
```

## 安装

下载 `wow-translation.skill` 文件，然后对 AI 助手说：

```
帮我安装这个 skill：wow-translation.skill
```

## 不上传的文件

以下文件保留在根目录，不上传到 GitHub：

- `.claude/` - AI 工具本地配置
- `wow-translation.skill` - 打包后的技能文件（由源码生成）

---

**许可证**: MIT License
