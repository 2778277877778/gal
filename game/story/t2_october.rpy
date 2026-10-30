################################################################################
## T2 十月「藏」—— 骨架，只有结构、行动入口和 Flag 判定，台词全部是占位
##
## 依据《回合事件表_v3.md》§2 的 T2：
##   月初 迎新晚会筹备（周墨拒绝上台）
##   固定 旧琴房（他撞见她弹琴）      → heard_piano
##   固定 迎新晚会（放录音伴奏）      → 只在台词里回指
##   固定 月考 + 楼梯间电话           → heard_call；月考线 35
##   自由 + 艺术楼（T2 起解锁）
##
## 台词回来后只替换方括号里的占位行和选项文字，不动结构。
################################################################################

## 背景图统一在 game/story/defs/images.rpy 定义，这里只用 scene bg xxx。

default t2_monthly_pass = False      # 第一次月考是否过线（线 35）
default t2_call = ""                 # stay / leave / water_only，楼梯间那三种处理

label t2_october:

    $ start_month(2)

    ## 月初 · 迎新晚会筹备
    scene bg classroom_day
    "〔T2-1 月初 · 迎新晚会筹备 · 台词待补〕"
    "〔合唱队缺伴奏，周墨拒绝上台 · 台词待补〕"

    ## 固定 · 旧琴房
    scene bg art_backstage
    "〔T2-2 旧琴房 · 他推门撞见她弹琴 · 台词待补〕"

    menu:
        "〔待补〕说破伴奏是她弹的":
            "〔T2-2 选项 A · 台词待补〕"

        "〔待补〕装作没看见":
            "〔T2-2 选项 B · 台词待补〕"

    # 两种反应都是「听见了琴」，Flag 只看这一点；台词差别留到写台词时分支
    $ set_flag("heard_piano")

    ## 固定 · 迎新晚会
    scene bg auditorium_night
    "〔T2-3 迎新晚会 · 放录音伴奏，主持人夸伴奏 · 台词待补〕"
    "〔他差点说漏嘴，被踩脚 · 台词待补〕"

    ## 固定 · 月考
    scene bg classroom_day
    $ exam_roll()
    $ t2_monthly_pass = exam_pass("monthly")
    if t2_monthly_pass:
        "〔T2-4 第一次月考 · 过线 35 · 台词待补〕"
    else:
        "〔T2-4 第一次月考 · 没过线 35 · 台词待补〕"

    ## 固定 · 楼梯间电话
    scene bg stairwell_night
    "〔T2-4 楼梯间 · 父亲打电话问数学为什么没满分 · 台词待补〕"

    menu:
        "〔待补〕过去放一瓶水":
            $ t2_call = "stay"
            "〔T2-4 选项 A · 台词待补〕"

        "〔待补〕走开":
            $ t2_call = "leave"
            "〔T2-4 选项 B · 台词待补〕"

        "〔待补〕放水就走，不留话":
            $ t2_call = "water_only"
            "〔T2-4 选项 C · 台词待补〕"

    # 他听见了这通电话，三种处理都算；具体怎么处理记在 t2_call，台词回来再读
    $ set_flag("heard_call")

    ## 自由行动（T2 起艺术楼解锁）
    call free_actions

    ## 月末结算
    scene bg dorm_402
    "〔T2 月末结算 · 学习 [study]，压力 [stress]，体力 [stamina]，钱 [money] · 台词待补〕"
    "〔T2 结束 · T3「揭」待写〕"
    # TODO: T3「揭」写好后把下面这行 return 换成跳到 T3 的 label（8 月回合表 §8 的命名）
    return
