-----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
-- This file contains the workflow diagram, prerequisite softwares, packages used for the project
-- This file is subjected to copyrights.
--
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
-- List of Softwares
--
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
S.No	Software				Version				Bit				OS type
--
 1)		Python 				3.12.0				64				Windows 11
 2)		Microsoft VS Code		1.84.1				64				Windows 11
 3)		PostgreSQL			16.1.1				64				Windows 11
 4)		PGAdmin				 7.8				64				Windows 11
 5)		Git				 2.43				64				Windows 11 
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
-- List of VS Code Extensions
--
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
S.No	Addin					Version
--
 1)		Jupyter				   v2024.1.0
 2)		Python				   v2024.0.0
 3)		Pylance				   v2023.12.1
 4)             Git                                v0.1.3
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
-- List of Python Packages
--
----------------------------------------------------------------------------------------------------------------------------------------------------------------- 
--
S.No	Package
--
 1)		os
 2)		json
 3)		pandas
 4)		numpy
 5)		psycopg2
 7)		urllib
 8)		streamlit
 9)		pillow
 10)            plotly
 -----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
-- Add the below paths to the Environmental Variable 'PATH' (both User and System)
-- Username VENKATESH is replaceable based on the respective machines on which the softwares are installed
-- The bin folder paths are replaceable based on the installation folder which is used during softwares installation 
--
----------------------------------------------------------------------------------------------------------------------------------------------------------------- 
--
 1) 	C:\Users\VENKATESH\AppData\Local\Programs\Python\Python312\
 2)		C:\Users\VENKATESH\AppData\Local\Programs\Python\Python312\Scripts\
 3)		C:\Users\VENKATESH\AppData\Local\Programs\Microsoft VS Code\bin\
 4)		C:\Program Files\PostgreSQL\16\bin\
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
--
-- Project Work Flow
-- Major Steps : 1) Data Collection and Cloning (GitHub)
--		 2) Data Cleanup (Pandas and Windows cmd)
--		 3) Data Storage & Transfer (SQL PGAdmin)
--		 4) Data Processing (Python,Streamlit)
--		 5) Data Display (Streamlit)
--
----------------------------------------------------------------------------------------------------------------------------------------------------------------- 
|
|
|--- 1) Data Collection and Cloning (GitHub)
|		|
|		|
|		|--- 1) Install Git software for windows and GitHub exntesion in VS Code
|		|
|		|	
|		|--- 2) Initialise the local repository in which the GiHub data has to be cloned (in this case, my system desktop is the local repository)
|		|
|		|   
|		|--- 3) Create a branch and commit changes locally to the Phonepe Pulse Dataset.
|		|
|		|
|		|--- 4) Copy the Phonepe Pulse github URL link
|		|
|		|
|		|--- 5) In the VS code terminal, use the "git clone" command and the dataset will be cloned in the local repository
|		|
|		|
|
|
|--- 2) 2) Data Cleanup (Pandas and Windows cmd)
|		|
|		|
|		|--- 1) Create a new folder named 'jsonfiles' in the Desktop.
|		|
|		|
|		|--- 2) Create two sub-folders named 'Aggregated' and 'Top' and inside them, create folders named 'Transactions' & 'Users' respectively.
|		|
|		|
|		|--- 3) Using windows cmd, copy the json files from the cloned repository to the above two folders.
|		|
|		|
|		|--- 4) While copying, rename the json files in the mentioned format ("Year"_"Quarter Number.json" for quarter-wise files and "State Name"_"Year"_"Quarter Number.json" for  
|               |       state-wise files (Ex: 2023_4.json, Andhra Pradesh_2023_4.json, etc.)
|		|
|		|
|		|--- 5) Using pandas, read these json files, perform cleanup activities and save them as two separate csv files named "AggregatedData.csv" and "TopData.csv"
|		|
|		|
|
|
|
|--- 3) Data Transfer to SQL DB (PGAdmin)  
|		|
|		|
|		|--- 1) Open PGAdmin and create the tables for aggregated data, top data, and latitude-longitude tables for state-wise, district-wise & pin-code-wise
|		|
|		|
|		|--- 2) Import the csv files into the corresponding tables via SQL commands
|		|
|		|
|
|
|--- 4) Data Processing (Python,Streamlit)
|		|
|		|
|		|--- 1) Import the psycopg2 and streamlit module
|		|
|		|
|		|--- 2) Develop the python code for streamlit gui to create statistical tables, charts and geo-data using plotly.
|		|
|		|
|
|
|--- 4) Data Display (Streamlit)
|		|
|		|
|		|--- 1) Save the python code as a .py file extension
|		|
|		|
|		|--- 2) In the terminal, run the streamlit application and call the above .py file
|		|
|		|
|		|--- 3) This will now display all the backend python code in the form of GUI using streamlit
|		|
|		|
|
|
----------------------------------------------------------------------------------------------------------------------------------------------------------------- 
