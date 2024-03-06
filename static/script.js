// JavaScript代码用于处理图像标注的交互逻辑

// 获取canvas元素和绘图上下文
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');

// 获取标注信息的API端点
const getRectanglesUrl = '/rectangles/';

// 在页面加载完成后执行
window.onload = function() {
    // 从API获取标注信息并绘制矩形
    fetch(getRectanglesUrl)
        .then(response => response.json())
        .then(rectangles => {
            rectangles.forEach(rectangle => {
                drawRectangle(rectangle);
            });
        });
};

// 绘制矩形函数
function drawRectangle(rectangle) {
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 2;
    ctx.strokeRect(rectangle.x1, rectangle.y1, rectangle.x2 - rectangle.x1, rectangle.y2 - rectangle.y1);

    // 绘制文本
    if (rectangle.text) {
        ctx.fillStyle = 'blue';
        ctx.font = '16px Arial';
        ctx.fillText(rectangle.text, Math.min(rectangle.x1, rectangle.x2), Math.min(rectangle.y1, rectangle.y2) - 5);
    }
}
