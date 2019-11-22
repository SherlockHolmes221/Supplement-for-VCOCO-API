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


def visualization(name="train", action='hit', show_num=1, index=-1):
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

    # np.random.seed(1)
    # positive_index = np.where(vcoco['label'] == 1)[0]
    # positive_index = np.random.permutation(positive_index)
    positive_index = [index]

    cc = plt.get_cmap('hsv', lut=4)

    for i in range(show_num):
        id = positive_index[i]
        # get image
        path = 'train' if "train" in vcoco['file_name'][id] else "val"
        file_name = 'coco/images/' + path + '2014/' + str(vcoco['file_name'][id])
        print(file_name)
        im = np.asarray(Image.open(file_name))

        # scale
        sy = 4.
        sx = float(im.shape[1]) / float(im.shape[0]) * sy

        # draw image
        fig, ax = subplot(plt, (1, 1), (sy, sx))
        ax.set_axis_off()
        ax.imshow(im)

        print("label:", vcoco['label'][id], vcoco['role_object_id'][id])

        # draw bounding box for agent
        draw_bbox(plt, ax, vcoco['bbox'][[id], :], edgecolor=cc(0)[:3])

        role_bbox = vcoco['role_bbox'][id, :] * 1.
        role_bbox = role_bbox.reshape((-1, 4))

        for j in range(1, len(vcoco['role_name'])):
            if not np.isnan(role_bbox[j, 0]):
                draw_bbox(plt, ax, role_bbox[[j], :], edgecolor=cc(j)[:3])
                print("draw_bbox")
        plt.show()


def visualization_list():
    import json
    anno_file = json.load(open('for_no_frills/data_process/anno_list_gt.json', 'r'))

    for anno in anno_file:
        # if anno['global_id'] != '379666':
        #     continue

        file_name = 'coco/images/train2014/COCO_train2014_' + anno['global_id'].zfill(12) + '.jpg'
        print(file_name)

        cc = plt.get_cmap('hsv', lut=4)
        im = np.asarray(Image.open(file_name))

        # scale
        sy = 4.
        sx = float(im.shape[1]) / float(im.shape[0]) * sy

        # draw image
        fig, ax = subplot(plt, (1, 1), (sy, sx))
        ax.set_axis_off()
        ax.imshow(im)

        for hoi in anno['hois']:
            # draw bounding box for agent
            draw_bbox1(plt, ax, np.array(hoi['human_bboxes']), edgecolor=cc(0)[:3], cat="person")
            draw_bbox1(plt, ax, np.array(hoi['object_bboxes']), edgecolor=cc(1)[:3], cat=hoi['object'])
        plt.show()


def draw_bbox1(plt, ax, box, fill=False, linewidth=2, edgecolor=[1.0, 0.0, 0.0], cat=None, **kwargs):
    print(box)
    ax.add_patch(plt.Rectangle((box[0], box[1]),
                               box[2] - box[0], box[3] - box[1],
                               fill=fill, linewidth=linewidth, edgecolor=edgecolor, **kwargs))
    plt.text(box[0], box[1], cat)


if __name__ == '__main__':
    # visualization_list()
    visualization(name='test', action='run', show_num=1, index=7358)
