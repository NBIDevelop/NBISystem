import math
import numpy as np
import cv2
from PIL import Image

# get NBI Image
def getNBIImage(image_blue, image_green, isAutoCutImage=False, isAutoProcessImage=False, offset=0):
    print("Input Image Size:\n\tBlue Image:{b}\n\tGreen Image:{g}".format(b=image_blue.size, g=image_green.size))
    if not image_blue.size == image_green.size:
        print("The Image Size Should be the same")
        if isAutoCutImage:
            print("Auto Cute Image to Same Size.")
            # 自动裁剪
            image_blue, image_green = autoCutImage(image_blue, image_green)
        else:
            return

    image_blue = pillow2cv2(image_blue)
    image_green = pillow2cv2(image_green)

    # 得到灰度图片
    gray_blue, gray_green = getGrayImage(image_blue, image_green)
    # cv2.imwrite('blue.jpg', gray_blue)
    # cv2.imwrite('green.jpg', gray_green)
    # print(getBrightness(gray_blue), getBrightness(gray_green))

    # 根据输入再次调整亮度
    gray_blue = updateBrightness(gray_blue, offset)
    gray_green = updateBrightness(gray_green, -1*offset)

    # 融合通道
    # r来自绿色灰度，g和b来自蓝色灰度
    # merge 是按照BGR格式合并
    mergeImage = cv2.merge([gray_blue, gray_blue, gray_green])

    # 输出前自动调整图片整体亮度以便于观测
    if isAutoProcessImage:
        mergeImage = aug(mergeImage)

    print("Get NBI Image Success.")
    return mergeImage

# 计算灰度图片，并且调整他们的亮度让后面合成的图片不会出现色彩偏移
def getGrayImage(image_blue, image_green, strength=0.4):
    # 转换为灰度图片
    gray_green = cv2.cvtColor(image_green, cv2.COLOR_BGR2GRAY)
    gray_blue = cv2.cvtColor(image_blue, cv2.COLOR_BGR2GRAY)

    # 调整色阶，使色阶更均匀
    out_blue = np.zeros(gray_blue.shape, gray_blue.dtype)
    cv2.normalize(gray_blue, out_blue, 255 * 0.05, 255 * 0.9, cv2.NORM_MINMAX)
    out_green = np.zeros(gray_green.shape, gray_green.dtype)
    cv2.normalize(gray_green, out_green, 255 * 0.05, 255 * 0.9, cv2.NORM_MINMAX)

    # 根据调整后的亮度进一步调整亮度，使得二者亮度一致
    averageBrightness = (getBrightness(out_blue)+getBrightness(out_green))/2
    out_blue = updateBrightness(out_blue, strength * (averageBrightness - getBrightness(out_blue)))
    out_green = updateBrightness(out_green, strength * (averageBrightness - getBrightness(out_green)))

    return out_blue, out_green

# 线性调整亮度
def updateBrightness(image, adjust):
    image = np.uint8(np.clip((1.1*image + adjust), 0, 255))
    return image

# 计算图片亮度,只针对单通道灰度图
def getBrightness(image):
    return cv2.mean(image)[0]

# 计算色阶分位点，⽬的是去掉的直⽅图两头的异常情况
def compute(img, min_percentile, max_percentile):
    """计算分位点，⽬的是去掉的直⽅图两头的异常情况"""
    max_percentile_pixel = np.percentile(img, max_percentile)
    min_percentile_pixel = np.percentile(img, min_percentile)
    return max_percentile_pixel, min_percentile_pixel

# 自动增强图片亮度
def aug(src):
    """图像亮度增强"""
    if src[:,:,2].mean()>130:
        return
    # 先计算分位点，去掉像素值中少数异常值，这个分位点可以⾃⼰配置。
    # ⽐如1中直⽅图的红⾊在0到255上都有值，但是实际上像素值主要在0到20内。
    max_percentile_pixel, min_percentile_pixel = compute(src, 0.5, 99.5)
    # 去掉分位值区间之外的值
    src[src>=max_percentile_pixel] = max_percentile_pixel
    src[src<=min_percentile_pixel] = min_percentile_pixel
    # 将分位值区间拉伸到0到255，这⾥取了255*0.05与255*0.9是因为可能会出现像素值溢出的情况，所以最好不要设置为0到255。
    out = np.zeros(src.shape, src.dtype)
    cv2.normalize(src, out, 255*0.02, 255*0.88,cv2.NORM_MINMAX)
    return out

def autoCutImage(image_blue, image_green):
    minWidth = min(image_blue.size[0], image_green.size[0])
    minHeight = min(image_blue.size[1], image_green.size[1])
    blue_left = math.ceil((image_blue.size[0] - minWidth) / 2)
    green_left = math.ceil((image_green.size[0] - minWidth) / 2)
    blue_top = math.ceil((image_blue.size[1] - minHeight) / 2)
    green_top = math.ceil((image_green.size[1] - minHeight) / 2)
    image_blue = image_blue.crop((blue_left, blue_top, blue_left + minWidth, blue_top + minHeight))
    image_green = image_green.crop((green_left, green_top, green_left + minWidth, green_top + minHeight))
    return image_blue, image_green

# PIL to cv2
def pillow2cv2(image):
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

# cv2 to PIL
def cv22pillow(image):
    return Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))

# for test
def showChannel(image):
    zeros = np.zeros(image.shape[:2], dtype="uint8")
    B, G, R = cv2.split(image)
    cv2.imshow("DISPLAY BLUE COMPONENT", cv2.merge([B, zeros, zeros]))  # 显示(B,0,0)图像
    cv2.imshow("DISPLAY GREEN COMPONENT", cv2.merge([zeros, G, zeros]))  # 显示(0,G,0)图像
    cv2.imshow("DISPLAY RED COMPONENT", cv2.merge([zeros, zeros, R]))
    cv2.waitKey()

"""function test"""
# 415nm是blue
# 540nm是green

# img_blue = Image.open(r"../static/media/B_1.jpg")
# img_green = Image.open(r"../static/media/G_1.jpg")
# img_blue = Image.open(r"../static/media/1-415nm.jpg")
# img_green = Image.open(r"../static/media/1-540nm.jpg")

# getNBIImage(image_blue=img_blue, image_green=img_green, isAutoCutImage=True, isAutoProcessImage=True, offset=12)