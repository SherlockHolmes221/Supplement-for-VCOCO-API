import io_utils as io

import vsrl_utils as vu
import numpy as np
import os
from pycocotools.coco import COCO


def get_aciton_num_and_roles_num(v_coco, dataset_name='vcoco_trainval', action_index=0):
    # Load the VCOCO annotations for vcoco_train image set
    vcoco_data = vu.load_vcoco(dataset_name)

    vcoco = vcoco_data[action_index]

    positive_index = np.where(vcoco['label'] == 1)[0]
    total = len(positive_index)
    # print("total", total)

    x1 = set()
    x2 = set()
    count1 = 0
    count2 = 0
    for i in range(1, len(vcoco['role_name'])):
        for j in range(vcoco_data[0]['ann_id'].shape[0]):
            if vcoco['role_object_id'][j][i] != 0:
                if i == 1:
                    # get anno id
                    x1.add(vcoco['role_object_id'][j][i])
                    count1 = count1 + 1
                else:
                    x2.add(vcoco['role_object_id'][j][i])
                    count2 = count2 + 1

    # print("count1", count1)
    # print("count2", count2)

    # get category_ids
    anns = v_coco.loadAnns(list(x1))
    category_ids = np.array([a['category_id'] for a in anns])
    category_ids_list1 = np.sort(list(set(category_ids)))

    anns = v_coco.loadAnns(list(x2))
    category_ids = np.array([a['category_id'] for a in anns])
    category_ids_list2 = np.sort(list(set(category_ids)))

    return [total, count1, count2, category_ids_list1, category_ids_list2, vcoco['role_name'], vcoco["action_name"]]


def get_names(coco, cats_list):
    # print(cats_list)
    # coco = COCO(os.path.join('coco/annotations/', 'instances_trainval2014.json'))
    cates = coco.loadCats(list(cats_list))
    # print(cates)
    return np.array([a['name'] for a in cates])


def merge_two_list(list1, list2):
    list_all = set()
    for i in range(len(list1)):
        list_all.add(list1[i])
    for j in range(len(list2)):
        list_all.add(list2[j])
    return np.sort(list(list_all))


def get_table1_one_row(v_coco, coco, action_index=0, dict={}):
    trainval_list = get_aciton_num_and_roles_num(v_coco, dataset_name='vcoco_trainval', action_index=action_index)
    test_list = get_aciton_num_and_roles_num(v_coco, dataset_name='vcoco_test', action_index=action_index)

    category_ids_list1 = merge_two_list(trainval_list[3], test_list[3])
    name_list1 = get_names(coco, category_ids_list1)
    # print(name_list1)

    if trainval_list[2] != 0:
        category_ids_list2 = merge_two_list(trainval_list[4], test_list[4])
        name_list2 = get_names(coco, category_ids_list2)
        # print(name_list2)

    print("1.Action:", trainval_list[6])
    print('2.Roles:', "1" if len(trainval_list[5]) == 2 else "2")
    print("3.numbers of example:", trainval_list[0] + test_list[0])

    result = {}
    for i in range(1, len(trainval_list[5])):
        print("4.", trainval_list[5][i])
        print("5.", trainval_list[1] + test_list[1] if i == 1 else trainval_list[2] + test_list[2])
        print("6.Objects in role:", trainval_list[5][i], name_list1 if i == 1 else name_list2)
        result[trainval_list[5][i]] = name_list1 if i == 1 else name_list2
    dict[trainval_list[6]] = result
    return dict


if __name__ == '__main__':
    coco = COCO(os.path.join('coco/annotations/', 'instances_trainval2014.json'))
    v_coco = vu.load_coco()
    dict = {}

    # get_table1_one_row(action='sit')
    for i in range(26):
        result = get_table1_one_row(v_coco, coco, action_index=i, dict=dict)

    assert len(dict) == 26

    io.dump_json_object(dict, "table_list.json")
