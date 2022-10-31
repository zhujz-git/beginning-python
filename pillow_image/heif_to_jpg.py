from PIL import Image
import pillow_heif
import glob


# 打开heif 转换成jpg
def heif_to_image(dir, imgname, filename):
    heif_file = pillow_heif.read_heif(filename)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )

    image.save(dir + '\\' + imgname + '.jpg', format("jpeg"))


if __name__ == '__main__':
    dir = 'D:\\娄桥市监所\\照片\\20221026 湾底巷45号列异'
    for img in glob.glob(dir + '\\*.heic'):
        # 获取文件名
        img_name = img.split('\\')[-1].split('.')[0]
        heif_to_image(dir, img_name, img)
