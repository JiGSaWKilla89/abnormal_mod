init -100 python:
    @renpy.pure
    class SimpleValue(renpy.object.Object):
        def get(self):
            raise Exception("Not implemented.")

        def set(self, value):
            raise Exception("Not implemented.")

    @renpy.pure
    class FieldSimpleValue(SimpleValue):
        def __init__(self, obj, name):
            self._obj = obj
            self._name = name

        def get(self):
            return getattr(self._obj, self._name)

        def set(self, value):
            setattr(self._obj, self._name, value)
            renpy.restart_interaction()

    @renpy.pure
    def VariableSimpleValue(name):
        return FieldSimpleValue(store, name)

    @renpy.pure
    class ScreenSimpleValue(SimpleValue):
        def __init__(self, name):
            self._name = name
            self._screen = renpy.current_screen()

        def get(self):
            return self._screen.scope[self._name]

        def set(self, value):
            self._screen.scope[self._name] = value
            renpy.restart_interaction()

    @renpy.pure
    class SimpleBarValue(BarValue):
        def __init__(self, simple_value, range, max_is_zero=False, style='bar', offset=0, step=None, action=None, force_step=False):
            self._simple_value = simple_value

            self.range = range
            self.max_is_zero = max_is_zero
            self.style = style
            self.offset = offset
            self.force_step = force_step

            if step is None:
                if isinstance(range, float):
                    step = range / 10.0
                else:
                    step = max(range / 10, 1)

            self.step = step
            self.action = action

        def changed(self, value):
            if self.max_is_zero:
                if value == self.range:
                    value = 0
                else:
                    value = value + 1

            value += self.offset

            self._simple_value.set(value)
            renpy.restart_interaction()

            renpy.run(self.action)

        def get_adjustment(self):
            value = self._simple_value.get()

            value -= self.offset

            if self.max_is_zero:
                if value == 0:
                    value = self.range
                else:
                    value = value - 1

            return ui.adjustment(
                range=self.range,
                value=value,
                changed=self.changed,
                step=self.step,
                force_step=self.force_step,
            )

        def get_style(self):
            return self.style, "v" + self.style


init -100 python in shaders:
    class vec2(tuple):
        def __new__(cls, *args):
            if len(args) == 1:
                return tuple.__new__(cls, (args[0], args[0]))
            elif len(args) == 2:
                return tuple.__new__(cls, args)
            raise ValueError('vec2 accept 1 or 2 arguments, not %s' % len(args))

        @property
        def x(self):
            return self[0]

        @property
        def y(self):
            return self[1]

        def __add__(self, o):
            return vec2(self[0] + o[0], self[1] + o[1])

        def __sub__(self, o):
            return vec2(self[0] - o[0], self[1] - o[1])

        def __mul__(self, m):
            return vec2(self[0] * m, self[1] * m)

    class vec3(tuple):
        def __new__(cls, *args):
            if len(args) == 1:
                return tuple.__new__(cls, (args[0], args[0], args[0]))
            elif len(args) == 3:
                return tuple.__new__(cls, args)
            raise ValueError('vec3 accept 1 or 3 arguments, not %s' % len(args))

        @property
        def x(self):
            return self[0]

        @property
        def y(self):
            return self[1]

        @property
        def z(self):
            return self[2]

        def __add__(self, o):
            return vec3(self[0] + o[0], self[1] + o[1], self[2] + o[2])

        def __sub__(self, o):
            return vec3(self[0] - o[0], self[1] - o[1], self[2] - o[2])

        def __mul__(self, m):
            return vec3(self[0] * m, self[1] * m, self[2] * m)
        
    def mix(x, y, a):
        return x * (1 - a) + y * a

# адаптация https://www.shadertoy.com/view/ls2yRz под renpy
init -10 python:
    from renpy.gl2.gl2mesh2 import Mesh2
    from renpy.display.layout import Container
    import pygame

    # sat_value picker
    renpy.register_shader("collection.color_picker.sat_value_rect", 
        variables="""
            varying vec2 v_tex_coord;
            varying vec2 v_position;

            attribute vec2 a_tex_coord;

            uniform vec3 u_color;
        """, 
        fragment_functions="""
            vec2 get_sat_val_from_position(in vec2 pos) {
                
                vec2 result = vec2(0.0);
                
                vec2 tl = vec2(0.0, 0.0);
                vec2 bl = vec2(0.0, 0.0);
                vec2 br = vec2(0.0, 1.0);
                vec2 tr = vec2(1.0, 0.0);

                vec2 interp_b = mix(bl, br, pos.x);
                vec2 interp_t = mix(tl, tr, pos.x);

                result = mix(interp_b, interp_t, pos.y);
                
                return result;
            }

            vec3 apply_sat_val_to_color(in vec2 sat_val, in vec3 color) {
                vec3 val = mix(vec3(0.0), vec3(1.0), sat_val.y);
                return mix(val, color, sat_val.x);
            }
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
            v_position = a_position.xy;
        """, 
        fragment_300="""
            vec2 uv = v_tex_coord;

            vec2 sat_value = get_sat_val_from_position(uv);
            gl_FragColor = vec4(apply_sat_val_to_color(sat_value, u_color), 1.0);
        """
    )

    renpy.register_shader("collection.color_picker.hue_rect",
        variables="""
            varying vec2 v_tex_coord;
            varying vec2 v_position;

            attribute vec2 a_tex_coord;
        """,
        fragment_functions="""
            const int num_color_stops = 6;
            vec3 get_color_stop(int i) {
                vec3 result = vec3(0);
                
                if (i == 0) 	 result = vec3(1.0, 0.0, 0.0);
                else if (i == 1) result = vec3(1.0, 0.0, 1.0);
                else if (i == 2) result = vec3(0.0, 0.0, 1.0);
                else if (i == 3) result = vec3(0.0, 1.0, 1.0);
                else if (i == 4) result = vec3(0.0, 1.0, 0.0);
                else if (i == 5) result = vec3(1.0, 1.0, 0.0);
                
                return result;

            }
            vec3 get_hue_from_position(in float pos) {
                const float frac = 1.0 / float(num_color_stops);
                int i = int(pos * float(num_color_stops));
                int ni = i + 1;
                
                float next_pos = float(ni) * frac;
                float diff = (next_pos - pos);
                float percent = 1.0 - diff / frac;

                //ni %= num_color_stops;
                if(ni == num_color_stops){
                    ni = 0;
                }

                vec3 current = get_color_stop(i);
                vec3 next = get_color_stop(ni);

                return mix(current, next, percent);
            }
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
            v_position = a_position.xy;
        """, 
        fragment_300="""
            vec2 uv = v_tex_coord;

            gl_FragColor = vec4(get_hue_from_position(1.0 - uv.y), 1.0);
        """
    )


    __COLOR_STOPS = [
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 1.0),
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 1.0),
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 0.0)
    ]

    def get_hue_from_position(pos):
        from store.shaders import vec3, mix

        num_color_stops = len(__COLOR_STOPS)

        frac = 1.0 / num_color_stops
        i = int(pos * num_color_stops)
        if i == num_color_stops:
            i = num_color_stops - 1
        ni = i + 1
        
        next_pos = float(ni) * frac
        diff = next_pos - pos
        percent = 1.0 - diff / frac

        ni %= num_color_stops

        current = vec3(*__COLOR_STOPS[i])
        next = vec3(*__COLOR_STOPS[ni])
    
        return mix(current, next, percent)


    class SaturationValueRect(renpy.Displayable):
        def __init__(self, hue, **kwargs):
            renpy.Displayable.__init__(self, **kwargs)
            self._hue = hue

            self._size = (0, 0)

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            self._size = (width, height)
            
            rv.mesh = Mesh2.texture_rectangle(
                0, 0, width, height,
                0.0, 0.0, 1.0, 1.0,
            )
            rv.add_shader('collection.color_picker.sat_value_rect')
            rv.add_uniform('u_color', get_hue_from_position(1.0 - self._hue.get()))

            return rv

        def event(self, ev, x, y, st):
            w, h = self._size
            if x >= w or y >= h:
                return None
            if (ev.type != pygame.MOUSEBUTTONDOWN) or ev.button != 1:
                return None
            return self._click_handler(x, y, *self._size)

    class ColorPickerHueRect(renpy.Displayable):
        def __init__(self, **kwargs):
            renpy.Displayable.__init__(self, **kwargs)
            self._size = (0, 0)

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            self._size = (width, height)
            
            rv.mesh = Mesh2.texture_rectangle(
                0, 0, width, height,
                0.0, 0.0, 1.0, 1.0,
            )
            rv.add_shader('collection.color_picker.hue_rect')
            
            return rv


    class SaturationValuePicker(renpy.Displayable):
        def __init__(self, cursor, hue, saturation, value, action=None, **kwargs):
            renpy.Displayable.__init__(self, **kwargs)

            self._cursor = renpy.easy.displayable(cursor)

            self._hue = hue
            self._sat = saturation
            self._value = value
            self._action = None

            self._sat_value_rect = SaturationValueRect(hue)

            self._size = (0, 0)

            self.focusable = True

        def render(self, width, height, st, at):
            sat, value = self._sat.get(), self._value.get()

            cursor = self._cursor
            rect_render = renpy.render(self._sat_value_rect, width, height, st, at)
            width, height = self._size = rect_render.get_size()

            rv = renpy.Render(width, height)
            cursor_render = renpy.render(cursor, width, height, st, at)
            rv.blit(rect_render, (0, 0))
            cursor.place(
                rv, 
                width * value - cursor_render.width / 2, 
                height * sat - cursor_render.height / 2,
                width, 
                height, 
                cursor_render
            )
            if self.focusable:
                rv.add_focus(self, None, 0, 0, width, height)

            return rv

        def _map_activate(self, ev):
            return ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1

        def _map_deactivate(self, ev):
            return ev.type == pygame.MOUSEBUTTONUP and ev.button == 1

        def event(self, ev, x, y, st):
            if not self.focusable:
                return None
            if not self.is_focused():
                return None

            grabbed = (renpy.display.focus.get_grab() is self)
            just_grabbed = False
            ignore_event = False

            old_value = value = self._sat.get(), self._value.get()

            def update_value():
                if old_value != value:
                    if old_value[0] != value[0]:
                        self._sat.set(value[0])
                    if old_value[1] != value[1]:
                        self._value.set(value[1])
                    
                    renpy.run(self._action)

            w, h = self._size

            if not grabbed and self._map_activate(ev):
                renpy.display.focus.set_grab(self)
                ignore_event = True
                grabbed = True
                just_grabbed = True

            if grabbed:
                if ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                    value = min(1.0, max(0.0, y / float(h))), min(1.0, max(0.0, x / float(w)))

            if grabbed and not just_grabbed and self._map_deactivate(ev):
                renpy.display.focus.set_grab(None)

                update_value()

                raise renpy.display.core.IgnoreEvent()

            update_value()
                    
            if ignore_event:
                raise renpy.display.core.IgnoreEvent()

        def visit(self):
            return [self._sat_value_rect, self._cursor]


transform color_picker_sat_value(color):
    shader "collection.color_picker.sat_value_rect"
    u_color color

init python:
    class HSVComponentValue(SimpleValue):
        def __init__(self, simple_value, index):
            self._value = simple_value
            self._index = index

        def get(self):
            color = Color(self._value.get())
            return color.hsv[self._index]

        def set(self, value):
            color = Color(self._value.get())
            hsv = list(color.hsv)
            hsv[self._index] = value
            self._value.set(Color(hsv=tuple(hsv)))

    class __ColorChangedAction:
        def __init__(self, callback, hue, saturation, value):
            self._callback = callback
            self._hue = hue
            self._sat = saturation
            self._value = value

        def __call__(self):
            callback = self._callback
            if callback is not None:
                callback(self._hue.get(), self._sat.get(), self._value.get())


screen color_picker(color, field):
    hbox:
        align (1.0,0.0)
        #spacing 4

        add SaturationValuePicker(
            Transform('mod/images/sat_value_picker.png', xysize=(50,50)),
            HSVComponentValue(color, 0),
            HSVComponentValue(color, 1),
            HSVComponentValue(color, 2),
            xsize=config.screen_height//2,
            ysize=config.screen_height//2
        )

        vbar:
            value SimpleBarValue(HSVComponentValue(color, 0), 1.0)
            ysize config.screen_height//2
            xsize gui.bar_size*2
            style 'vslider'
            base_bar ColorPickerHueRect()
            bar_invert True
            thumb Transform('mod/images/hue_picker.png',
                matrixcolor=ColorizeMatrix(getattr(persistent, field), "#FFFFFF"))


        

        