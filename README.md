
# Leveraging Adobe Extract API
This code is submitted for the Adobe Papyrus Nebula Hackathon 2023.
This is in response to the task which was assigned by the organizers. 

### Task
A test folder of 100 pdfs were needed to be extracted in the form of CSV file including important details from invoices(pdfs). This was to be done using Adobe Extract API.

### Implementation
Understood the implementation using Adobe Extract API documentation.

#### 1.) Extracting data through extracted.py
Run the file extracted1.py on terminal by providing the "input_pdf" variable the path of the pdf file you want to extract.
#### 2.) Extracting remaining data through extracted_2.py
Run the file extracted_2.py on terminal by providing the same path as used in previous file to extract remaining information from the invoice.

#### Note : 
This could be merged into a single code file instead of having two different files but is done in order to avoid any conflicts and exceptions that may occur during the extraction process.

#### 3.) Viewing the extracted data
A file name "merged_table.csv" will be formed which will be containing the extraction done by the API.

### Problems faced 
While programming , test file output1.pdf (from the test files provided) was taken into consideration.

It was thought that the code which run on this file will work perfectly for the rest of the files.

But this was not the case.The extract API extracted JSON data for each file differently , including paths and bounds due to which the code threw errors for rest of the files.

Tried to implement a loop so that the code itself runs for all the files from the folder but since the code was throwing exceptions for the rest of the files, it couldn't be resolved.

Tried to search about it but couldn't find any related solutions to this issue.

#### Illustration of problems faced :

Observe the code used for extracting Business Details :
<paste ss>

Since , the json file of this pdf had the following path:
<paste>

But on running the same code for a different pdf for example output47.pdf, the following path happened to be there :
<paste>

Hence, threw exceptions.

Along with it, the API extracted the Customer-Email-ID in the following format :
<paste>

For handling this , wrote the following code :
<paste>

But since other pdfs's mail address was extracted normally; eg.,
"abc123@gmail.com" and not "abc123@gmail.co" , "m". The code threw out of bounds errors.

Apart from this , while running the loop, encodings of a few pdf files couldn't be read and it constantly threw errors of "Codec couldn't be recognised".

### Conclusion

After trying constantly for over 12 days, I , hereby, submit the code which by far is running perfectly for pdf "output1.pdf".
I'm extremely apologetic for not being able to complete this task as asked.









