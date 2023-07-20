import os
import logging
from template import release_note
from constants import *


class ReleaseNote:
    def __init__(self, sp_dir_path,):
        self.sp_dir_path = sp_dir_path

    def create_release_note_file_data(self):
        release_note_file = self.__create_release_note_file()
        logging.debug("Successfully created {0} file".format(
            RELEASE_NOTE_FILE_NAME))
        release_note_file.write(release_note.substitute())
        release_note_file.close()
        logging.debug("Successfully written data in {0} file".format(
            RELEASE_NOTE_FILE_NAME))

    def __create_release_note_file(self):
        file_path = os.path.join(self.sp_dir_path, RELEASE_NOTE_FILE_NAME)
        return open(file_path, 'w')
