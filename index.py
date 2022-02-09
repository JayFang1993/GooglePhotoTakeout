import os
import json
from datetime import datetime


def foreach_photo_modify_files(path):
    files = os.listdir(path)
    for fi in files:
        fi_d = os.path.join(path, fi)
        if os.path.isdir(fi_d):
            foreach_photo_modify_files(fi_d)
        else:
            file_abs_path = os.path.join(path, fi_d)
            if not file_abs_path.endswith('.json') and not file_abs_path.endswith('.DS_Store'):
                modify_photo_meta(file_abs_path)


def foreach_photo_remove_files(path):
    files = os.listdir(path)
    for fi in files:
        fi_d = os.path.join(path, fi)
        if os.path.isdir(fi_d):
            foreach_photo_remove_files(fi_d)
        else:
            file_abs_path = os.path.join(path, fi_d)
            if not file_abs_path.endswith('.json') and not file_abs_path.endswith('.DS_Store'):
                remove_dup(file_abs_path)


def foreach_photo_remove_json(path):
    files = os.listdir(path)
    for fi in files:
        fi_d = os.path.join(path, fi)
        if os.path.isdir(fi_d):
            foreach_photo_remove_files(fi_d)
        else:
            file_abs_path = os.path.join(path, fi_d)
            if file_abs_path.endswith('.json'):
                newpath = os.path.join(os.path.dirname(file_abs_path) + '/json', os.path.basename(file_abs_path))
                os.rename(file_abs_path, newpath);


def remove_dup(file_abs_path):
    try:
        filename = os.path.splitext(os.path.basename(file_abs_path))[0]
        filedir = os.path.dirname(file_abs_path)
        filetype = os.path.splitext(file_abs_path)[-1]
        if filename.startswith('IMG_'):
            filenameorigin = ''
            if filename.endswith('(1)'):
                filenameorigin = os.path.join(filedir, filename.replace('(1)', '')) + filetype
            elif filename.endswith('(2)'):
                filenameorigin = os.path.join(filedir, filename.replace('(2)', '')) + filetype
            elif filename.endswith('(3)'):
                filenameorigin = os.path.join(filedir, filename.replace('(3)', '')) + filetype
            else:
                return
            if os.path.exists(filenameorigin):
                size1 = os.path.getsize(filenameorigin)
                size2 = os.path.getsize(file_abs_path)
                if (size1 >= size2):
                    print('DELETE，' + file_abs_path + ',' + str(size2) + ',' + str(size1))
                    os.rename(file_abs_path, os.path.join(filedir + '/del/', os.path.basename(file_abs_path)))
                else:
                    print('DELETE，' + filenameorigin + ',' + str(size1) + ',' + str(size2))
                    os.rename(filenameorigin, os.path.join(filedir + '/del/', os.path.basename(filenameorigin)))
                    os.rename(file_abs_path, filenameorigin)
    except FileNotFoundError:
        print('error')
    return False


def modify_photo_meta(file_abs_path):
    originMeta = {}
    photo_time = 0
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
            if filename.endswith('(3)'):
                metaFile = os.path.join(filedir, filename.replace('(3)', '') + filetype + '(3).json')
        ## 长文件名
        if not os.path.exists(metaFile):
            if len(filename) > 40:
                start_reg = filename[0:40]
                for sub in os.listdir(filedir):
                    if sub.endswith('.json') and sub.startswith(start_reg):
                        metaFile = os.path.join(filedir, sub)

        with open(metaFile) as f:
            originMeta = json.load(f)
        photo_time = (originMeta['photoTakenTime']['timestamp'])
        photo_time = int(photo_time)
    except FileNotFoundError:
        print(file_abs_path + ',Meta 信息缺失')
        if len(filename.split('mmexport')) > 1:
            photo_time = int(filename.split('mmexport')[1]) / 1000
        elif len(filename.split('wx_camera_')) > 1:
            photo_time = int(filename.split('wx_camera_')[1]) / 1000
        elif len(filename.split('wx_camera_')) > 1:
            photo_time = int(filename.split('wx_camera_')[1]) / 1000
        else:
            return
    try:
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


path = '/Users/Jay/Desktop/需要处理'
try:
    os.mkdir(path + '/del')
except FileExistsError:
    print('文件夹已经存在')
try:
    os.mkdir(path + '/json')
except FileExistsError:
    print('文件夹已经存在')
foreach_photo_modify_files(path)
foreach_photo_remove_files(path)
foreach_photo_remove_json(path)
