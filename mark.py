from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image


from hoverable import HoverBehavior


Builder.load_string('''

<RmButton>:
    canvas.before:
        Color:
            rgba: self.fillcolor
        Rectangle:
            size: self.width, self.height
            pos: self.pos
        
    fillcolor: (1, 1, 1, 0.0)
    on_enter: self.fillcolor = (1, 0, 0, 0.5); self.color = (0,0,0,1)
    on_leave: self.fillcolor = (1, 0, 0, 0.0); self.color = (1,1,1,1)
    
<Box>:
    pos: (0, 0)
    size: (0, 0)
    
    canvas.before:
        Color:
            rgba: (1,0,0,1)
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
            
    RmButton:
        pos: (root.center[0] - 5, root.center[1]-5)
        size: (10,10)
        text: 'X'
    
<Main@BoxLayout>:
    orientation: 'vertical'
    
    padding: 0
    spacing: 0
    Label:
        height: dp(100)
        text: 'double clik to remove box'
    MyIm:
        id: im
        Box:
        
    BoxLayout:
        Button:
            text: 'add box'
            on_press: im.addbox()

<MyIm>:
    canvas:
        Color:
            rgba: self.xcolor
        Rectangle:
            #texture: self.texture
            size: self.width, self.height
            #pos: self.x - 10, self.y - 10
            pos: self.pos
    xcolor: (1, 1, 1, 0.0)
    source: '01.jpg'
    size: (640, 480)
    size_hint: None, None
    on_touch_up: self.end()
    on_touch_down: args[1].grab(self); 
    on_touch_move: self.children[0].pos = args[1].opos; self.children[0].setsize(*args[1].pos)
        

''')



class RmButton(Label, HoverBehavior):
    def on_touch_up(self, e): 
        if e.is_double_tap:
            self.parent.setsize(0, 0)
            self.parent.pos = (0, 0)


class Box(Label):
    def setsize(self, x, y):
        self.size = (x - self.x, y - self.y)


class MyIm(Image):
    def addbox(self):
        self.add_widget(Box())
        
    def end(self):
        boxes = []
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


class Main(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    MyApp().run()

