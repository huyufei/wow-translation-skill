# WoW Translation Skill

魔兽世界英文翻译技能，用于翻译英文攻略、字幕等内容为中文。支持 SRT 字幕文件和纯文本翻译，自动处理魔兽世界术语、技能名称和玩家黑话。

## 功能特性

- **SRT 字幕翻译** — 保持原时间线，自动处理断句
- **文本翻译** — 支持任意格式的英文文本
- **术语自动对照** — 技能、天赋、黑话自动查找中文对应
- **黑话保留解释** — NPC、DPS 等保留原文并加括号解释
- **分段处理** — 长文本自动分段，避免上下文丢失
- **格式验证** — 翻译后自动验证格式一致性，支持修复

***

## 安装

本 Skill 提供两种使用方式，根据你的需求选择：

### 方式一：下载 .skill 文件（推荐，最简单）

适合普通用户，一键安装即可使用。

1. **下载技能文件**
   - 下载 `wow-translation.skill` 文件（这是一个包含所有术语和脚本的完整包）

2. **让 AI 助手帮忙安装**
   - 在你的 AI 工具中输入：
     ```
     帮我安装这个 skill：wow-translation.skill
     ```
   - AI 助手会自动识别文件类型并完成安装

3. **开始使用**
   - 安装完成后，直接使用 `/wow-translation` 命令触发翻译功能

**优点**：
- ✅ 单个文件，下载方便
- ✅ AI 自动安装，无需手动配置
- ✅ 包含所有必要内容，开箱即用

---

### 方式二：下载完整文件夹（开发者/高级用户）

适合需要查看源码、修改术语或贡献代码的用户。

1. **克隆或下载整个仓库**
   ```bash
   git clone https://github.com/你的用户名/wow-translation-skill.git
   # 或下载 ZIP 解压
   ```

2. **查看和修改源码**
   - 术语库：`references/` 目录下的 JSON 文件
   - 脚本：`scripts/` 目录下的 Python 文件
   - 核心定义：`SKILL.md`

3. **手动安装到 AI 工具**
   - 将整个 `wow-translation/` 文件夹复制到 AI 工具的 skills 目录：
     ```bash
     # Claude Code
     cp -r wow-translation ~/.claude/skills/
     
     # 或创建 .skill 文件后安装
     zip -r wow-translation.skill wow-translation/
     # 然后让 AI 安装 .skill 文件
     ```

**优点**：
- ✅ 可查看和编辑源码
- ✅ 可自定义术语和规则
- ✅ 方便贡献代码和提交 PR
- ✅ 了解 Skill 工作原理

### 技术说明

- `.skill` 文件本质上是一个 ZIP 包，包含与文件夹相同的内容
- 支持的 AI 工具包括：Claude Code、OpenClaw、Hermes、Cursor、Trae 等
- 两种方式的最终效果完全相同，只是安装路径不同

***

## Skill 文件内容

`.skill` 文件是一个 ZIP 包，包含以下内容：

```
wow-translation.skill (ZIP)
├── SKILL.md                    # Skill 主文件（翻译规则）
├── references/                 # 术语对照文件
│   ├── abilities_translation.json  # ~5000+ 技能
│   ├── trees_translation.json      # ~8000+ 天赋
│   ├── pvp_translation.json        # ~200+ PVP天赋
│   └── wow_slang.json              # ~50 黑话
├── scripts/                    # 处理脚本
│   ├── preprocess_srt.py       # 长文本预处理
│   └── validate_srt.py         # 格式验证修复
└── assets/samples/             # 翻译风格参考
    ├── en0.srt, cn0.srt
    ├── en2.srt, cn2.srt
```

**验证内容：**

```bash
# 查看 .skill 文件结构
unzip -l wow-translation.skill
```

***

## 使用方法

### 基本用法

在 AI 工具中输入以下命令触发技能：

```
/wow-translation
```

或直接描述任务：

```
帮我翻译这个 SRT 文件：video.srt
翻译这段魔兽攻略文本
```

### 翻译流程

```
1. 提供原版文件（SRT 或文本）
2. AI 自动加载术语对照表
3. 执行翻译，输出两种版本：
   - AI 模糊版本：直接翻译
   - 人工审核版本：不确定部分标注【需审核】
4. 运行格式验证脚本确保一致性
```

### 长文本处理（≥100 条字幕）

```bash
# 预处理分段
python scripts/preprocess_srt.py input.srt 50

# 查看分段内容和术语摘要
# AI 会逐段翻译，保持风格一致

# 翻译完成后验证
python scripts/validate_srt.py input.srt output.srt

# 如有格式问题，自动修复
python scripts/validate_srt.py input.srt output.srt --repair
```

### 输出格式示例

```
## AI 模糊版本
1
00:00:00,000 --> 00:00:04,900
嘿，大家好，这里是Spagette，欢迎回到全新的元素萨满指南

## 人工审核版本
1
00:00:00,000 --> 00:00:04,900
嘿，大家好，这里是Spagette，欢迎回到全新的【需审核：专精名称】萨满指南
```

***

## 重要提示

### Token 消耗说明

⚠️ **翻译任务可能消耗大量 Token，请注意以下事项：**

- **术语库加载**：每次翻译会自动加载约 13000+ 条术语对照，这会消耗一定 Token
- **长文本分段**：超过 100 条字幕的文件会自动分段处理，每段都会重复加载术语上下文
- **双版本输出**：同时输出"AI 模糊版本"和"人工审核版本"会使 Token 消耗翻倍

**💰 费用提醒**

翻译任务**可能产生较高费用**，具体取决于：
- 文本长度和复杂度
- 使用的 AI 模型定价
- 是否需要多次迭代优化

**估算参考**：
- 一个 10 分钟视频字幕（约 150-200 条）完整翻译可能消耗 **数万到数十万 Token**
- 建议先测试小段内容，了解大致成本后再进行完整翻译

**节省建议**：
- 短文本（< 50 条字幕）：可直接完整翻译
- 长文本（≥ 100 条字幕）：建议先使用预处理脚本分段，分批次翻译
- 如需节省 Token，可要求只输出单一版本
- 先用低成本模型生成初稿，再选择性使用高级模型精修关键部分

***

## 术语对照文件

| 文件                           | 用途       | 条目数     |
| ---------------------------- | -------- | ------- |
| `abilities_translation.json` | 技能中英文对照  | \~5000+ |
| `trees_translation.json`     | 天赋树中英文对照 | \~8000+ |
| `pvp_translation.json`       | PVP 天赋对照 | \~200+  |
| `wow_slang.json`             | 玩家黑话术语   | \~50    |

### 术语查找示例

```json
// abilities_translation.json
{
  "spell": 434969,
  "name_cn": "闪电打击",
  "name_en": "Lightning Strikes"
}

// wow_slang.json
{
  "abbr": "NPC",
  "full": "Non-Player Character",
  "meaning": "非玩家角色，由系统控制的角色"
}
```

***

## 相关资源

### 字幕下载网站

从 YouTube 等视频平台下载字幕：

| 网站                                             | 说明             | 格式            |
| ---------------------------------------------- | -------------- | ------------- |
| [DownSub](https://downsub.com/)                | YouTube 字幕下载   | SRT, VTT      |
| [SaveSubs](https://savesubs.com/)              | 多平台字幕下载        | SRT, VTT, TXT |
| [YouTube Transcript](https://www.youtube.com/) | YouTube 内置字幕功能 | 需手动复制         |

**使用步骤：**

1. 打开 YouTube 视频页面
2. 复制视频链接
3. 访问 [DownSub](https://downsub.com/)
4. 粘贴链接，选择语言和格式
5. 下载 SRT 文件

### 魔兽世界攻略网站

| 网站                                            | 说明        | 语言  |
| --------------------------------------------- | --------- | --- |
| [Wowhead](https://www.wowhead.com/)           | 最全面的魔兽数据库 | 英文  |
| [Icy Veins](https://www.icy-veins.com/)       | 职业/专精详细指南 | 英文  |
| [MMO-Champion](https://www.mmo-champion.com/) | 新闻和补丁说明   | 英文  |
| [暴雪官方](https://worldofwarcraft.blizzard.com/) | 官方资讯      | 多语言 |
| [NGA](https://nga.178.com/)                   | 中文玩家社区    | 中文  |
| [魔兽世界中文官网](https://wow.blizzard.cn/)          | 官方中文站     | 中文  |

**推荐用法：**

- Wowhead：查询技能 ID、天赋树结构
- Icy Veins：获取职业专精详细攻略
- YouTube：搜索视频教程，下载字幕翻译

***

## 目录结构

```
wow-translation-skill/
├── README.md                    # 本文件
├── wow-translation.skill        # 打包后的技能文件（ZIP）
├── abilities_translation.json   # 技能对照
├── trees_translation.json       # 天赋对照
├── pvp_translation.json         # PVP 天赋对照
├── wow_slang.json               # 黑话术语
├── samples/                     # 翻译样本（可选）
│   ├── en0.srt                  # 原版样本
│   ├── cn0.srt                  # 翻译样本
│   └── ...
└── scripts/                     # 处理脚本
    ├── preprocess_srt.py        # 长文本预处理
    └── validate_srt.py          # 格式验证修复
```

***

## 许可证

MIT License

***

## 致谢

- 术语数据来源于 Wowhead 和游戏内数据
- 翻译样本来源于 [@Whoknow](https://space.bilibili.com/11514076?spm_id_from=333.1007.0.0)（B站：逐梦之心）
- 感谢所有魔兽世界玩家社区的分享

### 关注作者

- **抖音**：[逐梦之心](https://v.douyin.com/t9KP1jeGXjc/)&#x20;
- **Bilibili**：[逐梦之心的个人空间](https://space.bilibili.com/11514076?spm_id_from=333.1007.0.0) 

