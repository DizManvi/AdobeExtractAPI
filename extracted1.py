#### THE EXTRACTION PROGRAM STARTS FROM THIS FILE


import logging
import os
import csv
import chardet

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



logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

zip_file = "./ExtractTextInfoFromPDF.zip"
merged_csv_file = "merged_tables.csv"
extracted_tables_dir = "./extracted_tables"

if os.path.isfile(zip_file):
    os.remove(zip_file)

# input_pdf
input_pdf = "output47.pdf"

try:
   
    credentials = Credentials.service_account_credentials_builder() \
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

    # Saving the result 
    result.save_as(zip_file)

    import zipfile

    # Specify the path to the ZIP file
    zip_file = "./ExtractTextInfoFromPDF.zip"

    # Specify the destination folder for the extracted files
    extracted_folder = "./extracted_tables"

    # Extract the files from the ZIP archive
    with zipfile.ZipFile(zip_file, 'r') as archive:
        archive.extractall(extracted_folder)

    import csv
    import shutil
    import pandas as pd

    # Specify the input file path
    input_file = './extracted_tables/tables/fileoutpart4.csv'

    # Create a temporary output file path
    output_file = './extracted_tables/tables/temp.csv'

    # Read the existing CSV file
    with open(input_file, 'r', newline='', encoding='utf-8-sig') as f_in:
        reader = csv.reader(f_in)
        data = list(reader)

    # Insert a blank row at the top
    data.insert(0, [''] * len(data[0]))

    # Write the modified data to the temporary output file
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(data)

    # Replace the input file with the temporary output file
    shutil.move(output_file, input_file)

    print("Blank row added successfully!")

    table_names = ["fileoutpart2.csv", "fileoutpart4.csv"]

    folder_path="./extracted_tables/tables"
    merged_data=[]

    # Loop through each table name
    for table_name in table_names:
        table_df = pd.read_csv(f"{folder_path}/{table_name}")
        print(table_df, "tabledf")

        if merged_data:
            table_df.columns = merged_data[0].columns
        print(merged_data , "merged data")
        
        # Append the table data to the merged_data list
        merged_data.append(table_df)

    # Concatenate the table data vertically (row-wise)
    merged_table = pd.concat(merged_data, ignore_index=True)

    # Assuming the merged table is stored in a DataFrame called 'merged_table'

    # Remove a column by specifying its name
    column_name = 'AMOUNT  '
    merged_table = merged_table.drop(column_name, axis=1)
   
    merged_table.to_csv("./merged_table.csv", index=False)
    
    import pandas as pd

    df = pd.read_csv('merged_table.csv')  

    column_names_mapping = {
        'ITEM  ': 'Invoice__BillDetails__Name',
        'QTY  ': 'Invoice__BillDetails__Quantity',
        'RATE  ': 'Invoice__BillDetails__Rate',
    }

    # Rename the columns 
    df = df.rename(columns=column_names_mapping)

    # Print the updated DataFrame 
    df.to_csv("./merged_table.csv", index=False)

    tax_table = pd.read_csv('./extracted_tables/tables/fileoutpart6.csv')  

    # Transpose the table to change the orientation
    transposed_table = tax_table.transpose()


    # Reset the column names to be the first row values
    transposed_table.columns = transposed_table.iloc[0]

    transposed_table = transposed_table[1:]
   
    transposed_table.to_csv("./extracted_tables/tables/fileoutpart6.csv", index=False)

    tax_table = pd.read_csv('./extracted_tables/tables/fileoutpart6.csv') 
    df2 = pd.read_csv('./merged_table.csv')


    # Extract the desired column from the tax table
    tax_column = tax_table['Tax %  ']

    # Repeat the tax column values for the desired range of rows in the merged table
    tax_values = pd.concat([tax_column] * (len(df2)), ignore_index=True)

    df2['Tax %  '] = tax_values
    
    df2.to_csv("./merged_table.csv", index=False)

    column_names_mapping = {
        'Tax %  ': 'Invoice__Tax',
    }

    # Rename the columns using the mapping dictionary
    df2 = df2.rename(columns=column_names_mapping)
    # Print the updated DataFrame with new column names
    print(df2)
    df2.to_csv("./merged_table.csv", index=False)

    import re

    new_table = pd.read_csv('./extracted_tables/tables/fileoutpart0.csv') 
    cell_value = str(new_table.iloc[0, 0])
    cell_value2= str(new_table.iloc[0, 1])
    cell_value3= str(new_table.iloc[0, 2])
   
    data = cell_value.split()
    data3 = cell_value3.split()

    vals = ', '.join(data)
    vals3 = ', '.join(data3)

    values = vals.split(',')
    print(values)
    values3 = vals3.split(',')
    print(values3)


    name = values[0].strip()
    lastname = values[1].strip()
    email = values[2].strip()
    M = values[3].strip()
    phone = values[4].strip()
    add1 = values[5].strip()
    add2 = values[6].strip()
    add3 = values[7].strip()
    add4 = values[8].strip()
    duedate =values3[2].strip()
    description=cell_value2.strip()

    # Merge columns
    name = f"{name} {lastname}"
    address = f"{add1} {add2} {add3}"
    emailnew= email+M


    # Create a DataFrame to store the values
    data = {
        'Customer__Name': [name],
        'Customer__Email': [emailnew],
        'Customer__PhoneNumber': [phone],
        'Customer__Address__line1': [address],
        'Customer__Address__line2': [add4],
        'Invoice__DueDate': [duedate],
        'Invoice__Description': [description]
    }


    df4 = pd.DataFrame(data)

    df4.to_csv("./extracted_tables/tables/fileoutpart0.csv", index=False)



    info_table = pd.read_csv('./extracted_tables/tables/fileoutpart0.csv') 
    df5 = pd.read_csv('./merged_table.csv')

    # Extract the desired column from the info table
    info_column0 = info_table['Customer__Name']
    info_column1 = info_table['Customer__Email']
    info_column2 = info_table['Customer__Address__line1']
    info_column3= info_table['Customer__Address__line2']
    info_column4= info_table['Customer__PhoneNumber']
    info_column5= info_table['Invoice__DueDate']
    info_column6= info_table['Invoice__Description']

    # Repeat the tax column values for the desired range of rows in the merged table
    info_values0 = pd.concat([info_column0] * (len(df5)), ignore_index=True)
    info_values1 = pd.concat([info_column1] * (len(df5)), ignore_index=True)
    info_values2 = pd.concat([info_column2] * (len(df5)), ignore_index=True)
    info_values3 = pd.concat([info_column3] * (len(df5)), ignore_index=True)
    info_values4 = pd.concat([info_column4] * (len(df5)), ignore_index=True)
    info_values5 = pd.concat([info_column5] * (len(df5)), ignore_index=True)
    info_values6 = pd.concat([info_column6] * (len(df5)), ignore_index=True)

    # Assign the tax values to a new column in the merged table
    df5['Customer__Name'] = info_values0
    df5['Customer__Email'] = info_values1
    df5['Customer__Address__line1'] = info_values2
    df5['Customer__Address__line2'] = info_values3
    df5['Customer__PhoneNumber'] = info_values4
    df5['Invoice__DueDate'] = info_values5
    df5['Invoice__Description'] = info_values6


    #mergin df5 to merged_table.csv
    df5.to_csv("./merged_table.csv", index=False)


except (ServiceApiException, ServiceUsageException, SdkException):
    logging.exception("Exception encountered while executing operation")


###### move to the next file ----> extracted_2.py