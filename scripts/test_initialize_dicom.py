#!/usr/bin/env python3

import os
import slicer

dicomDatabaseDir = "/home/rafael/SlicerDICOMDatabase"
databaseFilePath = os.path.join(dicomDatabaseDir, 'ctkDICOM.sql')

# Ensure the directory exists
if not os.path.exists(dicomDatabaseDir):
    os.makedirs(dicomDatabaseDir)

# Initialize the DICOM database with the full file path
slicer.dicomDatabase.initializeDatabase(databaseFilePath)

# Verify if the database is open
if slicer.dicomDatabase.isOpen:
    print("DICOM database initialized successfully.")
else:
    raise RuntimeError("DICOM database failed to open.")
