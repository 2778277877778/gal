################################################################################
## 通用自由行动段（T2 以后每个月都 call 它）
##
## 从 NODES 的解锁回合和 ACTIONS 的 key 出发，给玩家一个 AP 循环。
## 菜单条件用 node_open("<节点 key>")：key 写错会当场抛，不会让菜单项悄悄消失
## （「去礼堂看琴」就吃过这个亏：原来写的是 hall，NODES 里叫 auditorium）。
## 只放会消耗 AP 的行动：buy_shop 是 0 AP，放进这个 while 会死循环。
## 地图界面（campus_map）做出来以后，这里换成「点地图 → do_action」，其余不动。
################################################################################

label free_actions:

    "（本月还有 [ap] 点行动点。）"

    while ap > 0:

        menu:
            "去教室上课" if node_open("classroom"):
                $ do_action("attend_class")
                "（上课 · 台词待补）"

            "找周墨" if node_open("classroom"):
                $ do_action("ask_zhoumo")
                "（教室 · 台词待补）"

            "去图书馆自习" if node_open("library"):
                $ do_action("study")
                "（图书馆 · 台词待补）"

            "和周墨一起自习" if node_open("library") and turn >= 2:
                $ do_action("study_with")
                "（图书馆 · 台词待补）"

            "去食堂吃饭" if node_open("canteen"):
                $ do_action("eat_canteen")
                "（食堂 · 台词待补）"

            "去操场活动" if node_open("field"):
                $ do_action("do_sport")
                "（操场 · 台词待补）"

            "看周子博打球" if node_open("field"):
                $ do_action("watch_basketball")
                "（操场 · 台词待补）"

            "回宿舍休息" if node_open("dorm"):
                $ do_action("rest_dorm")
                "（宿舍 · 台词待补）"

            "站在琴房外听" if node_open("piano_room"):
                $ do_action("listen_piano")
                "（旧琴房 · 台词待补）"

            "去礼堂看琴" if node_open("auditorium"):
                $ do_action("visit_auditorium")
                "（礼堂 · 台词待补）"

            "去音乐社" if node_open("music_room"):
                $ do_action("visit_club")
                "（音乐教室 · 台词待补）"

    "（行动点用完了，这个月就这样。）"
    return
