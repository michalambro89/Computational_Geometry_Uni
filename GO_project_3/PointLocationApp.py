import PySimpleGUI as sg
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import os.path

fig, ax = plt.subplots()
ax.set_xlabel('y')
ax.set_ylabel('x')

min_x = 0
max_x = 0
min_y = 0
max_y = 0

def read_points_from_file(file_name):
    points = []
    with open(file_name, 'r') as file:
        for line in file:
            if line.strip():
                x, y = line.split()
                points.append((float(x), float(y)))
    return points

def draw_points(points, color, size, window: sg.Window):
    x = [point[1] for point in points]
    y = [point[0] for point in points]

    filtered_x = [x[i] for i in range(len(x)) if min_x <= x[i] <= max_x and min_y <= y[i] <= max_y]
    filtered_y = [y[i] for i in range(len(y)) if min_x <= x[i] <= max_x and min_y <= y[i] <= max_y]

    plt.scatter(filtered_x, filtered_y, color=color, s=size)
    plt.savefig('graph.png')
    window['graph'].update(filename='graph.png')

def draw_figure(points, color, line_width, window: sg.Window):
    global min_x, max_x, min_y, max_y
    x = [point[1] for point in points]
    y = [point[0] for point in points]

    plt.plot(x, y, color=color, linewidth=line_width)
    plt.savefig('graph.png')
    window['graph'].update(filename='graph.png')

    min_x = ax.get_xlim()[0]
    max_x = ax.get_xlim()[1]
    min_y = ax.get_ylim()[0]
    max_y = ax.get_ylim()[1]


def if_in_bounding_rectangle(figure_points, x, y):
    min_x = min([point[0] for point in figure_points])
    max_x = max([point[0] for point in figure_points])
    min_y = min([point[1] for point in figure_points])
    max_y = max([point[1] for point in figure_points])

    if min_x <= x <= max_x and min_y <= y <= max_y:
        return True
    else:
        return False
    
def if_in_figure(figure_points, x, y):
    if y > max([point[1] for point in figure_points]):
        return False

    on_edge = False
    counter = 0

    for i in range(len(figure_points)):
        point1 = figure_points[i]
        point2 = figure_points[(i + 1) % len(figure_points)]

        if (point1[1] == y == point2[1]) and (min(point1[0], point2[0]) <= x <= max(point1[0], point2[0])):
            return True

        if (point1[1] <= y < point2[1]) or (point2[1] <= y < point1[1]):
            if point1[1] != point2[1]:
                edge_x = point1[0] + (y - point1[1]) * (point2[0] - point1[0]) / (point2[1] - point1[1])
                if x == edge_x:
                    on_edge = True
                elif x < edge_x:
                    counter += 1

    if on_edge or (counter % 2 == 1):
        return True
    else:
        return False

def count_points_in_figure(figure_points, points):
    points_in_figure = 0
    for point in points:
        if if_in_bounding_rectangle(figure_points, point[0], point[1]):
            if if_in_figure(figure_points, point[0], point[1]):
                points_in_figure += 1
    return points_in_figure

def if_in_window(x, y, min_x, max_x, min_y, max_y):
    if min_x <= x <= max_x and min_y <= y <= max_y:
        return True
    else:
        return False
       
def main():
    px = sg.InputText(size=(10, 1), key='px')
    py = sg.InputText(size=(10, 1), key='py')
    P = sg.Frame('', [[px, py]])

    colors = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan']
    figure_color_combo = sg.Combo(colors, default_value='red', key='figure_color_combo', size=(10, 4), font=('Helvetica', 12),
                              change_submits=True)
    figure_line_width = sg.Combo(list(range(1, 11)), default_value=2, key='figure_line_width', size=(10, 4),
                             font=('Helvetica', 12), change_submits=True)
    point_color = sg.Combo(colors, default_value='red', key='point_color', size=(10, 4), font=('Helvetica', 12),
                           change_submits=True)
    point_size = sg.Combo(list(range(1, 11)), default_value=1, key='point_size', size=(1, 4),
                                font=('Helvetica', 12), change_submits=True)
    
    dodaj = sg.Button('Dodaj punkt', key='dodaj_button')
    points_in = sg.InputText(size=(10, 1), key='points_in', default_text='0', disabled=True, text_color='black', background_color='white')

    wczytaj_punkty = sg.Button('Wczytaj punkty z pliku', file_types=(('Pliki tekstowe', '*.txt'),), key='wczytaj_punkty')
    wczytaj_figure = sg.Button('Wczytaj wielokąt z pliku', file_types=(('Pliki tekstowe', '*.txt'),), key='wczytaj_figure')

    wyczysc = sg.Button('Wyczyść dane', key='wyczysc_button')
    
    if os.path.isfile('graph.png'):
        os.remove('graph.png')
    plt.plot(0, 0)
    plt.savefig('graph.png')
    graph_img = sg.Image(filename='graph.png', key='graph')

    layout = [
        [sg.Text('', size=(40, 1))],
        [sg.Text('', size=(40, 20)), sg.pin(graph_img, expand_x=True, expand_y=True), sg.Text('', size=(40, 20))],
        [sg.Text('', size=(65, 1)), sg.Text('Podaj współrzędne punktu P'), sg.Text('', size=(40, 1))],
        [sg.Text('', size=(45, 1)), sg.Text('Współrzędne punktu P'), P, dodaj, sg.Text('', size=(40, 1))],
        [sg.Text('', size=(55, 1)), sg.Text('Liczba punktów wewnątrz figury: '), points_in, sg.Text('', size=(40, 1))],
        [sg.Text('', size=(45, 1)), sg.Text('Kolor linii figury'), figure_color_combo, sg.Text('Szerokość linii figury'), figure_line_width], 
        [sg.Text('', size=(45, 1)), sg.Text('Kolor punktu P'), point_color, sg.Text('Rozmiar punktu P'), point_size],
        [sg.Text('', size=(55, 1)),wczytaj_punkty, wczytaj_figure],
        [sg.Text('', size=(70, 1)), wyczysc, sg.Text('', size=(40, 1))]
    ]

    window = sg.Window('PointLocationApp', layout)
    window.finalize()
    figure_points = []


    while True:
        points = []
        points_filename = ''
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            if os.path.isfile('graph.png'):
                os.remove('graph.png')
            break

        points_in = int(values.get('points_in', 0) or 0)

        if event == 'wczytaj_punkty':
            points_in = 0
            try:
                points_filename = askopenfilename(filetypes=(('Pliki tekstowe', '*.txt'),))
                if points_filename:
                    points = read_points_from_file(points_filename)
                    if figure_points:
                        draw_points(points, values['point_color'], values['point_size'], window)
                        points_in = points_in + count_points_in_figure(figure_points, points)
                        window['points_in'].update(points_in)
                    else:
                        sg.popup_error('nie wczytano wielokata')
            except Exception as e:
                sg.popup_error(f'błąd: {e}')

        if event == 'wczytaj_figure':
            points_in = 0
            points = []
            figure_points = []
            if os.path.isfile('graph.png'):
                os.remove('graph.png')

            fig, ax = plt.subplots()
            ax.set_xlabel('y')
            ax.set_ylabel('x')

            plt.savefig('graph.png')
            window['graph'].update(filename='graph.png')
            window['points_in'].update(points_in)
            
            try:
                figure_filename = askopenfilename(filetypes=(('Pliki tekstowe', '*.txt'),))
                if figure_filename:
                    figure_points = read_points_from_file(figure_filename)
                    draw_figure(figure_points, values['figure_color_combo'], values['figure_line_width'], window)
                    if points:
                        draw_points(points, values['point_color'], values['point_size'], window)
                        points_in = points_in + count_points_in_figure(figure_points, points)
                        window['points_in'].update(points_in)
            except:
                sg.popup_error('Nie wybrano pliku!')

        if event == 'dodaj_button':
            try:
                x = float(values['px'])
                y = float(values['py'])
                if figure_points:
                    if if_in_window(x, y, min_x, max_x, min_y, max_y):
                        if if_in_bounding_rectangle(figure_points, x, y):
                            if if_in_figure(figure_points, x, y):
                                points_in += 1
                                sg.popup_ok('Punkt wewnątrz wielokąta')
                            else:
                                sg.popup_ok('Punkt poza wielokątem')
                        points.append((x, y))
                        draw_points(points, values['point_color'], values['point_size'], window)
                        window['points_in'].update(points_in)
                        if not if_in_bounding_rectangle(figure_points, x, y):
                            sg.popup_ok('Punkt poza wielokątem')
                    else:
                        sg.popup_error('Punkt poza oknem')
                else:
                    sg.popup_error('Nie wczytano wielokata')
            except:
                sg.popup_error('Niepoprawne wspolrzedne punktu')

        if event == 'figure_color_combo':
            draw_figure(figure_points, values['figure_color_combo'], values['figure_line_width'], window)

        if event == 'figure_line_width':
            draw_figure(figure_points, values['figure_color_combo'], values['figure_line_width'], window)

        if event == 'point_color':
            draw_points(points, values['point_color'], values['point_size'], window)

        if event == 'point_size':
            draw_points(points, values['point_color'], values['point_size'], window)

        if event == 'wyczysc_button':
            points_in = 0
            points = []
            figure_points = []
            plt.clf()
            if os.path.isfile('graph.png'):
                os.remove('graph.png')
            plt.plot(0, 0)
            plt.savefig('graph.png')
            window['graph'].update(filename='graph.png')
            window['points_in'].update(points_in)

if __name__ == "__main__":
    sg.theme('DarkBlue')
    main()