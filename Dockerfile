FROM python:3.9
# 设置工作目录
WORKDIR /app
# 复制依赖文件到镜像中
COPY requirements.txt /app/
# 安装依赖
RUN pip3 install --no-cache-dir -r requirements.txt
# 复制应用程序代码到镜像中
COPY . /app
# 运行容器时执行的命令
CMD ["python3", "main.py"]
