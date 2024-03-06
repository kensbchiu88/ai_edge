# 第一阶段：构建应用程序和安装依赖
FROM python:3.10-buster AS builder
 
ENV PYTHONUNBUFFERED=1
 
WORKDIR /app
 
COPY requirements.txt .
 
# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt
 
# 第二阶段：构建最终镜像
FROM python:3.10-slim-buster
 
ENV PYTHONUNBUFFERED=1
 
WORKDIR /app
 
# 从第一阶段复制依赖
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
 
# 复制应用程序代码
COPY . .
 
# 清理不需要的文件
RUN rm -rf /root/.cache
 
# 启动应用程序
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]