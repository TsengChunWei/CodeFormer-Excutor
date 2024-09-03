from PackageRepair import OneImgRepairClass, RepairClass, OneVidRepairClass
from PackageInpaint import OneImgInpaintClass, InpaintClass
from PackageColorize import OneImgColorizeClass, ColorizeClass
from FileMover import FileMover


def One(_img_, _weight_p_, _bg_p_, _face_p_, _scale_p_):
    ORC = OneImgRepairClass(_img_)
    ORC.Repairing(_weight_p_, _bg_p_, _face_p_, _scale_p_)

def Multiple(_origin_, _repair_, _weight_p_, _bg_p_, _face_p_, _scale_p_):
    if not _origin_:
        return
    RC = RepairClass(_origin_)
    RC.pathNameOperate()
    RC.Repairing(_weight_p_, _bg_p_, _face_p_, _scale_p_)
    RC.recoverName()
    if _repair_ == '':
        file_mover = FileMover(RC.resultFolder, _origin_)
    else:
        file_mover = FileMover(RC.resultFolder, _repair_)
    file_mover.move_files()

def One_video(_img_, _weight_p_, _bg_p_, _face_p_, _scale_p_):
    OVRC = OneVidRepairClass(_img_)
    OVRC.Repairing(_weight_p_, _bg_p_, _face_p_, _scale_p_)


def One_inpaint(_img_):
    OIC = OneImgInpaintClass(_img_)
    OIC.Inpainting()

def Multiple_inpaint(_origin_, _repair_):
    if not _origin_:
        return
    IC = InpaintClass(_origin_)
    IC.pathNameOperate()
    IC.Inpainting()
    IC.recoverName()
    if _repair_ == '':
        file_mover = FileMover(IC.resultFolder, _origin_)
    else:
        file_mover = FileMover(IC.resultFolder, _repair_)
    file_mover.move_files()

def One_colorize(_img_):
    OCC = OneImgColorizeClass(_img_)
    OCC.Colorization()

def Multiple_colorize(_origin_, _repair_):
    if not _origin_:
        return
    CC = ColorizeClass(_origin_)
    CC.pathNameOperate()
    CC.Colorization()
    CC.recoverName()
    if _repair_ == '':
        file_mover = FileMover(CC.resultFolder, _origin_)
    else:
        file_mover = FileMover(CC.resultFolder, _repair_)
    file_mover.move_files()


if __name__ == "__main__":
    _weight_p_, _bg_p_, _face_p_, _scale_p_ = 0.7, True, False, 2

    # _img_ = 'C:/Users/willi/Desktop/一/一.jpg'
    # One(_img_, _weight_p_, _bg_p_, _face_p_, _scale_p_)
    
    # _origin_ = 'C:/Users/willi/Desktop/一'
    # _repair_ = 'C:/Users/willi/Desktop/一/二s'
    # Multiple(_origin_, _repair_, _weight_p_, _bg_p_, _face_p_, _scale_p_)

    _video_ = 'C:/Users/willi/Desktop/一/四/兎田ぺこらさん、新しい挨拶がセンシティブすぎると話題に.mp4'
    One_video(_video_, _weight_p_, _bg_p_, _face_p_, _scale_p_)

    # _img_ = 'C:/Users/willi/Desktop/一/三/三.png'
    # One_inpaint(_img_)

    # _origin_ = 'C:/Users/willi/Desktop/一/三'
    # _repair_ = 'C:/Users/willi/Desktop/一/二'
    # Multiple_inpaint(_origin_, _repair_)


    # _img_ = 'C:/Users/willi/Desktop/一/五/四.png'
    # One_colorize(_img_)

    # _origin_ = 'C:/Users/willi/Desktop/一/五'
    # _repair_ = 'C:/Users/willi/Desktop/一/二'
    # Multiple_colorize(_origin_, _repair_)