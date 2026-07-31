import pyodbc

#This Setup Is For Local Connection
Connect = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=.;"
    "DATABASE=Users;"
)

#This Setup Is For Non Local Connection
# Connect = pyodbc.connect(
#     "DRIVER={SQL Server Versions};"
#     "SERVER= Server;"
#     "UID= Username;"
#     "PWD= Password;"
#     "DATABASE=DB Name;"
# )

