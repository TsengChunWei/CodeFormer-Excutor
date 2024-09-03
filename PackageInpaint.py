from os import listdir, rename, makedirs
from os.path import dirname, basename, splitext, exists
from csv import writer as csvwriter
from csv import reader as csvreader
from inference_inpainting import main


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

class OneImgInpaintClass():
    def __init__(self, inpaint_img) -> None:
        self.CF_folder = dirname(__file__)
        self.inpaint_img = inpaint_img

    def Inpainting(self):
        origin_name, origin_ext = splitext(basename(self.inpaint_img))
        temp_img = f'{dirname(__file__)}/temp_storage/test_img{origin_ext}'
        rename(self.inpaint_img, temp_img)
        
        print("\n-------- Running CodeFormer... --------")
    
        _output_path_ = f'{dirname(__file__)}/results/test_inpainting_img'

        main(temp_img, _output_path_)

        print('-------- Repair complete --------\n')

        rename(temp_img, self.inpaint_img)
        self.move_and_rename(f'{_output_path_}/test_img.png', f'{dirname(self.inpaint_img)}/{origin_name}.png')

    def move_and_rename(self, src, dist):
        base, extension = splitext(dist)
        counter = 2
        while exists(dist):
            dist = f"{base} ({counter}){extension}"
            counter += 1
        rename(src, dist)


class InpaintClass():
    def __init__(self, repair_folder) -> None:
        self.CF_folder = dirname(__file__)
        self.repair_folder = repair_folder
        self.temp_storage_folder = f'{dirname(__file__)}/temp_storage'
        self.Extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

    def Inpainting(self):

        print("\n-------- Running CodeFormer... --------")
    
        _input_path_ = self.temp_storage_folder if self.repair_folder else './inputs/masked_faces'
        _temp_ = 'last_cname' if contain_ch_jp(self.repair_folder) else basename(self.repair_folder)
        self.resultFolder = f'{dirname(__file__)}/results/{_temp_}_inpaint'

        main(_input_path_, self.resultFolder)

        print('-------- Repair complete --------\n')

    
    def pathNameOperate(self):
        if not exists(self.temp_storage_folder):
            makedirs(self.temp_storage_folder)

        self.name_csv = f'{self.CF_folder}/_Names_.csv'

        imgFiles = [f for f in listdir(self.repair_folder) if splitext(f)[1].lower() == '.png']

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