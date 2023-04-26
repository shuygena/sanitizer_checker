# sanitizer_checker
Utility to detect sanitizers used in compilation

## :toolbox: Requirements:  
This project was done with python-3.8.10

## :link: Download & Run
Clone repository:
```
git clone https://github.com/shuygena/sanitizer_checker sanitizer_checker
```
Go to directory:
```
cd sanitizer_checker
```
Run:   
```
python3 sanitizer_checker.py [file] [option]
``` 
## :clipboard: Checker options  
1. Check only 1/3 sanitizer types: AddressSanitizer, MemorySanitizer, ThreadSanitizer
```
python3 sanitizer_checker.py [file]  
```  
2. Check all sanitizers: AddressSanitizer, MemorySanitizer, ThreadSanitizer, UndefinedBehaviorSanitizer, DataFlowSanitizer, LeakSanitizer
```
python3 sanitizer_checker.py [file] -a 
```  
3. Help option:
```
python3 sanitizer_checker.py -h 
```  
