from pathlib import Path
import os
import shutil
import glob
import multiprocessing
nb_cores = multiprocessing.cpu_count()

class FileHandling():
    
    def __init__(self, dir_name:str, debug:bool):
        """
        :parma dir_name: Temporary directory to store files.
        """
        self.worker = nb_cores
        self.debug = debug
        self.pwd = os.getcwd()
        self.directory = dir_name
        self.destination = os.path.join(str(self.pwd), self.directory)
        # Create temporary folder if not exist
        if os.path.isdir(str(self.destination)) == False:
            os.mkdir(self.destination)
            print("Directory '%s' created" %self.directory)
        else:
            shutil.rmtree(self.destination)
            os.mkdir(self.destination)
            print("Directory '%s' created" %self.directory)

    def read_write_image(self, filename:str, type:str='file', debug_dest:str='!debug'):
        """
        :param filname: Path of the file.
        :parma type: to check for directory or file to copy files.
        """  
        if type == 'file' and debug_dest == '!debug':
            self.new_destination = self.destination
        elif type == 'file' and debug_dest != '!debug':
            self.new_destination = os.path.join(str(debug_dest), Path(filename).name)
        elif type == 'dir' and debug_dest != '!debug':
            self.new_destination = os.path.join(str(debug_dest), Path(filename).name)
        elif  type == 'dir' and debug_dest == '!debug':
            self.new_destination = os.path.join(str(self.destination), Path(filename).name)

        self.dest = shutil.copyfile(filename, self.new_destination)  

    def change_file_name(self, filename:str, output_dir:str):
        """
        :param filname: Path of the file.
        :output_dir: Output directory where to copy files from temporary directory.
        """
        shutil.copyfile(f"{filename}", f"{output_dir}/{ Path(filename).name}")

    def create_dubug_directory(self, func_name:str):
        """
        :param func_name: Function name by user to create directory for debug.
        """
        self.source = os.path.join(str(os.getcwd()), self.directory)
        self.debug_destination = os.path.join(str(self.pwd), f"{self.directory}_{func_name}")
        self.files = glob.glob(f"{str(self.source)}/*.*")
        self.file_type = 'file' if len(self.files) == 1 else 'dir'

        if os.path.isdir(str(self.debug_destination)) == False:
            os.mkdir(self.debug_destination)
            print("Directory '%s' created" %f"{self.debug_destination} for debug.")
            with multiprocessing.Pool(processes=self.worker) as pool: # auto closing workers
                pool.starmap(self.read_write_image, zip(self.files, [self.file_type]*len(self.files), [self.debug_destination]*len(self.files)))
        else:
            shutil.rmtree(f"{self.debug_destination}")
            os.mkdir(self.debug_destination)
            print("Directory '%s' created" %f"{self.debug_destination} for debug")
            with multiprocessing.Pool(processes=self.worker) as pool: # auto closing workers
                pool.starmap(self.read_write_image, zip(self.files, [self.file_type]*len(self.files) ,[self.debug_destination]*len(self.files)))
            
        self.return_array = glob.glob(f"{str(self.debug_destination)}/*.*") + glob.glob(f"{str(self.source)}/*.*")

        return self.return_array