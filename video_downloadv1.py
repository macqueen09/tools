# coding: utf-8
import requests
import os
import logging
from multiprocessing import Pool
import time

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
             
class VideoDownload(object):
    """
    单个视频的下载，下载到指定文件夹中
    """
    def __init__(self, args=None):
        super(VideoDownload, self).__init__()
        self.timeout = 900

    def process(self, url, video_dir=None):
        """
        Download video by url.
        """
        try:
            if url.startswith("https://"):
                url = url.replace('https://', 'http://')

            # video_dir 为存储单个下载视频的文件夹
            assert video_dir is not None, "Video_dir should be not None."
            if not os.path.exists(video_dir):
                os.makedirs(video_dir)

            video_name = url.split("/")[-1].split(".mp4")[0] + ".mp4"
            # tmp1 = url.split("/")[-1]
            # if '.jpg' in tmp1:
            #     video_name = tmp1.split(".jpg")[0] + ".jpg"
            # elif '.jpeg' in tmp1:
            #     video_name = tmp1.split(".jpeg")[0] + ".jpeg"
            # elif '.png' in tmp1:
            #     video_name = tmp1.split(".png")[0] + ".png"
            # elif '.webp' in tmp1:
            #     video_name = tmp1.split(".webp")[0] + ".webp"
            # elif '.gif' in tmp1:
            #     video_name = tmp1.split(".gif")[0] + ".gif"
            # else:
            #     print("__________unknown video", tmp1)
            video_path = os.path.join(video_dir, video_name)

            # 将下载的视频内容保存到video_path中
            # logging.info("Downloading >>>> ")
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 404:
                logging.info("Warning.... [{} is invalid].".format(url))
                return None
            else:
                # logging.info('-->begin', video_path)
                f_mp4 = open(video_path, "wb")
                f_mp4.write(response.content)
                f_mp4.close()
                # logging.info("Success.... {} ==> {}".format(video_name, video_dir))
                return video_path

        except Exception as e:
            return None

class VideoDownloadBatch(object):
    """
    根据url.txt, 批量下载视频到指定文件夹中
    py3有效；py2会因为pickle问题报错。
    """
    def __init__(self, parallel_num=20):
        super(VideoDownloadBatch, self).__init__()
        self.video = VideoDownload()
        
        self.pool = Pool(parallel_num)

    def process(self, txt, video_dir=None):
        urls = open(txt, "r").readlines()
        for url in urls:
            self.pool.apply_async(self.video.process, (url.strip(), video_dir))
        self.pool.close()
        self.pool.join()

if __name__ == "__main__":
    """
    url = "http://vd3.bdstatic.com/mda-mc2rd1mdmin8kaf9/hd/mda-mc2rd1mdmin8kaf9.mp4"
    download = VideoDownload()
    mp4_path = download.process(url, "video")
    logging.info(mp4_path)
    python3 video_download.py
    """
    video = VideoDownloadBatch(parallel_num=5)
    onevideo = VideoDownload()
    txt = "/Users/makaili/Downloads/hit_video_videourl.txt"
    #mp4_dir = "/home/bpfsrw_4/cuidonglin/dataset/wujian20210322_20210328/mp4/"  # 下载的mp4存储位置
    mp4_dir = "/Users/makaili/project/data/porn4whit"
    video.process(txt, mp4_dir)    # run batch download
    # fpin = open(txt, 'r')
    # for oneline in fpin.readlines():
    #     oneline = oneline.strip()
    #     onevideo.process(oneline, mp4)
        # print(oneline, '----')

 

    #time.sleep( 15 )
    print("_end success_", time.asctime( time.localtime(time.time()) ))
# 11406 python video_download.py