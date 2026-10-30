################################################################################
## T3 十一月「揭」—— 骨架，只有结构、行动入口和 Flag 判定，台词全是占位
##
## 依据《回合事件表_v3.md》§2 的 T3：
##   月初 期中复习，她状态不对
##   固定 期中考试（物理失手，年级第三）  → 期中线 50
##   固定 家长会（他喊「周医生好」，她父亲冷淡）
##   固定 旧琴房（按不下去的键、多喝热水、纸巾被风吹跑、手指被夹）→ found_piano_room
##   固定 她的秘密（初二停琴）
##   自由 + 旧琴房（NODES 里 T3 解锁，已配好）
##
## 台词回来后只替换〔待补〕，不动结构。
################################################################################

## 背景图统一在 game/story/defs/images.rpy 定义，这里只用 scene bg xxx。

default t3_exam_pass = False         # 期中是否过线 50

label t3_november:

    $ start_month(3)

    ## 月初 · 期中复习
    scene bg classroom_day
    "〔T3-1 月初 · 期中复习，她状态不对 · 台词待补〕"

    ## 固定 · 期中考试
    scene bg classroom_day
    $ exam_roll()
    $ t3_exam_pass = exam_pass("midterm")
    if t3_exam_pass:
        "〔T3-2 期中 · 过线 50 · 台词待补〕"
    else:
        "〔T3-2 期中 · 没过线 50（物理失手，年级第三）· 台词待补〕"

    ## 固定 · 家长会
    scene bg classroom_day
    "〔T3-3 家长会 · 他喊「周医生好」，她父亲冷淡 · 台词待补〕"

    ## 固定 · 旧琴房
    scene bg piano_room_night
    "〔T3-4 旧琴房 · 她按着一个按不下去的键 · 台词待补〕"

    menu:
        "〔待补〕说「多喝热水」":
            "〔T3-4 选项 A · 台词待补〕"

        "〔待补〕蹲下去帮她看键":
            "〔T3-4 选项 B · 台词待补〕"

    # 撞见她弹琴 = 找到了琴房这条线，TRUE 必需
    $ set_flag("found_piano_room")

    ## 固定 · 她的秘密
    "〔T3-5 她的秘密 · 初二停琴、琴键不会问她考第几名 · 台词待补〕"

    ## 自由行动（旧琴房 T3 起解锁，free_actions 会自动出现）
    call free_actions

    ## 月末结算
    scene bg dorm_402
    "〔T3 月末结算 · 学习 [study]，压力 [stress]，体力 [stamina]，钱 [money] · 台词待补〕"
    "〔T3 结束 · T4「亮」待写〕"
    # TODO: T4 写好后把 return 换成 jump t4_december
    return
