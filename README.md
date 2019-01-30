# CloudLink Demo

## 知识tab免登陆集成示例

使用步骤：
- 环境准备python27 ,通过virtualenv venv 安装好虚拟环境
- 下载代码到本地
- pip install -r requirements.txt
- 配置config信息，换成微码平台创建应用时生成client_id 和 client_secret, 为了安全建议保存在本地环境中
- 配置knowledge_entity信息（非必需），为了演示需要，请修改为真实的用户id
- cd 到当前目录并激活虚拟环境
- 在终端中运行 python application.py
- 本地运行访问：http://127.0.0.1:5000/knowledge/ 可以看到效果

>由于app.js调用HWH5.getAuthCode的方法需要在真机上才能调用, 因此当你在本地运行起来时，无法获取到用户信息，建议部署在服务器上进行真实地址测试

Demo实现的逻辑：
- 服务端/userid/的地址，判断用户是否在手机上有cookie，如果有获取用户身份，并返回相应资源；如果没有返回匿名内容，这可以根据实际业务场景来设定
- 手机端用户首次或者cookie失效的时候，弹出模态窗口，此时在模态窗口会获取用户身份信息，成功后重新打开当前页面

## python SDK使用说明

- SDK目录结构
```
    cloudlinkpy
        |_ cloudlink
            |_ models
                |_ users.py
                |_ __init__py
            |_ __init__.py
        |_ helpers
            |_ error.py
            |_ __init__.py
        |_ __init__.py
        |_ __client.py
```
- 配置auth.ini，配置client_id 和 client_secret 等信息
- cd app 然后运行 python demo.py
- 点击Following URL 手动获取code, 并配置在input中，回车
> CloudLink不提供获取code服务接口，此处/auth/authorize服务做了
服务调用次数限制(每分钟3次，每天100次)仅满足做日常的调试，正式code获取请通过[开放平台文档](https://cloudlinkworkplace.huaweicloud.com/wecode/docs/dev/serverapi/authentication/wecode.html)
- 可以看到Terminal打印出access_token及用户信息，表示调用成功



## 更新内容

- 知识页面演示示例
- 补充cloudlink python SDK: cloudlinkpy 1.0