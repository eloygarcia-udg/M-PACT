import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

from MPACT import compute_thickness

global msg


def one_view (df, save_fig=None):
    view = np.unique(np.unique(df['MammographyView']))[0]

    fig, ax = plt.subplots(figsize=(8,8))

    colours = np.array(['green']*len(df.index))
    colours[df['S-score'] < -2.0] = 'red'
    colours[df['S-score'] > 2.0] = 'blue'

    if not 'CompressionForceN' in df.columns:
        bv = np.arange(102., 2000, 10)
        t2_vis, t2min_vis, t2max_vis, sdim = compute_thickness(bv, view, None, 2)
        t3_vis, t3min_vis, t3max_vis, sdim = compute_thickness(bv, view, None, 3)

        ax.plot(bv, t2_vis)
        ax.fill_between(bv, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
        ax.fill_between(bv, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')

        ax.scatter(df['BreastVolumeCm3'], df['RecordedThicknessCm'], color=colours)
        for idx, row in df.iterrows():
            ax.text(25+row['BreastVolumeCm3'], 0.15+row['RecordedThicknessCm'], row['PatientID'],
                       horizontalalignment='center', verticalalignment='bottom')
        ax.title.set_text(f"Mammography view {view}")
        ax.set_ylabel("Thickness (cm)")
        ax.set_xlabel("Breast Volume (cm³)")
    else:
        bv = np.arange(102., 2000, 10)
        cf = np.arange(0.5, 12.0, 11.5/len(bv))

        t2_vis, t2min_vis, t2max_vis, sdim = compute_thickness(bv, view, bv/cf, 2)
        t3_vis, t3min_vis, t3max_vis, sdim = compute_thickness(bv, view, bv/cf, 3)

        ax.plot(cf, t2_vis)
        ax.fill_between(cf, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
        ax.fill_between(cf, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')

        ax.scatter(df['BreastVolumeCm3'] / df['CompressionForceN'], df['RecordedThicknessCm'], color=colours)
        for idx, row in df.iterrows():
            ax.text(row['BreastVolumeCm3'] / row['CompressionForceN'], 0.15+row['RecordedThicknessCm'], row['PatientID'],
                       horizontalalignment='center', verticalalignment='bottom')
        ax.title.set_text(f"Mammography view {view}")
        ax.set_ylabel("Thickness (cm)")
        ax.set_xlabel("Breast Volume / Compression Force (cm³ / N)")

    if not save_fig == None:
        if save_fig.endswith('.png'):
            plt.savefig(save_fig)
            print(f"Image saved at {save_fig}")
        else:
            plt.savefig(save_fig + '.png')
            print(f"Image saved at {save_fig+'.png'}")
    else:
        plt.show()



def two_views(df, save_fig=None):
    views = np.unique(df['MammographyView'])

    fig, ax = plt.subplots(ncols=len(views), figsize=(16,8))
    for i in range(len(views)):
        vi=views[i]

        temp_df = df[df['MammographyView']==vi]

        colours = np.array(['green']*len(temp_df.index))
        colours[temp_df['S-score'] < -2.0] = 'red'
        colours[temp_df['S-score'] > 2.0] = 'blue'

        if not 'CompressionForceN' in temp_df.columns:
            bv = np.arange(102., 2000, 10)
            t2_vis, t2min_vis, t2max_vis, sdim = compute_thickness(bv, vi, None, 2)
            t3_vis, t3min_vis, t3max_vis, sdim = compute_thickness(bv, vi, None, 3)

            ax[i].plot(bv, t2_vis)
            ax[i].fill_between(bv, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
            ax[i].fill_between(bv, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')

            ax[i].scatter(temp_df['BreastVolumeCm3'], temp_df['RecordedThicknessCm'], color=colours)
            for idx, row in temp_df.iterrows():
                ax[i].text(25+row['BreastVolumeCm3'], 0.15+row['RecordedThicknessCm'], row['PatientID'],
                           horizontalalignment='center', verticalalignment='bottom')
            ax[i].title.set_text(f"Mammography view {vi}")
            ax[i].set_ylabel("Thickness (cm)")
            ax[i].set_xlabel("Breast Volume (cm³)")
        else:
            bv = np.arange(102., 2000, 10)
            cf = np.arange(0.5, 12.0, 11.5/len(bv))

            t2_vis, t2min_vis, t2max_vis, sdim = compute_thickness(bv, vi, bv/cf, 2)
            t3_vis, t3min_vis, t3max_vis, sdim = compute_thickness(bv, vi, bv/cf, 3)

            ax[i].plot(cf, t2_vis)
            ax[i].fill_between(cf, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
            ax[i].fill_between(cf, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')

            ax[i].scatter(temp_df['BreastVolumeCm3'] / temp_df['CompressionForceN'], temp_df['RecordedThicknessCm'], color=colours)
            for idx, row in temp_df.iterrows():
                ax[i].text(row['BreastVolumeCm3'] / row['CompressionForceN'], 0.15+row['RecordedThicknessCm'], row['PatientID'],
                           horizontalalignment='center', verticalalignment='bottom')
            ax[i].title.set_text(f"Mammography view {vi}")
            ax[i].set_ylabel("Thickness (cm)")
            ax[i].set_xlabel("Breast Volume / Compression Force (cm³ / N)")

    if not save_fig == None:
        if save_fig.endswith('.png'):
            plt.savefig(save_fig)
            print(f"Image saved at {save_fig}")
        else:
            plt.savefig(save_fig + '.png')
            print(f"Image saved at {save_fig+'.png'}")
    else:
        plt.show()


def visualization(df, save_fig=None):
    views = np.unique(df['MammographyView'])
    if len(views)==1:
        one_view(df, save_fig)
    else:
        two_views(df, save_fig)
