import os
import sys
import json
import subprocess
import numpy as np
import torch
from torch import nn
import scipy.io as sio

from opts import parse_opts
from model import generate_model
from mean import get_mean
from classify import classify_video_trecvid

if __name__=="__main__":
    opt = parse_opts()

    opt.model_name = 'resnet'
    opt.model_depth  = 50
    opt.mean = get_mean()
    opt.arch = '{}-{}'.format(opt.model_name, opt.model_depth)
    opt.sample_size = 112
    opt.sample_duration = 16
    opt.n_classes = 400
    opt.model = 'model_data/resnet-50-kinetics.pth'
    opt.mode = 'feature'
    opt.video_index_dir = 'video_index'
    model = generate_model(opt)
    print('loading model {}'.format(opt.model))
    model_data = torch.load(opt.model)
    assert opt.arch == model_data['arch']
    model.load_state_dict(model_data['state_dict'])
    model.eval()
    if opt.verbose:
        print(model)

    # input_files = []
    # with open(opt.input, 'r') as f:
    #     for row in f:
    #         input_files.append(row[:-1])

    # class_names = []
    # with open('class_names_list') as f:
    #     for row in f:
    #         class_names.append(row[:-1])

    ffmpeg_loglevel = 'quiet'
    if opt.verbose:
        ffmpeg_loglevel = 'info'

    if os.path.exists('tmp'):
        subprocess.call('rm -rf tmp', shell=True)



    for video_id in range(opt.begin_video, opt.end_video+1):

        outputs = []
        flag = 0
        with open(os.path.join(opt.video_index_dir, str(video_id)+'.txt')) as input_files:

            for input_file in input_files:
                video_path = input_file[0:-1]
                # video_path = '/home/reid/DATA/Trecvid2019/Dataset/0/shot0_615/shot0_615.mp4'
                if os.path.exists(video_path):
                    print(video_path)
                    subprocess.call('mkdir tmp', shell=True)
                    subprocess.call('ffmpeg -i {} tmp/image_%05d.jpg'.format(video_path),
                                    shell=True)

                    result = classify_video_trecvid('tmp', model, opt, video_path)
                    if flag == 0:
                        outputs = result
                        flag = 1
                    else:
                        outputs = np.vstack((outputs, result))


                    subprocess.call('rm -rf tmp', shell=True)

                else:
                    print('{} does not exist'.format(input_file))

        if os.path.exists('tmp'):
            subprocess.call('rm -rf tmp', shell=True)

        os.makedirs('result', exist_ok=True)
        sio.savemat(os.path.join('result', str(video_id)), {'feat': outputs})
    # with open(opt.output, 'w') as f:
    #     json.dump(outputs, f)
