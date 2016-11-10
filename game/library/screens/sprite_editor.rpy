init -10 python:
    """
    This builds a sprite by combining several separate images into one.
    for instance body parts, clothes to build a character.
    The combination of character and clothes is a state.
    The order of drawing is important to correctly display the character.
    An arm or leg can have several rotations. In a transition several
    rotations can be shown in sequence to get an impression of movement.
    Parts or characters can be drawn on different layers. The camera module
    is used for a 3d effect.
    A state can be saved.
    """
    import os
    import re
    import random
    import traceback
    import time

    def draw_frame(trans, new_frame):
        tr = body.modus['transition'].get(trans)
        l = len(tr.item)
        if l:
            l = new_frame % l
            body.change_state({ tr.bp: tr.item[l][0]}, False)
        return l
    class Woold(object):
        """
        abstract type
        `write once ordered list-dict' autovifification until locked
        """
        def __init__(self, subtype=None, *args, **kw):
            self.__dict__.update(kw)
            self.subtype = subtype or self
            self.d = []
            self.h = {}
            self.fetch = self.grow
        def __getitem__(self, i):
            if isinstance(i, (basestring, tuple)):
                return self.fetch(i)
            return self.d[i][1]
        def get(self, i):
            if isinstance(i, (basestring, tuple)):
                i = self.h[i]
            self.i = i
            return self.d[i][1]
        def __getattr__(self, key): return getattr(self.d[self.i][1], key)
        def __setitem__(self, key, value):
            if 'len' in self or key in self.h:
                raise KeyError('cannot set {} anymore'.format(key))
            self.h[key] = len(self.d)
            self.d.append((key,value))
        def grow(self, s):
            if not s in self.h:
                self.__setitem__(s, type(self.subtype)())
            return self.d[self.h[s]][1]
        def lookup(self, s): return self.__getitem__(self.h[s])
        def lock(self):
            self.len = len(self.d)
            self.fetch = self.lookup
            for n,d in filter(lambda d: isinstance(d[1], Woold), self.d):
                d.lock()
            self.i = 0
        def name(self):
            k, v = self.d[self.i]
            if isinstance(k, tuple) or not isinstance(v, Showable):
                return k
            return k+os.path.sep+str(v.name())
        def rotate(self, v): self.i = (self.i + v) % self.len if self.len else 0
        @property
        def k(self): return self.d[self.i][0]
        @property
        def v(self): return self.d[self.i][1]
        def __repr__(self): return type(self).__name__+"()"
        def __str__(self): return "instance of "+type(self).__name__

    class Part(object):
        def __init__(self, *args, **kw):
            self.__dict__.update(kw)
            self.img = Image(self.name+".png", rle=True)
            renpy.image(self.name, self.img)
            (self.w, self.h) = renpy.image_size(self.img)
        def move(self, p, transp=False):
            for i in range(len(p)):
                self.pos[i] += p[i]
        def get_placement(self):
            """ this seems to provide the correct position for storage """
            pmt = self.img.get_placement()
            return [self.pos[0] + pmt[4], self.pos[1] + pmt[5], self.pos[2]]
        def show(self, x, y): return ((x - self.w / 2, y - self.h), self.name)

    class Showable(Woold):
        def __init__(self, *args, **kw):
            self.hidden = True
            super(Showable, self).__init__(*args, **kw)
        def show(self, x, y):
            self.hidden = False
            return self.v.show(x, y)
        def hide(self, persistent=False):
            #if not persistent:
            #    for line in traceback.format_stack():
            #        print(line.strip())
            self.hidden = persistent
            if not isinstance(self.v, Part):
                self.v.hide(persistent)
        def rotate(self, v, visible_only = True):
            start = self.i
            while 1:
                super(Showable, self).rotate(v)
                if self.i == start or not (isinstance(self.d[self.i][1], Showable) and visible_only and self.d[self.i][1].hidden):
                    break;
            self.d[self.i][1].hidden = False
            self.hidden = False
            self.show(0, 0) #FIXME

    class Layer(Showable):
        """ after last '/' is part name """
        def __getitem__(self, s):
            if isinstance(s, basestring):
                m = re.match('^(.+)/([^/]*)$', s)
                if m:
                    return super(Layer, self).__getitem__(m.group(1))[m.group(2)]
            return super(Layer, self).__getitem__(s)
        def get(self, s):
            if isinstance(s, basestring):
                m = re.match('^(.+)/([^/]*)$', s)
                if m:
                    return super(Layer, self).get(m.group(1)).get(m.group(2))
            return super(Layer, self).get(s)
        def __setitem__(self, key, value):
            if 'len' in self:
                raise KeyError('cannot set {} anymore'.format(key))
            m = re.match('^(.+)/([^/]*)$', key) if isinstance(key, basestring) else None
            if not m:
                if key in self.h:
                    raise KeyError('cannot set {} anymore'.format(key))
                self.h[key] = len(self.d)
                self.d.append((key,value))
                if isinstance(key, tuple):
                    i=len(key)-1  # last part can have alternatives
                    if isinstance(key[i], tuple):
                        for v in key[i]:
                            ckey = key[:i]+(v,)
                            value.l[ckey] = Combi(pos=value._pos, l=value, n=ckey)
            else:
                # print(str(key))
                if m.group(1) in self.h:
                    entry = self.d[self.h[m.group(1)]][1]
                else:
                    self.h[m.group(1)] = len(self.d)
                    entry = type(self.subtype)()
                    self.d.append((m.group(1),entry))
                entry[m.group(2)] = value
        def rotate(self, v, visible_only = True):
            if isinstance(self.v, Combi) and self.v.rotate(v):
                return
            super(Layer, self).rotate(v, visible_only)

    class Combi(object):
        def __init__(self, pos, *args, **kw):
            self.__dict__.update(kw)
            self.m = []
            if isinstance(self.l, Combi):
                self.i = len(self.n) - 1
                self.len = self.l.len
            else:
                self.i = 0
                self.len = len(self.n)
            self.hidden = True
            self._pos = pos
            for p in pos:
                while len(p) < 3:
                    p.append(0)
            super(Combi, self).__init__(*args, **kw)
        def __getitem__(self, key):
            #if isinstance(key, tuple):
            return self.l[key]
        def get(self, s): return self.l.get(s)
        def rotate(self, v):
            if isinstance(self.l, Combi):
                return self.l.rotate(v)
            if self.i == (self.len - 1 if v == 1 else 0):
                return False
            if self.len:
                self.i = (self.i + v) % self.len
                L = len(self.n) # active of tuple of alternatives
                self.get(self.n if self.i < L else self.n[:L-1]+(self.n[L-1][self.i-L],))
            #self.l.hidden = False
            return True
        def get_placement(self): return self.pos
        @property
        def pos(self):
            L = len(self.n)
            if self.i and self.i == L - 1:
                if isinstance(self.l, Combi):
                    return self[self.n[self.i]].get_placement()
                return self._pos[L-2]
            return self[self.n[self.i]].get_placement()
        def hide(self, persistent=False):
            self.hidden = persistent
            for n in self.n:
                for t in n if isinstance(n, tuple) else [n]:
                    self.get(t)
                    self.l.hide(persistent)
            self.get(self.n) # activate combi
        def show(self, x, y):
            ret = ()
            self.hidden = False
            for i in range(len(self.n)):
                n = self.n[i]
                if isinstance(n, tuple):
                    for t in n:
                        self.get(t) # activate part
                        ret += self.l.show(x+self._pos[i-1][0], y+self._pos[i-1][1])
                else:
                    self.get(n) # activate part
            self.get(self.n) # activate combi
            return ret
        def move(self, pos):
            L = len(self.n)
            if self.i and self.i == L - 1:
                if isinstance(self.l, Combi):
                    self[self.n[self.i]].move(pos)
                else:
                    for i in range(len(pos)):
                        self._pos[L-2][i] += pos[i]
                    i = len(self.n)-2
                    if isinstance(self.n[L-1], tuple):
                        for t in self.n[L-1]:
                            self.get(t)
                        self.get(self.n)
                    else:
                        k = self.l.k
                        #self.get(self.n[L-1])
                        self.get(k)
            else:
                self[self.n[self.i]].move(pos)

    class Transition(object):
        def __init__(self, bp = None, *args, **kw):
            self.frame = 0
            self.bp = bp
            self.time_left = 100
            self.__dict__.update(kw)
        def __setitem__(self, key, value):
            super(Transition, self).__setitem__(key, value)
            print(key+": "+str(value))

    class Body(object):
        ''' The body is a tree of layers with parts (images) as endpoints '''
        def __init__(self, subdir, pos, n, *args, **kw):
            self.subdir = subdir
            self.n = n
            self.x = pos[0]
            self.y = pos[1]
            self.cy = 0
            self.part = Showable(subtype=Layer())
            self.modus = Woold()
            self.modus['move'] = {}
            self.modus['transition'] = Woold(subtype=Transition(), frame = 0, time_left = 100, play = {})
            self.modus['state'] = Woold(subtype={})
            self.modus['activity'] = Woold(subtype={})
            self.first = 0 
            self.orient = 0
            self.play_rate = 0.17
            self.last_time = time.time()
            self.orientations = 4 #8
            self.composite = ((0, 0),) # XXX: should be width/height of composite image ? 
        def register_layers(self, part=[]):
            self.layer = []
            layer=()
            for l in part:
                i = self.part.h[l]
                n = self.n+"_"+str(i)
                #register_3d_layer(n)
                layer += (n+"_L",)
                entry = [n, i, [(0,0)]]
                self.layer.append(entry)
            return layer + (self.n+"_L",)
        def register_layers2(self):
            for e in self.layer:
                e.append(self.make_layer_entry(e))
                renpy.image(e[0], DynamicDisplayable(e[3]))
            e = [self.n, 0, [(0,0)], body.draw_body]
            self.layer.append(e)
            renpy.image(self.n, DynamicDisplayable(e[3]))
        def make_layer_entry(self, entry):
            def draw_func(st, at):
                return LiveComposite(*entry[2]),None
            return draw_func
        def initiate(self, layer_pos):
            body.part.lock()
            self.modus.lock()
            for i in range(len(self.layer)):
                l = self.layer[i][0]
                layer_move(l+"_L", layer_pos[i])
                renpy.show(name=l, layer=l+"_L")

            self.change_state(body.modus.get('state').get(0)) # set to first state
        def hide(self):
            for t in self.part.d:
                t[1].hide(True)
        def redraw_part(self, k, p):
            self.part.get(k).hide(True) # previous
            self.part.get(k).get(p) # activate
            #self.part.get(k).hidden = False
            self.part.get(k).hide(False)
            self.first = min(self.first, self.part.i)
        def change_state(self, newstate, entirely=True):
            if self.n in newstate:
                self.x += newstate[self.n][0]
                self.cy += newstate[self.n][1]
                camera_move(self.x*100, self.y*100, 0, 0, 1)
                self.first = 0
            elif entirely:
                for t in self.part.d:
                    if t[0] in newstate:
                        self.redraw_part(t[0], newstate[t[0]])
                    else:
                        t[1].hide(True)
            else:
                for k, p in newstate.items():
                    self.redraw_part(k, p)
            self.redraw_body()
        def change_active_state(self):
            if "state" in self.modus.v.v and self.modus['state'].k != self.modus.v.v["state"]:
                self.change_state(self.modus['state'].get(self.modus.v.v['state']), True)
        def move_body(self, pos):
            self.part.v.move(pos)
            if self.first > self.part.i:
                self.first = self.part.i
            self.redraw_body()
        def orientate(self, v):
            if (self.orient ^ (self.orient + v)) & 2:
                self.y = config.screen_height - self.y
                camera_move(self.x*100, self.y*100, 0, 0, 1)

            self.orient = (self.orient + v) % self.orientations
            self.first = 0
            self.redraw_body()
        def redraw_body(self):
            trans = {'xzoom': 1.0, 'yzoom': 1.0}
            if self.orient & 1:
                trans['xzoom'] = -1.0
            if self.orient & 2:
                trans['yzoom'] = -1.0
            #if play:
            #    renpy.show(name, [renpy.store.Transform(function=renpy.curry(self.transform)(check_points=check_points, loop=loop))], layer=layer)
            #else:
            #    renpy.show(name, [renpy.store.Transform(**kwargs)], layer=layer)
            renpy.show("horm", at_list=[Transform(**trans)])
        def add_part(self, part, stance, pos):
            if len(pos) < 3:
                pos.append((len(self.part.d) - self.part.h[part] - 1) if part in self.part.h else 0)
            self.part[part][stance] = Part(name=self.subdir+part+os.path.sep+stance, pos=pos)

        def add_combi(self, part, combi, pos): #FIXME: bilateral
            """ bodyparts composed of several layers """
            for p in pos:
                if len(p) < 3:
                    p.append((len(self.part.d) - self.part.h[part] - 1) if part in self.part.h else 0)
            self.part[part][combi] = Combi(pos=pos, l=self.part[part], n=combi)
        def info_body(self, mode):
            n = str(self.part.name())
            if mode == "move":
                pos = self.part.v.get_placement()
                return "%s: (%d, %d, %d)" % (n, pos[0], pos[1], pos[2])
            return "%s" % n
        def getstate(self):
           return {k: str(v.name()) for k,v in filter(lambda d: not d[1].hidden, self.part.d)}
        def start_transition(self, t = None, delay = 0):
            tr = self.modus['transition']
            t = t or tr.k
            cotr = tr[t]
            if len(cotr.item) != 0:
                k = cotr.bp if cotr.bp else self.n
                if not k in tr.play: # new move for bp
                    tr.play[k] = {'current': t, 'collection': {t: [0, 0 + get_time(delay)]}}
                elif not t in tr.play[k]['collection']: #add move it wasn't already running
                    tr.play[k]['collection'][t] = [0, 0 + get_time(delay)]
        def stop_transition(self, t = None, k = None):
            tr = self.modus['transition']
            t = t or tr.k
            if not k:
                k = tr[t].bp if tr[t].bp else self.n
            if k in tr.play and t in tr.play[k]['collection']:
                del tr.play[k]['collection'][t]
                if tr.play[k]['current'] == t:
                    if len(tr.play[k]['collection']) == 0:
                        tr.play = {c: tr.play[c] for c in tr.play if c is not k}
                    else:
                        tr.play[k]['current'] = random.choice(tr.play[k]['collection'].keys())
        def play_body(self, moves):
            for k, mov in self.modus['transition'].play.iteritems():
                mc = mov['current']
                m = mov['collection'][mc]
                m[1] -= 10
                if m[1] <= 0:
                    item = self.modus['transition'][mc].item
                    m[0] = (m[0] + 1) % len(item)
                    if m[0] == 0 and len(mov['collection']) > 1:
                        # choose between multiple movements for same bodypart
                        mov['current'] = random.choice(mov['collection'].keys())
                    if k == self.n:
                        self.x += item[m[0]][0][0]
                        camera_move(self.x*10, self.y*10, 0, 0, 0.2)
                        self.cy += item[m[0]][0][1]
                        self.first = 0
                    else:
                        self.redraw_part(k, item[m[0]][0])
        def get_trans_predicted(self, t):
            predicted = []
            tr = self.modus['transition']
            if tr[t].bp:
                k = tr[t].bp
                for r in self.modus['transition'][t].item:
                    if isinstance(self.part[k][r[0]], Part): #FIXME: combi parts
                        print(self.part[k][r[0]].name)
                        predicted.append(self.part[k][r[0]].img)
            return predicted
        def get_predicted(self):
            tr = self.modus['transition']
            predicted = []
            if self.modus.k == "transition":
                predicted = self.get_trans_predicted(tr.k)
            elif self.modus.k == "activity":
                coact = body.modus['activity'].v
                if 'transition' in coact:
                    for k in coact['transition']:
                        predicted.extend(self.get_trans_predicted(k))
            return predicted

        def draw_body(self, st, at):
            now = time.time()
            if now - self.last_time < self.play_rate:
                return LiveComposite(*self.layer[len(self.layer)-1][2]),self.play_rate
            self.last_time = now
            if len(self.modus['transition'].play) != 0:
                self.play_body(self.modus['transition'].play)
            self.first = 0 #FIXME could do less but we seem to lose parts when rotating bp from combi to combi
            i = ct = 0
            self.layer[i][2] = ((0, 0),)
            arr = [p[1] for p in self.part.d[self.first:]]

            #self.composite = self.composite[:((self.first * 2) + 1)]

            #telkens: x - p.w / 2 # why divide by 2??
            while len(arr):
                ct += 1
                if ct == self.layer[i][1]:
                    i += 1
                    self.layer[i][2] = ((0, 0),)
                p = arr.pop(0)
                if isinstance(p, list): # instance of combi that was inserted in previous iter
                    (x, y, p) = (p[0], p[1], p[2])
                else:
                    if p.hidden:
                        continue
                    (x, y, p) = (self.x, self.y + self.cy, p.d[p.i][1])
                    if isinstance(p, Layer):
                        if p.hidden:
                            continue
                    elif isinstance(p, Combi):
                        if p.hidden:
                            continue
                        l = p.l.l if isinstance(p.l, Combi) else p.l
                        for i in range(1, len(p.n)):
                            n = p.n[i]
                            if isinstance(n, tuple):
                                n = n[p.i-len(p.n)]
                            z = l[n].pos[2] + p._pos[i-1][2]
                            #print(str(n)+":"+str(z))
                            arr.insert(z, [x+p._pos[i-1][0], y+p._pos[i-1][1], l[n]])
                        p = l[p.n[0]]
                self.layer[i][2] += p.show(x + p.pos[0],y + p.pos[1])
            self.first = self.part.len
            return LiveComposite(*self.layer[i][2]),self.play_rate

    #def filelinenr():
    #    """Returns the current file + line number."""
    #    c = inspect.currentframe().f_back
    #    return [c.f_code.co_filename, c.f_lineno]
    def f_mod(cmd, file_path):
        #Create temp file
        fh, abs_path = mkstemp()
        file_path = "library/" + file_path
        with open(abs_path,'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    for k in cmd.keys():
                        if k == 's':
                            for s in cmd['s']:
                                line = re.sub(s[0], s[1], line)
                        elif k == 'move_up':
                            for i in range(len(cmd['move_up'])):
                                mu = cmd['move_up'][i]
                                if re.match(mu[0]):
                                    line = re.sub('^(.*)$', mu[1]+r"\n\1", line)
                                    del cmd['move_up'][i]
                    new_file.write(line)
                if 'append' in cmd:
                    for line in cmd['append']:
                        new_file.write(line)
        os.close(fh)
        os.remove(file_path)
        move(abs_path, file_path)
    def scrn_str(s): return re.sub('\[','[[', str(s))
    def get_time(t):
        if isinstance(t, (list, tuple)):
            t = random.randint(t[0]/10, t[1]/10) * 10
        return t
    def display_msg():
        r = body.info_body(body.modus.k)
        if body.modus.k == "state":
            return "state: %s %s" % (body.modus.v.k, r)
        if body.modus.k == "move":
            return "move: %s" % (r)
        if body.modus.k == "transition":
            return "transition %s %d/%d:\n%s (%sms)" % (body.modus.v.k, body.modus['transition'].frame,
                    len(body.modus.v.v.item)-1, r, scrn_str(body.modus.v.v.time_left))
        if body.modus.k == "activity":
            return "activity: %s" % (body.modus.v.k)

    config.layers = ['master', 'background', 'middle']
    image_editor = '/usr/bin/gimp'

init -6:

    define horm = Character("Hormione")
    image horm = DynamicDisplayable(body.draw_body)

    #image imgA = LiveComposite((0,0), (-100,-300), "images/items/sock1l3.png", (-200,-300), "images/items/sock6ls2.png",)
    #image imgB = LiveComposite((0,0), (-100,-350), "images/items/skirt2d.png", (-200,-350), "images/items/sock9lu3h.png",)
    #image imgC = LiveComposite((0,0), (0,0), "imgA", (0,0), "imgB",)
    #python:

init python:
        #config.quit_action = Quit(confirm=False)
        config.keymap["action_editor"] = ['P']
        config.keymap["image_viewer"] = ['U']
        layers = body.register_layers(part=['body', 'leftarm'])
        config.layers.extend(list(('background', 'middle') + layers + ('transient', 'screens', 'overlay')))
        body.register_layers2()
        register_3d_layer('background', 'middle', *layers)
        img = Image("content/gfx/bg/h_profile.png", rle=True)
        renpy.image("bg", img)
        img2 = Image("content/gfx/sprites/npc/aine.png", rle=True)
        renpy.image("snape", img2)

label sprite_editor_init:
    python:
        # reset the camera and layers positions and allow layers position to be saved.
        camera_reset()
        layer_move("background", 3000)
        layer_move("middle", 2800)
        body.initiate(layer_pos=[2000, 2020, 2040])

    scene bg onlayer background
    #show perspect onlayer background
    show snape onlayer middle at left
    #show horm onlayer forward
    #show imgC onlayer front
    with dissolve
    $ camera_move(0, 0, 0)
    jump sprite_editor
    #$ camera_move(2800, 0, 0, 0, 1)
    #$ camera_move(0, 0, 0)


screen sprite_editor_screen():
    default msg = display_msg()

    text msg
    timer 0.02 action SetScreenVariable("msg", display_msg()) repeat True
    #key "mousedown_1" action Return(getMousePosition())
    #key "K_AC_BACK" action Quit()
    # see http://www.pygame.org/docs/ref/key.html
    key "K_KP8" action Return(['KP', 0, 10]) # keypad position/time(left,right)
    key "K_KP6" action Return(['KP', 10, 0])
    key "K_KP2" action Return(['KP', 0, -10])
    key "K_KP4" action Return(['KP', -10, 0])
    key "repeat_K_KP8" action Return(['KP', 0, 10]) # (when keeping pressed)
    key "repeat_K_KP6" action Return(['KP', 10, 0])
    key "repeat_K_KP2" action Return(['KP', 0, -10])
    key "repeat_K_KP4" action Return(['KP', -10, 0])
    key "shift_K_KP8" action Return(['KP', 0, 1]) # +shift finetune position/time(left,right)
    key "shift_K_KP6" action Return(['KP', 1, 0])
    key "shift_K_KP2" action Return(['KP', 0, -1])
    key "shift_K_KP4" action Return(['KP', -1, 0])
    key "K_DOWN" action Return(['<-', 0])
    key "K_LEFT" action Return(['<-', 1, True])
    key "K_UP" action Return(['<-', 2]) #depends on mode
    key "K_RIGHT" action Return(['<-', 3, True])
    key "repeat_K_DOWN" action Return(['<-', 0])
    key "repeat_K_LEFT" action Return(['<-', 1])
    key "repeat_K_UP" action Return(['<-', 2]) #depends on mode
    key "repeat_K_RIGHT" action Return(['<-', 3])
    key "K_HOME" action Return(['HE', -1])
    key "K_END" action Return(['HE', 1])
    key "K_PAGEUP" action Return(['pg', 1])
    key "K_PAGEDOWN" action Return(['pg', -1])
    key "K_KP_PLUS" action Return(['+'])
    key "K_KP_MINUS" action Return(['-', False])
    key "shift_K_KP_MINUS" action Return(['-', True])
    key "K_TAB" action Return(['\t'])
    key "shift_K_LEFT" action Return(['<-', 1, False])
    key "shift_K_RIGHT" action Return(['<-', 3, False])

    key "K_RETURN" action Return(['\n', True]) # store current position/transition
    key "shift_K_RETURN" action Return(['\n', False]) # store current position/transition
    key "K_SPACE" action Return([' ', 1]) # move: make default, state/transition: save entire position/transition
    key "K_g" action Return(['g']) # open image in editor

label sprite_editor:
    #"starting"
    show screen sprite_editor_screen

    label sprite_editor_loop:
        python:
            res = ui.interact()
            if res[0] == 'KP':
                if body.modus.k == "move":
                    body.move_body([res[1], -res[2], 0])
                elif body.modus.k == "transition":
                    if body.modus.v.len == 0:
                        renpy.jump("sprite_editor_loop")
                    t = body.modus['transition']
                    if res[1] != 0:
                        if res[1] & 1:
                            add = res[1]
                        else:
                            t.rotate(res[1]/10)
                            add = 0
                        if body.modus.v.v.bp:
                            if len(t.v.item) != 0:
                                t.frame = draw_frame(t.k, t.frame + add)
                                t.time_left = t.v.item[t.frame][1]
                    elif isinstance(t.time_left, (list, tuple)):
                        if res[2] > 0: #adapt higher
                            if res[2] & 1:
                                t.time_left[1] += 10
                            elif t.time_left[0] + 10 != t.time_left[1]:
                                t.time_left[0] += 10
                            else:
                                t.time_left = t.time_left[1] # no longer list
                        elif res[2] & 1:
                            if t.time_left[0] != 10:
                                t.time_left[0] -= 10
                        elif t.time_left[1] != t.time_left[0] + 10:
                            t.time_left[1] -= 10
                        else:
                            t.time_left = t.time_left[0] # no longer list
                    elif res[2] & 1:
                        if not isinstance(t.time_left, (list, tuple)):
                            if res[2] > 0:
                                t.time_left = [t.time_left, t.time_left + 10]
                            elif t.time_left != 10:
                                t.time_left = [t.time_left - 10, t.time_left]
                    elif t.time_left + res[2] > 0:
                        t.time_left += res[2]
                elif body.modus.k == "state":
                    if res[1] != 0:
                        if (res[1] & 1) == 0:
                            body.modus.v.rotate(res[1]/10)
                            body.change_state(body.modus.v.v, True)
                elif body.modus.k == 'activity':
                    if res[1] != 0:
                        if (res[1] & 1) == 0:
                            body.modus.v.rotate(res[1]/10)
                        body.change_active_state()
            elif res[0] == '<-':
                if res[1] & 1: #left/right
                    body.part.rotate(res[1] - 2, res[2])
                else:
                    #body.v.hide(True)
                    body.part.v.rotate(res[1] - 1)
                    body.first = body.part.i #FIXME
                    body.redraw_body()
                    #renpy.show("horm")
            elif res[0] == 'HE':
                body.orientate(res[1])
            elif res[0] == 'pg':
                remove_predicted = {}
                # previous:
                if body.modus.k == "transition" or body.modus.k == "activity":
                    for k in body.get_predicted():
                        remove_predicted[k] = True
                body.modus.rotate(res[1])
                m = body.modus.k
                if m == "transition":
                    f = draw_frame(body.modus['transition'].k, body.modus['transition'].frame)
                elif m == "activity":
                    body.change_active_state()

                if body.modus.k == "transition" or body.modus.k == "activity":
                    add_predicted = []
                    for k in body.get_predicted():
                        if k in remove_predicted:
                            del remove_predicted[k]
                        else:
                            add_predicted.append(k)
                    if len(add_predicted):
                        renpy.start_predict(*add_predicted)

                if len(remove_predicted):
                    renpy.stop_predict(*remove_predicted.keys())

            elif res[0] == '\n':
                if body.modus.k == "transition":  # store transition bp + duration
                    k, ins = body.modus['transition'].d[body.modus['transition'].i]
                    ins.item.insert(ins.frame, [body.part.v.name(), ins.time_left])
                    ins.frame += 1 # for next
                    ins.time_left = 100 # default duration for new
                    if ins.frame < len(ins.item):
                        ins.time_left = ins.item[ins.frame][1]

                    f_mod({'s': [["^( *body.modus\['transition'\]\['"+k+"'\] = Transition\(bp = '"+ins.bp+"', item = ).*$",
                        r'\1'+str(ins.item)+"})"]]}, 'states.rpy')
                elif body.modus.k == "state": # update state
                    body.modus['state'].v['item'] = body.getstate()
                    f_mod({'s': [["^( *body.modus\['state'\]\['"+body.modus["state"].k+"'\] = ).*$", r'\1'+str(body.modus['state'].v['item'])]]}, 'states.rpy')
                elif body.modus.k == "move":  # store position
                    (k, v) = body.part.d[body.part.i]
                    s = v.name()
                    if isinstance(s, tuple):
                        v = v.v
                        if v.i:
                            (cs, L) = (re.escape(str(s)), len(s))
                            if v.i == L-1: # last element can be a list (several options)
                                if isinstance(v.l, Combi):
                                    act = [r"^( *body\.add_part\('"+k+"', *'"+s[L-1]+"', ).*$", r'\1'+str(v.l[s[L-1]].get_placement())+')']
                                    v.l[s]
                                else:
                                    cs = re.sub(r"(\\'[^']+')\\\), \[", r"(?:\1|\((?:'[^']+', *)*\1(?:, *'[^']+')*)\), \[", cs)
                                    act = [r"^( *body\.add_combi\('"+k+"', *"+cs+r", \[(\[[^]]+\], *)*)\[[^]]+\]\]\)$", r'\1'+str(v.pos)+'])']
                            else:
                                act = [r"^( *body\.add_combi\('"+k+"', *"+cs+r"(, *'[^']+')*(, *\[[^]]+\])?, *\[(\[[^]]+\], *){"+str(v.i)+r"}, *)\[[^]]+\]", r'\1'+str([v.pos])] # array on purpose
                        else:
                            act = [r"^( *body\.add_part\('"+k+"', *'"+s[0]+"', ).*$", r'\1'+str(v.l[s[0]].get_placement())+')']
                        v.l[s]
                    else:
                        act = [r"^( *body\.add_part\('"+k+"', *'"+s+"', ).*$", r'\1'+str(v.get_placement())+')']
                    print(str(act))
                    f_mod({'s': [act]}, 'sprite_bodyparts.rpy');
            elif res[0] == ' ': #FIXME
                m = body.modus.k
                if m == "move": # set as default position (FIXME: does nothing)
                    r = body.part.k
                    k = body.part.v.k
                    #f_mod({ 's':[['^( *bps = ).*$', r'\1'+str(body.parts)]]}, 'body.rpy')
                    # TODO: store default , 'move_up': _subst("^( *body.set_pos('"+r+"'" ...
                    #f_mod('^( *bodypart\["'+r+'"\] = \[)(("[^"]+",)*"[^"]+"),("'+re.sub("(\]|\[)", r"\\\1", str(k))+'")([],])', r'\1\4,\2\5', 'body.rpy')
                    #renpy.say(horm, scrn_str(k)+' will be the default for '+r+' after restart')
                elif len(body.modus['transition'].play) == 0:
                    while 1:
                        name = renpy.input("Give a variable name for "+m+" [[A-z][[A-9_]*), none to cancel:")
                        if re.match("^[A-Za-z][A-Za-z0-9_]*$", name):
                            if not name in body.modus[m].h or renpy.input(body.modus.k+" "+name+" already exists, do you want to overwrite it? (y/n)", allow = 'y,n', length = 1) == 'y':
                                break
                        elif name == "":
                            renpy.jump("sprite_editor_loop")
                    ccomp[m] = [len(body.modus[m].d), 0, 100] # the respective composition will be created shortly.
                    if m == "state":
                        body.modus[m][name] = body.getstate()
                        ins = str(body.getstate())
                    elif m == "transition":
                        body.modus[m][name] = {'bp': body.part.k, 'item': []}
                        ins = "{'bp': '"+r+"', 'item': "+str(body.getstate())+"}"

                    # and store in script
                    f_mod({'append':["    body.modus['"+m+"']['"+name+"'] = "+ins+"\n"]}, 'sprite_states.rpy')
            elif res[0] == 'g':
                # fixme: the path and extension should be at least configurable. Also can use *LIST
                k,v = body.part.d[body.part.i]
                name = v.name()
                if isinstance(name, tuple):
                    name = name[v.v.i]
                if not isinstance(name, tuple):
                    call([image_editor, os.path.join(config.searchpath[0], body.subdir, k, name)+'.png'])
            elif res[0] == '+':
                if body.modus.k == "transition":
                    body.start_transition()
                elif body.modus.k == "move":
                    body.move_body([0, 0, 1])
                elif body.modus.k == 'activity':
                    coact = body.modus['activity'].v
                    if 'transition' in coact:
                        for k in coact['transition']:
                            body.start_transition(k, coact['transition'][k])
            elif res[0] == '-':
                if res[1]:
                    body.part.v.hide(True)
                    body.redraw_body()
                elif body.modus.k == "transition":
                    body.stop_transition(body.modus["transition"].k)
                elif body.modus.k == "move":
                    body.move_body([0, 0, -1])
                elif body.modus.k == 'activity':
                    coact = body.modus['activity'].v
                    if 'transition' in coact:
                        for k in coact['transition']:
                            body.stop_transition(k, body.modus['transition'][k].bp)

        jump sprite_editor_loop

