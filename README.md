# <center>汉语新解</center>
基于 李继刚 所编写prompt ："汉语新解"的网页版的拓展应用
能够犀利、一针见血的解释抽象的网络热词，并生成简洁优雅的解释卡片。

## 1、网页内截图
主页面

生成卡片

## 2、docker-compose部署
1. 创建项目目录
```
mkdir -p /opt/hanyu-app
cd /opt/hanyu-app
```
3. git clone项目到本地
```
mkdir -p /opt/hanyu-app
```
4. 配置.env文件，填入实际的API密钥、URL和model
```
cp .env.example .env
vim .env
```
5. 创建日志目录并设置权限
```
mkdir -p logs
chmod 777 logs
```
6. 构建和启动容器
```
docker-compose up -d --build
```
