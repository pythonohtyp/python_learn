# -*- coding:utf-8 -*-
import itchat
from echarts import Echart,Legend,Pie
itchat.auto_login(enableCmdQR=1,hotReload=True)
friends = itchat.get_friends(update=True)[0:]
male = female = other = 0
for i in friends[1:]:
    sex = i["Sex"]
    print i
    if sex == 1:
        male+=1
    elif sex == 2:
        female+=1
    else:
        other+=1
total = len(friends[1:])

print total

print "男性好友：%.2f%%" %(float(male)/total*100)
print "女性好友：%.2f%%" %(float(female)/total*100)
print "未备注好友：%.2f%%" %(float(other)/total*100)

chart = Echart('%s的微信好友性别比例' %(friends[0]),'from WeChat')
chart.use(Pie('WeChat',
              [{'value':male,'name':"男性好友：%.2f%%" %(float(male)/total*100)},
              {'value':male,'name':"女性好友：%.2f%%" %(float(female)/total*100)},
              {'value':male,'name':"未备注好友：%.2f%%" %(float(other)/total*100)}],
               radius=["20%","40%"]))

chart.use(Legend(["male","female","other"]))
del chart.json["xAxis"]
del chart.json["yAxis"]
chart.plot()