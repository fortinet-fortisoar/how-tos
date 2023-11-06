import zipfile
import os
import logging


class Utility:

    def __init__(self, path):
        self.path = path

    def unzip_zip_folder(self):
        with zipfile.ZipFile(self.path, 'r') as unzip_path:
            unzip_path.extractall(path=os.path.dirname(unzip_path.filename))
            unzipped_folder_path = os.path.join(os.path.dirname(unzip_path.filename), os.path.splitext(os.path.basename(self.path))[0])
        logging.debug('Successfully unzip Solution Pack')
        return unzipped_folder_path
        # with ZipFile(self.sp_path, 'r') as zip_ref:
        #     # Extract all contents to the same directory as the zip file
        #     extract_path = os.path.dirname(zip_ref.filename)
        #     zip_ref.extractall(path=extract_path)
        #
        #     # Get the expected directory name
        #     base_name = os.path.splitext(os.path.basename(self.sp_path))[0]
        #     expected_dir_name = base_name.split(' ')[0]
        #     print('expected_dir_name ', expected_dir_name)
        #
        #     # Check if the expected directory exists
        #     extracted_dir = os.path.join(extract_path, expected_dir_name)
        #     if not os.path.exists(extracted_dir):
        #         # Rename the extracted directory to the expected name
        #         os.rename(os.path.join(extract_path, base_name), extracted_dir)
        #
        #     # Return the path of the renamed directory
        #     return extracted_dir
