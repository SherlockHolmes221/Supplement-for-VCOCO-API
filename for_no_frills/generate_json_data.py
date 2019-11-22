import os

import _init_path
import vsrl_utils as vu
import io_utils as io
from pycocotools.coco import COCO
import json


def generate_json_data_for_vcoco_total_with_gt():
    hoi_list = json.load(open(os.path.join(os.getcwd(), 'data_process', 'hoi_list.json'), 'r'))
    coco = COCO(os.path.join('..', 'coco/annotations/', 'instances_trainval2014.json'))
    anno_list = []
    verb_set = set()
    object_set = set()

    for dataset_name in ["vcoco_train", "vcoco_val", "vcoco_test"]:
        vcoco_data = vu.load_vcoco(dataset_name)
        # train_data add bbox and role_bbox
        for x in vcoco_data:
            x = vu.attach_gt_boxes(x, coco)

        assert len(vcoco_data) == 26
        for data in vcoco_data:
            # print(data.keys())
            verb_set.add(data['action_name'])

            image_ids = data['image_id']
            for i in range(len(image_ids)):
                assert data['role_object_id'][i][0] == data['ann_id'][i]

                if data['label'][i] == 0:
                    continue
                path = 'train' if 'train' in data['file_name'][i] else 'val'
                global_id = "COCO_" + path + "2014_" + str(image_ids[i][0]).zfill(12)
                image_path_postfix = os.path.join(path + '2014', global_id + '.jpg')

                global_id = str(image_ids[i][0])

                human_bboxes = data['bbox'][i]

                assert len(human_bboxes) == 4
                # get image size
                image_size = data['image_size'][i]
                assert len(image_size) == 2

                hois = []
                assert len(data['role_name']) <= 3
                for j in range(1, len(data['role_name'])):
                    object_anno_id = data['role_object_id'][i][j]
                    if object_anno_id == 0:
                        continue
                    d = {}
                    object_anno = coco.loadAnns(int(object_anno_id))[0]
                    object_bboxes = data['role_bbox'][i][4 * j:4 * (j + 1)]

                    cat_id = object_anno['category_id']
                    object_name = coco.loadCats(int(cat_id))[0]['name']
                    object_set.add(object_name)

                    id = -1
                    for k in hoi_list:
                        if k['action'] == data['action_name'] and k['object'] == object_name:
                            id = k['id']
                            break
                    assert id > 0
                    d['object'] = object_name
                    d['human_bboxes'] = human_bboxes
                    d['id'] = id
                    d['invis'] = 0
                    d['action'] = data['action_name']
                    d['object_bboxes'] = object_bboxes
                    hois.append(d)

                if hois == []:
                    # print(i, data["action_name"], data['label'][i], data['role_object_id'][i])
                    continue
                d_per_image = {}
                d_per_image['global_id'] = global_id
                d_per_image['hois'] = hois
                d_per_image['image_path_postfix'] = image_path_postfix
                d_per_image['image_size'] = image_size
                anno_list.append(d_per_image)

        print(dataset_name, len(anno_list))

    anno_dict = {}
    print(len(anno_list))

    for item in anno_list:
        assert item['hois'] is not None

        if item['global_id'] not in anno_dict:
            anno_dict[item['global_id']] = item
        else:
            anno_dict[item['global_id']]['hois'].append(item['hois'][0])

    print(len(anno_dict))
    anno_list = []
    for _, value in anno_dict.items():
        anno_list.append(value)

    io.dump_json_object(anno_list, 'data_process/' + 'anno_list_gt.json')

    ob_index = 1
    object_set = sorted(object_set)
    object_list = []
    for ob in object_set:
        object_list.append({
            "id": str(ob_index).zfill(3),
            "name": ob
        })
        ob_index += 1
    io.dump_json_object(object_list, 'data_process/' + 'object_list_gt.json')

    vb_index = 1
    verb_set = sorted(verb_set)
    verb_list = []
    for verb in verb_set:
        verb_list.append({
            "id": str(vb_index).zfill(3),
            "name": verb
        })
        vb_index += 1
    io.dump_json_object(verb_list, 'data_process/' + 'verb_list_gt.json')


if __name__ == '__main__':
    generate_json_data_for_vcoco_total_with_gt()
