# baidu-index-spider

**轻量**的百度指数收集接口

## 特性

- 移动端接口，无需复杂的解析过程
- 第三方库仅仅依赖 requests ，无需驱动浏览器

## 流程

每次查询 1-3 个关键词的数据，然后同时对这几个关键词进行解析

## 说明

- 本程序所有数据均来源于[百度指数](http://index.baidu.com)
- 本程序仅为简化周期性获取关键词热度的繁琐过程所开发，不参与任何商业用途
- **仅仅为了重构，不做完整的功能支持**，电脑端的也是做过的（`branch/v1`），而且根本不需要什么字符识别，直接模板匹配就行了



## 查询域名权重


python3 seo.py -r ./domain.txt

域名列表
domain.txt


## 搜索

MagicBaidu
https://github.com/napoler/MagicBaidu?organization=napoler&organization=napoler


