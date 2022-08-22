from PIL import Image
from numpy import ones as np_ones, uint8 as np_uint8, array as np_array
from numpy.random import choice as np_choice
from random import randint as random_randint
from pick import pick
from os import system as os_system, name as os_name


def square_matrix(size):
    width, height = size
    return np_ones([width, height, 3], dtype=np_uint8)


def color_gen():
    return tuple(np_choice(range(256), size=3))


def color_tiles(size, colors):
    tiles = square_matrix(size)
    width, height = size
    tiles[:, :, 0] = colors[0][0]
    tiles[:, :, 1] = colors[0][1]
    tiles[:, :, 2] = colors[0][2]

    for col in range(width):
        for row in range(height):
            index = random_randint(0, len(colors) - 1)
            tiles[col, row, 0] = colors[index][0]  # R
            tiles[col, row, 1] = colors[index][1]  # G
            tiles[col, row, 2] = colors[index][2]  # B

    return tiles


def img_show(tiles):
    img = Image.fromarray(tiles)
    img = img.resize(tuple(10 * x for x in img.size), resample=Image.NEAREST, box=None)
    img.show()


class pixelPatterns:

    def __init__(self):
        self.number_of_colors = 3
        self.colors = [color_gen() for n in range(self.number_of_colors)]
        self.size = (50, 50)
        self.tiles = square_matrix(self.size)
        self.number_of_gif = 3
        self.keep_color = False
        self.duration = 100
        self.main_menu()

    def number_colors(self):
        self.number_of_colors = input('Input the number of colors:')
        try:
            if self.number_of_colors.isdigit() > 0:
                self.number_of_colors = int(self.number_of_colors)
                print(f'Numer of colors set to {self.number_of_colors}')
        except TypeError:
            print('None numerical value entered.\nSetting delay default values.')
        finally:
            if isinstance(self.number_of_colors, int):
                pass
            else:
                self.number_of_colors = 3
                print(f'default value loaded: {self.number_of_colors}')

        self.main_menu()

    def set_colors(self):
        self.colors = []
        color_rgb = None
        print('Format examples: \nHex: #B4FBB8 \nRGB: 180, 251, 184')
        for index in range(self.number_of_colors):
            color_code = input('Enter color code:')
            if not len(color_code):
                color_rgb = color_gen()
            else:
                try:
                    if '#' in color_code:
                        color_hex = color_code.lstrip('#')
                        color_rgb = tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))
                    else:
                        color_rgb = eval(color_code)
                except NameError:
                    print('Using a random color instead.')
                finally:
                    if isinstance(color_rgb, tuple):
                        pass
                    else:
                        print('Using a random color instead.')
                        color_rgb = color_gen()

            self.colors.append(color_rgb)

        self.main_menu()

    def set_size(self):
        print('Format example: \n\t        50, 50 \n\t     Width, Height')
        self.size = input('Enter size:')
        try:
            self.size = eval(self.size)
        except TypeError:
            print('Using a random color instead.')
        finally:
            if isinstance(self.size, tuple):
                pass
            else:
                self.size = (50, 50)

        self.main_menu()

    def refresh(self):
        self.tiles = color_tiles(self.size, self.colors)
        img_show(self.tiles)

        self.main_menu()

    def generate(self):
        self.colors = [color_gen() for n in range(self.number_of_colors)]
        self.tiles = color_tiles(self.size, self.colors)

        img_show(self.tiles)

        self.main_menu()

    def number_for_gif(self):
        self.number_of_gif = input('Set Number of Images:')
        try:
            if self.number_of_gif.isdigit() > 0:
                self.number_of_gif = int(self.number_of_gif)
                print(f'Images set to {self.number_of_gif}')
        except TypeError:
            print('None numerical value entered.\nSetting delay default values.')
        finally:
            if isinstance(self.number_of_gif, int):
                pass
            else:
                self.number_of_gif = 3
                print(f'default value loaded: {self.number_of_gif}')

        self.gif_menu()

    def keep_colors(self):
        self.keep_color = True
        self.gif_menu()

    def random_colors(self):
        self.keep_color = False
        self.gif_menu()

    def gif_duration(self):
        self.duration = input('Set Gif Duration:')
        try:
            if self.duration.isdigit() > 0:
                self.duration = int(self.duration)
                print(f'Duration set to {self.duration}ms')
        except TypeError:
            print('None numerical value entered.\nSetting delay default values.')
        finally:
            if isinstance(self.duration, int):
                pass
            else:
                self.duration = 100
                print(f'default value loaded: {self.duration}ms')

        self.gif_menu()

    def make_gif(self):
        gif_name = 'pixelsPatterns.gif'

        if self.keep_color:
            image = [color_tiles(self.size, self.colors) for n in range(self.number_of_gif)]
        else:
            image = [color_tiles(self.size, [color_gen() for n in range(self.number_of_colors)]) for n in
                     range(self.number_of_gif)]

        image = [Image.fromarray(img) for img in image]
        image = [image[n].resize(tuple(10 * x for x in self.size), resample=Image.NEAREST, box=None) for n in
                 range(len(image))]
        image[0].save(gif_name,
                      save_all=True, append_images=image[1:],
                      optimize=False, duration=self.duration, loop=0)

        os_system(gif_name)

        self.gif_menu()

    def gif_menu(self):
        # Clear terminal
        os_system('cls' if os_name == 'nt' else 'clear')

        title = f'----- Create a Gif ----- \n\nNumber of Images Set to: {self.number_of_gif} \nKeep Colors Set to: {self.keep_color} \nDuration Set to: {self.duration}ms \n\n------------------------ '
        options = ['Set Number of Images', 'Keep Colors', 'Random Colors', 'Duration', 'Make Gif', 'Go Back']
        option, index = pick(options, title)

        if index == 0:
            self.number_for_gif()
        if index == 1:
            self.keep_colors()
        if index == 2:
            self.random_colors()
        if index == 3:
            self.gif_duration()
        if index == 4:
            self.make_gif()
        if index == 5:
            self.main_menu()

    def main_menu(self):
        # Clear terminal
        os_system('cls' if os_name == 'nt' else 'clear')

        colors = np_array(self.colors)

        title = f'Pixel Pattern Generator\n\n--- Current Settings ---\n\nColors: \n{colors}\nWidth: {self.size[0]} Height: {self.size[1]} \n\n------------------------ '
        options = ['Generate', 'Refresh', 'Set Number of Colors', 'Set Colors', 'Set Size', 'Create Gif']
        option, index = pick(options, title)

        if index == 0:
            self.generate()
        if index == 1:
            self.refresh()
        if index == 2:
            self.number_colors()
        if index == 3:
            self.set_colors()
        if index == 4:
            self.set_size()
        if index == 5:
            self.gif_menu()


def main():
    # Set terminal size to optimal size
    os_system('mode con cols=35 lines=20')

    pixelPatterns()


if __name__ == '__main__':
    main()
