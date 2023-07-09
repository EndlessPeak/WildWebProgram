function checkImageLoaded() {
    var img = document.getElementById('image-container');
    if (img.complete && img.naturalWidth !== 0) {
        // 图片加载成功
        location.reload();  // 刷新页面
    } else {
        // 图片尚未加载完成，继续轮询检查
        setTimeout(checkImageLoaded, 1000);  // 每隔1秒检查一次
    }
}

// 在页面加载完成后启动轮询检查
window.addEventListener('load', function () {
    checkImageLoaded();
});