# 高中校园物语

Ren'Py 校园视觉小说，简体中文，13+，首版只做 Windows。Demo 覆盖高一学年（9–12 月、次年 3–6 月），8 个回合，一个月一回合，设计通关时长 20 到 60 分钟。完整版计划做到高三、多角色多结局；眼下只做周墨线，两个结局。

玩法参考《火山的女儿》的日程和属性、《星露谷物语》的地图探索。

## 进度

现在从主菜单能玩到 T1 九月的月底结算：报到、开学典礼、军训、班委选举，加 3 点行动点的自由行动段，结束回主菜单。T2 十月、T3 十一月的结构已经进仓库，台词还是占位；T2 结尾接到 T3，但 T1 还没接 T2，所以实际能走完的只有 T1。

已完成：

- `game/systems/stats.rpy`：四项数值（学习、压力、体力、金钱）、行动点、12 个行动、9 个地图节点、13 个 Flag、考试线和结局判定
- 标题、中文字体、1920×1080 界面；`gui.rpy` 和 `ui_theme.rpy` 负责样式，`screens.rpy` 结构没动
- 冒烟用例在 `game/testcases.rpy`，覆盖从主菜单开始、推进 T1 开头几句台词

还没做：T1 接 T2、T2 和 T3 的台词、T4–T8 剧本、地图和个人界面、立绘、背景、音乐。素材目录是空的，背景用纯色占位。

## 运行

需要 Ren'Py 8.5.3 SDK，解压版即可，不用装进系统。下面 `<SDK>` 是 SDK 目录，`<仓库>` 是仓库根目录。

```powershell
# 启动游戏
"<SDK>\renpy.exe" "<仓库>"

# 提交前检查
"<SDK>\lib\py3-windows-x86_64\python.exe" renpy.py "<仓库>" lint

# 生成 .rpyc
... renpy.py "<仓库>" compile

# 冒烟自测
... renpy.py "<仓库>" test

# 打包 Windows 版
... renpy.py "<仓库>" distribute
```

环境细节、沙箱里的存档目录设置、数值系统的函数说明，都在 [开发环境说明.md](开发环境说明.md)。

## 目录

```
game/
  script.rpy        入口，跳到 t1_september
  options.rpy       标题、版本 0.0.1-demo、存档目录
  gui.rpy           GUI 变量（1920×1080）
  screens.rpy       默认界面
  ui_zh.rpy         界面中文化
  ui_theme.rpy      样式微调
  testcases.rpy     冒烟用例
  systems/stats.rpy 数值、AP、Flag、节点表的唯一入口
  story/
    t1_september.rpy  T1 全稿
    t2_october.rpy    T2 骨架（台词待补）
    t3_november.rpy   T3 骨架（台词待补）
    free_actions.rpy  通用自由行动段
    defs/
      characters.rpy  人物定义
      images.rpy      全部背景图定义
  fonts/ gui/ images/ audio/
高中校园物语/         策划文档
美术/                UI 规范、界面风格、预览图
开发环境说明.md       环境、命令、数值系统
```

## 文档

现行三份：

- [剧本大纲_高一学年_v3.md](高中校园物语/剧本大纲_高一学年_v3.md)：v3.4，八回合结构、角色、主题
- [回合事件表_v3.md](高中校园物语/回合事件表_v3.md)：v3.0，每月事件、行动表、Flag 表、数值曲线
- [游戏设定总表_v2.md](高中校园物语/游戏设定总表_v2.md)：v2.5，世界、玩法、调参表

另外 [变量命名规范_v1.md](高中校园物语/变量命名规范_v1.md) 是代码和文档之间 key 的对照。

第一幕全稿是 [剧本_周墨线_第一幕_开学.md](高中校园物语/剧本_周墨线_第一幕_开学.md)，已经转成 `game/story/t1_september.rpy`。

目录里只留现行版本。早先的 20 回合旧结构、三幕 15 天结构、苏瑶角色稿、SKS 脚本示例、设定总表 v1 和最初的 `项目文档.md` 已经删掉，要翻旧内容去 git 历史。

根目录不放文档副本，只改 `高中校园物语/` 里的版本。

## 约定

- 数值只走 `stats.rpy` 里的函数，剧情里不写 `$ study += 5`。
- 剧本先写成 markdown，标好 bg / bgm / sfx、选项和 Flag，再转 `.rpy`。
- key 一律英文小写 snake_case。改一个 key 要同时改三处：`变量命名规范_v1.md`、`stats.rpy`、回合事件表 §3 §5。
- 回合内的选择变量写成 `t<回合号>_<含义>`，值用小写英文，在 story 文件顶部 `default` 一次，不要放进 `flags`。`flags` 只放那 13 个正式 Flag。
- 主角名暂用 `XXX`，定稿后全仓替换一次。

## 还没定

校名、主角名、第三位女同学的名字。周墨的琴考到几级、停了多少年、旧琴是谁的。立绘要几个表情和姿势，素材从哪来。小游戏做选择题、实时操作还是只算数值。

## 许可

MIT，见 [LICENSE](LICENSE)。
