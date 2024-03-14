# tricolor_light_inference
#### 三色燈顏色辨識系統
透過元件標記系統中取得Camera rtsp streaming中三色燈的位置，擷取影像中的三色燈圖片，並使用Hugging Face的model判斷三色燈的顏色，並將結果送至MQTT Broker

## Run
```
docker compose up -d
```