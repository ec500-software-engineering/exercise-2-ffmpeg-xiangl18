# python-ci-template  
[![Build Status](https://travis-ci.com/ec500-software-engineering/asyncio-subprocess-ffmpeg.svg?branch=master)](https://travis-ci.com/ec500-software-engineering/exercise-2-ffmpeg-xiangl18)  
minimal template for Python Travis-CI. Prereqs installed from requirements.txt
## Quick run  
To run this program, please directly input 
```python
python main_async.py 
```
or  
```python
python main_sync.py 
```
in your command line.  
## Tests  
You can test the duration of the output video by running:  
```python
python test_duration.py 
```  
## Estimation
The total running time for converting inital test video to outputVideo720p.mp4: 720p, 1M bit rate, 60fps , and outputVideo480p.mp4:480p, 1M bit rate, 60fps asynchronously is:  
```python
running time: 1551068425.1034057.  
```  
As for the Estimation of the processing power, when running the main_sync.py, the two process cost 90% of cpus:  
![image](https://github.com/ec500-software-engineering/exercise-2-ffmpeg-xiangl18/blob/master/image/cpu.png) 
