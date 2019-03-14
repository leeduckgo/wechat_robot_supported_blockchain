from PIL import Image
import numpy as np
import cv2

def pic_to_handwork(pic_path, save_path):
    """
    图片转手绘
    :param pic_path:
    :param save_path:
    :return:
    """
    a = np.asarray(Image.open(pic_path)
                   .convert('L')).astype('float')

    depth = 10.0  # 浮点数，预设深度值为10
    grad = np.gradient(a)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像的梯度值
    grad_x = grad_x * depth / 120.  # 根据深度调整 x 和 y 方向的梯度值
    grad_y = grad_y * depth / 120.
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)  # 构造x和y轴梯度的三维归一化单位坐标系
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A

    vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
    vec_az = np.pi / 4.0  # 光源的方位角度，弧度值
    dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对 x 轴的影响，np.cos(vec_el)为单位光线在地平面上的投影长度
    dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对 y 轴的影响
    dz = np.sin(vec_el)  # 光源对 z 轴的影响

    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 梯度与光源相互作用，将梯度转化为灰度
    b = b.clip(0, 255)  # 为避免数据越界，将生成的灰度值裁剪至0‐255区间

    im = Image.fromarray(b.astype('uint8'))  # 重构图像
    im.save(save_path)  # 保存图片的地址
    # im.show()


def pic_to_cartoon(pic_path, save_path):
    """
    图片转卡通
    :param pic_path:
    :param save_path:
    :return:
    """
    imgInput_FileName = pic_path
    imgOutput_FileName = save_path
    num_down = 2         #缩减像素采样的数目
    num_bilateral = 7    #定义双边滤波的数目
    img_rgb = cv2.imread(imgInput_FileName)     #读取图片
    #用高斯金字塔降低取样
    img_color = img_rgb

    #重复使用小的双边滤波代替一个大的滤波
    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color,d=9,sigmaColor=9,sigmaSpace=7)
    #转换为灰度并且使其产生中等的模糊
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)
    #检测到边缘并且增强其效果
    img_edge = cv2.adaptiveThreshold(img_blur,255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=9,
                                     C=2)
    #转换回彩色图像
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    img_cartoon = cv2.bitwise_and(img_color, img_edge)
    # 保存转换后的图片
    cv2.imwrite(imgOutput_FileName, img_cartoon)
