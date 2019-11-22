import os
import io_utils as io


# def save_hois_txt(data_list, name='train'):
#     path = os.path.join(os.getcwd(), 'hois', name + '.txt')
#     f = open(path, 'w+')
#     id = 1
#     for action_verb_dict in data_list:
#         action = list(action_verb_dict.keys())[0]
#         verb_count_dict = action_verb_dict[action]
#         for verb in verb_count_dict.keys():
#             count = verb_count_dict[verb]
#             # print(action, verb, count)
#             str = '{:<5d}'.format(id) + '{:<20s}'.format(action) + '{:<25s}'.format(verb) + \
#                   '{:<8d}'.format(count)
#             f.write(str + '\n')
#             id = id + 1
#     f.close()
#
#
# def save_hois_txt_total(data_dict, name='all'):
#     data_dict = dict(sorted(data_dict.items(), key=lambda d: d[0], reverse=False))
#
#     path = os.path.join(os.getcwd(), 'hois', name + '.txt')
#     f = open(path, 'w+')
#     str = '{:<8s}'.format("id") + '{:<20s}'.format("verb") + '{:<25s}'.format("object") + \
#           '{:<10s}'.format("train") + '{:<10s}'.format("val") + \
#           '{:<10s}'.format("test")
#     f.write(str + '\n')
#     f.write("--------------------------------------------------------------------------------------------" + '\n')
#     id = 1
#     for action_ob_key in data_dict.keys():
#         name = action_ob_key.split('/')
#         assert len(name) == 2
#         action = name[0]
#         ob = name[1]
#         set_num_dict = data_dict[action_ob_key]
#         # print(set_num_dict)
#         # assert len(list(set_num_dict.keys())) == 4
#         str = '{:<8d}'.format(id) + '{:<20s}'.format(action) + '{:<25s}'.format(ob) + \
#               '{:<10d}'.format(set_num_dict.get('train', 0)) + \
#               '{:<10d}'.format(set_num_dict.get('val', 0)) + \
#               '{:<10d}'.format(set_num_dict.get('test', 0))
#         f.write(str + '\n')
#         id = id + 1
#     f.close()


def save_hois_to_json(data_dict):
    data_dict = dict(sorted(data_dict.items(), key=lambda d: d[0], reverse=False))
    id = 1
    data_list = []
    rare_list = []
    non_rare_list = []
    for action_ob_key in data_dict.keys():
        name = action_ob_key.split('/')
        assert len(name) == 2
        action = name[0]
        ob = name[1]
        set_num_dict = data_dict[action_ob_key]
        temp = {
            'id': str(id).zfill(3),
            'verb': action,
            'object': ob,
            'train_num': set_num_dict.get('train', 0),
            'val_num': set_num_dict.get('val', 0),
            'test_num': set_num_dict.get('test', 0),
            'rare': True if set_num_dict.get('train', 0) < 10 else False

        }
        if temp['rare']:
            rare_list.append(id)
        else:
            non_rare_list.append(id)

        id = id + 1
        data_list.append(temp)

    print(data_list)
    print(type(data_list))
    print(type(data_list[0]))

    file = os.path.join(os.getcwd(), 'hois', 'hoi_list.json')
    io.dump_json_object(data_list, file)
