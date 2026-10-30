################################################################################
## 背景图定义 —— 全工程唯一一处
##
## 命名：bg_<地点>_<时段/天气>，地点用英文小写，跟 NODES 的 key 对得上就尽量对上
## （dorm / classroom / playground / corridor / stairwell / art / auditorium）。
## 现在全是纯色占位；美术给出 images/bg_*.png 后，把 Solid 换成对应文件，
## 剧本里的 scene bg xxx 一行都不用改。
##
## 规矩：剧本文件里不许再写 image 语句，新背景只往这里加。
################################################################################

## 通用 / 入口
image bg room              = Solid("#101820")

## 校园与宿舍
image bg school_gate_rain  = Solid("#1b2430")
image bg dorm_402          = Solid("#221f1a")

## 教室
image bg classroom_morning = Solid("#1d232a")
image bg classroom_day     = Solid("#1f252b")

## 操场
image bg playground_sun    = Solid("#2a2b24")
image bg playground_heat   = Solid("#302a22")

## 走廊 / 楼梯间
image bg corridor_night    = Solid("#14181d")
image bg stairwell_night   = Solid("#15191e")

## 艺术楼 / 礼堂
image bg art_backstage     = Solid("#1a1d22")
image bg auditorium_night  = Solid("#12161b")
