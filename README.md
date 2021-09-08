# **Aiqiyi-Sign**

> 爱奇艺会员签到打卡
>
> 爱奇艺会员签到打卡，增加经验值，增加爱奇艺会员天数（连续打卡28天，可以增加5天会员），**前提是爱奇艺会员**
>
> 项目地址：[Aiqiyi_Sign](https://github.com/ioutime/Aiqiyi_Sign)


## 脚本功能：

1. 登录爱奇艺,手机号+密码（可能因为安全验证导致失败）或 cookie（需要手动获取）
2. 支持爱奇艺会员签到打卡，并显示今日成长值，vip到期时间等
3. 支持本地命令行执行
4. 支持pushplus 微信公众号推送
5. 支持 GitHub Actions 部署
6. 支持多个账户签到（P00001)
7. 支持腾讯云函数部署


## 注意事项：

- **需要是爱奇艺会员**，否则脚本执行会不成功

  

使用方法:
---

### 安装依赖

```shell
pip install -r requirements.txt
```

### 本地执行脚本----local_action.py

**必须**：**替换local_action.py的第十四行为自己的cookie值（下面有获取cookie的方法）**，否则运行不成功

参数,选填

```shell
usage: local_action.py [-h] [-t TOKEN]

optional arguments:
  -h, --help  show this help message and exit
  -t TOKEN    pushplus的token值
```

eg:

```shell
python local_action.py
```

结果

```
签到成功
成长值+2
连续签到：3天
签到周期：3天/7天
VIP等级：4
升级需成长值：315
VIP到期时间:2021-10-04
```



### COOKIE值获取

1、打开[爱奇艺](https://www.iqiyi.com/)官网，并***登录***，一定要登录

2、按下**F12**，选择**network**（或者是网络）, 按下 **F5** 刷新页面，如下图所示

<img src="/img/2021-7-20 1-1.png"  />

3、点击第一个**www. iqiyi .com**，右边的**Headers**，找到 **Request Headers**，中的cookie值（从冒号开始）

<img src="/img/2021-7-20 1-2.png"  />

### pushplus 微信公众号推送

使用[pushplus](http://www.pushplus.plus/)平台进行推送。

使用方法：

1. 访问[pushplus](http://www.pushplus.plus/)官网，登录
2. 找到**一对一推送**，并复制你的**token**
3. 执行脚本时指定参数`-t`，后接上述 token 值

<img src="/img/2021-7-15 token.png"  />

示例：

```shell
python local_action.py -t token
```

结果：

```
签到成功
成长值+2
连续签到：3天
签到周期：3天/7天
VIP等级：4
升级需成长值：315
VIP到期时间:2021-10-04
```



### github仓库部署:

#### 	1. Fork 该仓库

<img src="/img/2021-7-15 1-0.png" style="zoom:50%;" />

#### 	2. 创建 Secrets，必填COOKIE（由于手机号登录容易出现安全验证，所以取消PHONE和PASSWORD的必填，改为选填）

```
创建 COOKIE (必填)
创建 PHONE，填入手机号（选填）
创建 PASSWORD，明文密码（选填）
创建 TOKEN (选填,pushplus的token值)		
```

***cookie值获取方法见上面***

<img src="/img/2021-7-15 1.png" style="zoom:50%;" />	  

#### 	3.启用 Action

点击 Actions，选择 **I understand my workflows, go ahead and enable them**（第一次用可能会出现）

<img src="/img/2021-7-15 1-1.png"  />

**直接fork来的仓库不会自动执行！！！**，最简单的方法就是， **手动修改项目**提交上去，最简单的方法就是修改下图的README.md文件（右侧有网页端编辑按钮）。

<img src="/img/2021-7-15 2.png" style="zoom: 80%;" />	

随便修改什么都行，修改完commit就可以了

<img src="/img/2021-7-15 3.png" style="zoom: 67%;" />

之后**每天 0 点**会自动执行一次脚本



### 多个爱奇艺账号github仓库部署：

多个账号部署，和上**面的github仓库部署流程一样**，只是创建的**Secrets**不一样。

#### 创建 Secrets，必填P00001 （下面有如何获取）


```
创建 P00001 (必填,注意是四个零; 多个以英文逗号【','】隔开，必须是英文的逗号)
创建 TOKEN (选填,pushplus的token值)	
```

#### P00001的获取与如何填入数据

1、打开[爱奇艺](https://www.iqiyi.com/)官网，并***登录***，一定要登录

2、按下**F12**，选择**Application**（或者是应用程序）, 并选择左侧栏的Cookies ,如下图所示

<img src="/img/2021-8-4 1-1.png"  />

3、在搜索栏中输入P00001，回车，如下图所示，复制P00001

<img src="/img/2021-8-4 1-2.png"  />



腾讯云函数部署：
---

详细过程请看[腾讯云部署.md](https://github.com/ioutime/Aiqiyi_Sign/blob/master/腾讯云部署.md)文件

## 建议：

1. 建议关注爱奇艺的公众号，能接收到会员天数的增加消息
2. 建议添加微信公众号推送，以便接收是否打卡成功
3. 如果复刻了该项目，建议设置同步更新，网上有很多
4. 如果使用cookie签到，网页端登录后别退出一直保持登录，建议一个月更新一次cookie值，**不更新也没事，可以正常签到**，但是不能获取个人详细信息（如vip到期时间等）

