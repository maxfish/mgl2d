from distutils import dirname

from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.shader_program import ShaderProgram
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2


class CharDef:
    def __init__(self):
        self.id = 0
        self.x = self.y = 0
        self.width = self.height = 0
        self.offset_x = self.offset_y = 0
        self.advance_x = 0
        self.page_index = 0
        # not supported (1 = blue, 2 = green, 4 = red, 8 = alpha, 15 = all channels)
        self.texture_channel = 0
        self.letter = ''


# File format: http://www.angelcode.com/products/bmfont/doc/file_format.html
class BMFontDef:
    def __init__(self, filename):
        self._page_files = []
        self._char_defs = {}
        self._parse_file(filename)

    @property
    def size(self):
        return self._size

    @property
    def page_width(self):
        return self._page_w

    @property
    def page_height(self):
        return self._page_h

    @property
    def bold(self):
        return self._bold

    @property
    def italic(self):
        return self._italic

    @property
    def page_files(self, ):
        return self._page_files

    def get_char(self, letter):
        return self._char_defs[letter]

    def extents_for_char(self, char):
        oc = ord(char)
        if oc not in self._char_defs:
            return 0, 0
        c = self._char_defs[oc]
        width = c.advance_x
        height = c.height + c.offset_y
        return width, height

    def _parse_file(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                tokens = self._tokenize_line(line)
                section, data = tokens
                if not section:
                    continue

                if section == 'info':
                    self._parse_info(data)
                elif section == 'common':
                    self._parse_common(data)
                elif section == 'page':
                    self._parse_page(data)
                elif section == 'chars':
                    pass
                elif section == 'char':
                    self._parse_char(data)

    def _parse_info(self, data):
        self._face = data['face'].replace('"', '')
        self._size = int(data['size'])
        self._bold = True if int(data['bold']) == 1 else False
        self._italic = True if int(data['italic']) == 1 else False
        self._unicode = True if int(data['unicode']) == 1 else False
        self._stretch_h = int(data['stretchH'])
        self._smooth = int(data['smooth'])
        self._super_sampling = int(data['aa'])
        # self._char_paddind = data['padding']
        # self._char_spacing = data['spacing']

    def _parse_common(self, data):
        self._line_height = int(data['lineHeight'])
        self._base = int(data['base'])
        self._page_w = int(data['scaleW'])
        self._page_h = int(data['scaleH'])
        self._packed = int(data['packed'])
        self._page_files = [''] * int(data['pages'])

    def _parse_page(self, data):
        # page id=0 file="ProstoOne.png"
        self._page_files[int(data['id'])] = data['file'].replace('"', '')

    def _parse_char(self, data):
        char = CharDef()
        char.id = int(data['id'])
        char.x = int(data['x'])
        char.y = int(data['y'])
        char.width = int(data['width'])
        char.height = int(data['height'])
        char.offset_x = int(data['xoffset'])
        char.offset_y = int(data['yoffset'])
        char.advance_x = int(data['xadvance'])
        char.page_index = int(data['page'])
        char.texture_channel = int(data['chnl'])
        char.letter = data['letter'].replace('"', '')
        if char.letter == 'space':
            char.letter = ' '
        self._char_defs[char.letter] = char

    def _tokenize_line(self, line):
        line = line.splitlines()[0]
        if not line:
            return None, None

        data = {}
        tokens = []
        for part in line.split('='):
            tokens.extend(part.rsplit(' ', 1))
        cmd, tokens = tokens[0], tokens[1:]

        for k, v in zip(tokens[::2], tokens[1::2]):
            data[k] = v

        return cmd, data


# Supports multiple font files with unique sizes
class Font:
    def __init__(self):
        self._font_faces = {}
        self._page_textures = {}
        self._character_program = ShaderProgram.from_sources(vert_source=self.vert_shader_base,
                                                             frag_source=self.frag_shader_texture)
        self._quad = QuadDrawable()
        self._quad.shader = self._character_program

    def load_bmfont_file(self, filename):
        base_dir = dirname(filename)
        font_def = BMFontDef(filename)
        self._font_faces[font_def.size] = font_def
        self._page_textures[font_def.size] = []
        for file in font_def.page_files:
            path = base_dir + '/' + file
            self._page_textures[font_def.size].append(Texture().load_from_file(path))

    def draw_string(self, screen, font_size, string, x, y, scale=1):
        font = self._font_faces[font_size]
        for char in string:
            c = font.get_char(char)
            self._quad.texture = self._page_textures[font_size][c.page_index]
            self._quad.size = Vector2(c.width, c.height) * scale
            self._quad.pos = Vector2(x, y + c.offset_y * scale)
            self._character_program.bind()
            self._character_program.set_uniform_2f('area_pos', c.x / font.page_width, c.y / font.page_height)
            self._character_program.set_uniform_2f('area_size', c.width / font.page_width, c.height / font.page_height)
            self._quad.draw(screen)
            x += c.advance_x * scale

    def draw_char(self, screen, font_size, char, x, y, scale=1):
        font = self._font_faces[font_size]
        c = font.get_char(char)
        s = self._character_program

        self._quad.texture = self._page_textures[font_size][c.page_index]
        self._quad.size = Vector2(c.width, c.height) * scale
        self._quad.pos = Vector2(x, y + c.offset_y * scale)
        self._quad.shader = s
        s.bind()
        s.set_uniform_matrix4('projection', screen.projection_matrix.m)
        s.set_uniform_2f('area_pos', c.x / font.page_width, c.y / font.page_height)
        s.set_uniform_2f('area_size', c.width / font.page_width, c.height / font.page_height)
        self._quad.draw(screen)

        return c.advance_x

    vert_shader_base = """
        #version 330 core

        uniform mat4 model;
        uniform mat4 projection;
        uniform vec2 area_pos;
        uniform vec2 area_size;

        layout(location=0) in vec2 vertex;
        layout(location=1) in vec2 uv;

        out vec2 uv_out;

        void main() {
            vec2 texture_out = uv;
            if (gl_VertexID == 0) {
                texture_out = area_pos;
            } else if (gl_VertexID == 1) {
                texture_out = vec2(area_pos.x, area_pos.y+area_size.y);
            } else if (gl_VertexID == 2) {
                texture_out = vec2(area_pos.x+area_size.x, area_pos.y+area_size.y);
            } else if (gl_VertexID == 3) {
                texture_out = vec2(area_pos.x+area_size.x, area_pos.y);
            }
            
            vec4 vertex_world = model * vec4(vertex, 1, 1);
            gl_Position = projection * vertex_world;
            uv_out = texture_out;
        }
        """

    frag_shader_texture = """
        #version 330 core

        in vec2 uv_out;
        out vec4 color;

        uniform sampler2D tex;

        void main() {
            color = texture(tex, uv_out);
        }
        """
