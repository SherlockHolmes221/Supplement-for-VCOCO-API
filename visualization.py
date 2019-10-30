import __init__
import vsrl_utils as vu
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image


def draw_bbox(plt, ax, rois, fill=False, linewidth=2, edgecolor=[1.0, 0.0, 0.0], **kwargs):
    for i in range(rois.shape[0]):
        roi = rois[i, :].astype(np.int)
        ax.add_patch(plt.Rectangle((roi[0], roi[1]),
                                   roi[2] - roi[0], roi[3] - roi[1],
                                   fill=fill, linewidth=linewidth, edgecolor=edgecolor, **kwargs))


def subplot(plt, Y_X, sz_x_y=(10, 10)):
    plt.rcParams['figure.figsize'] = (Y_X[1] * sz_x_y[0], Y_X[0] * sz_x_y[1])
    fig, axes = plt.subplots(Y_X[0], Y_X[1])
    return fig, axes


def visualization(name="train", action='hit', show_num=5):
    assert name == 'train' or name == 'trainval' or name == 'val' or name == 'test', \
        "illegal name "

    # Load COCO annotations for V-COCO images
    # instances_vcoco_all_2014.json images+annotations
    coco = vu.load_coco()

    # Load the VCOCO annotations for vcoco_train image set
    vcoco_data = vu.load_vcoco('vcoco_' + name)

    # train_data add bbox and role_bbox
    for x in vcoco_data:
        x = vu.attach_gt_boxes(x, coco)

    classes = [x['action_name'] for x in vcoco_data]
    cls_id = classes.index(action)
    vcoco = vcoco_data[cls_id]

    np.random.seed(1)
    positive_index = np.where(vcoco['label'] == 1)[0]
    positive_index = np.random.permutation(positive_index)
    cc = plt.get_cmap('hsv', lut=4)

    for i in range(show_num):
        id = positive_index[i]
        # get image
        file_name = 'coco/images/' + name + '2014/' + str(vcoco['file_name'][id])
        print(file_name)
        im = np.asarray(Image.open(file_name))

        # scale
        sy = 4.
        sx = float(im.shape[1]) / float(im.shape[0]) * sy

        # draw image
        fig, ax = subplot(plt, (1, 1), (sy, sx))
        ax.set_axis_off()
        ax.imshow(im)

        # draw bounding box for agent
        draw_bbox(plt, ax, vcoco['bbox'][[id], :], edgecolor=cc(0)[:3])

        role_bbox = vcoco['role_bbox'][id, :] * 1.
        role_bbox = role_bbox.reshape((-1, 4))

        for j in range(1, len(vcoco['role_name'])):
            if not np.isnan(role_bbox[j, 0]):
                draw_bbox(plt, ax, role_bbox[[j], :], edgecolor=cc(j)[:3])
                print("draw_bbox")
        plt.show()


if __name__ == '__main__':
    visualization(name='train', action='carry', show_num=5)
