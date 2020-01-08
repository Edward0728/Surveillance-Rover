import os


while True:
    button=input()
    print(button)
    
   # if button=='1':
       # os.system('python stream.py')
        #os.system('python stop_python.py') 
        
        # press keyboard 2 to run the moving script in the same folder
    if button=='2':
        os.system('python moving.py')
    
   # if button=='3':
       # os.system('python stop_stream.py')
        
       # press keyboard 3 to run the detectio script in the same folder
    if button=='4':
        os.system('python detection.py')
        
        # press keyboard 5 to stop running detection script 
    if button=='5':
        os.system('python stop_detection.py')