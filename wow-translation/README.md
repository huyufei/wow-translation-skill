# WoW Translation Skill

魔兽世界英文翻译技能源码目录。

---

## ⚠️ 重要提示

### 翻译质量与英文字幕质量直接相关

本工具翻译的**准确性取决于原版英文字幕的质量**。由于英文字幕通常是通过**语音识别自动生成**的，存在以下常见问题：

| 问题来源 | 具体表现 | 对翻译的影响 |
|---------|---------|-------------|
| **口音问题** | 原作者英语带口音，如 `Frost Strike` 被识别为 `First Strike` | 技能名翻译错误 |
| **连读/吞音** | `Blood Plague` 被识别为 `Blood Play` 或 `Blood Plug` | 术语无法匹配 |
| **游戏术语缺失** | 语音模型不认识魔兽专有名词 | 生造词或错误识别 |
| **背景噪音** | 游戏音效干扰语音识别 | 整句乱码或缺失 |

### 建议

1. **高价值内容建议人工校对** — 关键攻略视频建议对照原视频核对关键术语
2. **关注【需审核】标记** — 翻译输出中的不确定部分需要特别关注
3. **口音重的作者风险高** — 非母语作者的视频，英文字幕错误率可能高达 20-30%

> 💡 **核心原则**：Garbage in, Garbage out — 英文字幕质量差，再好的翻译模型也无法产出准确译文。

---

## 目录说明

```
wow-translation/
├── SKILL.md                    # Skill 核心定义文件（翻译规则）
├── LICENSE                     # MIT 许可证
├── wow-translation.skill       # 打包好的技能文件（可直接安装）
├── references/                 # 术语数据库
│   ├── abilities_translation.json   # ~5000+ 技能对照
│   ├── trees_translation.json       # ~8000+ 天赋对照
│   ├── pvp_translation.json         # ~200+ PVP天赋对照
│   └── wow_slang.json               # ~50 玩家黑话
├── scripts/                    # 辅助脚本
│   ├── preprocess_srt.py       # 长文本预处理（分段）
│   └── validate_srt.py         # 格式验证与修复
└── assets/samples/             # 翻译样例参考
    ├── cn0.srt, en0.srt
    └── ...
```

## 快速开始

**详细文档请查看项目根目录的 README.md**

仓库地址：https://github.com/huyufei/wow-translation-skill

## 安装方式

### 方式一：使用 .skill 文件（推荐）

1. 下载 `wow-translation.skill` 文件
2. 对 AI 助手说：
   ```
   帮我安装这个 skill：wow-translation.skill
   ```

### 方式二：使用源码

将整个 `wow-translation/` 文件夹复制到 AI 工具的 skills 目录：

```bash
# Claude Code
cp -r wow-translation ~/.claude/skills/

# 或使用 .skill 文件
zip -r wow-translation.skill wow-translation/
```

## 使用方法

安装完成后，在 AI 工具中输入：

```
/wow-translation
```

或描述任务：

```
帮我翻译这个 SRT 文件：video.srt
翻译这段魔兽攻略文本
```

## 脚本使用

```bash
# 预处理分段（适用于 ≥100 条字幕）
python scripts/preprocess_srt.py input.srt 50

# 验证翻译结果
python scripts/validate_srt.py input.srt output.srt

# 修复格式问题
python scripts/validate_srt.py input.srt output.srt --repair
```

## 许可证

MIT License
