import itchat
import pandas as pd
import json

itchat.auto_login()
users = itchat.get_friends(update=True)[1:]   #第一个元素为自己的账号信息，略去
itchat.check_login()
itchat.logout()
#保存为txt文件，不存在中文编码问题
with open('./output/users_yl.txt','wb') as f:
    f.write(str(users).encode('utf-8'))
#转为json，存在中文编码问题，但在web或python3上以及其它unicode编码控制台上能正常显示
with open('./output/users_yl.json','w') as f:
    json.dump(users,f)
#转换为数据框
#方法一，先转换为列表，然后转为数据框
with open('./output/users_yl.json','r') as f:
    myfriends = json.load(f)
myfriends_df = pd.DataFrame(myfriends)
# myfriends_df = pd.DataFrame(json.loads(line) for line in open('./output/users.json','r')) 另外一种写法
#方法二，直接读取json文件转为数据框
myfriends_df = pd.read_json('./output/users_yl.json')

#只取想要的列，组成新的数据框
myfriends_df2 = myfriends_df.ix[:,['NickName','ContactFlag','RemarkName','Sex','Signature','Province','City','SnsFlag','KeyWord']]

#统计分析
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

group = myfriends_df2['Sex'].value_counts() #性别分布
explode = [0,0,0.1]
plt.pie(x=group.values,labels=['女','男','未知'],autopct='%.2f%%',explode=explode,startangle=90)
plt.title('微信好友性别比例')
plt.axis('equal')
plt.show()
group.to_json('./output/wechat_sex.json')

group = myfriends_df2['Province'].value_counts()    #省份分布
plt.pie(x=group.values, labels=group.index, autopct='%.2f%%', startangle=90)
plt.title('微信好友省份比例')
plt.axis('equal')
plt.show()
group.to_json('./output/wechat_province.json')

group = myfriends_df2['City'].value_counts()    #城市分布
plt.pie(x=group.values, labels=group.index, autopct='%.2f%%', startangle=90)
plt.title('微信好友省份比例')
plt.axis('equal')
plt.show()
group.to_json('./output/wechat_city.json',orient='split')