# Supplement for VCOCO-API
the origin v-coco api please click [here](https://github.com/s-gupta/v-coco.git)

### What I change 
- modify code to build for python3
- add v-coco-table.py 

  To show how to generate the data in table1 of the paper ```Visual Semantic Role Labeling```
- add get_hois.py, save_hois.py and io_utils.py
  
  To calculate all HOIs like HOI-DET
- add visualization.py 
  
  More concise to visualization without download from Internet

- add eval_example.py for Evaluation and and some explanations of APs in README.md  

## Experiments and Results
- Visualization
```
# You can change the configurations to visual different actions and datasets
cd ROOT_DIR
python visualization.py
```
![](https://github.com/SherlockHolmes221/Supplement-for-VCOCO-API/raw/master/carry_train.png)

- Calculation about the Table1 in ```Visual Semantic Role Labeling```
![](https://github.com/SherlockHolmes221/Supplement-for-VCOCO-API/raw/master/table1_part.png)
```
cd ROOT_DIR
python v-coco-table1.py
```
- HOIs in the datasets
```hois/vcoco-hois.json```
![](https://github.com/SherlockHolmes221/Supplement-for-VCOCO-API/raw/master/hois_part.png)
```
# generate this file by running:
python get_hois.py
``` 

## Preparation
### build the project 
```
# todo
git clone --recursive https://github.com/SherlockHolmes221/Supplement-for-VCOCO-API.git

# setup the environment
conda create -n vcocoapi python=3.6.9 
conda activate vcocoapi
pip install numpy==1.16.0
pip install cython 
(need to supplement here when you acturally build)

#cmake
cd ROOT_DIR/coco/PythonAPI/
make
make install
cd ROOT_DIR
make 
```

### Download COCO2014 dataset
Current V-COCO release uses a subset of MS-COCO images
If your already have coco2014 dataset, you just need a soft link list this
```
cd cd ROOT_DIR/coco
ln -s your/path/to/coco/images images
ln -s your/path/to/coco/annotations annotations
```
If you don't have coco2014 dataset, please follow to download:
```
cd ROOT_DIR/coco
URL_2014_Train_images=http://images.cocodataset.org/zips/train2014.zip
URL_2014_Val_images=http://images.cocodataset.org/zips/val2014.zip
URL_2014_Test_images=http://images.cocodataset.org/zips/test2014.zip
URL_2014_Trainval_annotation=http://images.cocodataset.org/annotations/annotations_trainval2014.zip

wget -N $URL_2014_Train_images
wget -N $URL_2014_Val_images
wget -N $URL_2014_Test_images
wget -N $URL_2014_Trainval_annotation

mkdir images

unzip train2014.zip -d images/
unzip val2014.zip -d images/
unzip test2014.zip -d images/
unzip annotations_trainval2014.zip

rm train2014.zip
rm val2014.zip
rm test2014.zip
rm annotations_trainval2014.zip
```

### Get the data used in v-coco
This file will generate ```instances_vcoco_all_2014.json``` in the ROOT_DIR/data,
and these include all the images and instance used in v-coco dataset
```
cd ROOT_DIR 
python script_pick_annotations.py coco/annotations

# format about instances_vcoco_all_2014.json
# image_id       - Nx1
# ann_id         - Nx1
# label          - Nx1
# action_name    - string
# role_name      - ['agent', 'obj', 'instr']
# role_object_id - N x K matrix, obviously [:,0] is same as ann_id

# format about ground-truth per test image when evaluating
                     shape 
# id                                      image_id
# boxes          len(vaild_box), 4        x1,y1,x2,y2
# is_crowd       len(vaild_box), 1
# gt_classes     len(vaild_box), 4        class id 
# gt_actions     len(vaild_box), 26       mark as 1 if involve the action
# gt_role_id     len(vaild_box), 26 ,2    
```

## Evaluation
```
python eval_example.py 
```
### Details of agent AP (person with action only)
```
# Pseudo code
# input: test_gt_image and prediction

for each test_gt_image:
    get the box in boxes which gt_class==1(person) and gt_inds
    using gt_inds select the person gt_boxes and gt_actions
    
    for each actions:
        compute nums of the i_th action (in all test_gt_images after all cycle) as npos[i]
    
    select the predicted data by image_id as pred_agents
    
    for each actions:
        get valid predicted boxes by scores in pred_agents
        
        for each box in all valid predicted boxes from score high to low:
            compute overlaps with all gt_boxes and get ovmax
            sc[i] : i_th action scores for each valid box (in all test_gt_images)
            fp[i] : fp[i] == 0 when tp[i] == 1 else 1
            tp[i] : tp[i] == 1 if is_true_action and ovmax>ovr_thresh 
                    for each action in each test_gt_image

# compute ap for each action
for each actions:
    get sc[i] fp[i] tp[i] sort descending
    compute recall and prec 
    compute AP
compute mAP
```
### Details of role AP 
```
# Pseudo code
# input: test_gt_image and prediction
for each test_gt_image:
    get the box in boxes which gt_class==1(person) and gt_inds
    using gt_inds select the person gt_boxes and gt_actions
    
    for each actions:
        compute nums of the i_th action (in all test_gt_images after all cycle) as npos[i]
        
    select the predicted data by image_id as pred_agents and pred_roles
    
    for each actions:
        for each roles:
            get gt_roles_boxes for each valid gt_box as gt_roles
            get predicted agent_boxes,role_boxes and agent_scores
            
                for each box in all valid predicted boxes from score high to low:
                    compute person_overlaps using each box and all gt_boxes and get ovmax
                    
                    if gt_box with max overlap has no role:
                        if eval_type == 'scenario_1':
                            if : predicted box also has no role
                                role_overlap = 1
                            else:
                                role_overlap = 0
                        else eval_type == 'scenario_2':
                            role_overlap = 1
                    
                    sc[i][j] : action scores for each role in each valid box (in all test_gt_images)
                    fp[i][j] : fp[i] == 0 when tp[i] == 1 else 1
                    tp[i][j] : tp[i] == 1 if is_true_action and preson_overlap>ovr_thresh and roles_overlap>ovr_thresh and 
                               for each role in each action in each test_gt_image
# compute ap for each role in each action
for each actions:
    for each roles:
        get sc[i][j] fp[i][j] tp[i][j] sort descending
        compute recall and prec 
        compute AP
compute mAP
```
