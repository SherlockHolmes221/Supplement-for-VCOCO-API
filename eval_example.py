import __init__
import vsrl_eval as eva

if __name__ == '__main__':
    vcocoeval = eva.VCOCOeval('data/vcoco/vcoco_test.json', 'data/instances_vcoco_all_2014.json',
                              'data/splits/vcoco_test.ids')
    # todo need to change according to your own path
    this_output = '/path/to/detections/detections.pkl'
    vcocoeval._do_eval(this_output, ovr_thresh=0.5)
