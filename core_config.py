activate_core_name = 'resnet50'

CORE_ARGS = {
    'resnet50': {
        'MODEL_PATH': './data/merge-03_001_cc.pth',
        'DEVICE_NAME': 'cuda:0',
        'MODEL_TYPE': 'ori_resnet50',
        'NUM_CLASSES': 2,
        'PREPROCESS': 'autolevel',
        'BATCH_SIZE': 8
    }
}
