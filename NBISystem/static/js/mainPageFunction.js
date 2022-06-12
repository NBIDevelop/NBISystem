function mainPageInitProcess(){
    // 初始化滑块数值
    var slider = document.getElementById("brightnessAdjustRange");
    var value = document.getElementById("brightnessValue");
    slider.setAttribute("value", 0);
    value.innerText = 0;

    // 给与临时id
    var tempUserId = String(Date.parse(new Date())) + String(Math.ceil(Math.random()*9));
    document.getElementById("tempUserId").innerText = tempUserId;

    // 初始化触发器
}

// 这里仅仅是选择图片
function uploadBlueImage(){
    var blueBotton = document.getElementById("blueImageBotton");
    blueBotton.click();
}

function blueImageShowChange(){
    var blueBotton = document.getElementById("blueImageBotton");
    var imageShow = document.getElementById("icon_blue");
    var file = blueBotton.files[0]; // 获取input上传的图片数据;
    var read = new FileReader(); // 创建FileReader对像;
    read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
    read.onload = function() {
        var url = read.result; // 拿到读取结果;
        imageShow.src = url;
    }
    imageShow.className = "uploadImageShow";
}

function uploadGreenImage() {
    var greenBotton = document.getElementById("greenImageBotton");
    greenBotton.click();
}

function greenImageShowChange(){
    var greenBotton = document.getElementById("greenImageBotton");
    var imageShow = document.getElementById("icon_green");
    var file = greenBotton.files[0]; // 获取input上传的图片数据;
    var read = new FileReader(); // 创建FileReader对像;
    read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
    read.onload = function() {
        var url = read.result; // 拿到读取结果;
        imageShow.src = url;
    }
    imageShow.className = "uploadImageShow";
}

// 把前面选择好的图片上传
function checkInputAndUploadImage(){
    var blueBotton = document.getElementById("blueImageBotton");
    var greenBotton = document.getElementById("greenImageBotton");
    var tempUserId = document.getElementById("tempUserId");
    var offset = document.getElementById("brightnessAdjustRange").value;
    var isAutoTuneBrightness = document.getElementById("isAutoChangeBrightness").checked;

    var uploadButton = document.getElementById("uploadAllImage");
    uploadButton.innerText = "图片生成中...";
    var imageForm = new FormData();
    imageForm.append("image_blue", blueBotton.files[0]);
    imageForm.append("image_green", greenBotton.files[0])
    imageForm.append("user", tempUserId.innerText);
    imageForm.append("offset", offset);
    imageForm.append("autoBrightness", isAutoTuneBrightness);
    //通过ajax进行上传
    
    $.ajax({
        url: '/NBI/upload/',
        type: 'POST',
        cache: false,
        data: imageForm,
        async: true,
        processData: false,
        contentType: false,
    }).done(function (responseData) {
        if (responseData == 1){
            alert("请求方式错误！");
        }
        else if (responseData == 2){
            alert("请先选择输入图片！");
        }
        else if (responseData == 3){
            alert("图片处理错误！");
        }
        else{
            // console.log(responseData)
            alert(responseData)
            // 正常返回结果
            showResultImage(responseData);
        }
        uploadButton.innerText = "生成图片";
    });
}

function brightnessValueChange(){
    var slider = document.getElementById("brightnessAdjustRange");
    var bvalue = document.getElementById("brightnessValue");
    bvalue.innerText = slider.value;
}

function showResultImage(imageName){
    var container = document.getElementById("imgBackPart");
    var defaultText = document.getElementById("outImageDefault");
    if (defaultText != null) {
        defaultText.parentNode.removeChild(defaultText);
    }

    var lastResultImage = document.getElementById("resultImage");
    if (lastResultImage != null){
        lastResultImage.parentNode.removeChild(lastResultImage);
    }

    var resultImage = document.createElement("img");
    resultImage.id = "resultImage";
    resultImage.src = "/static/media/"+imageName;

    container.appendChild(resultImage);
}

function downloadResult(){
    // 检查是否存在生成图片
    var resultImage = document.getElementById("resultImage");
    if (resultImage == null){
        alert("请先点击生成图片！");
        return -1;
    }

    downloadByBlob(resultImage.src, "resultNBI.jps");
}

function downloadByBlob(url,name) {
    let image = new Image()
    image.setAttribute('crossOrigin', 'anonymous')
    image.src = url
    image.onload = () => {
        let canvas = document.createElement('canvas')
        canvas.width = image.width
        canvas.height = image.height
        let ctx = canvas.getContext('2d')
        ctx.drawImage(image, 0, 0, image.width, image.height)
        canvas.toBlob((blob) => {
            let url = URL.createObjectURL(blob)
            download(url,name)
            // 用完释放URL对象
            URL.revokeObjectURL(url)
        })
    }
}

function download(href, name) {
    let eleLink = document.createElement('a')
    eleLink.download = name
    eleLink.href = href
    eleLink.click()
    eleLink.remove()
}