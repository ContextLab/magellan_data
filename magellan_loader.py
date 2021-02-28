import numpy as np
import pandas as pd
import scipy as sp
import matplotlib as mpl
import seaborn as sns
import datetime as dt
from glob import glob as lsdir
import os
import itertools

def load_env(fname):
    return pd.read_json(fname)

def load_subj_data(fname, freq=None):
    x = pd.read_json(fname)
    if freq is not None:
        x = x.resample(freq).mean()
        x = x.drop('heading', axis=1)
    return x.loc[np.sum(np.isnan(x[['x', 'y']]), axis=1) == 0]

def get_conditions(data, columns, unique=False):
    if type(columns) not in [list, np.array]:
        columns = np.array(columns)
    vals = [data[c].values for c in columns]    

    if unique:
        return [np.unique(v) for v in vals]
    else:
        return vals

def apply_by_condition(x, columns, f, args=[], kwargs={}):
    vals = get_conditions(x, columns, unique=True)    
    inds = [[x[c] == v for v in vals[i]] for i, c in enumerate(columns)]

    results = []
    for i in itertools.product(*inds):
        next_inds = i[0]
        for j in range(1, len(columns)):
            next_inds = np.logical_and(next_inds, i[j])

        if np.any(next_inds):
            results.append(f(*[x.loc[next_inds], *args], **kwargs))
    return results

def get_env_dims(env):
    width = int(np.ceil(np.max(env['x'])))
    height = int(np.ceil(np.max(env['y'])))
    return width, height

def plot_environment(env):
    markers = {'landmark': 's', 'store': 'o'}
    palette = {'landmark': [0.9, 0.9, 0.9], 'store': [0.25, 0.25, 0.25]}
    sns.scatterplot(data=env, x='x', y='y', style='type', hue='type', legend=False, palette=palette, markers=markers, s=200)

    width, height = get_env_dims(env)

    x_intersections, y_intersections = np.meshgrid(np.arange(0, width + 1), np.arange(0, height + 1))
    ax = sns.scatterplot(x=x_intersections.ravel(), y=y_intersections.ravel(), marker='.', color=[0.85, 0.85, 0.85], s=50)

    #set grid
    ax.set_xlim([-0.5, width + 0.5])
    ax.set_ylim([-0.5, height + 0.5])
    return ax

def plot_envs(envs, size, scale=4):
    fig, ax = mpl.pyplot.subplots(nrows=size[0], ncols=size[1], figsize=(scale * size[1], scale * size[0]))
    for i, e in enumerate(np.unique(list(envs.keys()))): #quick way to get environments in sorted order
        mpl.pyplot.axes(ax.ravel()[i])
        a = plot_environment(envs[e])
        a.set_title(f'Layout {e}')

        if i < (np.prod(size) - size[1]): #bottommost row
            a.set_xlabel(None)

        if i not in np.arange(0, np.prod(size), size[1]): #leftmost column
            a.set_ylabel(None)

    for a in ax.ravel()[(i + 1):]:
        a.set_visible(False)
    
    return fix, ax

def plot_paths(x, envs, scale=4):
    import warnings    
    warnings.simplefilter('ignore')

    def plotter(data, ax, ind_gen):
        i, j = next(ind_gen)
        
        deliveries = get_conditions(data, ['delivery'])
        unique_deliveries = np.unique(deliveries)
        n_deliveries = len(unique_deliveries)

        forage_palette = sns.color_palette('crest', n_colors=n_deliveries)
        seek_palette = sns.color_palette('flare', n_colors=n_deliveries)
        auto_palette = sns.light_palette('seagreen', n_colors=n_deliveries)

        if type(ax) == np.ndarray:
            if ax.ndim == 2:
                a = ax[i, j]
            else:
                a = ax[np.max([i, j])]
        elif type(ax) == tuple:
            a = ax[np.max([i, j])]
        else:
            a = ax
        
        mpl.pyplot.axes(a)
        for k, d in enumerate(unique_deliveries):
            delivery_path = data.query(f'delivery == {d}')

            #forage path
            forage_path = delivery_path.query('mode == "forage"')
            mpl.pyplot.plot(forage_path['x'], forage_path['y'], c=forage_palette[k], linewidth=2)

            #seek path
            seek_path = delivery_path.query('mode == "seek"')
            mpl.pyplot.plot(seek_path['x'], seek_path['y'], c=seek_palette[k], linewidth=2)

            #auto path
            auto_path = delivery_path.query('mode == "autopilot"')
            mpl.pyplot.plot(auto_path['x'], auto_path['y'], c=auto_palette[k], linewidth=2)

        #plot environment
        env_id = data.iloc[0]['env']
        plot_environment(envs[env_id])

        #set title to current environment
        if i == 0 and j == 0:
            a.set_title(f'{np.unique(x["subj"])[0]}: Layout {env_id}')
        else:
            a.set_title(f'Layout {env_id}')

        #adjust tick labels
        if i == 0:
            a.xaxis.set_ticklabels([])
            a.set_xlabel(None)

        try:
            if i == ax.shape[0] - 1:
                a.set_xlabel(f'Environment {j}')
        except:
            a.set_xlabel(f'Environment {j}')

        if j == 0:
            a.set_ylabel(f'Session {i}')
        elif j > 0:
            a.yaxis.set_ticklabels([])
            a.set_ylabel(None)

    #create subplots
    columns = ['session', 'env_num']
    vals = get_conditions(x, columns, unique=True)
    sizes = [len(v) for v in vals]
    ranges = [np.arange(s, dtype=int) for s in sizes]

    fig, ax = mpl.pyplot.subplots(nrows=sizes[0], ncols=np.prod(sizes[1]), figsize=(scale * sizes[1], scale * sizes[0]))    
    apply_by_condition(x, columns, plotter, args=[ax, itertools.product(*ranges)])

    return fig, ax

def round_coords(x):
    x = x.copy()

    if type(x) == pd.DataFrame:
        x['x'] = x['x'].apply(np.round)
        x['y'] = x['y'].apply(np.round)
    else:
        x['x'] = np.round(x['x'])
        x['y'] = np.round(x['y'])
    return x
 
