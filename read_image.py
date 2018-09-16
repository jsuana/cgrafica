import struct
from PIL import Image

class RImage:
  rows = []
  list_pixels = []
  header_image_file = {}

  def read_file_header(self, image_file):
    self.header_image_file={
      "type": image_file.read(2),
      "size": struct.unpack('I', image_file.read(4))[0],
      "reserved_1": struct.unpack('H', image_file.read(2))[0],
      "reserved_2": struct.unpack('H', image_file.read(2))[0],
      "offset": struct.unpack('I', image_file.read(4))[0],
      "dib_header_size": struct.unpack('I', image_file.read(4))[0],
      "width": struct.unpack('I', image_file.read(4))[0],
      "height": struct.unpack('I', image_file.read(4))[0],
      "colour_planes": struct.unpack('H', image_file.read(2))[0],
      "bits_per_pixel": struct.unpack('H', image_file.read(2))[0],
      "compression_method": struct.unpack('I', image_file.read(4))[0],
      "raw_image_size": struct.unpack('I', image_file.read(4))[0],
      "horizontal_resolution": struct.unpack('I', image_file.read(4))[0],
      "vertical_resolution": struct.unpack('I', image_file.read(4))[0],
      "number_colours": struct.unpack('I', image_file.read(4))[0],
      "important_colours": struct.unpack('I', image_file.read(4))[0]
    }

  def read_rows(self, path):
    with open(path, mode='rb') as my_image:
      # Obtener datos la cabecera
      self.read_file_header(my_image)
      row = []
      pixel_index = 0
      my_image.seek(54)
      byte = my_image.read(1)

      while byte != b'':
        if pixel_index == self.header_image_file["width"]:
          pixel_index = 0
          self.rows.insert(0, row)
          row = []

        r = ord(byte)
        g = ord(my_image.read(1))
        b = ord(my_image.read(1))

        #Ordenar en tuplas
        row.append((b,g,r))

        byte = my_image.read(1)
        pixel_index += 1


  def repack_sub_pixels(self):
    for r in self.rows:
      for px in r:
        self.list_pixels.append(px)

if __name__ == '__main__':
  n_image = RImage()
  n_image.read_rows("gota.bmp")
  n_image.repack_sub_pixels()

  print(n_image.header_image_file["size"])

  w = n_image.header_image_file["width"]
  h = n_image.header_image_file["height"]
  image_recompose = Image.new('RGB', (w, h), "white")
  image_recompose.putdata(n_image.list_pixels)
  image_recompose.show()
