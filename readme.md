
# FAFU Network Login Script

这是一个用于自动登录FAFU网络的Python脚本。它可以通过命令行接收用户信息，并尝试使用提供的凭据登录到指定的网络。

## 功能

- 接受用户名、密码和后缀作为命令行参数。
- 支持通过SOCKS5代理进行登录。
- 等待一定时间后尝试登录，以跳过封禁时间。
- 解析登录页面的隐藏参数，并使用这些参数进行登录。

## 安装

在开始使用之前，请确保你的环境中已安装以下依赖：

- requests
- beautifulsoup4
- argparse

你可以通过以下命令安装这些依赖：

```bash
pip install requests bs4 argparse
````

## 使用方法

使用以下命令行参数启动脚本：

```bash
python login_script.py -u <username> -p <password> -s <suffix> -s5 <socks5_proxy> -t <time_sleep>
```

- `-u`, `--username`: 用户名
- `-p`, `--password`: 密码
- `-s`, `--suffix`: 运营商 [中国移动：@cmcc,中国电信：@telecom,中国联通：@unicom]
- `-s5`, `--socks5_proxy`: SOCKS5代理地址（可选），理论可以写http代理地址
- `-t`, `--time_sleep`: 登录前等待的时间（秒）（可选，默认为300秒）

## 示例

```bash
python login_script.py -u your_username -p your_password -s your_suffix
```

如果你需要通过SOCKS5代理进行登录，可以添加`-s5`参数：

```bash
python login_script.py -u your_username -p your_password -s your_suffix -s5 "socks5://127.0.0.1:1080"
```

## 注意事项

- 确保提供的用户名、密码和后缀是正确的。
- 如果使用代理，请确保代理服务器是可用的。
- 该脚本可能需要根据FAFU网络的实际登录页面进行调整。

## 贡献

如果你有任何改进建议或发现问题，欢迎提交Issue或Pull Request。