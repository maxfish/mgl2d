from OpenGL.GL import *

from mgl2d.graphics.shader_program import ShaderProgram


class Shapes:
    def __init__(self):
        self._dummy_vao = glGenVertexArrays(1)
        self._circle_program = ShaderProgram.from_sources(vert_source=self.vert_shader_base,
                                                          geom_source=self.geom_circle_shader,
                                                          frag_source=self.frag_shader_solid)
        self._polyline_program = ShaderProgram.from_sources(vert_source=self.vert_shader_base,
                                                            geom_source=self.geom_polyline_shader,
                                                            frag_source=self.frag_shader_solid)

    def draw_line(self, screen, x1, y1, x2, y2, color):
        self.draw_polyline(screen, [(x1, y1), (x2, y2)], color)

    def draw_polyline(self, screen, vertices, color):
        # Vertices is a list of tuples
        self._polyline_program.bind()
        self._polyline_program.set_uniform_matrix4('projection', screen.projection_matrix.m)
        self._polyline_program.set_uniform_2fv('vertices', vertices)
        self._polyline_program.set_uniform_1i('num_points', len(vertices))
        self._polyline_program.set_uniform_4f('color', color.r, color.g, color.b, color.a)
        # Passing the dummy VAO
        glBindVertexArray(self._dummy_vao)
        glDrawArrays(GL_POINTS, 0, 1)
        glBindVertexArray(0)

    def draw_circle(self, screen, center_x, center_y, radius, color, num_segments=10, start_angle=0):
        self._circle_program.bind()
        self._circle_program.set_uniform_matrix4('projection', screen.projection_matrix.m)
        self._circle_program.set_uniform_2f('center', center_x, center_y)
        self._circle_program.set_uniform_1f('radius', radius)
        self._circle_program.set_uniform_1i('num_segments', num_segments)
        self._circle_program.set_uniform_1i('start_angle', start_angle)
        self._circle_program.set_uniform_4f('color', color.r, color.g, color.b, color.a)
        # Passing the dummy VAO
        glBindVertexArray(self._dummy_vao)
        glDrawArrays(GL_POINTS, 0, 1)
        glBindVertexArray(0)

    geom_circle_shader = """
        #version 330 core

        layout(points) in;
        layout(line_strip, max_vertices = 100) out;

        uniform mat4 projection;
        uniform vec2 center;
        uniform float radius;
        uniform int num_segments;
        uniform int start_angle;

        const float PI = 3.14159265359;
                
        void main() {
            vec4 pos = vec4(center, 0, 1);
            float delta_angle = 2*PI/num_segments;
            float angle = start_angle;
            for(int i = 0; i <= num_segments; i++) {
                gl_Position = projection * (pos + vec4(radius*cos(angle), radius*sin(angle), 0, 0));
                EmitVertex();
                angle += delta_angle; 
            }
            EndPrimitive();
        }
        """

    geom_polyline_shader = """
        #version 330 core

        layout(points) in;
        layout(line_strip, max_vertices = 100) out;

        uniform mat4 projection;
        uniform vec2 vertices[100];
        uniform int num_points;

        void main() {
            for(int i = 0; i < num_points; i++) {
                gl_Position = projection * vec4(vertices[i], 0, 1);
                EmitVertex();
            }
            EndPrimitive();
        }
        """

    vert_shader_base = """
        #version 330 core

        uniform mat4 projection;

        layout(location=0) in vec2 vertex;
        layout(location=1) in vec2 uv;

        out vec2 uv_out;

        void main() {
            vec4 vertex_world = vec4(vertex, 0, 1);
            gl_Position = projection * vertex_world;
            uv_out = uv;
        }
        """

    frag_shader_solid = """
        #version 330 core

        uniform vec4 color;
        out vec4 fragment;

        void main() {
            fragment = color;
        }
        """
