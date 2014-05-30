# upcloud

![upload](./img/upload.png)
![upload](./img/ls.png)


这个项目的目标是实现 **云空间本地化管理**。你可以用本项目提供的操作同步或备份你的云空间数据。


**Github:**  https://github.com/kehr/upcloud  
**GitCafe:** https://gitcafe.com/kehr/upcloud-for-UPYUN   
**投票地址:** http://upyun.gitcafe.com/projects?category=top50      
**项目名:** upcloud-for-UPYUN   


   
**如果你觉得这东西挺有意思，请投上你宝贵的一票吧！你的支持是我最大的动力，先谢过！**继续码字符去了。


目前所有预计实现的命令已经完成，正在测试和重构代码。 


###现在提供测试账号一枚：

**空间名(bucket):**  kehrspace   

**用户名:** test01   

**密码:** testtest

空间内文件都是测试文件，请不要上传私人文件，测试账号会在比赛结束后自动停用。如果你发现bug，提出issue，我会尽快回复。欢迎fork和star，这不仅仅是比赛，也是一个学习的过程。


##安装  

```bash
sudo pip install upcloud
```
该项目正在开发，目前发布版本是`v0.1.5 alpha`。最新版本会修复bug，完善命令功能，更加易用。  
你可以使用`sudo pip install upcloud --upgrade`升级你当前使用的版本（ **强烈建议！**）  

感谢你的支持！欢迎提出你的意见和想法。

##使用 

```bash
upcloud -b BUCKET -u USERNAME -p
```
获取命令帮助:`command [-h|--help]`  
获取详细说明:`man [command]`

如果使用过程中出现文件不存在错误，请使用命令`ls -r`刷新本地缓存。   

##文档   

**参考在线使用教程：**[Tutorial](docs/README.md)  
下载文档：[Tutorial](docs/Tutorial.pdf)

##特色  

1. 支持命令历史回滚

2. 支持`<Tab>`键命令补全  

3. 支持`<Tab> <Tab>` 显示命令列表

4. 支持执行shell命令  

5. 支持清屏操作  

6. 支持文件批量上传/下载，自定义目录结构   

7. 内置bash环境，可以使用命令`bash` 进入  

8. 支持在线查看文件内容

9. 支持当前工作目录下，文件名自动补全  

10. 支持显示上传下载进度条  
. . . . . .  

以上特性已经完成，其它小特性待完成后补充。总之，就是让你感觉操作云空间就像操作你本地空间一样爽快。这也是这个项目的目标和动力。


##History:    
2014-5-24 增加上传下载进度条    
2014-5-10 完成Tutorial手册   
2014-5-09 完成当前工作目录下文件名自动补全和所有命令帮助文档    
2014-5-03 发布0.1.3 alpha,优化部分代码   
2014-5-02 完成所有命令   
2014-5-01 完成put命令批量上传，重构部分代码。  
2014-4-30 完成参数解析和90%命令的实现。  
2014-4-25 完成终端命令交互和基本帮助文档。正在解析参数，调试与 upyun空间 的交互。  
2014-4-17 根据文档，开始敲代码，初始化仓库。本地完成部分功能测试。    
2014-4-16 创建项目，开始查资料，敲代码。其实我也不会⊙﹏⊙b汗！  

##TODO   

1. 实现复制和重命名文件/文件夹  
2. 测试和重构代码  

SDK问题已经解决了，项目还有点小问题，我再倒腾倒腾。

##Other    
已经安顿下来了，在京的小伙伴，求交流，求学习！
    
