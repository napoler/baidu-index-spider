# Baidu_Indexation
## 使用说明：
本程序提供百度指数批量查询功能，仅为简化不必要的周期性工作
### 免责声明：
1. 本程序所有数据均来源于[百度指数](http://index.baidu.com)
2. 本程序仅为简化周期性获取关键词热度的繁琐过程所开发，不参与任何商业用途
3. 本程序源码将以较低频率爬取，尽量降低对服务器的负担，但开源后不保证使用者对其进行修改

### 使用流程：
1. 配置**data**文件夹下的**Login.txt**文件中的用户名和密码，暂时仅支持手机、邮箱、用户名登录，不支持其他账号以及扫码登录（如果一定要用这些方式，请在程序驱动Chrome时自行登录）
2. 配置**input.csv**文件，模式为**0**或**缺省**时收集最近n天数据，**1**时收集开始时间到结束时间数据，前两行分别为表头和示例，不参与收集
ps：csv文件不保存公式、格式等数据，若使用excel添加数据时使用了公式（比如拖动填充柄），请在保存时忽略掉公式即可（即：选择“是”）
3. 运行程序
4. 读取**output**文件夹下的csv文件（为作区分，当前文件名为数据生成时间）
5. 数据处理（由于csv文件无法保存格式与公式等信息，数据处理部分请另存为或者新建xls/xlsx文件）

## 注意事项：
1. 当前程序容错性极低，请尽量按照示例格式对Login.txt文件和input.csv文件进行配置
2. 登录部分尚存在很多问题，未考虑cookies过期问题，如果出现问题请及时联系我
3. 第一次使用将会驱动Chrome（当前仅提供32位Chromedriver）获取cookies以便后续操作，如果首次操作未成功驱动Chrome，请查看自己的Chrome版本号下载对应driver（[对应关系](https://blog.csdn.net/cz9025/article/details/70160273)），并将软件包内的driver替换掉重试
4. 请确保所查询热词已存在，若**查询不存在的词可能引发程序崩溃**




## 参考链接：
1. [百度指数爬取工具（java实现）](https://songgeb.github.io/2017/01/29/%E7%99%BE%E5%BA%A6%E6%8C%87%E6%95%B0%E7%88%AC%E5%8F%96%E5%B7%A5%E5%85%B7/)
2. [百度指数爬虫思路总结](https://blog.csdn.net/zhangwei3781871/article/details/78850207)
3. [requests利用cookies跳过登陆验证码](https://blog.csdn.net/zjupeco/article/details/77648596)
4. [Python Selenium Cookie 绕过验证码实现登录](http://www.cnblogs.com/BlueSkyyj/p/8615879.html)
5. [截图抓取百度指数](http://www.sohu.com/a/213141817_654419)
6. [抓取百度指数图片，自行渲染还原为原图](http://www.sohu.com/a/214025473_654419)
7. [PhantomJS在Selenium中被标记为过时的应对措施](https://www.cnblogs.com/zhuxiaoxi/p/8425686.html)
8. [图片裁剪](https://www.cnblogs.com/sun-haiyu/p/7127582.html)
9. [图片拼接](https://blog.csdn.net/zm714981790/article/details/54931909)
10. [Python、图片汉明距离实现](https://blog.csdn.net/gavinking0110/article/details/53672974)
11. [图片汉明距离](https://blog.csdn.net/qq_37267015/article/details/71330600?locationNum=4&fps=1)
12. [对像素颜色进行转换](https://blog.csdn.net/xwbk12/article/details/78998196)

## 更新日志：
### 版本号：1.1
#### 开发中
#### 内容：
1. 增加自行输入密码机制
2. 增加爬取失败时重新请求cookies机制
3. 对电脑端抓取百度指数进行实现，但由于其实际功能不如手机端所抓取，且效率较低、操作繁琐，因此暂仅作为`Indexation_standby`备用
4. 托管于GitHub

### 版本号：1.0
#### 发布日期：2018.07.04
#### 内容：
1. 实现基本的对百度指数收集功能

### By Sigure_Mo
