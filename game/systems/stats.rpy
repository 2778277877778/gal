## systems/stats.rpy
##
## 四数值 / 行动点 / Flag 的唯一入口。
## 口径来源：《回合事件表_v3.0》§0 §3 §5 §7、《游戏设定总表_v2.5》§四。
##
## 规矩：剧情里不要写 `$ study += 5`，一律调用本文件的函数。
## 数值全部可调，改数字只改这里。

init -1 python:

    ## 初始值（设定总表 §四：学习 30 / 压力 10 / 体力 40 / 金钱 100）
    STAT_INIT = {"study": 30, "stress": 10, "stamina": 40, "money": 100}

    ## 回合规则
    ALLOWANCE_PER_MONTH = 150   # 月初生活费
    AP_PER_MONTH = 3            # 每月行动点
    AP_LAST_MONTH = 2           # T8 只有 2 点

    ## 阈值（设定总表 §四）
    STRESS_INSOMNIA = 80        # ≥80 失眠：学习减半
    STRESS_SICK = 95            # ≥95 生病：少 1 AP
    STAMINA_LOW = 20            # <20 学习/小游戏收益减半

    ## 考试线（回合事件表 §1）。key 一律英文，见变量命名规范 §3
    EXAM_LINES = {"monthly": 35, "midterm": 50, "final": 60, "yearly": 70}

    ## 结局门槛（回合事件表 §7）
    END_STUDY = 75
    END_STRESS = 70
    TRUE_FLAGS = ("found_piano_room", "art_fair", "club", "music_hall", "subject_support", "same_subject")

    ## 13 个 Flag 的唯一名单（回合事件表 §5）。set_flag 只认这些名字，
    ## 拼错一个字母会当场抛异常，不会静默写进字典、让 TRUE 永远拿不到。
    FLAG_NAMES = (
        "met_zhoumo", "offered_candy", "heard_piano", "heard_call",
        "found_piano_room", "art_fair", "sheet_music", "piano_crisis",
        "club", "music_hall", "subject_support", "same_subject", "confession",
    )

    ## 行动表（回合事件表 §3）。study/stress/stamina 是纯增量，money 是花费。
    ## ap = 0 表示不消耗行动点。key 同时是剧情里调 do_action() 时传的名字。
    ACTIONS = {
        "attend_class":     dict(label="去教室上课",     ap=1, study=5,  stress=8,  stamina=-7),
        "ask_zhoumo":       dict(label="找周墨问题",     ap=1, stress=-2),
        "study":            dict(label="去图书馆自习",   ap=1, study=5,  stress=8,  stamina=-7),
        "study_with":       dict(label="和周墨一起自习", ap=1, study=4, stress=5),
        "eat_canteen":      dict(label="去食堂吃饭",     ap=1, stress=-4, stamina=3, money=12),
        "buy_shop":         dict(label="去小卖部",       ap=0),   # 只开商店界面，扣钱走 add_stat("money", -价)
        "do_sport":         dict(label="打球/跑操",      ap=1, stress=-4, stamina=10),
        "watch_basketball": dict(label="看周子博打球",   ap=1, stress=-4),
        "rest_dorm":        dict(label="回宿舍休息",     ap=1, stress=-10, stamina=8),
        "listen_piano":     dict(label="站在琴房外听",   ap=1, stress=-8),   # 旧琴房，T3–T4
        "visit_auditorium": dict(label="去礼堂看琴",     ap=1, stress=-8),   # 礼堂，T5 后
        "visit_club":       dict(label="去音乐社",       ap=1, stress=-6),   # 艺术楼，T6 后
    }

    ## 地图节点（回合事件表 §4）。key 由 campus_map 和剧情共用，label 是界面上的字，
    ## unlock 是解锁回合号（T 几）。节点常驻的人写在文档里，不进代码。
    NODES = {
        "dorm":         dict(label="宿舍",     unlock=1),
        "classroom":    dict(label="教室",     unlock=1),
        "library":      dict(label="图书馆",   unlock=1),
        "canteen":      dict(label="食堂",     unlock=1),
        "shop":         dict(label="小卖部",   unlock=1),
        "field":        dict(label="操场",     unlock=1),
        "art_building": dict(label="艺术楼",   unlock=2),
        "piano_room":   dict(label="旧琴房",   unlock=3),
        "auditorium":   dict(label="礼堂",     unlock=5),
        "music_room":   dict(label="音乐教室", unlock=6),
    }

    def unlocked_nodes():
        """当前回合能点的节点 key 列表，按 NODES 里的顺序。"""
        return [k for k, v in NODES.items() if store.turn >= v["unlock"]]

    def node_open(key):
        """这个节点在本回合开放没有。key 拼错直接抛，不静默返回 False。

        菜单条件写成 node_open("auditorium")：写错 key 会当场炸出来，
        而不是像 `in unlocked_nodes()` 那样让整条菜单项悄悄消失。
        """
        if key not in NODES:
            raise Exception("未知节点：%s（NODES 里没有这个 key）" % key)
        return store.turn >= NODES[key]["unlock"]

    def node_label(key):
        if key not in NODES:
            raise Exception("未知节点：%s（NODES 里没有这个 key）" % key)
        return NODES[key]["label"]

    def clamp(value, low=0, high=100):
        return max(low, min(high, value))

    def gain_multiplier():
        """失眠或体力不足时，正向收益减半（只作用于学习与体力类收益）。"""
        if store.stress >= STRESS_INSOMNIA:
            return 0.5
        if store.stamina < STAMINA_LOW:
            return 0.5
        return 1.0

    def add_stat(name, delta, affected_by_state=False):
        """改数值的唯一入口。affected_by_state=True 时按失眠/低体力打折正收益。

        打折后四舍五入取整（5 减半 = 2.5 → 3），不用 Python 的 round()：
        round(2.5) 走 banker's rounding 会给 2，失眠时反而比「减半」更狠。
        """
        if affected_by_state and delta > 0:
            delta = int(delta * gain_multiplier() + 0.5)
        if name == "money":
            store.money = max(0, store.money + delta)
        else:
            setattr(store, name, clamp(getattr(store, name) + delta))
        return delta

    def can_act():
        return store.ap > 0

    def do_action(key):
        """执行一次行动，扣 AP 并结算数值。返回实际变化，供 UI 显示。"""
        act = ACTIONS.get(key)
        if act is None:
            raise Exception("未知行动：%s" % key)
        if act["ap"] and not can_act():
            return False
        if act["ap"]:
            store.ap -= 1
        changed = {}
        for stat in ("study", "stress", "stamina"):
            if stat in act:
                changed[stat] = add_stat(stat, act[stat], affected_by_state=(stat == "study"))
        if "money" in act:
            changed["money"] = add_stat("money", -act["money"])
        return changed

    def start_month(turn_index, allowance=ALLOWANCE_PER_MONTH):
        """月初：生活费到账、行动点重置。turn_index 从 1 开始（T1..T8）。"""
        store.turn = turn_index
        add_stat("money", allowance)
        ap = AP_LAST_MONTH if turn_index >= 8 else AP_PER_MONTH
        if store.stress >= STRESS_SICK:
            ap -= 1                       # 生病：少 1 AP
        store.ap = max(0, ap)

    def exam_roll():
        """掷一次：学习 + 随机(−5, +5)，存进 store.exam_score 并返回。

        同一回合查多条及格线（月考/期中/期末）共用这一次掷点，不会各掷一个随机数。
        """
        store.exam_score = clamp(store.study + renpy.random.randint(-5, 5))
        return store.exam_score

    def exam_pass(line_key):
        """拿 store.exam_score 比 EXAM_LINES 的及格线，不重新掷。

        key：monthly 35 / midterm 50 / final 60 / yearly 70。
        调用约定：同一回合必须先 exam_roll() 再 exam_pass()，月末流程固定是
        「exam_roll() → exam_pass(key)」。没掷过（exam_score 是 None）会直接抛，
        不会静默判不及格。
        """
        if store.exam_score is None:
            raise Exception("还没掷点：exam_pass(%r) 之前必须先调 exam_roll()" % line_key)
        return store.exam_score >= EXAM_LINES[line_key]

    def set_flag(name):
        if name not in FLAG_NAMES:
            raise Exception("未知 Flag：%s（名单见 FLAG_NAMES / 变量命名规范 §5）" % name)
        store.flags[name] = True

    def has_flag(name):
        return bool(store.flags.get(name))

    def true_ending():
        """TRUE「最后一个音」：学习 ≥75、压力 ≤70、六个 Flag 全触发（不看好感）。"""
        return store.study >= END_STUDY and store.stress <= END_STRESS and all(has_flag(f) for f in TRUE_FLAGS)

    def end_variant():
        """END「琴盖没开」的正文变体（回合事件表 §7.1）：A 表被改回 / B 没跟着填 / C 曲子弹断了。

        只该在 true_ending() 为假（走 END）时调用；TRUE 分支调它会拿到一个不属于结局的变体。
        本函数只决定取哪一版正文，正文以大纲 §5 为准。
        """
        if not has_flag("subject_support"):
            return "A"
        if not has_flag("same_subject"):
            return "B"
        return "C"


## 存档状态 ####################################################################
## 初始值只写在 STAT_INIT 一处，这里从它取，别再重复写数字。

default study = STAT_INIT["study"]
default stress = STAT_INIT["stress"]
default stamina = STAT_INIT["stamina"]
default money = STAT_INIT["money"]
default ap = AP_PER_MONTH
default exam_score = None   # 最近一次 exam_roll() 的掷点；None = 本回合还没掷，exam_pass 会抛
default turn = 1
default flags = {}
