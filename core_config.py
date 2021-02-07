use_core = 'resnet50'

CORE_ARGS = {
    'resnet50': {
        'MODEL_PATH': './data/099.pth',
        'DEVICE_NAME': 'cuda:0',
        'MODEL_TYPE': 'ori_resnet50',
        'NUM_CLASSES': 2,
        'PREPROCESS': 'autolevel',
    }
}
