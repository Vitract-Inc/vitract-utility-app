import os
import glob
import shutil
import zipfile

def process_sample_files(source_folder, output_folder):
    """
    Process FASTQ files from source_folder that follow the naming convention:
      SAMPLE_R1_001.fastq.gz and SAMPLE_R2_001.fastq.gz.
    For each sample:
      - Create a folder named SAMPLE in output_folder.
      - Copy the paired FASTQ files into that folder.
      - Create a ZIP file named SAMPLE.zip in output_folder which,
        when extracted, reproduces the folder SAMPLE containing the files.
    """
    # Find all .fastq.gz files in the source folder
    fastq_files = glob.glob(os.path.join(source_folder, "*.fastq.gz"))
    # Group files by sample prefix based on the revised naming conventions.
    samples = {}
    for file in fastq_files:
        basename = os.path.basename(file)
        if basename.endswith("_R1_001.fastq.gz"):
            prefix = basename[:-len("_R1_001.fastq.gz")]
            samples.setdefault(prefix, {})["R1"] = file
        elif basename.endswith("_R2_001.fastq.gz"):
            prefix = basename[:-len("_R2_001.fastq.gz")]
            samples.setdefault(prefix, {})["R2"] = file

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each sample: copy files and create ZIP archive
    for sample, files in samples.items():
        if "R1" in files and "R2" in files:
            sample_folder = os.path.join(output_folder, sample[:9])
            os.makedirs(sample_folder, exist_ok=True)
            
            # Copy the FASTQ files into the sample folder
            dest_R1 = os.path.join(sample_folder, os.path.basename(files["R1"]))
            dest_R2 = os.path.join(sample_folder, os.path.basename(files["R2"]))
            shutil.copy(files["R1"], dest_R1)
            shutil.copy(files["R2"], dest_R2)
            
            # Create a ZIP archive from the sample folder
            zip_path = os.path.join(output_folder,  sample[:9] + ".zip")

            if os.path.exists(zip_path):
                os.remove(zip_path)
                
            # Use ZipFile to create the archive while preserving folder structure.
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, file_names in os.walk(sample_folder):
                    for filename in file_names:
                        file_path = os.path.join(root, filename)
                        # The arcname ensures that the sample folder is included in the ZIP.
                        arcname = os.path.relpath(file_path, output_folder)
                        print(arcname)
                        print(file_path)
                        zipf.write(file_path, arcname)
                        
            print(f"Processed sample '{sample[:9]}': created folder and ZIP archive.")
        else:
            print(f"Warning: Sample '{sample[:9]}' is missing one of the paired files; skipping.")


date = '20250210'

source_folder = r'D:/VitractData/Laragen/' + date   # Change to your actual path
    # Define the folder where you want to store the new sample folders and ZIP files
output_folder = r'D:/VitractData/Laragen/' + date + '/' + date        # Change to your desired output location
    
process_sample_files(source_folder, output_folder)
