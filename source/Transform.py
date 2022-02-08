import glob
from pathlib import Path
import os
import shutil
import multiprocessing
from functools import wraps
from cv2 import flip
nb_cores = multiprocessing.cpu_count()   # Get number of cpu
# Import base class
from source.FileHandle import FileHandling

class Transformation(FileHandling):
    """
    Get the base class for handling copy files and renaming the files
    """
    return_array = []
    global file
    file = ''

    def __init__(self, filepath:str, dir_name:str, num_worker:int=nb_cores, debug:bool=False):
        """
        :filepath: File path from user.
        :dir_name: Directory name by user.
        :worker: Number of worker given by user default it takes by var nb_cores.
        :debug: bool True for debugging.
        """
        super().__init__(dir_name, debug)
        self.temp_folder = self.destination
        self.worker = num_worker
        self.debug = debug

        # check the filepath if file or directory of files.
        if os.path.isfile(filepath):
            print("Creating temporary file.")
            self.name = Path(filepath).name   
            self.source = filepath
            self.destination = f"{self.destination}/{self.name}"
            super().read_write_image(self.source, 'file')
            Transformation.return_array = [self.destination]
            return True 

        elif os.path.isdir(filepath):
            print("Creating temporary files from directory")
            self.source = glob.glob(f"{str(filepath)}/*.*")
            with multiprocessing.Pool(processes=self.worker) as pool: # auto closing workers
                pool.starmap(super().read_write_image, zip(self.source, ['dir']*len(self.source)))
            Transformation.return_array = glob.glob(f"{str(self.destination)}/*.*")
            return True

        else:
            print(f"Error: {filepath} does not exist.")
            exit()
    def output(self, output_dir:str):
        """
        :param output_dir: Output directory for user.
        """
        self.output_dir = output_dir
        if os.path.isdir(self.output_dir):
            self.source = glob.glob(f"{str(self.temp_folder)}/*.*")
            with multiprocessing.Pool(processes=self.worker) as pool:
                pool.starmap(super().change_file_name, zip(self.source, [self.output_dir]* len(self.source)))
            shutil.rmtree(f"{self.temp_folder}")
        return "Success"

    # decorator function to perform the task for each file in temporary directory
    def transform(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            return_array = Transformation.return_array
            return_func = ''
            if self.debug == True:
                function_name = func.__name__
                return_array = super().create_dubug_directory(func_name=function_name)   
            for file in return_array:
                return_func = func(self, input=file)
            return return_func
        return decorator


  