# zks era 撸毛脚本

## 使用方式
### 下载

通过`github`下载

### 配置环境
* 打开powershell
* 切换虚拟环境
* 运行demo.py
## 准备 Prepare
### python 安装
版本：**3.10.11** [downlown](https://www.python.org/downloads/release/python-31011/)

**踩坑** 
- 3.11版本无法安装pysha3包
- 3.6版本直接搜索不到包

**升级pip 23.2**
```bash
python -m pip install --upgrade pip
```

**安装依赖包**

`pip install zksync2`

**安装过程中出现问题**
```
Building wheels for collected packages: pysha3
  Building wheel for pysha3 (pyproject.toml) ... error
  error: subprocess-exited-with-error

  │ exit code: 1
  ╰─> [9 lines of output]
      running bdist_wheel
      running build
      running build_py
      creating build
      creating build\lib.win-amd64-cpython-310
      copying sha3.py -> build\lib.win-amd64-cpython-310
      running build_ext
      building '_pysha3' extension
      error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pysha3
Failed to build pysha3
ERROR: Could not build wheels for pysha3, which is required to install pyproject.toml-based projects
```

原因：未安装C++编译器，无法编译

解决方案：

下载 [`Microsoft C++ Build Tools`](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 并安装。

安装过程中切换`单个组件`，勾选`Window 10 SDK`

安装好之后启动，然后重新运行 `pip` 安装命令。

### 创建Metamask钱包

#### 安装Chrome插件
[下载地址](https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn)

备好 **密码** 和 **助记词**

查看 **账户地址** 和 **private key**

## 开发 Develop
