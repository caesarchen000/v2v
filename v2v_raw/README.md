## Author: 陳胤亮、陳裕穎  
# **Workflow**


![Workflow Diagram](./png_file/workflow.png)
See workflow.png

## Details

### 1. Driver --> Voice Input --> Whisper Speech Detection 

Input data type: .wav  
Output data type: .txt   
Function: speech_to_text(.wav): -> .txt

### 2. Whisper Speech Detection  --> Message Formatting 

Input data type: .txt   
Output data type: .json 
Function: message_format(.txt): -> .json


### 3.1 Message Formatting --> Function Call 

Input data type: .json  
Output data type: .json (send.json)  

### 3.2 Message Formatting --> Driver Check 

Input data type: .json   
Output data type: bool   
Function: check_format(.json): -> bool (send_or_not)

#### 3.2.1 Incorrect: Driver Check --> Tell Driver Voice Input Err and Again

Input data type: bool   
Output data type: .wav   
Function: ask_again(bool) -> .wav

#### 3.2.2 Correct --> Function Call

Input data type: bool   
Output data type: .json   
Functon: send_message_to_others(bool): -> .json

### 4. Deliver to target car

Input data type: .json   
Output data type: .json (to another car)   

### HOW TO RECEIVE ??

### 5. Target car -->  Message Deformmatting

Input data type: .json   
Output data type: .txt   
Function: message_deformat(.json) -> .txt

### 6. Message Deformatting --> Tell the target car's driver

Input data type: .txt   
Output data type: .wav
Function:text_to_wav(.txt): -> .wav  
and wait for driver's response

### 7. Target car driver response --> Voice Input --> Whisper Speech Detection 

Input data type: .wav  
Output data type: .txt   
Function: speech_to_text(.wav): -> .txt 

### 8. Go back to 2. but in target's car



# **Function Call**

## need confirm


## not need confirm
![not_need_confirm concept](./png_file/not_need_confirm.png)
refer to https://www.zeczec.com/projects/carwink?fbclid=IwY2xjawJ4GnZleHRuA2FlbQIxMABicmlkETFEd1QxR0JpRTNBRkFSR2dNAR4D5lQG2wPU_v4MneM3H4Zj04jvbceCE1RH31Up85tDjLHWr--ANMx_P8FC-A_aem_LhIWldTD6KqgByj8zVOO0Q

