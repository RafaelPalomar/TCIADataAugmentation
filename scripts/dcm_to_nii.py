#!/usr/bin/env python3
import os
import subprocess

# Path to your dataset root
dataset_root = "/home/rafael/Downloads/CRLM/manifest-1669817128730/Colorectal-Liver-Metastases"

# Output directory for NIfTI/NRRD files
output_root = "/home/rafael/Downloads/CRLM/converted_files"  # Ensure this directory exists or will be created

# Paths to executables
dcm2niix_executable = "dcm2niix"  # Ensure dcm2niix is in your PATH
segimage2itkimage_executable = "/opt/dcmqi-1.3.4-linux/bin/segimage2itkimage"  # Update if necessary

def convert_volume(volume_input_dir, output_dir, patient_id):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filename = f"{patient_id}_volume"
    command = [
        dcm2niix_executable,
        "-z", "y",          # Compress output using gzip
        "-f", output_filename,
        "-o", output_dir,
        volume_input_dir
    ]
    print(f"Converting volume for patient {patient_id}")
    try:
        subprocess.run(command, check=True)
        print(f"Volume conversion completed for patient {patient_id}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting volume for patient {patient_id}: {e}")

def convert_segmentation(seg_input_dir, output_dir, patient_id):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    command = [
        segimage2itkimage_executable,
        "--inputDICOM", seg_input_dir,
        "--outputDirectory", output_dir,
        "-t", "nrrd",             # Specify output format
        "--mergeSegments"         # Optional: merge all segments into one file
    ]
    print(f"Converting segmentation for patient {patient_id}")
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Segmentation conversion completed for patient {patient_id}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting segmentation for patient {patient_id}: {e}")
        print(f"Standard Output:\n{e.stdout.decode()}")
        print(f"Standard Error:\n{e.stderr.decode()}")

# Iterate over patient folders
for patient_folder in sorted(os.listdir(dataset_root)):
    patient_path = os.path.join(dataset_root, patient_folder)
    if not os.path.isdir(patient_path):
        continue

    print(f"\nProcessing patient: {patient_folder}")

    # Iterate over study folders
    for study_folder in os.listdir(patient_path):
        study_path = os.path.join(patient_path, study_folder)
        if not os.path.isdir(study_path):
            continue

        segmentation_folder = None
        volume_folder = None

        # Iterate over series folders within the study
        for series_folder in os.listdir(study_path):
            series_path = os.path.join(study_path, series_folder)
            if not os.path.isdir(series_path):
                continue

            # Identify segmentation and volume folders
            if "Segmentation" in series_folder or "SEG" in series_folder:
                segmentation_folder = series_path
                print(f"Found segmentation folder: {segmentation_folder}")
            else:
                # You may need to refine this condition based on your dataset structure
                volume_folder = series_path
                print(f"Found volume folder: {volume_folder}")

        output_dir = os.path.join(output_root, patient_folder)

        if volume_folder:
            convert_volume(volume_folder, output_dir, patient_folder)
        else:
            print(f"No volume folder found for patient {patient_folder}")

        if segmentation_folder:
            convert_segmentation(segmentation_folder, output_dir, patient_folder)
        else:
            print(f"No segmentation folder found for patient {patient_folder}")
