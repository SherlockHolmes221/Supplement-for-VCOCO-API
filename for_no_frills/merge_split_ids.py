import os

import _init_path
import io_utils as io
import numpy as np


def merge():
    splits_id_path = '../data/splits'
    vcoco_train = np.loadtxt(os.path.join(splits_id_path, 'vcoco_train.ids'))
    print(len(vcoco_train))
    train_list = [str(int(id)) for id in vcoco_train]

    vcoco_val = np.loadtxt(os.path.join(splits_id_path, 'vcoco_val.ids'))
    print(len(vcoco_val))
    val_list = [str(int(id)) for id in vcoco_val]

    vcoco_test = np.loadtxt(os.path.join(splits_id_path, 'vcoco_test.ids'))
    print(len(vcoco_test))
    test_list = [str(int(id)) for id in vcoco_test]

    vcoco_trainval = np.loadtxt(os.path.join(splits_id_path, 'vcoco_trainval.ids'))
    print(len(vcoco_trainval))
    trainval_list = [str(int(id)) for id in vcoco_trainval]

    d = {}
    d["train"] = train_list
    d["val"] = val_list
    d["test"] = test_list
    d["trainval"] = trainval_list

    stats = {}
    stats["test"] = len(test_list)
    stats["train"] = len(train_list)
    stats["trainval"] = len(trainval_list)
    stats["val"] = len(val_list)

    io.dump_json_object(d, 'data_process/split_ids_all.json')
    io.dump_json_object(stats, 'data_process/split_ids_stats_all.json')


if __name__ == '__main__':
    merge()
