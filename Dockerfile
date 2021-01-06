FROM waggle/plugin-opencv:4.1.1

LABEL version="0.1.0" \
      description="Image sampler"

COPY app.py requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/app.py"]
