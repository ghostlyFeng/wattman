import cv2
import argparse



def imagePadding(src, mask, h_ratio=0.5, w_ratio=0.5):

    src = cv2.imread(src)
    mask = cv2.imread(mask)

    assert src.shape[2] == mask.shape[2]

    # 原图的高度和宽度
    height_src = src.shape[0]
    width_src = src.shape[1]

    #按比例计算覆盖中心点
    h = height_src * h_ratio
    w = width_src * w_ratio

    # 叠加图的高度和宽度
    height_mask = mask.shape[0]
    width_mask = mask.shape[1]

    left_top = int(h-height_mask/2)
    right_top = int(h+height_mask/2)
    left_bottom = int(w-width_mask/2)
    right_bottom = int(w+width_mask/2)

    #解决mask尺寸比src大的情况
    if left_top < 0:
        left_top = 0
    if right_top > height_src:
        right_top = height_src
    if left_bottom < 0:
        left_bottom = 0
    if right_bottom > width_src:
        right_bottom = width_src

    if height_src < height_mask or width_src < width_mask:
        h_new = height_mask * h_ratio
        w_new = width_mask * w_ratio
        src[left_top:right_top, left_bottom:right_bottom, :] = mask[int(h_new-height_src/2):int(h_new+height_src/2),int(w_new-width_src/2):int(w_new+width_src/2),:]
    else:
        src[left_top:right_top, left_bottom:right_bottom, :] = mask
    return src


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="Source image path")
    parser.add_argument("mask", type=str, help="Paste image path")
    parser.add_argument("s_p", type=str, default=".", help="Save path")
    parser.add_argument("h_r", type=float, default=0.5, help="Height ratio")
    parser.add_argument("w_r", type=float, default=0.5, help="Width ratio")
    args = parser.parse_args()


    res = imagePadding(args.src, args.mask, args.h_r, args.w_r)
    cv2.imwrite("result.png", res)

    # cv2.imshow("result", res)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
