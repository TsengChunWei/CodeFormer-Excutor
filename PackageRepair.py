from os import listdir, rename, makedirs
from os.path import dirname, basename, splitext, exists
from shutil import rmtree
from csv import writer as csvwriter
from csv import reader as csvreader
from inference_codeformer import main


def contain_ch_jp(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':  # 中日統一表意文字
            return True
        elif '\u3040' <= char <= '\u309f':  # 平假名
            return True
        elif '\u30a0' <= char <= '\u30ff':  # 片假名
            return True
        elif '\u31f0' <= char <= '\u31ff':  # 片假名擴展
            return True
        elif '\uFF66' <= char <= '\uFF9D':  # 半形片假名
            return True
    return False

class OneVidRepairClass():
    def __init__(self, repair_img) -> None:
        self.CF_folder = dirname(__file__)
        self.repair_img = repair_img
        self.Extensions = {'.mp4', '.avi', '.mov'}

    def Repairing(self, weight: float, bg: bool, face: bool, scale: int):
        origin_name, origin_ext = splitext(basename(self.repair_img))
        temp_img = f'{dirname(__file__)}/temp_storage/test_video{origin_ext}'
        rename(self.repair_img, temp_img)
        
        print("\n-------- Running CodeFormer... --------")
    
        _output_path_ = f'{dirname(__file__)}/results/test_video_{weight}'
        _bg_upsampler_ = 'realesrgan' if bg else 'None'

        main(weight, temp_img, _output_path_, _bg_upsampler_, face, scale)

        print('-------- Repair complete --------\n')

        rename(temp_img, self.repair_img)
        self.move_and_rename(f'{_output_path_}/test_video.mp4', f'{dirname(self.repair_img)}/{origin_name}.mp4')
        try:
            rmtree(f'{_output_path_}/final_results')
            print('Frames removed')
        except:
            print('Frames not deleted')

    def move_and_rename(self, src, dist):
        base, extension = splitext(dist)
        counter = 2
        while exists(dist):
            dist = f"{base} ({counter}){extension}"
            counter += 1
        rename(src, dist)


class OneImgRepairClass():
    def __init__(self, repair_img) -> None:
        self.CF_folder = dirname(__file__)
        self.repair_img = repair_img
        self.Extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

    def Repairing(self, weight: float, bg: bool, face: bool, scale: int):
        origin_name, origin_ext = splitext(basename(self.repair_img))
        temp_img = f'{dirname(__file__)}/temp_storage/test_img{origin_ext}'
        rename(self.repair_img, temp_img)
        
        print("\n-------- Running CodeFormer... --------")
    
        _output_path_ = f'{dirname(__file__)}/results/test_img_{weight}'
        _bg_upsampler_ = 'realesrgan' if bg else 'None'

        main(weight, temp_img, _output_path_, _bg_upsampler_, face, scale)

        print('-------- Repair complete --------\n')

        resultFolder = f'{_output_path_}/final_results'
        rename(temp_img, self.repair_img)
        self.move_and_rename(f'{resultFolder}/test_img.png', f'{dirname(self.repair_img)}/{origin_name}.png')

    def move_and_rename(self, src, dist):
        base, extension = splitext(dist)
        counter = 2
        while exists(dist):
            dist = f"{base} ({counter}){extension}"
            counter += 1
        rename(src, dist)

class RepairClass():
    def __init__(self, repair_folder) -> None:
        self.CF_folder = dirname(__file__)
        self.repair_folder = repair_folder
        self.temp_storage_folder = f'{dirname(__file__)}/temp_storage'
        self.Extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

    def Repairing(self, weight: float, bg: bool, face: bool, scale: int):

        print("\n-------- Running CodeFormer... --------")
    
        _input_path_ = self.temp_storage_folder if self.repair_folder else './inputs/whole_imgs'
        _temp_ = 'last_cname' if contain_ch_jp(self.repair_folder) else basename(self.repair_folder)
        _output_path_ = f'{dirname(__file__)}/results/{_temp_}_{weight}'
        _bg_upsampler_ = 'realesrgan' if bg else 'None'

        main(weight , _input_path_, _output_path_, _bg_upsampler_, face, scale)

        print('-------- Repair complete --------\n')

        self.resultFolder = f'{_output_path_}/final_results'

    
    def pathNameOperate(self):
        if not exists(self.temp_storage_folder):
            makedirs(self.temp_storage_folder)

        self.name_csv = f'{self.CF_folder}/_Names_.csv'

        imgFiles = [f for f in listdir(self.repair_folder) if splitext(f)[1].lower() in self.Extensions]

        count = 0
        with open(self.name_csv, 'w', newline='') as csvfile:
            writer = csvwriter(csvfile)
            for file in imgFiles:
                name, ext = splitext(file)
                old_name = f'{self.repair_folder}/{file}'
                new_name = f'{self.temp_storage_folder}/{count:03}{ext}'
                rename(old_name, new_name)
                writer.writerow([f'{count:03}', name, ext])
                count += 1
        print('Reorder success, available to run CodeFormer.')
    
    def recoverName(self):
        with open(self.name_csv, 'r') as csvfile:
            reader = csvreader(csvfile)
            for row in reader:
                num_name, original_name, original_ext = row
                result_name = f"{self.resultFolder}/{num_name}.png"
                result_recover_name = f"{self.resultFolder}/{original_name}.png"
                new_name = f"{self.temp_storage_folder}/{num_name}{original_ext}"
                old_name = f"{self.repair_folder}/{original_name}{original_ext}"
                rename(result_name, result_recover_name)
                rename(new_name, old_name)
                print(original_name, 'recover')
        print('Recover images name success.')
