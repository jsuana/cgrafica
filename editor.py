from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from read_bmp import RImage
import os

class Editor():

  def __init__(self):
    self.ed_root = Tk()
    self.ed_root.geometry('700x400')
    self.ed_root.resizable(width=False,height=False)
    self.ed_root.title('Editor de Imágenes')
    self.ed_root.option_add('*tearOff', False)

    #Definiendo barra de menú
    menu_bar = Menu(self.ed_root)
    self.ed_root['menu'] = menu_bar
    menu_bar_archivo = Menu(menu_bar)
    menu_bar_pgi = Menu(menu_bar)
    menu_bar_ftl = Menu(menu_bar)
    menu_bar_tg = Menu(menu_bar)
    menu_bar_ctf = Menu(menu_bar)

    menu_bar.add_cascade(menu=menu_bar_archivo,label="Archivo")
    menu_bar_archivo.add_command(label='Abrir', command=self.f_open_image,underline=0, compound=LEFT)
    menu_bar_archivo.add_command(label='Abrir BMP', command=self.f_open_bmp,underline=0, compound=LEFT)
    menu_bar_archivo.add_separator()
    menu_bar_archivo.add_command(label='Cerrar', command=self.f_exit,underline=0, compound=LEFT)

    menu_bar.add_cascade(menu=menu_bar_pgi,label="Procesamiento")
    menu_bar.add_cascade(menu=menu_bar_ftl,label="Filtros")
    menu_bar.add_cascade(menu=menu_bar_tg,label="Transformaciones")
    menu_bar.add_cascade(menu=menu_bar_ctf,label="Dominio frecuencial")

    self.frame_c_image=Frame(self.ed_root, relief="raised", width=500, height=400)
    self.frame_c_image.grid(row=0, column=0)
    self.frame_image_label=Frame(self.frame_c_image, relief="raised", width=500, height=25, border=1)
    self.frame_image_label.grid(row=0, column=0)

    self.frame_image_img=Frame(self.frame_c_image, relief="raised", width=500, height=375)
    self.frame_image_img.grid(row=1, column=0)

    self.frame_c_param=Frame(self.ed_root, relief="raised", width=200, height=400)
    self.frame_c_param.grid(row=0, column=1)
    self.frame_param_label=Frame(self.frame_c_param, relief="raised", width=200, height=25, border=1)
    self.frame_param_label.grid(row=0, column=0)

    self.frame_param_data=Frame(self.frame_c_param, relief="raised", width=200, height=375, border=1)
    self.frame_param_data.grid(row=1, column=0)
    self.frame_param_data.grid_propagate(0)

    # Create a canvas that can fit the above image
    self.canvas_image_ing = Canvas(self.frame_image_img, width = 495, height = 370)
    self.canvas_image_ing.pack()

    self.var_image_label = StringVar()
    self.image_label = Label(self.frame_image_label, textvariable=self.var_image_label)

    self.var_param_label = StringVar()
    self.param_label = Label(self.frame_param_label, textvariable=self.var_param_label)

    self.ed_root.mainloop()

  def f_open_image(self):
    self.ed_root.filename =  filedialog.askopenfilename(initialdir=os.getcwd(),title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    if not self.ed_root.filename:
      return
    self.var_image_label.set(self.ed_root.filename)
    self.image_label.pack()
    self.cv_img = cv2.cvtColor(cv2.imread(self.ed_root.filename), cv2.COLOR_BGR2RGB)
    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
    self.height, self.width, no_channels = self.cv_img.shape
    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
    self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
    # Add a PhotoImage to the Canvas
    self.canvas_image_ing.create_image(0, 0, image=self.photo, anchor=NW)

  def f_open_bmp(self):
    self.ed_root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select BMP File", filetypes=[("BMP Files","*.bmp")])
    if not self.ed_root.filename:
      return
    self.var_image_label.set(self.ed_root.filename)
    self.image_label.pack()
    n_image = RImage()
    n_image.clean_data()
    n_image.read_rows(self.ed_root.filename)
    n_image.repack_sub_pixels()

    self.var_param_label.set("Parametros")
    self.param_label.pack()

    Label(self.frame_param_data, text="Tipo:  " + str(n_image.header_image_file["type"])).grid(row=0,ipadx = 10,ipady = 10)
    Label(self.frame_param_data, text="Tamaño:  " + str(n_image.header_image_file["size"])).grid(row=1,ipadx = 10,ipady = 10)
    Label(self.frame_param_data, text="Ancho:  " + str(n_image.header_image_file["width"])).grid(row=2,ipadx = 10,ipady = 10)
    Label(self.frame_param_data, text="Alto:  " + str(n_image.header_image_file["height"])).grid(row=3,ipadx = 10,ipady = 10)
    Label(self.frame_param_data, text="Planos de color:  " + str(n_image.header_image_file["colour_planes"])).grid(row=4,ipadx = 10,ipady = 10)
    Label(self.frame_param_data, text="Bits por pixel:  " + str(n_image.header_image_file["bits_per_pixel"])).grid(row=5,ipadx = 10,ipady = 10)
    Label(self.frame_param_data, text="Metodo de compresion:  " + str(n_image.header_image_file["compression_method"])).grid(row=6,ipadx = 10,ipady = 10)
    Label(self.frame_param_data, text="Numero de colores:  " + str(n_image.header_image_file["number_colours"])).grid(row=7,ipadx = 10,ipady = 10)

    w = n_image.header_image_file["width"]
    h = n_image.header_image_file["height"]
    image_recompose = Image.new('RGB', (w, h), "white")
    image_recompose.putdata(n_image.list_pixels)
    self.photo = ImageTk.PhotoImage(image = image_recompose)
    self.canvas_image_ing.create_image(0, 0, image=self.photo, anchor=NW)


  def f_exit(self):
    #Exit
    self.ed_root.destroy()

def main():
    mi_editor = Editor()
    return 0

if __name__ == '__main__':
    main()
