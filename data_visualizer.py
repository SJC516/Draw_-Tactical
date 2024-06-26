import numpy as np
import argparse

import os
from os import listdir
from os.path import join

import time
import matplotlib
matplotlib.use('agg')  # run backend
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Arc

from utils import DataFactory


def get_res(seqcond_,seq_):

    results_data= np.zeros((seq_.shape[0], 50, 23))

    results_data[:,:,:10]=seq_[:,:,:10]
    results_data[:,:,-3:-1]=seq_[:,:,-2:]

    for i in range (results_data.shape[0]):
        for j in range(results_data.shape[1]):
            if np.count_nonzero(1) == 1:
                # 获取元素为 1 的索引
                location_1=np.where(seqcond_[i,j]==1)[0]
                if not location_1.size==0 :
                    if not location_1[0]==5 :
                        index = location_1[0]
                #print("1 的位置是:", index)
                    results_data[i,j,-3:-1]=results_data[i,j,index*2:index*2+2]
    return results_data






def update_all(frame_id, player_circles, ball_circle, annotations, data):
    """ 
    Inputs
    ------
    frame_id : int
        automatically increased by 1
    player_circles : list of pyplot.Circle
        players' icon
    ball_circle : list of pyplot.Circle
        ball's icon
    annotations : pyplot.axes.annotate
        colors, texts, locations for ball and players
    data : float, shape=[amount, length, 23]
        23 = ball's xyz + 10 players's xy
    """
    max_length = data.shape[1]
    # players
    for j, circle in enumerate(player_circles):
        circle.center = data[frame_id, 2 + j * 2 + 0], data[frame_id, 2 +
                                                            j * 2 + 1]
        annotations[j].set_position(circle.center)
    # print("Frame:", frame_id)
    # ball
    ball_circle.center = data[frame_id, 0], data[frame_id, 1]
    annotations[10].set_position(ball_circle.center)

    return


def plot_data(data, length, file_path=None, if_save=False, fps=6, dpi=128):
    """
    Inputs
    ------
    data : float, shape=[amount, length, 23]
        23 = ball's xyz + 10 players's xy
    length : int
        how long would you like to plot
    file_path : str
        where to save the animation
    if_save : bool, optional
        save as .gif file or not
    fps : int, optional
        frame per second
    dpi : int, optional
        dot per inch
    Return
    ------
    """
    court = plt.imread("court.png")  # 500*939
    name_list = [
        'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', '0'
    ]

    # team A -> red circle, ball -> small green circle
    player_circles = []
    [
        player_circles.append(plt.Circle(xy=(0, 0), radius=2.5, color='r'))
        for _ in range(5)
    ]
    [
        player_circles.append(plt.Circle(xy=(0, 0), radius=2.5, color='b'))
        for _ in range(5)
    ]
    ball_circle = plt.Circle(xy=(0, 0), radius=1.5, color='g')

    # plot
    ax = plt.axes(xlim=(0, 100), ylim=(50, 0))
    ax.axis('off')
    fig = plt.gcf()
    ax.grid(False)

    for circle in player_circles:
        ax.add_patch(circle)
    ax.add_patch(ball_circle)

    # annotations on circles
    annotations = [
        ax.annotate(name_list[i],
                    xy=[0., 0.],
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontweight='bold') for i in range(11)
    ]
    # animation
    anim = animation.FuncAnimation(fig,
                                   update_all,
                                   fargs=(player_circles, ball_circle,
                                          annotations, data),
                                   frames=length,
                                   interval=100)

    plt.imshow(court, zorder=0, extent=[0, 100 - 6, 50, 0])
    if if_save:
        anim.save(file_path, fps=fps, dpi=dpi, writer='ffmpeg')
        print('!!!Animation is saved!!!')
    else:
        plt.show()
        print('!!!End!!!')

    # clear content
    plt.cla()
    plt.clf()


def test(test_data):
    """
    test only
    """
    '''train_data = np.load(opt.data_path)
    data_factory = DataFactory(train_data)
    train_data = data_factory.fetch_ori_data()
    train_data = data_factory.recover_data(train_data)'''
    for i in range(opt.amount):
        plot_data(test_data[i:i + 1],
                  length=100,
                  file_path=opt.save_path + 'play_' + str(i) + '.mp4',
                  if_save=opt.save)


if __name__ == '__main__':
    # parameters
    parser = argparse.ArgumentParser(description='NBA Games visulization')
    parser.add_argument('--save',
                        type=bool,
                        default=True,
                        help='bool, if save as gif file')
    parser.add_argument('--amount',
                        type=int,
                        default=10,
                        help='how many event do you want to plot')
    parser.add_argument('--seq_length',
                        type=int,
                        default=100,
                        help='how long for each event')
    parser.add_argument('--save_path',
                        type=str,
                        default='./SJC_0416',
                        help='string, path to save event animation')
    parser.add_argument('--data_path',
                        type=str,
                        default='../../data/FEATURES-4.npy',
                        help='string, path of target data')

    opt = parser.parse_args()
    
    seqcond=np.load('/Users/cesar/Library/Mobile Documents/com~apple~CloudDocs/Desktop/同步储存/Sports Analytics/hoop_transformer/BasketballGAN-master/data/SeqCond.npy')
    seq=np.load('/Users/cesar/Library/Mobile Documents/com~apple~CloudDocs/Desktop/同步储存/Sports Analytics/hoop_transformer/BasketballGAN-master/data/50Seq.npy')
    test_data=get_res(seqcond[:10,:,:],seq[:10,:,:])
    
    if not os.path.exists(opt.save_path):
        os.makedirs(opt.save_path)
    test(test_data)
