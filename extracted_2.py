#### After running extracted1.py , run this file on termminal

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
import os.path
import zipfile
import json
import pandas as pd
import logging
import os
import csv
import chardet
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

zip_file = "./ExtractTextInfoFromPDF2.zip"

if os.path.isfile(zip_file):
    os.remove(zip_file)

#input pdf
input_pdf = "output47.pdf"
table_columns = ["Bussiness__Name", "Column2", "Bussiness__Zipcode", "Column4", "Bussiness__Description"]
table_data = []

try:

    
    credentials = Credentials.service_account_credentials_builder()\
        .from_file("./pdfservices-api-credentials.json") \
        .build()

    
    execution_context = ExecutionContext.create(credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()

    
    source = FileRef.create_from_local_file(input_pdf)
    extract_pdf_operation.set_input(source)

    extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
        .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
        .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
        .with_table_structure_format(TableStructureType.CSV) \
        .build()
    extract_pdf_operation.set_options(extract_pdf_options)

    result: FileRef = extract_pdf_operation.execute(execution_context)

    #Save the result 
    result.save_as(zip_file)


    # Specify the destination folder for the extracted files
    extracted_folder = "./extracted_tables/extracted_tables2"

    # Extract the files from the ZIP archive
    with zipfile.ZipFile(zip_file, 'r') as archive:
        archive.extractall(extracted_folder)

    archive = zipfile.ZipFile(zip_file, 'r')
    jsonentry = archive.open('structuredData.json')
    jsondata = jsonentry.read()
    data = json.loads(jsondata)


    extracted_text = []
    for element in data["elements"]:
        if element["Path"].endswith("/Sect/P"):
            extracted_text.append(element["Text"])
        if element["Path"].endswith("/Sect/P[2]"):
            extracted_text.append(element["Text"])
        if element["Path"].endswith("/Sect/P[3]"):
            extracted_text.append(element["Text"])
        if element["Path"].endswith("/Sect/P[4]"):
            extracted_text.append(element["Text"])
        if element["Path"].endswith("/Sect/P[5]"):
            extracted_text.append(element["Text"])

    print(extracted_text)

    table_data.append(extracted_text)
    df = pd.DataFrame(table_data, columns=table_columns)

    import csv
    import re
    cell_value = str(df.iloc[0, 1])
    cell_value3 = str(df.iloc[0, 3])
    data = cell_value.split()
    data3 = cell_value3.split()

    vals = ', '.join(data)
    vals3 = ', '.join(data3)
    values = vals.split(',')
    values3 = vals3.split(',')

    number=values[0].strip()
    road1=values[1].strip()
    road2=values[2].strip()
    Business__City=values[4].strip()
    country1=values[6].strip()
    country2=values[8].strip()
    invoice=values3[1].strip()
    issuedate=values3[4].strip()
     
    Business__Street = f"{number} {road1} {road2}"  
    Business__Country = f"{country1} {country2}" 

    data = {
    'Business__Street': [Business__Street],
    'Business__City': [Business__City],
    'Business__Country': [Business__Country],
    'Invoice__Number': [invoice],
    'Invoice__IssueDate': [issuedate],

    }

    df2 = pd.DataFrame(data)

    # Merge `df1` and `df2` using the `concat` function
    merged_df = pd.concat([df, df2], axis=1)

    # Drop two columns from the merged dataframe
    columns_to_drop = ['Column2', 'Column4'] 
    updated_df = merged_df.drop(columns_to_drop, axis=1)

    # Print the updated dataframe
    print(updated_df)


    df5 = pd.read_csv('./merged_table.csv')

    # Extract the desired column from the info table
    comp_column0 = updated_df['Bussiness__Name']
    comp_column1 = updated_df['Bussiness__Zipcode']
    comp_column2 = updated_df['Bussiness__Description']
    comp_column3= updated_df['Business__Street']
    comp_column4= updated_df['Business__City']
    comp_column5= updated_df['Business__Country']
    comp_column6= updated_df['Invoice__Number']
    comp_column7= updated_df['Invoice__IssueDate']

    # Repeat the tax column values for the desired range of rows in the merged table
    comp_values0 = pd.concat([comp_column0] * (len(df5)), ignore_index=True)
    comp_values1 = pd.concat([comp_column1] * (len(df5)), ignore_index=True)
    comp_values2 = pd.concat([comp_column2] * (len(df5)), ignore_index=True)
    comp_values3 = pd.concat([comp_column3] * (len(df5)), ignore_index=True)
    comp_values4 = pd.concat([comp_column4] * (len(df5)), ignore_index=True)
    comp_values5 = pd.concat([comp_column5] * (len(df5)), ignore_index=True)
    comp_values6 = pd.concat([comp_column6] * (len(df5)), ignore_index=True)
    comp_values7 = pd.concat([comp_column7] * (len(df5)), ignore_index=True)

    # Assign the tax values to a new column in the merged table
    df5['Bussiness__Name'] = comp_values0
    df5['Bussiness__Zipcode'] = comp_values1
    df5['Bussiness__Description'] = comp_values2
    df5['Business__Street'] = comp_values3
    df5['Business__City'] = comp_values4
    df5['Business__Country'] = comp_values5
    df5['Invoice__Number'] = comp_values6
    df5['Invoice__IssueDate'] = comp_values7
    sorted_df = df5.sort_index(axis=1)

    # Print the sorted dataframe
    print(sorted_df)
   
    sorted_df.to_csv("./merged_table.csv", index=False)

   

except (ServiceApiException, ServiceUsageException, SdkException):
    logging.exception("Exception encountered while executing operation")


##### CODE ENDS #####