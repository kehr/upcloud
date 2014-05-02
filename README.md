# upcloud

这个项目的目标是实现`云空间本地化管理`。你可以用本项目提供的操作同步或备份你的云空间数据。

**Github:**  https://github.com/kehr/upcloud  
**GitCafe:** https://gitcafe.com/kehr/upcloud-for-UPYUN   
**投票地址:** http://upyun.gitcafe.com/projects?category=top50      
**项目名:** upcloud-for-UPYUN   


   
**如果你觉得这东西挺有意思，请投上你宝贵的一票吧！你的支持是我最大的动力，先谢过！**继续码字符去了。

正在紧张的开发中...

##安装  

```bash
sudo pip install upcloud
```
该项目正在开发，目前发布版本是`0.1.2`。最新版本会修复bug，完善命令功能，更加易用。  
你可以使用`sudo pip install upcloud --upgrade`升级你当前使用的版本（强烈建议！）  

感谢你的支持！欢迎提出你的意见和想法。

##使用 

```bash
upcloud -b BUCKET -u USERNAME -p PASSWD
```
获取命令帮助:`command [-h|--help]`  
获取详细说明:`man [command]`

##特色  

1. 支持命令历史回滚

2. 支持`<Tab>`键命令补全  

3. 支持`<Tab> <Tab>` 显示命令列表

4. 支持执行shell命令  

5. 支持清屏操作  

6. 支持文件批量上传   

7. 内置bash环境，可以使用命令`bash` 进入  
......  

以上特性已经完成，其它小特性待完成后补充。总之，就是让你感觉操作云空间就像操作你本地空间一样爽快。这也是这个项目的目标和动力。

正在实现，当前目录下文件名自动补全。这个我觉得比较给力～

##History:  
2014-5-01 完成put命令批量上传，重构部分代码。  
2014-4-30 完成参数解析和90%命令的实现。  
2014-4-25 完成终端命令交互和基本帮助文档。正在解析参数，调试与 upyun空间 的交互。  
2014-4-17 根据文档，开始敲代码，初始化仓库。本地完成部分功能测试。    
2014-4-16 创建项目，开始查资料，敲代码。其实我也不会⊙﹏⊙b汗！  

##TODO   

1. 实现get命令和cat命令  
2. 测试和重构代码  
3. 完善帮助文档

(P.S. 又拍云的SDK用起来真不好受::cry::)
