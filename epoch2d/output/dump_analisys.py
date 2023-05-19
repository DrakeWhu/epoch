import os
import logging
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import sdf_helper as sh
import sdf
from io import BytesIO

base_directory = "/home/juan/Documentos/GitHub/epoch/epoch2d/output/dumps/density_scan"

logging.basicConfig(filename='dump_analisys.log', level=logging.INFO, format='%(asctime)s %(message)s')

def number_density_animation(data_list, output_directory):
    logging.info("Creating number density animation")
    fig, ax = plt.subplots()
    ims = []
    for i in range(len(data_list)):
        im = ax.imshow(data_list[i].T, animated=True)
        if i == 0:
            ax.imshow(data_list[i].T)
        ims.append([im])
    animation = ani.ArtistAnimation(fig, ims, interval=100, blit=False, repeat_delay=1000)
    output_file = os.path.join(output_directory, "number_density.gif")
    animation.save(output_file)

def ex_animation(data_list, output_directory):
    logging.info("Creating longitudinal electric field animation")
    fig, ax = plt.subplots()

    def animate(i):
        ax.cla()
        ex_row = data_list[i][:,150]

        ax.plot(x, ex_row)
        ax.set_xlabel('x')
        ax.set_ylabel('Ex')
        ax.set_title(f'Ex - Row {row_index} - Dump {i}')

    animation = ani.FuncAnimation(fig, animate, frames=len(data_list), interval = 100)
    animation_path = os.path.join(output_directory, 'ex.gif')
    animation.save(animation_path, writer='pillow')
            

def create_animations(directory):
    logging.info("Processing directory: %s", directory)
    file_names = os.listdir(directory)

    number_density_data = [sh.getdata(i, directory).Derived_Number_Density_electron.data for i in range(41)]
    number_density_animation(number_density_data, directory)

    ex_data = [sdf.read(f"{directory}/{file_name}").Electric_Field_Ex for file_name in file_names if file_name.endswith('.sdf')]
    ex_animation(ex_data, directory)

    # transversal_electric_field_data = [sh.getdata(i, directory).Electric_Field_Ey for i in range(40)]

for root, directories, files in os.walk(base_directory):
    for directory in directories:
        directory_path = os.path.join(root, directory)
        create_animations(directory_path)



