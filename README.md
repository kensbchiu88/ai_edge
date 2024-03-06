# tricolor_light_inference
#### 三色燈判別系統
透過標記Camera rtsp streaming中三色燈的位置，擷取影像中的三色燈圖片，並使用Hugging Face的model判斷三色燈的顏色，並將結果送至MQTT Broker


## Run
Build the Docker image
```
docker build -t my_python_310_code --target builder .
```