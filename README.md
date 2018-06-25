# 简道云 API接口调用演示

此项目为python开发环境下，调用简道云API接口进行表单字段查询和数据增删改查的示例。

具体API接口参数请参考帮助文档： https://hc.jiandaoyun.com/doc/10993

## 演示代码

演示工程使用了第三方的request框架，经过 Python 3.x 环境测试。

使用前首先安装相关依赖(推荐使用 virtualenv 配置测试环境)：

```bash
pip install -r requirements.txt
```

修改appId、entryId和APIKey

```python
appId = '5b1747e93b708d0a80667400'
entryId = '5b1749ae3b708d0a80667408'
api_key = 'CTRP5jibfk7qnnsGLCCcmgnBG6axdHiX'
```

按照表单配置修改请求参数

启动运行

```bash
python ./demo.py
```
