dataset_info = dict(
    dataset_name='mouse',
    # paper_info=dict(
    #     author='Lin, Tsung-Yi and Maire, Michael and '
    #     'Belongie, Serge and Hays, James and '
    #     'Perona, Pietro and Ramanan, Deva and '
    #     r'Doll{\'a}r, Piotr and Zitnick, C Lawrence',
    #     title='Microsoft coco: Common objects in context',
    #     container='European conference on computer vision',
    #     year='2014',
    #     homepage='http://cocodataset.org/',
    # ),
    keypoint_info={
        0: dict(name='Ear_tip', id=0, color=[51, 153, 255], type='upper', swap=''),
        1: dict(name='Earhole', id=1, color=[51, 153, 255], type='upper', swap=''),
        2: dict(name='Ear_back', id=2, color=[51, 153, 255], type='upper', swap=''),
        3: dict(name='Ear_front', id=3, color=[51, 153, 255], type='upper', swap=''),
        4: dict(name='Eye_back', id=4, color=[51, 153, 255], type='upper', swap=''),
        5: dict(name='Eye_front', id=5, color=[51, 153, 255], type='upper', swap=''),
        6: dict(name='Eye_bottom', id=6, color=[51, 153, 255], type='upper', swap=''),
        7: dict(name='Eye_top', id=7, color=[51, 153, 255], type='upper', swap=''),
        8: dict(name='Nose_top', id=8, color=[51, 153, 255], type='upper', swap=''),
        9: dict(name='Nose_bottom', id=9, color=[51, 153, 255], type='upper', swap=''),
        10:dict(name='Mouth', id=10, color=[51, 153, 255], type='upper', swap=''),
    },
    skeleton_info={
        0: dict(link=('Ear_tip', 'Earhole'), id=0, color=[0, 255, 0]),
        1: dict(link=('Ear_back', 'Ear_front'), id=1, color=[0, 255, 0]),
        2: dict(link=('Earhole', 'Eye_back'), id=2, color=[0, 255, 0]),
        3: dict(link=('Eye_back', 'Eye_top'), id=3, color=[0, 255, 0]),
        4: dict(link=('Eye_back', 'Eye_bottom'), id=4, color=[0, 255, 0]),
        5: dict(link=('Eye_bottom', 'Eye_front'), id=5, color=[0, 255, 0]),
        6: dict(link=('Eye_top', 'Eye_front'), id=6, color=[0, 255, 0]),
        7: dict(link=('Eye_front', 'Nose_top'), id=7, color=[0, 255, 0]),
        8: dict(link=('Nose_top', 'Nose_bottom'), id=8, color=[0, 255, 0]),
        9: dict(link=('Nose_bottom', 'Mouth'), id=9, color=[0, 255, 0]),
        10: dict(link=('Mouth', 'Eye_front'), id=10, color=[0, 255, 0]),

    },
    joint_weights=[
        1., 1., 1., 1., 1., 1., 1., 1.2, 1.2, 1.5, 1.5,
    ],
    sigmas=[
        0.026, 0.025, 0.025, 0.035, 0.035, 0.079, 0.079, 0.072, 0.072, 0.062,
        0.062
    ])