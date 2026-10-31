init -100 python in gui:

    def scale(n):
        # gui.rpy / screens.rpy 里的数字是按 1280×720 设计的模板值，
        # 工程实际是 1920×1080，所以统一放大 1.5 倍。
        # 不放大时字会小 1/3，对白条只有 185px 高（应为 278px）。
        return int(round(n * 1.5))


## 模板自带的这段会在每次启动（包括 lint）时，按 gui.accent_color 重新烘焙
## gui/ 下的图片：按钮、滑条、滚动条、菜单底图……而且只补缺失的文件。
##
## 现在对白条、名札、选项按钮换成了手绘素材（tools/mkui.py 生成），自动烘焙会
## 把它们覆盖回默认样子，所以关掉。要换主题色重新烘焙时：
##   1. 删掉 game/gui/ 下的 png
##   2. 临时打开下面这段，跑一次 lint
##   3. 关回去，再跑 tools/mkui.py 恢复手绘素材
##
## 打开时注意第一行判断：`if config.developer and not renpy.mobile`。
## config.developer 打包后自动为 False，所以就算忘了关回去，发布版也不会执行这段
## （它会把 SDK 的 launcher/game 插进 sys.path 再 import gui7，只能在开发机上跑）。
##
# init 100 python in gui:
#
#     if config.developer and not renpy.mobile:
#         from store import config
#
#         import sys
#         import os
#         sys.path.insert(0, os.path.join(config.renpy_base, "launcher", "game"))
#
#         from gui7.parameters import GuiParameters
#         from gui7.images import ImageGenerator
#         from gui7 import generate_gui
#
#         p = GuiParameters(
#             config.gamedir, config.gamedir,
#             config.screen_width, config.screen_height,
#             accent_color, "#000000", False, None,
#             True, False, False, "gui")
#
#         p.skip_backup = True
#
#         generate_gui(p)
#
#         _skip_backup = True
#         _gui_images()
