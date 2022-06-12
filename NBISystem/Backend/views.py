import random

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image as pillowImage
from Model.NBIGenerator import getNBIImage
import cv2

# 处理单张提交图片
@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        # image_blue=pillowImage(request.FILES.get('image_blue'))
        # image_green=pillowImage(request.FILES.get('image_green'))
        user=request.POST.get('user')
        offset = int(request.POST.get("offset"))
        isAutoBrightness = request.POST.get("autoBrightness") == 'true'
        print("\tUSER ID: {uid}\n\tOffset: {off}\n\tautoBrightness: {ab}".format(uid=user, off=offset, ab=isAutoBrightness))

        image_blue = request.FILES.get("image_blue")
        image_green = request.FILES.get("image_green")
        # 检查是否为空，若为空则没有选择图片
        if image_green is None or image_blue is None:
            # 返回2表示未选中图片则提交
            return HttpResponse(2)

        # 处理图片
        try:
            image_blue = pillowImage.open(image_blue)
            image_green = pillowImage.open(image_green)
            # 返回一个pillow类型的图片
            resultImage = getNBIImage(
                image_blue=image_blue,
                image_green=image_green,
                isAutoCutImage=False, # TODO
                isAutoProcessImage=isAutoBrightness,
                offset=offset
            )
        except Exception:
            # 返回3表示图片处理过程中出现问题
            return HttpResponse(3)

        resultName = "result_{uid}_{rand}.jpg".format(uid=user,rand=random.randint(0,100))
        cv2.imwrite("./static/media/"+resultName, resultImage)

        return HttpResponse(resultName)
    else:
        # 返回1表示请求方式错误
        return HttpResponse(1)

def mainPage(request):
    return render(request, 'mainPage.html')
