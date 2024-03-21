### Documentation is included in the Documentation folder ###



**Robotic Enterprise Framework**

### Process ###
I have a folder with files of names 1-10 
I have two more folders, with names, even and odd 
The third folder is for primes or exceptions BRE. 
Take each file if the file name is even kept in even, if file name is odd keep in odd 
If the file name is prime, send it to the exception folder. 

Read folder, take files, depending on the file name move it to different folders 

1. **INITIALIZE PROCESS**
+ Add code for dispatcher
+ Directory .get files (input folder) - For each file in folder
+ For loop - For each file in folder
+ Add Queue item

2. **GET TRANSACTION DATA**
 + ./Framework/*GetTransactionData* - Fetches transactions from an Orchestrator queue defined by Config("OrchestratorQueueName") or any other configured data source

3. **PROCESS TRANSACTION**
 + Add Log Message to check the specific content. Fetch the values from Queue
 + Assign the file path to Variable
 + Use a condition to check even or odd and then move files to respective folders
 + Apart from Even and Odd folder, send files to Exception folder

4. **END PROCESS**
 + ./Framework/*CloseAllApplications* - Logs out and closes applications used throughout the process


### For New Project ###

1. Check the Config.xlsx file and add/customize any required fields and values
2. Implement InitiAllApplications.xaml and CloseAllApplicatoins.xaml workflows, linking them in the Config.xlsx fields
3. Implement GetTransactionData.xaml and SetTransactionStatus.xaml according to the transaction type being used (Orchestrator queues by default)
4. Implement Process.xaml workflow and invoke other workflows related to the process being automated
