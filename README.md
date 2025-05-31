# VisProject

## 安装 Node.js

### 安装 Node.js


* 在 [Node.js 官网](https://nodejs.org/en/) 下载安装包并安装。

* 双击安装包，一直点击下一步。

* 点击change按钮，更换到自己的指定安装位置，点击下一步（不修改默认位置也是可以的 ）。

* 一直点击下一步，最后安装成功即可。

在命令行界面输入

```shell
node -v
```

需要版本号大于等于 v22.14.0 才能正常运行。

### 修改环境变量

创建两个文件夹 `node_global` 及 `node_cache`，并将这两个文件夹添加到环境变量中。即输入指令：
```shell
npm config set prefix "<your_path>\node_global"
npm config set cache "<your_path>\node_cache"
```
其中 `<your_path>` 为你自己新建问价夹的路径，推荐新建在 `Node.js` 安装目录下。

### 新建环境变量

在 `系统变量` 下新建 `NODE_PATH`  变量，值为 `<your_path>\node_global\node_modules`

在 `系统变量` 下新建 `Path`  变量，值为 `<your_path>\node_global`

### 安装 npm

输入指令

```shell
npm install express -g
```

安装 express 包，`-g` 参数表示全局安装。

输入指令

```shell
npm -v
```

需要版本号大于等于 10.9.2

可以更换 npm 镜像源，如淘宝源。
```shell
   npm config set registry <yout_registry>
```

## 运行项目

安装必要的依赖

进入项目目录

```shell
cd src\VisProject
```

运行以下命令安装依赖

```shell
npm install
```

启动本地服务器

```shell
npm run dev
```
