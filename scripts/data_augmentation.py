import os
from DICOMLib import DICOMUtils
import slicer

# Define the root directory containing the dataset
datasetRoot = "/home/rafael/Downloads/CRLM/manifest-1669817128730/Colorectal-Liver-Metastases"

# Iterate over each patient folder
for patientFolder in sorted(os.listdir(datasetRoot)):
    patientPath = os.path.join(datasetRoot, patientFolder)
    if not os.path.isdir(patientPath):
        continue

    print(f"Processing patient: {patientFolder}")

    # Initialize variables for segmentation and volume folders
    segmentationFolder = None
    volumeFolder = None

    # Debugging: Log all subfolders being checked
    for studyFolder in os.listdir(patientPath):
        studyPath = os.path.join(patientPath, studyFolder)
        if not os.path.isdir(studyPath):
            continue

        print(f"  Checking study folder: {studyPath}")
        for seriesFolder in os.listdir(studyPath):
            seriesPath = os.path.join(studyPath, seriesFolder)
            if not os.path.isdir(seriesPath):
                continue
            print(f"    Checking series folder: {seriesPath}")

            # Identify segmentation and volume folders
            if "Segmentation" in seriesFolder:
                segmentationFolder = seriesPath
                print(f"      Found segmentation folder: {segmentationFolder}")
            elif "-NA" in seriesFolder or seriesFolder.endswith("00000"):  # Adjust this if needed
                volumeFolder = seriesPath
                print(f"      Found volume folder: {volumeFolder}")
            else:
                print(f"      Folder did not match criteria: {seriesFolder}")

    # Ensure both segmentation and volume folders are found
    if segmentationFolder and volumeFolder:
        print(f"Segmentation folder: {segmentationFolder}")
        print(f"Volume folder: {volumeFolder}")

        # Use a temporary DICOM database for processing
        with DICOMUtils.TemporaryDICOMDatabase() as db:
            # Import DICOM files for the volume and segmentation
            print("Importing DICOM files...")
            DICOMUtils.importDicom(volumeFolder, db)
            DICOMUtils.importDicom(segmentationFolder, db)

            # Get patient UIDs
            patientUIDs = db.patients()
            if not patientUIDs:
                print(f"No patients found in the DICOM database for: {patientFolder}")
                continue

            for patientUID in patientUIDs:
                # Load all data for the patient
                print(f"Loading patient UID: {patientUID}")
                loadedNodeIDs = DICOMUtils.loadPatientByUID(patientUID)

                # Identify and process the nodes
                volumeNode = None
                segmentationNode = None

                for nodeID in loadedNodeIDs:
                    node = slicer.mrmlScene.GetNodeByID(nodeID)
                    if isinstance(node, slicer.vtkMRMLVolumeNode):
                        volumeNode = node
                    elif isinstance(node, slicer.vtkMRMLSegmentationNode):
                        segmentationNode = node

                # Ensure both nodes are loaded
                if volumeNode:
                    print(f"Volume node loaded: {volumeNode.GetName()}")
                else:
                    print(f"Volume node not found for patient: {patientFolder}")
                if segmentationNode:
                    print(f"Segmentation node loaded: {segmentationNode.GetName()}")
                else:
                    print(f"Segmentation node not found for patient: {patientFolder}")

                # Add your custom processing logic here
                if volumeNode and segmentationNode:
                    print(f"Processing volume and segmentation for patient: {patientFolder}")

    else:
        print(f"Could not find both segmentation and volume for: {patientFolder}")
        if not segmentationFolder:
            print(f"  Debug: Could not find segmentation folder for patient {patientFolder}.")
        if not volumeFolder:
            print(f"  Debug: Could not find volume folder for patient {patientFolder}.")

print("Processing complete.")
