"# wx_oslo" 
# 需求分析
## 项目名称
> 基于公众号测试号

## 具体需求
- 根据用户关注后发的关键字进行分组

## 附加说明
> linux 下运行项目

# 运行测试
## 导入环境变量
export AppID= && export AppSecret=
## 启动
python manage.py runserver 0.0.0.0:80

# ubuntu编码问题
## 安装 sudo apt-get -y install language-pack-zh-hans
vim /var/lib/locales/supported.d/local
> 加入：en_US.UTF-8 UTF-8
vim /etc/default/locale
> 加入： LANG="zh_CN.UTF-8"
        LANGUAGE="zh_CN:zh"
        LC_ALL="zh_CN.UTF-8"
>终端输入 dpkg-reconfigure locales
> locale