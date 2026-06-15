# %%
# in this, we will take PPC advertiser name and id not the cmpaign and placement details due to the 50k row limitaion in PPC
import pandas as pd
import numpy as np
import os
import mimetypes

# %%
## PART-1: Cheking the headers for all files

# Folder path where your files are stored
folder_path = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports\SA360 CSV files"

# List all files in the folder
all_files = os.listdir(folder_path)

# With mimetypes you can check the formats of the files
for file in all_files:
    file_path = os.path.join(folder_path, file)
    mime_type, _ = mimetypes.guess_type(file_path)
    print(f"{file}: {mime_type}")

# %%
# Filter to include only CSV and Excel files
# Create an empty list to store valid file names
valid_files = []

for file in all_files:  # Loop through each file in the files list
    if file.endswith('.csv') or file.endswith('.xlsx'):  # Check if the file is CSV or Excel
        valid_files.append(file)  # Add the file to the valid_files list
        
print(valid_files)        

# you can use below code as well to for Filter to include only CSV and Excel files
# valid_files = [file for file in files if file.endswith('.csv') or file.endswith('.xlsx')] '''

# %%
'''This is a library used for detecting the encoding of a file. 
Since the encoding might not be UTF-8 (which is the default), 
charset-normalizer helps to determine the correct encoding, especially for files that might have non-UTF-8 characters. '''
import charset_normalizer
import csv 

# Initialize a list to store headers
headers_list = []

# Loop through files in the folder to extract headers
for file in valid_files:
    file_path = os.path.join(folder_path, file)
    try:
        # Process CSV files
        if file.endswith('.csv'):
            # Detect the encoding
            with open(file_path, 'rb') as f:
                result = charset_normalizer.from_path(f.name).best()
            encoding = result.encoding
            print(f"Detected encoding for {file}: {encoding}")

            # Read the CSV file with utf-16 encoding and tab as the delimiter
            df = pd.read_csv(
                file_path,
                encoding='utf-16',  # Specify utf-16 encoding
                delimiter='\t',  # Specify the delimiter, check it by opening file in Notepad
                skiprows=2,  # Skip the first two rows if they contain metadata
                quoting=csv.QUOTE_NONE,  # Disable special quoting rules
                on_bad_lines='warn',  # Skip problematic rows
                engine='python'  # Use the Python engine for flexibility
            )

        # Process Excel files
        elif file.endswith('.xlsx'):
            df = pd.read_excel(file_path, skiprows=2)

        # Handle empty or corrupted files
        if df.empty:
            print(f"{file} is empty or has no valid headers.")
            continue

        # Extract headers and add to the list
        headers = set(df.columns)
        headers_list.append(headers)
        print(f"Headers in {file}: {headers}")

    except Exception as e:
        print(f"Error reading {file}: {e.__class__.__name__} - {e}")

# Print all collected headers
print("\nCollected Headers:")
print(headers_list)

# %%
## PART-2: Merging all CSV files from SA360 platfom

import os
import pandas as pd

# Specify the folder where the CSV files are stored
input_folder = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports\SA360 CSV files"  # Folder containing CSV files

# List all CSV files in the input folder
all_csv_files = os.listdir(input_folder)

# Create an empty list to store csv file names
csv_files = []

for file in all_csv_files:  # Loop through each file in the csv files list
    if file.endswith('.csv'):  # Check if the file is CSV
        csv_files.append(file)  # Add the file to the csv_files list
        
# you can use below code for all step 2
'''
[file for file in os.listdir(input_folder) if file.endswith('.csv')] 
'''        
        

# Initialize an empty list to hold DataFrames
dataframes = []

# Loop through each file and read its contents
for file in csv_files:
    file_path = os.path.join(input_folder, file)  # Get the full path of the file
    try:
        # Read the CSV file
        df = pd.read_csv(
            file_path,
            encoding='utf-16',  # Specify utf-16 encoding
            delimiter='\t',  # Specify the delimiter, check it by opening file in Notepad
            skiprows=2,  # Skip the first two rows if they contain metadata
            quoting=csv.QUOTE_NONE,  # Disable special quoting rules
            on_bad_lines='warn',  # Skip problematic rows
            engine='python'  # Use the Python engine for flexibility
            
        )
        dataframes.append(df)  # Append the DataFrame to the list
        print(f"Successfully read: {file}")
    except Exception as e:
        print(f"Error reading {file}: {e.__class__.__name__} - {e}")


# %%
# Combine all DataFrames into one
if dataframes:
    merged_df = pd.concat(dataframes, ignore_index=True)  # Combine all DataFrames row-wise
    print("DataFrames have been successfully merged into 'merged_df'.")
else:
    print("No valid CSV files found to merge.")

# %%
## Part 3- Add new columns in platform data. here we will extract brand name from sub-manager and create a new columns named brand

# Extracting 'brand' using regular expressions
# Import regular expressions module
import re  

# Check if the 'sub_manager' column exists
if 'Sub-manager' in merged_df.columns:
    # Apply regex to extract the brand Brand (between MB~ and _MK)
    merged_df['Brand'] = merged_df['Sub-manager'].str.extract(r'MB~(.*?)_MK')
    
    # Extract Market_Code (after MK~ and optionally followed by _)
    merged_df['Market_Code'] = merged_df['Sub-manager'].str.extract(r'MK~(.*?)(?:_|$)')
    
    # Display the first few rows of the updated DataFrame
    print(merged_df[['Sub-manager','Brand','Market_Code']].head())
else:
       print("The column 'Sub-manager' does not exist in the DataFrame.")    
       
              
# Add a new column 'Platform' with the value 'SA360' in all rows
merged_df['Platform'] = "SA360"

# %%
# Remove the data for pharma and vaccine advertisers from platform data

# Check if 'sub_manager' column exists
if 'Sub-manager' in merged_df.columns:
    # Filter out rows where 'sub_manager' contains 'VAX'
    filtered_df = merged_df[~merged_df['Sub-manager'].str.contains('VAX', na=False)]

    # Display the number of rows before and after filtering
    print(f"Number of rows before filtering: {len(merged_df)}")
    print(f"Number of rows after filtering: {len(filtered_df)}")

    # Update merged_df to only keep the filtered rows
    merged_df = filtered_df
else:
    print("The column 'sub_manager' does not exist in the DataFrame.")


# %%
# in impression column some of the values are coming under "" with coma ("1,159"). we need to remove "" and , from values.
merged_df['Impr.'] = merged_df['Impr.'].str.replace('"', '', regex=False)  # Remove double quotes
merged_df['Impr.'] = merged_df['Impr.'].str.replace(',', '', regex=False)  # Remove commas

merged_df['Clicks'] = merged_df['Clicks'].str.replace('"', '', regex=False)  # Remove double quotes
merged_df['Clicks'] = merged_df['Clicks'].str.replace(',', '', regex=False)  # Remove commas


# %%
# Sub-manager(Advertiser id) have dash '-' between it 3 times the need to be removed.

merged_df['Sub-manager ID'] = merged_df['Sub-manager ID'].str.replace('-', '', regex=False)

# %%
# This code is to get country name by country code for platform as we don't have country name on platform. 
# we are using 2 diffrent market/country_code sheet for Platform and Lumina
# the reason for 2 sheets is that we have some differnt country name in PPC file due to the himanshu's lumina vs PR dashboard.

# Specify the path to the Excel file with Country code
Market_code_file = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports\All 3 Reports\Market_Master_SA360 for platform.xlsx"

Market_code_df = pd.read_excel(Market_code_file)


# Merge lumina DataFrame with Market_code_df
merged_df = merged_df.merge(Market_code_df, on='Market_Code', how='left')

#Market_Name

# %%
# Save the merged DataFrame to a new excel file
output_folder = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports\All 3 Reports"  # Folder to save the merged file

output_file_path = os.path.join(output_folder, "platform_SA360_merged_file.xlsx")
merged_df.to_excel(output_file_path, sheet_name='platform_merged', index=False)  # Save as tab-delimited

# %%
## Part 4- Change data types, add extra column like Country code and countrycode_Platform_brand

# now we will open files in a folder with specific names and compare the data in dataframe 

# Define the folder path
folder_path_3_files = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports\All 3 Reports"

# List all files in the folder
All_3_files = os.listdir(folder_path_3_files)

# Identify files based on keywords in their names

lumina_file = None
pppc_file = None
platform_file = None

for file in All_3_files:
    if 'lumina' in file:
        lumina_file = os.path.join(folder_path_3_files, file)
    elif 'ppc' in file:
        ppc_file = os.path.join(folder_path_3_files, file)
    elif 'platform' in file:
        platform_file = os.path.join(folder_path_3_files, file)
        
        
# Load the identified files into DataFrames

if lumina_file:
    lumina_df = pd.read_excel(lumina_file)
else:
    print("Lumina file not found")
    
if ppc_file:
    ppc_df = pd.read_excel(ppc_file)
else:
    print("ppc file not found")    
    
if platform_file:
    platform_df = pd.read_excel(platform_file)
else:
    print("platform file not found")    
    
    
#print(ppc_df.head())
#print(lumina_df.head())
#print(platform_df.head())
        

# %%
# Check for column names, data types, and missing values in each sheet

print(ppc_df.info())
print(lumina_df.info())
print(platform_df.info())

# %%
# We need to remove last row in ppd_df as it contains subtotal

ppc_df = ppc_df.drop(ppc_df.index[-1])  # -1 refers to the last index


# We need to Remove the last 3 digits ('001') from all values in 'Advertiser Id'
ppc_df['ADVERTISER_ID_FINAL'] = ppc_df['ADVERTISER_ID_FINAL'].astype(str).str[:-3]

# Extracting 'brand' and country code using regular expressions
# Import regular expressions module
import re  

# Check if the 'sub_manager' column exists
if 'ADVERTISER NAME' in ppc_df.columns:
    # Apply regex to extract the brand Brand (between SAD~ and _SEI)
    ppc_df['Short_Brand'] = ppc_df['ADVERTISER NAME'].str.extract(r'MB~(.*?)_MK')
    
    # Extract Market_Code (after MK~ and optionally followed by _)
    ppc_df['Market_Code'] = ppc_df['ADVERTISER NAME'].str.extract(r'MK~(.*?)(?:_|$)')
    
     # Display the first few rows of the updated DataFrame
    print(ppc_df[['ADVERTISER NAME', 'Short_Brand', 'Market_Code']].head())
else:
    print("The column 'ADVERTISER NAME' does not exist in the DataFrame.") 

# %%
# Convert 'Date' column to date type first then for same format chanding it to string(object). we can use dt.date function or dt.normalize() method. 
# Here date doen't converted in date datatype yet becuse we used strftime() function in the end
ppc_df['Year/Month'] =pd.to_datetime(ppc_df['Year/Month'], errors= 'coerce',format='%Y/%m').dt.strftime('%Y/%m')
platform_df['Month'] = pd.to_datetime(platform_df['Month'], errors='coerce',format='%B %Y').dt.strftime('%Y/%m')

print(ppc_df['Year/Month'].dtypes)
print(platform_df['Month'].dtypes)

# %%
# If we want to change datatype to date and create new columns for Year and Month we can use below code. 

ppc_df['Year/Month'] =pd.to_datetime(ppc_df['Year/Month'], errors= 'coerce',format='%Y/%m')
platform_df['Month'] = pd.to_datetime(platform_df['Month'], errors='coerce',format='%Y/%m')


# Extract 'Year' and 'Month' into separate columns for ppc_df
ppc_df['Year'] = ppc_df['Year/Month'].dt.year
ppc_df['Month'] = ppc_df['Year/Month'].dt.month


# Convert to integers, while handling missing values
ppc_df['Year'] = ppc_df['Year'].fillna(0).astype(int)  # Replace NaN with 0 and convert to integer
ppc_df['Month'] = ppc_df['Month'].fillna(0).astype(int)


# Extract 'Year' and 'Month' into separate columns for platform_df
platform_df['Year'] = platform_df['Month'].dt.year
platform_df['Month_Number'] = platform_df['Month'].dt.month  # Rename to avoid conflict if 'Month' already exists

print(ppc_df['Year/Month'].dtypes)
print(platform_df['Month'].dtypes)

# %%
# Here we don't have the matching columns names for common columns in 2 datafram#
# We need to Rename the columns in both DataFrames to have matching names for the common columns.

# Standardize column names in pr_df
platform_df.rename(columns={
    'Account name': 'Campaign',
    'Month': 'Year/Month',
    'Sub-manager': 'Advertiser Name',
    'Sub-manager ID':'Advertiser Id',
    'Campaign': 'Placement',
    'Currency code': 'Currency',
    'Market_Name': 'Market',
    'Impr.': 'Impressions',
    'Clicks': 'Clicks',
    'Cost' : 'Cost',
    'Brand': 'Brand',
    'Platform': 'Platform',
    'Year': 'Year',
    'Month_Number': 'Month'
},inplace=True  )

# Standardize column names in lumina_df
ppc_df.rename(columns={
    'Year/Month': 'Year/Month',
    'Data Source': 'Platform',
    'Campaign': 'Campaign',
    'ADVERTISER NAME': 'Advertiser Name',
    'Placement': 'Placement',
    'Currency': 'Currency',
    'Market Name': 'Market',
    'ADVERTISER_ID_FINAL' : 'Advertiser Id',
    'Brand': 'Long_Brand',
    'Short_Brand': 'Brand',
    'Clicks' : 'Clicks',
    'Impressions' : 'Impressions',
    'Spend GBP' : 'Spend GBP',
    'Spend Platform Currency' : 'Spend Platform Currency',
    'Year': 'Year',
    'Month_Number': 'Month'   
}, inplace=True  )

# %%
# Convert columns to strings 
platform_df['Campaign'] = platform_df['Campaign'].astype(str)
platform_df['Advertiser Name'] = platform_df['Advertiser Name'].astype(str)
platform_df['Placement'] = platform_df['Placement'].astype(str)
platform_df['Market'] = platform_df['Market'].astype(str)
platform_df['Brand'] = platform_df['Brand'].astype(str)
platform_df['Platform'] = platform_df['Platform'].astype(str)

ppc_df['Platform'] = ppc_df['Platform'].astype(str)
#ppc_df['Campaign'] = ppc_df['Campaign'].astype(str)
ppc_df['Advertiser Name'] = ppc_df['Advertiser Name'].astype(str)
#ppc_df['Placement'] = ppc_df['Placement'].astype(str)
ppc_df['Market'] = ppc_df['Market'].astype(str)
ppc_df['Brand'] = ppc_df['Brand'].astype(str)


# Convert 'Spend GBP' columns to numeric, coercing errors to NaN
# You can set errors='coerce', which will convert non-convertible values to NaN (Not a Number)  

platform_df['Cost'] = pd.to_numeric(platform_df['Cost'], errors='coerce')

ppc_df['Spend GBP'] = pd.to_numeric(ppc_df['Spend GBP'], errors='coerce')
ppc_df['Spend Platform Currency'] = pd.to_numeric(ppc_df['Spend Platform Currency'], errors='coerce')

# Convert Impressions, clicks and Advertiser Id as Int data type
platform_df['Impressions'] = platform_df['Impressions'].fillna(0).astype(int)  # Replace NaN with 0 and convert to integer
platform_df['Clicks'] = platform_df['Clicks'].fillna(0).astype(int)

ppc_df['Impressions'] = ppc_df['Impressions'].fillna(0).astype(int)
ppc_df['Clicks'] = ppc_df['Clicks'].fillna(0).astype(int)
#ppc_df['Advertiser Id'] = ppc_df['Advertiser Id'].fillna(0).astype(int)

# Fill NaN values with 0
platform_df['Cost'].fillna(0, inplace=True)
ppc_df['Spend GBP'].fillna(0, inplace=True)
ppc_df['Spend Platform Currency'].fillna(0, inplace=True)

# Replace inf and -inf with 0
platform_df['Cost'].replace([np.inf, -np.inf], 0, inplace=True)
ppc_df['Spend GBP'].replace([np.inf, -np.inf], 0, inplace=True)
ppc_df['Spend Platform Currency'].replace([np.inf, -np.inf], 0, inplace=True)

# Convert numeric values to 2 decimal places
platform_df['Cost'] = platform_df['Cost'].round(2)
ppc_df['Spend GBP'] = ppc_df['Spend GBP'].round(2)
ppc_df['Spend Platform Currency'] = ppc_df['Spend Platform Currency'].round(2)


# %%
# transform Lumina data 

# # Split the Lumina MVB string into Market, Platform, and Brand columns

lumina_df[['Market', 'Platform', 'Brand']] = lumina_df['Lumina MVB'].str.split('_', expand=True)

# Convert the new columns to Proper Case
lumina_df['Market'] = lumina_df['Market'].str.title()
lumina_df['Platform'] = lumina_df['Platform'].str.title()
lumina_df['Brand'] = lumina_df['Brand'].str.title()

# Cahnge the data types of columns
# Convert 'Year' column to datetime with year-only format
lumina_df['Year'] = lumina_df['Year'].astype(int)
# no need to convert year into date datatype as futher when platform and ppc will merge the year woul be in int datatypw
#lumina_df['Year'] =pd.to_datetime(lumina_df['Year'], errors= 'coerce',format='%Y')
#lumina_df['Year'] = pd.to_datetime(lumina_df['Year'].dt.year, format='%Y')

lumina_df['Market'] = lumina_df['Market'].astype(str)
lumina_df['Brand'] = lumina_df['Brand'].astype(str)
lumina_df['Platform'] = lumina_df['Platform'].astype(str)

lumina_df['Lumina Spends GBP'] = pd.to_numeric(lumina_df['Lumina Spends GBP'], errors='coerce')

# Set all values in the 'Platform' column to 'SA360' from Google
lumina_df['Platform'] = 'SA360'

#Sometimes, column names have invisible spaces. Use .strip() to clean them:
platform_df.columns = platform_df.columns.str.strip()
ppc_df.columns = ppc_df.columns.str.strip()
lumina_df.columns = lumina_df.columns.str.strip()


print(lumina_df.head())

# %%
# This code is to get country code by country name. I have a additional file in the folder with country name and code which i created
# However we can get the brand name and country code directly from Campaign/Account name 

#---------------------------------------------------------------------------------------
# Add Country code to all 3 dataframes

# Specify the path to the Excel file with Country code
Country_code_file = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports\All 3 Reports\country_name_code for lumina.xlsx"

Country_code_df = pd.read_excel(Country_code_file)


#Sometimes, column names have invisible spaces. Use .strip() to clean them:
platform_df.columns = platform_df.columns.str.strip()
ppc_df.columns = ppc_df.columns.str.strip()
lumina_df.columns = lumina_df.columns.str.strip()
Country_code_df.columns = Country_code_df.columns.str.strip()

# Merge platform DataFrame with Market_code_df But we already have Market_Code for platform_df so need for below code
# platform_df = platform_df.merge(Market_code_df, on='Market', how='left')

# Merge PPC DataFrame with Market_code_df But we already have Market_Code for ppc_df so need for below code
# ppc_df = ppc_df.merge(Market_code_df, on='Market', how='left')



# Merge lumina DataFrame with Market_code_df
lumina_df = lumina_df.merge(Country_code_df, on='Market', how='left')



# fill NA for missing Market codes in all dataframe
platform_df['Market_Code'] = platform_df['Market_Code'].fillna('NA')   # fill NA for missing Market codes
ppc_df['Market_Code'] = ppc_df['Market_Code'].fillna('NA')
lumina_df['Market_Code'] = lumina_df['Market_Code'].fillna('NA')


# Count rows with 'NA' in Market_Code for each DataFrame
platform_na_count = (platform_df['Market_Code'] == 'NA').sum()
ppc_na_count = (ppc_df['Market_Code'] == 'NA').sum()
lumina_na_count = (lumina_df['Market_Code'] == 'NA').sum()


# Print the results
print(f"Rows with 'NA' in Market_Code in platform_df: {platform_na_count}")
print(f"Rows with 'NA' in Market_Code in ppc_df: {ppc_na_count}")
print(f"Rows with 'NA' in Market_Code in lumina_df: {lumina_na_count}") 


# %%
# Save all the dataframe as excel files for poweb BI Dashboard

# Define the output folder where the files will be saved
Updated_output_folder = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports\All 3 Reports_updated"

# Ensure the folder exists (create it if it doesn't)
os.makedirs(Updated_output_folder, exist_ok=True)

# Save PPC DataFrame
ppc_file_path = os.path.join(Updated_output_folder, "ppc_updated.xlsx")
ppc_df.to_excel(ppc_file_path, index=False)
print(f"PPC DataFrame saved to {ppc_file_path}")

# Save Platform DataFrame
platform_file_path = os.path.join(Updated_output_folder, "platform_updated.xlsx")
platform_df.to_excel(platform_file_path, index=False)
print(f"Platform DataFrame saved to {platform_file_path}")

# Save Lumina DataFrame
lumina_file_path = os.path.join(Updated_output_folder, "lumina_updated.xlsx")
lumina_df.to_excel(lumina_file_path, index=False)
print(f"Lumina DataFrame saved to {lumina_file_path}")

# %%
# Aggregate the data for both dataframe (based on all columns currency will get combined if other column vlaues are same)
# Group by the specified columns and aggregate by summing up the values

# Aggregating platform_df
# Aggregating platform_df
aggregated_platform_df = platform_df.groupby(
    ['Year', 'Month', 'Platform', 'Advertiser Name', 'Market_Code', 'Brand'], as_index=False
).agg({
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Cost': 'sum'
})

# Aggregating ppc_df
aggregated_ppc_df = ppc_df.groupby(
    ['Year', 'Month', 'Platform', 'Advertiser Name', 'Market_Code', 'Brand'], as_index=False
).agg({
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Spend GBP': 'sum',
    'Spend Platform Currency': 'sum'
})



# Perform the first merge: aggregated_platform_df with aggregated_ppc_df
merged_platform_ppc_df = pd.merge(aggregated_platform_df, aggregated_ppc_df, 
                     on=['Year', 'Month', 'Platform', 'Advertiser Name', 'Market_Code', 'Brand'], 
                     how='outer', 
                     suffixes=('_platform', '_ppc'))

# Display the first few rows of the merged DataFrame
print(merged_platform_ppc_df.head())

# %%
# Aggregating merged_platform_ppc_df on year level to match lumina data

aggre_merged_platform_ppc_df = merged_platform_ppc_df.groupby(
    ['Year', 'Platform', 'Market_Code', 'Brand'], as_index=False
).agg({
    'Impressions_platform': 'sum',
    'Impressions_ppc': 'sum',
    'Clicks_platform': 'sum',
    'Clicks_ppc': 'sum',
    'Cost': 'sum',
    'Spend GBP': 'sum',
    'Spend Platform Currency': 'sum'
})

# %%
# Define the common columns

common_columns = ['Year', 'Platform', 'Market_Code', 'Brand']

# Merge the DataFrames on common columns
final_merged_df = pd.merge(aggre_merged_platform_ppc_df, lumina_df, on=common_columns, how='outer')

# print(final_merged_df.columns)

# Group by common columns and aggregate relevant numeric columns
final_aggregated_df = final_merged_df.groupby(common_columns, as_index=False).agg({
#    'Impressions_platform': 'sum',
#    'Impressions_ppc': 'sum',
#    'Clicks_platform': 'sum',
#    'Clicks_ppc': 'sum',
    'Spend GBP': 'sum',
    'Lumina Spends GBP': 'sum',     
    'Spend Platform Currency': 'sum',
    'Cost': 'sum'
})

# Display the aggregated DataFrame (optional)
print(final_aggregated_df.head())

# No need to aggregate Lumina Spends GBP as it is already done from begining

# %%
# Calculate the percentage difference between 'Lumina Spends GBP' and 'Spend GBP'
final_aggregated_df['%_Spend Diff_Lumina/PPC'] = ((abs(final_aggregated_df['Lumina Spends GBP'] - final_aggregated_df['Spend GBP']) / final_aggregated_df['Spend GBP']) * 100).round(2).astype(str)

# Calculate the percentage difference between 'Cost' and 'Spend Platform Currency'
final_aggregated_df['%_Spend Diff_Platform/PPC'] = ((abs(final_aggregated_df['Cost'] - final_aggregated_df['Spend Platform Currency']) / final_aggregated_df['Spend Platform Currency']) * 100).round(2).astype(str)

# Calculate the difference between 'Lumina Spends GBP' and 'Spend GBP'
final_aggregated_df['Spend Diff_Lumina/PPC'] = (abs(final_aggregated_df['Spend GBP'] - final_aggregated_df['Lumina Spends GBP'])).round(2)

# Calculate the percentage difference between 'Spend Platform Currency' and 'Cost'
final_aggregated_df['Spend Diff_Platform/PPC'] = (abs(final_aggregated_df['Spend Platform Currency'] - final_aggregated_df['Cost'])).round(2)

# Replace inf values with NaN in the percentage difference columns. We are using numpy for this 
# inf values comes when you devide a vlaue with 0
# inf value will create issue while making dashboard in power BI 
import numpy as np

diff_columns = ['%_Spend Diff_Lumina/PPC', '%_Spend Diff_Platform/PPC', 'Spend Diff_Lumina/PPC', 'Spend Diff_Platform/PPC']

final_aggregated_df[diff_columns] = final_aggregated_df[diff_columns].replace([np.inf, -np.inf], np.nan)

#final_aggregated_df[diff_columns] = final_aggregated_df[diff_columns].fillna(0)  # Replace NaN with 0

# Check for any remaining inf values
#print(merged_df[diff_columns].isinf().sum())

print(final_aggregated_df.columns)


# %%
# Define the desired order of columns

desired_order_final = [
       
       'Year', 'Platform', 'Market_Code', 'Brand', 
#      'Impressions_platform', 'Impressions_ppc', 'Clicks_platform','Clicks_ppc', 
       'Spend GBP', 'Lumina Spends GBP','%_Spend Diff_Lumina/PPC','Spend Diff_Lumina/PPC',
       'Spend Platform Currency','Cost','%_Spend Diff_Platform/PPC','Spend Diff_Platform/PPC'
       ]

# Check if all desired columns exist in the DataFrame before reordering
missing_columns = [col for col in desired_order_final if col not in final_aggregated_df.columns]
if missing_columns:
    print(f"Missing columns in final_aggregated_df DataFrame: {missing_columns}")
else:
    # Reorder the columns in the merged DataFrame
    final_aggregated_df = final_aggregated_df[desired_order_final]
    
    
# Convert 'Month' to datetime
#final_aggregated_df['Month'] = pd.to_datetime(final_aggregated_df['Month'], errors='coerce').dt.date


# %%
# Replace missing or non-finite values in integer columns with 0 (or another appropriate value)
#final_aggregated_df['Impressions_platform'] = final_aggregated_df['Impressions_platform'].fillna(0).astype(int)
#final_aggregated_df['Impressions_ppc'] = final_aggregated_df['Impressions_ppc'].fillna(0).astype(int)
#final_aggregated_df['Clicks_platform'] = final_aggregated_df['Clicks_platform'].fillna(0).astype(int)
#final_aggregated_df['Clicks_ppc'] = final_aggregated_df['Clicks_ppc'].fillna(0).astype(int)
#final_aggregated_df['Impressions_platform'] = final_aggregated_df['Impressions_platform'].fillna(0).astype(int)


# Enforce correct data types for other columns
final_aggregated_df = final_aggregated_df.astype({
    'Year': 'int64',
    'Platform': 'object',
    'Market_Code': 'object',
    'Brand': 'object',
#    'Impressions_platform': 'int64',
#    'Impressions_ppc': 'int64',
#    'Clicks_platform': 'int64',
#    'Clicks_ppc': 'int64',
    'Spend GBP': 'float64',
    'Lumina Spends GBP': 'float64',
    '%_Spend Diff_Lumina/PPC': 'object',
    'Spend Diff_Lumina/PPC': 'float64',
    'Spend Platform Currency': 'float64',
    'Cost': 'float64',
    '%_Spend Diff_Platform/PPC': 'object',
    'Spend Diff_Platform/PPC': 'float64'
})

# Round all spend columns to 2 decimal places
spend_columns = ['Spend GBP', 'Lumina Spends GBP', '%_Spend Diff_Lumina/PPC', 
                 'Spend Diff_Lumina/PPC', 'Spend Platform Currency', 
                 'Cost', '%_Spend Diff_Platform/PPC', 'Spend Diff_Platform/PPC']

final_aggregated_df[spend_columns] = final_aggregated_df[spend_columns].round(2)


import numpy as np

# List of columns to clean
columns_to_clean = ['%_Spend Diff_Lumina/PPC', '%_Spend Diff_Platform/PPC']

# Clean and format the columns
for col in columns_to_clean:
    final_aggregated_df[col] = (
        final_aggregated_df[col]
        .replace([np.inf, -np.inf, 'inf', 'nan'], np.nan)  # Replace problematic values with NaN
        .astype(float)  # Convert to numeric type
        .round(2)  # Round numeric values to 2 decimal places
        .apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else 'NA')  # Append '%' or replace NaN with 'NA'
    )


# Check the data types
print(final_aggregated_df.dtypes) 

# Display the rearranged DataFrame columns
#print(final_aggregated_df.columns)

# Display the rearranged DataFrame
#print(final_aggregated_df.head())

# %%
# Save final_aggregated_df DataFrame to excel in Platform Reports folder

# Define the output folder where the files will be saved
final_aggregated_df_output_folder = r"C:\Users\gaujat\Documents\Data Analytics\MITvsPR_Utitilty_SA360\Platform Reports"

final_aggregated_df_file_path = os.path.join(final_aggregated_df_output_folder, "final_aggregated_df.xlsx")

final_aggregated_df.to_excel(final_aggregated_df_file_path, index=False)

print(f"final_aggregated_df DataFrame saved to {final_aggregated_df_file_path}")


