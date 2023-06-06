from PIL import Image

# 打开原始图像
image = Image.open("smcalc_logo_1024.png")

# 处理不同尺寸的图像
sizes = [180,60,120,167,152,1024]


for size in sizes:
    # 调整图像大小
    resized_image = image.resize((size, size), resample=Image.BILINEAR)
    
    # 构造新文件名
    filename = f"smcalc_icon_{size}.png"
    
    # 保存新图像
    resized_image.save(filename)