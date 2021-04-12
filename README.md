# chromo-scheduler

Operations like listing lots of files, moving files from CIFS, AI scoring and sorting on CIFS are slow. So they are seperated from realtime file watchdog.  
Lister, mover, scorer and sorter can be used seperately to create a fully async pipeline. Or we could combine mover, scorer and sorter into a single worker for simplicity.  

## Initialize

1. initialize database  

```sh
python create_sql_tables.py
```

2. create scheduler paths  

```sh
sudo mkdir /media/scheduler
sudo chown voyager.voyager /media/scheduler
mkdir ./tmp
```

3. update config.py

```py
DEBUG = True
TRACK = False

SORT_SIMULATION = True  # VERY IMPORTANT! SET TO FALSE AFTER DEBUGGING!

# global config
src_path = '/media/msd'
export_path = '/media/cs/test'
dest_path = '/media/scheduler'
tmp_path = './tmp'
backup_path = './backup'
```

4. update core_config.py

```py
activate_core_name = 'resnet50'

CORE_ARGS = {
    'resnet50': {
        'MODEL_PATH': './data/merge-03_001_cc.pth', # set to your model path
        'DEVICE_NAME': 'cuda:0',
        'MODEL_TYPE': 'ori_resnet50',
        'NUM_CLASSES': 2,
        'PREPROCESS': 'autolevel',
        'BATCH_SIZE': 8
    }
}
```

5. start pipeline  

```sh
conda activate chromo-scheduler
nohup python -u worker.py > worker.log 2>&1 &
```

## Tests

* pipeline_test.py - tests for lister, ls_scheduler and other wokers, just for debugging, do NOT run this test after deployment  
* gpu_perf_test.py - gpu performance test  

Please run tests from root path of chromo-scheduler project:  

```sh
cd chromo-scheduler
python test/gpu_perf_test.py
```
