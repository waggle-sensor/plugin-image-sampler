FROM waggle/plugin-base:1.1.1-base

# COPY app.py /app/
COPY app.py requirements.txt /app/
RUN pip3 install --no-cache-dir -U -r /app/requirements.txt

ENTRYPOINT ["python3", "-u", "/app/app.py"]
