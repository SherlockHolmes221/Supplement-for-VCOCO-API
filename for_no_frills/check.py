import os

import _init_path
import vsrl_utils as vu
import io_utils as io
from pycocotools.coco import COCO


def check():
    anno_file = os.path.join("data_process", 'anno_list_gt.json')
    anno_list = io.load_json_object(anno_file)
    global_ids = [anno['global_id'] for anno in anno_list]
    print(len(global_ids))

    ids = io.load_json_object(os.path.join("data_process", 'split_ids_all.json'))

    train_lost = []
    val_lost = []
    test_lost = []

    train_list = []
    val_list = []
    test_list = []
    trainval_list = []

    for id in ids['train']:
        if not id in global_ids:
            print("train", id)
            train_lost.append(id)
        else:
            train_list.append(id)
            trainval_list.append(id)

    for id in ids['val']:
        if not id in global_ids:
            print("val", id)
            val_lost.append(id)
        else:
            val_list.append(id)
            trainval_list.append(id)

    for id in ids['test']:
        if not id in global_ids:
            print("test", id)
            test_lost.append(id)
        else:
            test_list.append(id)

    d = {}
    d['train'] = train_lost
    d["val"] = val_lost
    d['test'] = test_lost
    io.dump_json_object(d, 'data_process/id_lost.json')

    d = {}
    d['train'] = len(train_lost)
    d["val"] = len(val_lost)
    d['test'] = len(test_lost)
    io.dump_json_object(d, 'data_process/id_lost_stats.json')

    d = {}
    d['train'] = train_list
    d["val"] = val_list
    d['test'] = test_list
    d['trainval_list'] = trainval_list
    io.dump_json_object(d, 'data_process/split_ids.json')

    d = {}
    d['train'] = len(train_list)
    d["val"] = len(val_list)
    d['test'] = len(test_list)
    d['trainval_list'] = len(trainval_list)
    io.dump_json_object(d, 'data_process/split_ids_stats.json')


def check_id(dataset, id):
    for dataset_name in [dataset]:
        vcoco_data = vu.load_vcoco(dataset_name)
        assert len(vcoco_data) == 26

        for data_per_action in vcoco_data:
            # print(len(data_per_action['image_id']))
            assert len(data_per_action['image_id']) == len(data_per_action['ann_id']) \
                   == len(data_per_action['label']) == len(data_per_action['role_object_id'])

            for i in range(len(data_per_action['image_id'])):
                if data_per_action['image_id'][i] == id and data_per_action['label'][i] == 1:
                    print(data_per_action["action_name"], i,
                          data_per_action['role_object_id'][i])


if __name__ == '__main__':
    check()
    # check_id("vcoco_test", 589)
