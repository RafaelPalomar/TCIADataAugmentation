import slicer
import os

# Define the path to the tar package
tar_path = "/33130-linux-amd64-Sofa-git365fd33-2024-11-24.tar"

# Check if the file exists
if not os.path.exists(tar_path):
    raise FileNotFoundError(f"Extension archive not found at {tar_path}")

# Get the Extensions Manager model
extensions_manager = slicer.app.extensionsManagerModel()

# Install the extension using positional arguments
success = extensions_manager.installExtension(tar_path, False, True)  # archiveFile, installDependencies, waitForCompletion

# Check the installation status
if success:
    print(f"Extension installed successfully from {tar_path}. Restart Slicer to load the extension.")
    slicer.app.exit(0)
else:
    print(f"Failed to install the extension from {tar_path}. Check the log for more details.")
    slicer.app.exit(1)
