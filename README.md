# AI Edge
## Description

賦予邊緣計算AI相關的功能。功能如下:

#### 元件標記

標記Camera rtsp streaming中需要辨識元件(三色燈，文字，指針式儀表等)的位置，提供給辨識系統，讓辨識系統可抓取影像中的元件進行辨識。

#### 三色燈顏色辨識

透過元件標記系統中取得Camera rtsp streaming中三色燈的位置，擷取影像中的三色燈圖片，並使用Hugging Face的model判斷三色燈的顏色，並將結果送至MQTT Broker

## 目錄

- object_labeling : 元件標記系統
- tricolor_light_inference : 三色燈顏色辨識系統

## 系統架構

[系統架構介紹](https://hackmd.io/47qOWgqjRde3-J2l0fY5ww)

## 測試環境安裝

#### RTSP Server(optional)

可在local環境中模擬攝影機的RTSP Streaming
- [happytime-rtsp-server](https://happytimesoft.com/)
