import os
import json
from datetime import datetime


def foreach_photo_files(path):
    files = os.listdir(path)
    for fi in files:
        fi_d = os.path.join(path, fi)
        if os.path.isdir(fi_d):
            foreach_photo_files(fi_d)
        else:
            file_abs_path = os.path.join(path, fi_d)
            if not file_abs_path.endswith('.json') and not file_abs_path.endswith('.DS_Store'):
                modify_photo_meta(file_abs_path)


def modify_photo_meta(file_abs_path):
    originMeta = {}
    try:
        filename = os.path.splitext(os.path.basename(file_abs_path))[0]
        filedir = os.path.dirname(file_abs_path)
        filetype = os.path.splitext(file_abs_path)[-1]
        metaFile = file_abs_path + '.json'
        ## 重复文件
        if not os.path.exists(metaFile):
            if filename.endswith('(1)'):
                metaFile = os.path.join(filedir, filename.replace('(1)', '') + filetype + '(1).json')
            if filename.endswith('(2)'):
                metaFile = os.path.join(filedir, filename.replace('(2)', '') + filetype + '(2).json')
        ## 长文件名
        if not os.path.exists(metaFile):
            if len(filename) > 40:
                start_reg = filename[0:40]
                for sub in os.listdir(filedir):
                    if sub.endswith('.json') and sub.startswith(start_reg):
                        metaFile = os.path.join(filedir, sub)

        with open(metaFile) as f:
            originMeta = json.load(f)
    except FileNotFoundError:
        print(file_abs_path + ',Meta 信息缺失')
        return
    try:
        photo_time = (originMeta['photoTakenTime']['timestamp'])
        photo_time = int(photo_time)

        dt_object = datetime.fromtimestamp(photo_time)
        time_str = dt_object.strftime('%Y%m%d%H%M.%S')
        cmd = 'touch -m -t ' + time_str + ' ' + file_abs_path.replace('(', '\(').replace(')', '\)').replace(' ',
                                                                                                            '\ ')
        os.system(cmd)
    except KeyError:
        print(file_abs_path + ',没有Meta信息')

    # with exiftool.ExifTool() as et:
    #     metadata = et.get_metadata(file_abs_path)
    #     print("{},{},{}".format(metadata["EXIF:CreateDate"], metadata['EXIF:GPSLongitude'], metadata['EXIF:Model']))


path = '/Users/Jay/Desktop/Takeout/Google/2020'
foreach_photo_files(path)
