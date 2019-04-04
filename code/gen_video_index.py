from parseshot import *
#prefix = os.path.join('', 'TRECVID2019')
#prefix = os.path.join(prefix, 'Dataset')
prefix = '/home/reid/DATA/Trecvid2019/Dataset'
map_dict = get_map(collection)
lines = clip_video(clip_file=clip_file)

for video_index in range(0, 244):
    video_index = str(video_index)

    list = []
    [list.append(i) for i in lines if i[0] == video_index]


    with open(os.path.join('video_index', video_index + '.txt'), 'w') as f:

        for i in list:
            video = i[0]
            shot = i[1]
            path = os.path.join(prefix, video)
            path = os.path.join(path, shot)
            path = os.path.join(path, shot + '.mp4\n')
            f.write(path)





