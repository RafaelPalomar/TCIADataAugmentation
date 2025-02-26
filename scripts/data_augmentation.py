import os
import re
from DICOMLib import DICOMUtils
import slicer

# Define the root directory containing the dataset
datasetRoot = "/home/rafael/Downloads/TCIA/Colorectal-Liver-Metastases-November-2022-manifest/Colorectal-Liver-Metastases/"

# Adapted from https://stackoverflow.com/questions/4639506/os-walk-with-regex
def iter_matching(dirpath, regexp):
    """Generator yielding all files under `dirpath` whose absolute path
       matches the regular expression `regexp`. (requires `import re`)
       Usage:

           >>> for filename in iter_matching('/', re.compile('/home.*\.bak')):
           ....    # do something
    """
    for dir_, dirnames, filenames in os.walk(dirpath):
        for dirname in dirnames:
            abspath = os.path.join(dir_, dirname)
            if regexp.match(abspath):
                yield abspath

loadedNodeIDs = []
with DICOMUtils.TemporaryDICOMDatabase() as db:
    for volumeDirectory in iter_matching(datasetRoot, re.compile('.*109.000000-84324')):
        print("Importing volumes DICOM files...")
        DICOMUtils.importDicom(volumeDirectory, db)

    for segmentationDirectory in iter_matching(datasetRoot, re.compile('.*100.000000-Segmentation-93044')):
        print("Importing segmentations DICOM files...")
        DICOMUtils.importDicom(segmentationDirectory, db)

    patientUIDs = db.patients()
    for patientUID in patientUIDs:
        loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))


# # Import dicom volumes in a temporary dicom database
# #for volumeDirectory in iter_matching(datasetRoot, re.compile('.*\d+\.\d+-\d+')):

# # Import dicom segmentaations in a temporary dicom database
# segmentationsDb = DICOMUtils.createTemporaryDatabase()
# #for segmentationDirectory in iter_matching(datasetRoot, re.compile('.*\d+\.\d+-Segmentation-\d+')):
# for segmentationDirectory in iter_matching(datasetRoot, re.compile('100.000000-Segmentation-93044')):
#     print("Importing segmentations DICOM files...")
#     DICOMUtils.importDicom(segmentationDirectory, segmentationsDb)

# patientUIDs = DICOMUtils.allSeriesUIDsInDatabase(volumesDb)
# print(patientUIDs)
# for i in patientUIDs:
#     DICOMUtils.loadPatientByUID(i)

# if not patientUIDs:
#     print(f"No patients found in the DICOM database")
# print(patientUIDs)


# slicer.app.exit()


# # Iterate over each patient folder
# for patientFolder in sorted(os.listdir(datasetRoot)):
#     patientPath = os.path.join(datasetRoot, patientFolder)
#     print(patientFolder)
#     if not os.path.isdir(patientPath):
#         continue

#     print(f"Processing patient: {patientFolder}")

#     # Initialize variables for segmentation and volume folders
#     segmentationFolder = None
#     volumeFolder = None

#     # Debugging: Log all subfolders being checked
#     for studyFolder in os.listdir(patientPath):
#         studyPath = os.path.join(patientPath, studyFolder)
#         if not os.path.isdir(studyPath):
#             continue

#         print(f"  Checking study folder: {studyPath}")
#         for seriesFolder in os.listdir(studyPath):
#             seriesPath = os.path.join(studyPath, seriesFolder)
#             if not os.path.isdir(seriesPath):
#                 continue
#             print(f"    Checking series folder: {seriesPath}")

#             # Identify segmentation and volume folders
#             if "Segmentation" in seriesFolder:
#                 segmentationFolder = seriesPath
#                 print(f"      Found segmentation folder: {segmentationFolder}")
#             elif "-NA" in seriesFolder or seriesFolder.endswith("00000"):  # Adjust this if needed
#                 volumeFolder = seriesPath
#                 print(f"      Found volume folder: {volumeFolder}")
#             else:
#                 print(f"      Folder did not match criteria: {seriesFolder}")

#         continue

#     continue
#     # Ensure both segmentation and volume folders are found
#     if segmentationFolder and volumeFolder:
#         print(f"Segmentation folder: {segmentationFolder}")
#         print(f"Volume folder: {volumeFolder}")

#         # Use a temporary DICOM database for processing
#         with DICOMUtils.TemporaryDICOMDatabase() as db:
#             # Import DICOM files for the volume and segmentation
#             print("Importing DICOM files...")
#             DICOMUtils.importDicom(volumeFolder, db)
#             DICOMUtils.importDicom(segmentationFolder, db)

#             # Get patient UIDs
#             patientUIDs = db.patients()
#             if not patientUIDs:
#                 print(f"No patients found in the DICOM database for: {patientFolder}")
#                 continue

#             for patientUID in patientUIDs:
#                 # Load all data for the patient
#                 print(f"Loading patient UID: {patientUID}")
#                 loadedNodeIDs = DICOMUtils.loadPatientByUID(patientUID)

#                 # Identify and process the nodes
#                 volumeNode = None
#                 segmentationNode = None

#                 for nodeID in loadedNodeIDs:
#                     node = slicer.mrmlScene.GetNodeByID(nodeID)
#                     if isinstance(node, slicer.vtkMRMLVolumeNode):
#                         volumeNode = node
#                     elif isinstance(node, slicer.vtkMRMLSegmentationNode):
#                         segmentationNode = node

#                 # Ensure both nodes are loaded
#                 if volumeNode:
#                     print(f"Volume node loaded: {volumeNode.GetName()}")
#                 else:
#                     print(f"Volume node not found for patient: {patientFolder}")
#                 if segmentationNode:
#                     print(f"Segmentation node loaded: {segmentationNode.GetName()}")
#                 else:
#                     print(f"Segmentation node not found for patient: {patientFolder}")

#                 # Add your custom processing logic here
#                 if volumeNode and segmentationNode:
#                     print(f"Processing volume and segmentation for patient: {patientFolder}")

#     else:
#         print(f"Could not find both segmentation and volume for: {patientFolder}")
#         if not segmentationFolder:
#             print(f"  Debug: Could not find segmentation folder for patient {patientFolder}.")
#         if not volumeFolder:
#             print(f"  Debug: Could not find volume folder for patient {patientFolder}.")

# print("Processing complete.")
