# chromo-scheduler

Operations like listing lots of files, moving files from CIFS, AI scoring and sorting on CIFS are slow. So they are seperated from realtime file watchdog.  
Lister, mover, scorer and sorter can be used seperately to create a fully async pipeline. Or we could combine mover, scorer and sorter into a single worker for simplicity.  
