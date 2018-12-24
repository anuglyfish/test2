# encoding=utf8
import requests    #引入请求模块
import re   #re模块提供对正则表达式(处理字符串的工具)的支持
#from bs4 import BeautifulSoup
#from tkinter import scrolledtext  # 导入滚动文本框的模块
#from tkinter import ttk
#import tkinter as tk
import threading  #线程模块


# 获取网页内容
def getHtml(ID):   #定义名getHtml函数
    url = 'https://movie.douban.com/top250?start=%s&filter=' % ID   #导入网址
    print('url  ' + url)   #打印
    headers = {      #防止网站不允许程序访问 为了模拟浏览器属性 设置headers属性
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'
        ,      #模拟服务器访问    agent为访问网站请求的身份  无此身份服务器不一定响应
        'Cookie': 'bid=I0klBiKF3nQ; ll="118277"; gr_user_id=ffdf2f63-ec37-49b5-99e8-0e0d28741172; ap=1; _vwo_uuid_v2=8C5B24903B1D1D3886FE478B91C5DE97|7eac18658e7fecbbf3798b88cfcf6113; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1498305874%2C%22https%3A%2F%2Fbook.douban.com%2Ftag%2F%25E9%259A%258F%25E7%25AC%2594%3Fstart%3D20%26type%3DT%22%5D; _pk_id.100001.4cf6=4e61f4192b9486a8.1485672092.5.1498306809.1498235389.; _pk_ses.100001.4cf6=*'
#使用cookie登录  Cookie 是由 Web 服务器保存在用户浏览器（客户端）上的小文本文件，它包含有关用户的信息
    }
    req = requests.get(url, headers)  #get方法得到
    return req.text   #返回值


# 解析网页并且获取相应内容
def parseHtml(html):
    # soup = BeautifulSoup(html,'lxml')   # 现在改为用正则
    print('init html.....')
    # print(html)

    # 1 取出title
    # titleRe = r'<span class="title">(.*?)</span>'
    titleRe = r'<span class="title">(.[^&]*?)</span>'  # 这里除去了副标题，（根据&nbsp 空格号进行筛选）
    regTitle = re.compile(titleRe)  #compile函数帮助将正则表达式语法转化成正则表达式对象
    titleStr = re.findall(regTitle, html)  #返回html中所有与regTitle相匹配的全部字串 形式为列表 等同于titleStr=regTitle.findall(html)
    # print(titleStr)
    # for verTitle in titleStr:
    #     print(verTitle)


    # 2 取出评分
    retStars = r'.*?"v:average">(.*?)</span>'
    regStars = re.compile(retStars)
    starts = re.findall(regStars, html)
    #print(starts)#打印评分 以数组形式

    # 取出评价
    regCommend = r'<span>(.*?)</span>'
    regCommends = re.compile(regCommend)
    commends = []
    commends = re.findall(regCommends, html)
    # print(commends)
    commends.remove('·')  #使用remove删除某东东
    commends.remove('更多')
    commends.remove('{{= year}}')
    commends.remove('{{= sub_title}}')
    commends.remove('{{= address}}')
    commends.remove('集数未知')
    commends.remove('共{{= episode}}集')
    # print(commends)

#取出导演，剧情（未实现）
    #regDoc= r'.*?<p class>(.*?)<br>'
    #regDoc=u'<p*?class="info">导演:(.*?)'
    #regxDoc = re.compile(regDoc)
    #list_doc = re.findall(regxDoc,html)
    #print(list_doc)
    #print('*'*40)

    # 片言(未实现)
    # regAction = r'<p class>.*?<br>(.*?)</p>'
    # regx_action = re.compile(regAction)
    # list_action = re.findall(regx_action,html)
    # print(list_action)

    # 取出引言  希望让人自由
    regScrip = r'.*?"inq">(.*?)</span>'
    regx_scrip = re.compile(regScrip)
    list_scrip = re.findall(regx_scrip, html)
    #print(list_scrip)

    # 取出图片地址(未实现)
    # regImg = r'<div class="pic">.*?src= "(.*?)"'
    # regx_img = re.compile(regImg)
    # list_imgaddress = re.findall(regx_img,html)
    # print(list_imgaddress)

    ver_info = list(zip(titleStr,commends,list_scrip,starts))  #用list强转为列表形式  zip函数将四个函数的返回值组合形成一个新的元组
    return ver_info  #将值返回


# html = getHtml(0)
# ver_infos = parseHtml(html)
# print(ver_infos)


def write():     #输出爬取的数据
    print('开始爬取内容及写入文件')
    filePath='C:\PC\PC.xls'
    file=open(filePath,'w',encoding='utf-8')
    ID = 0
    nums = 1
    while ID < 250: #设置循环
        html = getHtml(ID) 
        ver_infos = parseHtml(html) #调用函数 将三个参数用列表形式返回
        ID += 25   #把25部电影及25条信息为一波
        for ver in ver_infos:  #ver就跟i一样 只是一个代数罢了
            varStr ='No.%d\t%-30s%s\t(描述:)%-30s\t星星:%-30s' % (nums, ver[0], ver[1],ver[2],ver[3])
            #% 操作符只能直接用于字符串('123')，列表([1,2,3])、元组
#将编号  名称 评价及描述 星星 赋予varStr
            print(varStr)  #把每一个电影打印出来
            file.write(varStr)
            nums += 1
            print('爬取成功'+str(nums-1))

            

            

def start():
    print('start  init ....')  #作为开始标志
    t1 = threading.Thread(target=write())  #目标是write函数
#通过threading.Thread()创建线程。threading.Thread(target=,args=())
#其中target接收的是要执行的函数名字，args接收传入函数的参数，以元组（）的形式表示
    t1.start() #和threading.Thread是固定配套的 需要.start启动线程 让线程开始执行

start()   #主函数


# 以下方法丢弃
# def save():
#     print('save  init ...')
#     content = name.get()
#     textFile = open(u'C:\\豆瓣电影排行250.txt')
#     textFile.write(content)
#     textFile.close()
#
# print('^'*40)
# win = tk.Tk()
# win.title('呵呵呵')
#
# # 滚动文本框
# scrolW = 30 # 设置文本框的长度
# scrolH = 3 # 设置文本框的高度
# scr = scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD)     # wrap=tk.WORD   这个值表示在行的末尾如果有一个单词跨行，会将该单词放到下一行显示,比如输入hello，he在第一行的行尾,llo在第二行的行首, 这时如果wrap=tk.WORD，则表示会将 hello 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
# scr.grid(column=0, columnspan=3)
#
# # 文本框
# name = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
# nameEntered = ttk.Entry(win, width=42, textvariable=name)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
# nameEntered.grid(column=0, row=4)       # 设置其在界面中出现的位置  column代表列   row 代表行
# nameEntered.focus()     # 当程序运行时,光标默认会出现在该文本框中
#
# # 添加开始按钮
# start = ttk.Button(win,text='开始',command=start())
# start.grid(column=0,row=0) #按钮的添加位置
#
# # 保存按钮
# save = ttk.Button(win,text='保存',command=save())
# save.grid(column=1,row=0)
#
# win.mainloop()


