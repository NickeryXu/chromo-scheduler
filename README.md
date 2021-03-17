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

3. start pipeline  

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
