from source.Transform import Transformation, file
import cv2
from pathlib import Path
import time

class ImageProcess(Transformation):

    def __init__(self, file_path, temp_name, num_worker):
        super().__init__(file_path, temp_name, num_worker, debug=False)

    @Transformation.transform
    def flip(self, input=file, flipside=0):
        self.image = cv2.imread(input, cv2.IMREAD_GRAYSCALE)
        self.flip = cv2.flip(self.image, flipside)
        cv2.imwrite(input, self.flip)
        print(f"{Path(input).name} is fliped.")
        return self

    @Transformation.transform
    def resize_image(self, input=file, height=100, width=100):
        self.image = cv2.imread(input, cv2.IMREAD_GRAYSCALE)
        self.resized_img = cv2.resize(self.image, (width, height), interpolation = cv2.INTER_NEAREST)    
        cv2.imwrite(input, self.resized_img)
        print(f"{Path(input).name} is resized.")
        return self
                    

test = ImageProcess('', 'temp', num_worker=2).\
    flip(flipside=0).resize_image().output('')
print(test)

# t1 = time.perf_counter()
# folder_test = ImageProcess('/home/ubuntu/project/images/1000_images/', 'temp', num_worker=2). \
#     flip(flipside=0).resize_image(height=300, width=500).output('/home/ubuntu/project/python-base-class/results/')
# print(folder_test)
# print(time.perf_counter() - t1)