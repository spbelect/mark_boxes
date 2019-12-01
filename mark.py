import os
#os.environ["KIVY_VIDEO"] = "ffmpeg"

from kivy.config import Config

Config.set('kivy', 'log_level', 'debug')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('postproc', 'double_tap_time', '400')
Config.set('postproc', 'double_tap_distance', '20')


from getinstance import InstanceManager
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stencilview import StencilView

from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.video import Video
from kivy.core.window import Window


from hoverable import HoverBehavior


Builder.load_string('''

<BoxMenu>:
    orientation: 'vertical'
    scale: min(self.parent.scatter.scale, 3) if self.parent else 1
    width: 200/ self.scale
    height: 50/ self.scale
    Button:
        text: 'Удалить'
        on_press: root.del_box()
        #font_size: 40/ self.parent.scale
        
<Box>:
    pos: (0, 0)
    size: (0, 0)
    border_width: 1
    border_opacity: 0.7
    border_color: (1,.2,.2, self.border_opacity)
    
    on_enter: self.border_opacity = 1; self.border_width = 2
    on_leave: self.border_opacity = 0.7; self.border_width = 1
    
    canvas.before:
        Color:
            rgba: (0,0,0,1)
        Line:
            width: self.border_width / self.scatter.scale
            rectangle: self.x + 1 / self.scatter.scale, self.y - 1 / self.scatter.scale, self.width, self.height
        Color:
            rgba: self.border_color
        Line:
            width: self.border_width / self.scatter.scale
            rectangle: self.x, self.y, self.width, self.height
            
    
<Main@BoxLayout>:
    orientation: 'vertical'
    
    padding: 0
    spacing: 0
    Label:
        #z_index: 112
        height: dp(50)
        size_hint_y: None
        text: 'Двойной клик - добавить'
    
    #Video:
        #source: '/home/z/uik-2212-c1.ts'
        #state: 'play'
        
    StencilLayout:
        id: stencil
        MyScatter:
            id: scatter
            #bbox: self.size
            do_rotation: False
            do_translation: True
            #do_scale: False
            auto_bring_to_front: False
            scale: 1
            #z_index: 111
            #size: 200,200
            #size_hint: None, None
            
            #canvas.after:
                #Color:
                    #rgba: (0,0,1,0.3)
                #Rectangle:
                    #pos: self.pos
                    #size: self.size
            

#<MyImage>:
    #source: '05.jpg'
    ###size: (640, 480)
    #size_hint: None, None
    #size_hint: 1, 1
    #pos_hint: {'x':0, 'y':0}
    ###on_touch_up: self.end()
    ###on_touch_down: args[1].grab(self); 
        

''')



class BoxMenu(BoxLayout):
    instances = InstanceManager()
    
    def del_box(self):
        #print('del')
        #if self.parent:
        self.parent.parent.remove_widget(self.parent)
        #del self.parent.parent
        del self
        #import gc
        #gc.collect()
        #print('del')
        
    def close(self):
        #print('cl')
        if self.parent:
            self.parent.remove_widget(self)
        del self
        #import gc
        #gc.collect()

    

class Box(Label, HoverBehavior):
    border_width = NumericProperty(1)
    border_color = ListProperty()
    scatter = ObjectProperty()
    
    def on_touch_down(self, touch):
        #x, y = touch.x, touch.y
        #self.prev_x = touch.x
        #self.prev_y = touch.y
        #print(3)
        #if touch.is_mouse_scrolling:
        #print(f"{self} {touch.button}")
        if touch.button == 'right' and self.collide_point(*touch.pos):
            print(f"{self} right mouse clicked")
            super().on_touch_down(touch)
            self.add_widget(BoxMenu(pos=touch.pos))
            return False
            
        return super().on_touch_down(touch)
    

class StencilLayout(StencilView, BoxLayout):
    
    instances = InstanceManager()

class MyScatter(ScatterLayout):
    
    #def apply_transform(self, trans, post_multiply=False, anchor=(0, 0)):
        #print(self.transform)
        #print(self.scale)
        #print(self.bbox)
        #print(self.children[0].pos)
        #if self.children[0].children:
            #print(self.children[0].height)
            #print(self.children[0].children[0].height)
        #print(self.height)
        #print('ss', StencilLayout.instances.get().height)
        #return super().apply_transform(trans, post_multiply, anchor)
    
    
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                ## zoom in
                if self.scale < 10:
                    self.scale = self.scale * 1.1

            elif touch.button == 'scrollup':
                if self.scale > 1:
                    self.scale = self.scale * 0.8
        return super().on_touch_down(touch)

class MyImage(Image):
    def on_touch_down(self, e): 
        #print(f"{self} mouse clicked")
        if e.button == 'right':
            BoxMenu.instances.all().close()
            
        res = super().on_touch_down(e)
        if e.button == 'right':
            return False
        
        if e.is_double_tap and self.collide_point(*e.pos):
            Window.set_system_cursor('crosshair')
            e.grab(self)
            self.add_widget(Box(scatter=self.parent.parent))
            return True
        if e.button == 'left':
            BoxMenu.instances.all().close()
        return res
    
    def on_touch_move(self, e): 
        if e.grab_current is self and self.children:
            box = self.children[0]
            box.pos = min(e.ox, e.x), min(e.oy, e.y)
            box.size = abs(e.ox - e.x), abs(e.oy - e.y)
                
    def on_touch_up(self, e):
        res = super().on_touch_up(e)
        if e.grab_current is not self:
            return res
        #print(self.children[-1].size)
        boxes = []
        Window.set_system_cursor('arrow')
        for box in self.children:
            if box.size != (0,0):
                x, y = box.x - self.x, box.y - self.y
                boxes.append([[xx/640.0, 1 - yy/480.0] for xx, yy in [
                    [x, y],
                    [x + box.width, y],
                    [x + box.width, y + box.height],
                    [x, y + box.height]
                ]])
        print(boxes)
        return res

        #ffmpeg -ss 00:03 -i part.000000.ts -vframes 1 -q:v 2 output.jpg
class Main(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        Window.maximize()
        mainwidget = Main()
        #mainwidget.ids.im.source='05.jpg'
        self.ii = MyImage(source='04.jpg')
        #self.ii.size=(640,480)
        mainwidget.ids.scatter.add_widget(self.ii)
        #mainwidget.ids.scatter.scale = 1
        #mainwidget.ids.scatter.scale = float(mainwidget.ids.stencil.height) / self.ii.height
        #print('aa', mainwidget.ids.stencil.height, self.ii.height)
        #print(mainwidget.ids.scatter.scale )
        return mainwidget

if __name__ == '__main__':
    MyApp().run()

