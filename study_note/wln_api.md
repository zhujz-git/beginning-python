# 万里牛OpenApi准备

正式环境
https://erp-open.hupun.com/api/v1/

万里牛联调账号
公司：万里牛对接测试
登入地址：https://erp.hupun.com/login
账号：836680073@qq.com密码：qw123456.
账号2：1477398766@qq.com 密码 qw123456.
b2c接口（正式环境）：
appkey：5R5U6S7
appsecret：62CBC8F3A4553E529D309A337CBF995C
open接口（正式环境）： 
appkey：3823532979
appsecret：ea5b29320cb3d15a9883c1fa4654bd02
api接口文档地址：http://open-doc.hupun.com/#/api
如需要个人测试账号，联系管理员添加。
在线时间段如下：
工作日（上午9.00——12.00 下午13.30——18.30）
为了方便更效率解决您的问题，请安排在合理时间咨询。其他erp业务问题可以直接咨询在线客服同学，本群只提供api对接支持！

生成规则:密钥+请求参数+密钥，MD5加密后得到（密钥为万里牛提供）。
具体规则：
根据参数名称将所有请求参数（包括业务参数）按照字母先后顺序排序:key + value .... key +value
例如：将foo=1,bar=2,baz=3 排序为bar=2,baz=3,foo=1，参数名和参数值链接后，得到拼装字符串bar=2&baz=3&foo=1。
系统目前支持MD5加密方式:将密钥 拼接到参数字符串头、尾进行md5加密后，得到32位结果，格式如下： md5(secretkey1=value1&key2=value2...secret)
其中value需要url encode

 

PS: 有个用户使用C#计算签名，一直不通，后来经用户查验，原来是url encode的结果不同，java是大写的，C#是小写的（未验证是否如此），最好url encode转码的时候弄成大写的

建议使用HttpUtility.UrlEncode进行编码，参考https://blog.csdn.net/ma_jiang/article/details/81283209