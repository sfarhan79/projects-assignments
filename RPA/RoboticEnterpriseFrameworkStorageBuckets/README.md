### Documentation is included in the Documentation folder ###


**Robotic Enterprise Framework**

### How It Works ###
Read a file, if any, from Storage Bucket. Extract data from Web and Append to the file. Upload the appended file to Storage Bucket.  

1. **INITIALIZE PROCESS**
 + Reading file from the Storage Bucket (create a file manually as required)
 + Using Queues: Adding file to Queue

2. **GET TRANSACTION DATA**
 + ./Framework/*GetTransactionData* - Fetches transactions from an Orchestrator queue defined by Config("OrchestratorQueueName") or any other configured data source

3. **PROCESS TRANSACTION**
 + Extracting data from Web to append.
 + Appending the data to file
 + Uploading to Storage Bucket (create a Storage Bucket for automation)

4. **END PROCESS**
 + ./Framework/*CloseAllApplications* - Logs out and closes applications used throughout the process
