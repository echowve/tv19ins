import os

pwd = os.getcwd()
print("current work root path is {}".format(pwd))
ffmpeg_file  = 'ffmpeg-20190325-c3b517d-win64-static'




# dir = os.path.join(pwd, ffmpeg_file)
# dir = os.path.join(dir, 'bin')
# dir_ffmpeg = os.path.join(dir, 'ffmpeg.exe')

dir_ffmpeg = 'ffmpeg'

# check ffmpeg tools
# if not os.path.isfile(dir_ffmpeg):
#     raise(FileNotFoundError)

def get_map(collection):
    with open(os.path.join(pwd,collection)) as f:

        dict = {}
        video_id = 0
        for line in f.readlines():
            if len(line) < 40:
                continue
            dict[video_id] = line[10:-12]
            video_id = video_id + 1

        return dict


def clip_video(clip_file=None):
    with open(os.path.join(pwd, clip_file)) as f:
        lines = []
        for line in f.readlines():
            tmp = line.split(' ')
            line = []
            [line.append(i) for i in tmp if i is not '']
            if len(line)>2:
                lines.append(line)
        return lines


def split_video(lines_index=None, video_in=None, shot_out=None):

    i=0
    f = open('test.txt', 'w')
    for line in lines_index:
        video = line[0]
        shot = line[1]
        begin_time = line[2][1:-6]
        begin_time = begin_time.split(':')

        begin_time_int = int(begin_time[0])*3600 + int(begin_time[1])*60 + int(begin_time[2]) + 1


        end_time = line[3][1:-7]
        end_time = end_time.split(':')

        end_time_int = int(end_time[0])*3600 + int(end_time[1])*60 + int(end_time[2])



        real_video_name = map_dict[int(video)]

        geshi = real_video_name[-4:]
        d = os.path.join(video_in, real_video_name)

        outfile = shot + geshi

        outdir = os.path.join(shot_out, video)
        outdir = os.path.join(outdir, shot)
        os.makedirs(outdir, exist_ok=True)

        outfile = os.path.join(outdir, outfile)
        if begin_time_int >= end_time_int:
           continue


        cmd = dir_ffmpeg + ' -i ' + d + ' -ss ' + str(begin_time_int) + ' -to ' + str(end_time_int) + ' -strict -2 ' + outfile
        print(cmd)
        os.system(cmd)
        f.write(cmd)
        f.write('\n')

    f.close()









collection = 'split_files/eastenders.collection.xml'
clip_file = 'split_files/eastenders.masterShotReferenceTable'
video_dir = r'/home/jlx/trecvid2019/TRECVID/TRECVID2013/original/2013video/video/'
shot_save_dir = r'/home/jlx/trecvid2019/TRECVID/Dataset'

map_dict = get_map(collection)
lines = clip_video(clip_file=clip_file)
# with open('lines.txt', mode='w') as f:
#     for i in lines:
#         f.write(str(i))
#         f.write('\n')
split_video(lines_index=lines, video_in = video_dir, shot_out=shot_save_dir)






