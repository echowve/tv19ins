import torch
from torch.autograd import Variable
import numpy as np

from dataset import Video
from spatial_transforms import (Compose, Normalize, Scale, CenterCrop, ToTensor)
from temporal_transforms import LoopPadding

def classify_video_trecvid(video_dir, model, opt):
    assert opt.mode is 'feature'

    spatial_transform = Compose([Scale(opt.sample_size),
                                 CenterCrop(opt.sample_size),
                                 ToTensor(),
                                 Normalize(opt.mean, [1, 1, 1])])
    temporal_transform = LoopPadding(opt.sample_duration)
    data = Video(video_dir, spatial_transform=spatial_transform,
                 temporal_transform=temporal_transform,
                 sample_duration=opt.sample_duration)
    data_loader = torch.utils.data.DataLoader(data, batch_size=opt.batch_size,
                                              shuffle=False, num_workers=opt.n_threads, pin_memory=True)

    video_outputs = []
    video_indexes = []
    for i, (inputs, index) in enumerate(data_loader):
        inputs = Variable(inputs, volatile=True)
        outputs = model(inputs)

        video_outputs.append(outputs.cpu().data)
        video_indexes.append(index)


    video_outputs = np.array(video_outputs)
    video_indexes = np.array(video_indexes)

    return np.hstack(video_indexes, video_outputs)

    # video_outputs = torch.cat(video_outputs)
    # video_segments = torch.cat(video_segments)
    # results = {
    #     'video': video_name,
    #     'clips': []
    # }
    #
    # _, max_indices = video_outputs.max(dim=1)
    # for i in range(video_outputs.size(0)):
    #     clip_results = {
    #         'segment': video_segments[i].tolist(),
    #     }
    #
    #     if opt.mode == 'score':
    #         clip_results['label'] = class_names[max_indices[i]]
    #         clip_results['scores'] = video_outputs[i].tolist()
    #     elif opt.mode == 'feature':
    #         clip_results['features'] = video_outputs[i].tolist()
    #
    #     results['clips'].append(clip_results)
    #
    # return results
