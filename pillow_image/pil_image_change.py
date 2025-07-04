from PIL import Image
import numpy as np

a = np.array(
    Image.open('./pillow_image/zhujinzhou.jpg').convert('L')).astype('float')

depth = 10.0

#取图像灰度值
grad = np.gradient(a)
grad_x, grad_y = grad
grad_x = grad_x * depth / 100
grad_y = grad_y * depth / 100
A = np.sqrt(grad_x**2 + grad_y**2 + 1.0)
uni_x = grad_x / A
uni_y = grad_y / A
uni_z = 1.0 / A

#光源俯视效果
vec_el = np.pi / 2.2
vec_az = np.pi / 4.
dx = np.cos(vec_el) * np.cos(vec_az)
dy = np.cos(vec_el) * np.sin(vec_az)
dz = np.sin(vec_el)

b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)
b = b.clip(0, 255)

im_c = Image.fromarray(b.astype('uint8'))

im_c.save('./pillow_image/zhujinzhou5.jpg')