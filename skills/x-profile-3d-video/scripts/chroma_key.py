# 绿幕抠图：python3 chroma_key.py in.jpg out.png
import sys, cv2, numpy as np
im = cv2.imread(sys.argv[1]).astype(np.float32)
b, g, r = im[..., 0], im[..., 1], im[..., 2]
d = g - np.maximum(r, b)                       # 绿色程度
a = 1 - np.clip((d - 25) / 60, 0, 1)           # 透明度
a = cv2.GaussianBlur(a, (3, 3), 0)
im[..., 1] = np.where(d > 0, np.minimum(g, np.maximum(r, b) + 10), g)  # 去绿边
out = np.dstack([im, a * 255]).astype(np.uint8)
ys, xs = np.where(a > 0.5)
out = out[max(0, ys.min() - 6):ys.max() + 6, max(0, xs.min() - 6):xs.max() + 6]
cv2.imwrite(sys.argv[2], out)
