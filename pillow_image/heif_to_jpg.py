from PIL import Image
import pillow_heif
import os
import re

# 打开heif 转换成jpg
def heif_to_image(dir, heic, filename):
    heif_file = pillow_heif.read_heif(dir+'\\'+heic)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )

    image.save(dir + '\\'+filename + '.jpg', format("jpeg"))

# 遍历文件夹下所有的heic文件
def get_all_change(dir):
    pat = re.compile('(.+)\.heic')
    img_list = [(n, pat.match(n).group(1)) for n in list(os.walk(dir))[0][2]
                if pat.match(n)]
    for img in img_list:
        heif_to_image(dir, img[0], img[1])

if __name__ == '__main__':
    dir = 'D:\\娄桥市监所\\照片\\20220825 云泰查封'
    get_all_change(dir)