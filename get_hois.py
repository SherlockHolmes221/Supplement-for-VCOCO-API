import __init__
import vsrl_utils as vu
import os
from pycocotools.coco import COCO
import save_hios
import numpy as np

coco = COCO(os.path.join('coco/annotations/', 'instances_trainval2014.json'))

# return COCO all data in train_val_test
v_coco_all = vu.load_coco()


def get_data(name, data_dict, is_positive=False):
    vcoco = vu.load_vcoco('vcoco_' + name)
    posivive_labels = [np.where(i['label'] != 0)[0] for i in vcoco]

    print(len(vcoco))

    for k in range(len(vcoco)):  # len=26
        x = vcoco[k]
        action_name = x['action_name']
        for i in range(1, len(x['role_name'])):
            if not is_positive:
                anno_num = vcoco[0]['ann_id'].shape[0]
                anno_list = range(anno_num)
            else:
                anno_list = posivive_labels[k]
            for j in anno_list:
                if x['role_object_id'][j][i] > 0:

                    # get ann_id
                    ann_id = x['role_object_id'][j][i]
                    # print("ann_id", ann_id)
                    # get ann
                    anns = coco.loadAnns([ann_id])
                    # get cats name
                    cat_name = coco.loadCats([anns[0]['category_id']])[0]['name']
                    # print("cat_name", cat_name)
                    # print(type(cat_name))
                    temp_dict = {}
                    temp_dict[name] = temp_dict.get(name)

                    key = action_name + "/" + cat_name
                    d = data_dict.get(key, {})
                    if not d:
                        d[name] = 1
                    elif not d.get(name, {}):
                        d[name] = 1
                    else:
                        d[name] = d[name] + 1

                    data_dict[key] = d
        # break

    print(len(data_dict))
    # print(data_dict)

    return data_dict


def get_all(is_positive=False):
    data_dict = {}
    data_dict = get_data("train", data_dict, is_positive=is_positive)
    data_dict = get_data("val", data_dict, is_positive=is_positive)
    # data_dict = get_data("trainval", data_dict, is_positive=is_positive)
    data_dict = get_data("test", data_dict, is_positive=is_positive)
    # save_hios.save_hois_txt_total(data_dict, name="all_positive" if is_positive else "all")
    save_hios.save_hois_txt_total_json(data_dict, name="all_positive" if is_positive else "all")


if __name__ == '__main__':
    get_all(True)
