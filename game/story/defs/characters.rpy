################################################################################
## 人物定义
##
## 剧本里一律用这些变量，别在台词里写裸字符串。
## 外观 / 立绘表情等进 Character 的 image= 参数，等美术定稿再补。
################################################################################

define mc     = Character("XXX")                 # 主角名未定，正文暂用 XXX
define zm     = Character("周墨")
define zzb    = Character("周子博")
define zeng   = Character("曾老师")
define stu_a  = Character("同学甲")
define stu_b  = Character("同学乙")
define bro    = Character("广播")                 # 校园广播，不是人

## 心里独白：无声，用斜体区分
define inner  = Character(None, what_italic=True)
