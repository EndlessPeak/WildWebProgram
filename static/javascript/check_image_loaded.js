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


// 在页面加载时赋给脚本路径的参数，并本地存储
window.addEventListener('DOMContentLoaded', function () {
    var url = "{{ url }}";
    // 将图片路径保存到 LocalStorage
    localStorage.setItem("infer_image_path", url);
    document.getElementById("infer-image-container").src = url;
});