from os import path
from pandas import read_csv
from plotly.express import histogram, bar, box, scatter

from scripts.constants import RESULTS_PATH, IMAGES_PATH, SELECTED

AREA_ORDER = ['Aachen', 'Halle (Saale)', 'Heidelberg', 'Osnabrück', 'Alfeld (Leine)', 'Aue-Bad Schlema',
              'Bad Soden am Taunus', 'Landau in der Pfalz', 'Ankum', 'Kandern', 'Kühlungsborn', 'Seefeld']
GROUP_ORDER = ['children 10-17', '45-64', '65 and over', 'men', 'women']


def bar_chart(column, color, x, filespec, prefix='analysis', path_end='15-18-21_Sat_104', filename=None,
              folder='analysis', assigned_color=None, title=None, labels=None, order=None, img_height=None, norm=None):
    df = read_csv(path.join(RESULTS_PATH, folder, f'{prefix}_{filespec}_{path_end}.csv'))
    sorted_df = df.sort_values(by=color)

    if title is None and column is not None:
        title = f'{column.replace("_", " ").capitalize()} in {filespec.replace("_", " ")}'

    if x == 'departure time':
        sorted_df['departure time'] = sorted_df['departure time'].astype(str)

    fig = histogram(sorted_df, x=x, y=column, color=color, color_discrete_map=assigned_color, title=title,
                    labels=labels, category_orders=order, barnorm=norm)
    fig.update_layout(bargap=0.5)

    if filename is None:
        fig.show()
    else:
        if prefix == 'all':
            img_height = 400
        fig.write_image(path.join(IMAGES_PATH, f'{filename}_{column}.jpeg'), height=img_height, scale=1.8)


def actual_bar_chart(column, color, x, filespec, prefix='analysis', path_end='15-18-21_Sat_104', filename=None,
                     folder='groups', assigned_color=None, title=None, labels=None, order=None,  barmode='relative'):
    df = read_csv(path.join(RESULTS_PATH, folder, f'{prefix}_{filespec}_{path_end}.csv'))
    sorted_df = df.sort_values(by=color)

    if title is None:
        title = f'{column.replace("_", " ").capitalize()} in {filespec.replace("_", " ")}'

    fig = bar(sorted_df, x=x, y=column, color=color, color_discrete_map=assigned_color, color_continuous_scale=['#636efa', '#ef553b'],
              title=title, labels=labels, category_orders=order)
    fig.update_layout(barmode=barmode, xaxis={'categoryorder': 'category descending'})

    if filename is None:
        fig.show()
    else:
        fig.write_image(path.join(IMAGES_PATH, f'bar_{filename}_{column}.jpg'), scale=1.8)


def all_box_chart(column, color, x, filespec, prefix='analysis', path_end='15-18-21_Sat_104', filename=None,
                  title=None, labels=None, order=None):
    df = read_csv(path.join(RESULTS_PATH, 'analysis', f'{prefix}_{filespec}_{path_end}.csv'))
    if title is None:
        title = f'{column.capitalize()} in {filespec}'
    title = title.replace('_', ' ')

    fig = box(df, x=x, y=column, color=color, title=title, labels=labels, category_orders=order)

    if filename is None:
        fig.show()
    else:
        fig.write_image(path.join(IMAGES_PATH, f'boxplot_{filename}_{column}.jpeg'), height=400, scale=1.8)


def scatter_chart(dependent, independent, color=None, prefix='analysis', path_end='15-18-21_Sat_104', filename=None,
                  title=None, labels=None):
    df = read_csv(path.join(RESULTS_PATH, 'analysis', f'{prefix}_{path_end}.csv'))
    if title is None:
        title = f'{dependent.replace("_", " ").capitalize()} / {independent.replace("_", " ")}'

    fig = scatter(df, x=independent, y=dependent, color=color, title=title, labels=labels)

    if filename:
        fig.write_image(path.join(IMAGES_PATH, f'scatter_{filename}_{dependent}-{independent}.jpeg'), scale=1.8)
    else:
        fig.show()


if __name__ == "__main__":
    pe = '15-18-21_Sat_104'

    bar_chart('average duration', 'level', 'area', 'starts_variables_filled', 'all', pe, 'all_overview',
              title='Average duration per start point',
              labels={
                  'average duration': 'average duration (in s)',
                  'level': 'regional centrality'},
              order={'area': AREA_ORDER,
                     'level': ['top', 'mid', 'base']})

    for var in ['average duration', 'average speed', 'distance_start_cinema']:
        all_box_chart(var, 'level', 'area', 'analysis_filled', 'all', pe, 'all',
                      title=f'Data distribution {var}',
                      labels={'average duration': 'average duration (in s)',
                              'average speed': 'average speed (in m/s)',
                              'distance_start_cinema': 'distance from start point to cinema (in m)',
                              'level': 'regional centrality'},
                      order={'area': AREA_ORDER,
                             'level': ['top', 'mid', 'base']})

    for var in ['distance_start_cinema', 'average walk share']:
        scatter_chart('average duration', var, 'level', 'all_analysis', pe, 'all_duration',
                      labels={'average duration': 'average duration (in s)',
                              'distance_start_cinema': 'distance from start point to cinema (in m)',
                              'average walk share': 'average walk share (in % of total route)',
                              'level': 'regional centrality'})
        scatter_chart('average speed', var, 'level', 'all_analysis', pe, 'all_speed',
                      labels={'average speed': 'average speed (in m/s)',
                              'distance_start_cinema': 'distance from start point to cinema (in m)',
                              'average walk share': 'average walk share (in % of total route)',
                              'level': 'regional centrality'})

    for name in SELECTED['top']:
        print(name)

        for var in ['distance_start_cinema']:
            scatter_chart('average duration', var, None, f'analysis_{name}', pe, name,
                          title=f'Average duration in {name}',
                          labels={'average duration': 'average duration (in s)',
                                  'distance_start_cinema': 'distance from start point to cinema (in m)'})

        # compare departure times
        for var in ['fastest mode', 'fastest overall mode']:
            bar_chart(None, var, 'departure time', name, 'time_analysis', pe, f'{var}_{name}',
                      assigned_color={'car': '#00cc96', 'transit': '#636efa', 'foot': '#ef553b'})

        # groups analysis
        for var in ['likely', 'possible']:
            bar_chart('average travel time', f'average {var}', 'group', name, 'groups', '[15, 18, 21]', f'{var}_{name}',
                      'groups',
                      assigned_color={'yes': '#00cc96', 'no': '#ef553b', 'no data': 'grey'},
                      labels={
                          'average travel time': 'average travel time (in s)',
                          'average likely': 'cinema is accessible<br>within "social life and<br>entertainment" time',
                          'average possible': 'cinema is accessible<br>within total leisure time'},
                      order={'group': GROUP_ORDER})

        actual_bar_chart('osm_cinemas', 'likely count', 'group', name, 'groups_cum', 'average', f'likely_{name}',
                         title=f'Cinemas accessible within "social life and entertainment" time frame<br>in {name}',
                         labels={'osm_cinemas': 'routes to cinemas',
                                 'likely count': 'accessible<br>cinemas'},
                         order={'group': GROUP_ORDER})
