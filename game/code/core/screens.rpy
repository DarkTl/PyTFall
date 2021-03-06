init python:
    def dummy_interaction_restart(*args, **kwargs):
        renpy.restart_interaction()

    def dev_mode_switch():
        config.developer = not(config.developer)
        config.debug = not(config.debug)

################### Specialized ####################
init: # Items:
    image water_texture__ = Movie(channel="main_gfx_bow", play="content/gfx/animations/water_texture_webm/movie.webm")
    screen items_inv(char=None, main_size=(553, 282), frame_size=(90, 90), return_value=['item', 'get']):
        frame:
            background Null()
            xysize main_size
            has hbox box_wrap True
            for item in char.inventory.page_content:
                frame:
                    xysize frame_size
                    if char.inventory[item]:
                        background Frame("content/gfx/frame/frame_it2.png", -1, -1)
                        use r_lightbutton (img=ProportionalScale(item.icon, 70, 70), return_value=return_value+[item], align=(0.5, 0.5))
                        label (u"{color=#ecc88a}%d" % char.inventory[item]):
                            align (0.995, 0.995)
                            style "stats_label_text"
                            text_size 18
                            text_outlines [(2, "#9c8975", 0, 0), (1, "#000000", 0, 0)]
                    else:
                        # in groups indicate some have the item
                        background Frame("content/gfx/frame/frame_it1.png", -1, -1)
                        use r_lightbutton (img=ProportionalScale(im.Sepia(item.icon), 70, 70), return_value=return_value+[item], align=(0.5, 0.5))

    screen eqdoll(active_mode=True, char=None, frame_size=[55, 55], scr_align=(0.23, 0.23), return_value=['item', 'get'], txt_size=17, fx_size=(300, 320)):
        # active_mode = Allows equipped item to be focused if true, otherwise just dispayes a picture of an item (when equipped).
        # char = source of equipment slots.
        # Slots and the doll ------------------------------------------------------------>
        if char == hero:
            # add Transform(hero.show("sprofile", resize=(400, 720)), alpha=0.8) align(0.5, 1.0)
            add im.Scale("content/gfx/interface/images/doll_male.png", 286, 400) align (0.5, 0.5)
        elif not isinstance(char, dict):
            #f rame:
                # align (0.5, 0.5)
                # background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
            add (char.show("vnsprite", resize=(288, 400), cache=True)) alpha 0.9 align (0.5, 1.0)
            # add im.Scale("content/gfx/interface/images/doll_fem.png", 350, 500) align (0.25, 0.23)

        fixed:
            style_group "content"
            align scr_align
            xysize fx_size

            for slot in equipSlotsPositions:
                python:
                    is_multiple_pytgroup = False

                    if isinstance(char, dict):
                        # saved equipment state
                        equipment = char[slot]

                    elif isinstance(char.eqslots[slot], list):

                        is_multiple_pytgroup = True
                        equipment = char.eqslots[slot][0]
                    else:
                        equipment = char.eqslots[slot]

                    if equipment and active_mode:
                        # Frame background:
                        img = im.Sepia(equipment.icon) if is_multiple_pytgroup else equipment.icon
                        # Old dark/light frame codes, to be removed at review.
                        if equipment.bg_color == "dark":
                            bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                        else:
                            bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                        equipment = [equipment, slot]
                    else:
                        bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                        key = "ring" if slot.startswith("ring") else slot
                        img = blank
                frame:

                    background bg
                    pos (equipSlotsPositions[slot][1]+ (0 if not isinstance(char, dict) or equipSlotsPositions[slot][1] < 0.5 else -0.619), equipSlotsPositions[slot][2])
                    xysize (frame_size[0], frame_size[1])
                    if active_mode and equipment:
                        if not isinstance(char, dict):
                            use r_lightbutton(img=ProportionalScale(img, frame_size[0]*0.78, frame_size[1]*0.78), return_value=return_value+equipment)
                        else:
                            add ProportionalScale(img, frame_size[0]*0.71, frame_size[1]*0.71) align (0.5, 0.5)
                    else:
                        add Transform(ProportionalScale("content/gfx/interface/buttons/filters/%s_bg.png"%key, frame_size[0]*0.71, frame_size[1]*0.71), alpha=0.35) align (0.5, 0.5)


    screen shopping(left_ref=None, right_ref=None):
        use shop_inventory(ref=left_ref, x=0.0)
        use shop_inventory(ref=right_ref, x=1.0)

        if focus:
            vbox:
                align .5, .5
                frame:
                    background Frame("content/gfx/frame/frame_dec_1.png", 30, 30)
                    xalign .5
                    padding 30, 30

                    use itemstats(item=focus, size=(580, 350))

                null height 3

                frame:
                    background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                    xalign .5
                    padding 10, 10

                    has vbox ysize 100

                    frame:
                        xalign .5
                        style_prefix "proper_stats"
                        $ total_price = item_price * amount
                        padding 3, 3
                        fixed:
                            xysize 250, 25
                            label "Retail Price:" text_color gold text_size 22 xalign .0 yalign .5
                            label "[total_price]" text_color gold text_size 22 xalign 1.0 yalign .5

                    fixed:
                        xsize 180
                        xalign .5
                        use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 25, 25), return_value=['control', -10], align=(0, .5))
                        use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 30, 30), return_value=['control', -5], align=(.1, .5))
                        use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 40, 40), return_value=['control', -1], align=(.25, .5))
                        text ("{size=36}[amount]") align .5, .5 color ivory style "proper_stats_label_text"
                        use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 40, 40), return_value=['control', 1], align=(.75, .5))
                        use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 30, 30), return_value=['control', 5], align=(.9, .5))
                        use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 25, 25), return_value=['control', 10], align=(1.0, .5))

                    button:
                        style_prefix "basic"
                        action Return(['item', 'buy/sell'])
                        xsize 100
                        xalign 0.5
                        if purchasing_dir == "buy":
                            text "Buy"
                        elif purchasing_dir == "sell":
                            text "Sell"

        use exit_button

    screen itemstats(item=None, size=(635, 380), style_group="content", mc_mode=False):
        if item:
            vbox:
                xysize size
                align .5, .5
                frame:
                    xalign .5
                    xysize (440, 40)
                    background Frame("content/gfx/frame/p_frame7.png", 10, 10)
                    label '[item.id]' text_color gold xalign 0.5 text_size 20 text_outlines [(1, "#000000", 0, 0)] text_style "interactions_text"

                vbox:
                    align .5, .5
                    label ('{color=#ecc88a}----------------------------------------') xalign .5
                    hbox:
                        xalign .5
                        xfill True
                        frame:
                            xalign .0
                            yalign 0.5
                            background Frame("content/gfx/frame/frame_it2.png", 5, 5)
                            xysize (130, 130)
                            add (ProportionalScale(item.icon, 110, 110)) align .5, .5
                        frame:
                            background Frame("content/gfx/frame/p_frame4.png", 10, 10)
                            padding 15, 15
                            align .5, .5
                            style_prefix "proper_stats"
                            has vbox spacing 1
                            frame:
                                xysize 195, 22
                                padding 4, 1
                                text ('Price:') color gold xalign .0 yoffset -1
                                label ('[item.price]') xalign 1.0 text_size 18 text_color gold yoffset -2
                            frame:
                                xysize 195, 22
                                padding 4, 1
                                text ('Slot:') color ivory xalign .0 yoffset -1
                                python:
                                    if item.slot in SLOTALIASES:
                                        slot = SLOTALIASES[item.slot]
                                    else:
                                        slot = item.slot.capitalize()
                                label ('{size=-3}[slot]') align 1.0, .5
                            frame:
                                xysize 195, 22
                                padding 4, 1
                                text ('Type:') color ivory yalign 0.5
                                label ('{size=-3}%s'%item.type.capitalize()) xalign 1.0 text_size 18 yoffset -2
                            frame:
                                xysize 195, 22
                                padding 4, 1
                                text ('Sex:') color ivory xalign .0 yoffset -1
                                if item.slot in ["gift", "resources", "loot"]:
                                    label "N/A" xalign 1.0 text_size 18 yoffset -2
                                elif item.type == "food" and item.sex == 'unisex':
                                    label "N/A" xalign 1.0 text_size 18 yoffset -2
                                elif item.sex == 'male':
                                    label ('{color=#FFA54F}%s'%item.sex.capitalize()) xalign 1.0 text_size 18 yoffset -2
                                elif item.sex == 'female':
                                    label ('{color=#FFAEB9}%s'%item.sex.capitalize()) xalign 1.0 text_size 18 yoffset -2
                                elif item.sex == 'unisex':
                                    label ('%s'%item.sex.capitalize()) xalign 1.0 text_size 18 yoffset -2
                        frame:
                            xalign 1.0
                            xysize (165, 130)
                            background Frame("content/gfx/frame/p_frame7.png", 5, 5)
                            has viewport mousewheel True draggable True style_group "proper_stats" xysize (165, 122) child_size 160, 500
                            vbox:
                                spacing 1
                                if item.mod:
                                    label ('Stats:') text_size 18 text_color gold xpos 10
                                    for stat, value in item.mod.items():
                                        frame:
                                            xysize 153, 20
                                            text stat.capitalize() color ivory size 16 align (0.02, 0.5)
                                            label (u'{size=-4}[value]') align (0.98, 0.5)
                                    null height 2
                                if item.max:
                                    label ('Max:') text_size 18 text_color gold xpos 10
                                    for stat, value in item.max.items():
                                        frame:
                                            xysize 153, 20
                                            text stat.capitalize() color ivory size 16 align (0.02, 0.5)
                                            label u'{size=-4}[value]' align (0.98, 0.5)
                                    null height 2
                                if item.min:
                                    label ('Min:') text_size 18 text_color gold xpos 10
                                    for stat, value in item.min.items():
                                        frame:
                                            xysize 153, 20
                                            text stat.capitalize() color ivory size 16 align (0.02, 0.5)
                                            label (u'{size=-4}%d'%value) align (0.98, 0.5)
                                    null height 2
                                if item.addtraits:
                                    label ('Adds Traits:') text_size 16 text_color gold xpos 10
                                    for trait in item.addtraits:
                                        frame:
                                            xysize 153, 20
                                            text(u'%s'%trait.capitalize()) color ivory size 16 align (0.5, 0.5)
                                    null height 2
                                if item.removetraits:
                                    label ('Removes Traits:') text_size 16 text_color gold xpos 10
                                    for trait in item.removetraits:
                                        frame:
                                            xysize 153, 20
                                            text(u'%s'%trait.capitalize()) color ivory size 16 align (0.5, 0.5)
                                    null height 2
                                if item.add_be_spells:
                                    label ('Adds Skills:') text_size 16 text_color gold xpos 10
                                    for skill in item.add_be_spells:
                                        frame:
                                            xysize 153, 20
                                            text(u'%s'%skill.capitalize()) color ivory size 16 align (0.5, 0.5)
                                    null height 2
                                if item.remove_be_spells:
                                    label ('Removes Skills:') text_size 16 text_color gold xpos 10
                                    for skill in item.remove_be_spells:
                                        frame:
                                            xysize 153, 20
                                            text (u'%s'%skill.capitalize()) color ivory size 16 align (0.5, 0.5)
                                    null height 2
                                if item.addeffects:
                                    label ('Adds Effects:') text_size 16 text_color gold xpos 10
                                    for effect in item.addeffects:
                                        frame:
                                            xysize 153, 20
                                            text(u'%s'%effect.capitalize()) color ivory size 16 align (0.5, 0.5)
                                    null height 2
                                if item.removeeffects:
                                    label ('Removes Effects:') text_size 16 text_color gold xpos 10
                                    for effect in item.removeeffects:
                                        frame:
                                            xysize 153, 20
                                            text(u'%s'%effect.capitalize()) color ivory size 16 align (0.5, 0.5)
                                if hasattr(item, 'mtemp'):
                                    if item.mtemp:
                                        label ('Frequency:') text_size 18 text_color gold xpos 10
                                        frame:
                                            xysize 153, 20
                                            if item.mreusable:
                                                if item.mtemp > 1:
                                                    text "Every [item.mtemp] days" color ivory size 16 align (0.02, 0.5)
                                                else:
                                                    text "Every day" color ivory size 16 align (0.02, 0.5)
                                            else:
                                                if item.mtemp > 1:
                                                    text "After [item.mtemp] days" color ivory size 16 align (0.02, 0.5)
                                                else:
                                                    text "After one day" color ivory size 16 align (0.02, 0.5)
                                        if hasattr(item, 'mdestruct'):
                                            if item.mdestruct:
                                                frame:
                                                    xysize 153, 20
                                                    text "Disposable" color ivory size 16 align (0.02, 0.5)
                                        if hasattr(item, 'mreusable'):
                                            if item.mreusable:
                                                frame:
                                                    xysize 153, 20
                                                    text "Reusable" color ivory size 16 align (0.02, 0.5)
                                        if hasattr(item, 'statmax'):
                                            if item.statmax:
                                                frame:
                                                    xysize 153, 20
                                                    text "Stat limit" color ivory size 16 align (0.02, 0.5)
                                                    label (u'{size=-4}%d'%item.statmax) align (0.98, 0.5)
                                if hasattr(item, 'ctemp'):
                                    if item.ctemp:
                                        label ('Duration:') text_size 18 text_color gold xpos 10
                                        frame:
                                            xysize 153, 20
                                            if item.ctemp > 1:
                                                text "[item.ctemp] days" color ivory size 16 align (0.02, 0.5)
                                            else:
                                                text "One day" color ivory size 16 align (0.02, 0.5)
                    label ('{color=#ecc88a}----------------------------------------') xalign .5
                    frame:
                        xalign .5
                        background Frame("content/gfx/frame/p_frame7.png", 10, 10)
                        has viewport mousewheel True xysize (460, 100)
                        text '[item.desc]' style "TisaOTM" size 16 color gold

    # Inventory paging
    screen paging(path="content/gfx/interface/buttons/", use_filter=True, ref=None, xysize=(270, 60), root=None, align=(.5, .0)):
        frame:
            background Frame("content/gfx/frame/BG_choicebuttons.png", 10, 10)
            ypadding 15

            style_group "content"
            xpadding 15
            xysize xysize
            align align

            vbox:
                align .5, .5
                # Filter
                if use_filter:
                    hbox:
                        xmaximum xysize[0] - 15
                        xfill True
                        xalign 0.5
                        $ img = "".join([path, 'prev.png'])
                        imagebutton:
                            align .0, .5
                            idle img
                            hover im.MatrixColor(img, im.matrix.brightness(.15))
                            action Function(ref.apply_filter, "prev")

                        python:
                            if ref.slot_filter in SLOTALIASES:
                                slot = SLOTALIASES[ref.slot_filter]
                            else:
                                slot = ref.slot_filter.capitalize()
                        label "[slot] " align .5, .5  text_color ivory

                        imagebutton:
                            align 1.0, .5
                            idle path+'next.png'
                            hover im.MatrixColor(path+'next.png', im.matrix.brightness(.15))
                            action Function(ref.apply_filter, "next")
                # Listing
                hbox:
                    xalign 0.5
                    xmaximum xysize[0] - 5
                    xfill True
                    hbox:
                        align (0.0, 0.5)
                        imagebutton:
                            yalign 0.5
                            idle (path+'first.png')
                            hover (im.MatrixColor(path+'first.png', im.matrix.brightness(0.15)))
                            action Function(ref.first)
                        imagebutton:
                            yalign 0.5
                            idle (path+'prev.png')
                            hover (im.MatrixColor(path+'prev.png', im.matrix.brightness(0.15)))
                            action Function(ref.prev)
                    label ("%d - %d"%(ref.page+1, ref.max_page)) align (0.5, 0.5) text_color ivory
                    hbox:
                        align (1.0, 0.5)
                        imagebutton:
                            yalign 0.5
                            idle (path+'next.png')
                            hover (im.MatrixColor(path+'next.png', im.matrix.brightness(0.15)))
                            action Function(ref.next)
                        imagebutton:
                            yalign 0.5
                            idle (path+'last.png')
                            hover (im.MatrixColor(path+'last.png', im.matrix.brightness(0.15)))
                            action Function(ref.last)

    screen shop_inventory(ref=None, x=0.0):
        key "mousedown_4" action ref.inventory.next
        key "mousedown_5" action ref.inventory.prev

        frame at fade_in_out(t1=0.5, t2=0.5):
            style_group "content"
            background Frame(Transform("content/gfx/frame/mes11.jpg", alpha=0.5), 5, 5)
            xalign x
            yfill True
            has vbox

            use paging(ref=ref.inventory, xysize=(260, 90))

            null height 5

            hbox:
                xalign 0.5
                add im.Scale("content/gfx/interface/icons/gold.png", 25, 25) align (0.0, 0.5)
                null width 10
                text u'[ref.gold]' align (0.5, 1.0) color gold size 23

            null height 5

            if isinstance(ref, ItemShop):
                label "[ref.name]" text_color ivory xalign 0.5
            elif isinstance(ref, PytCharacter):
                label "[ref.nickname]" text_color ivory xalign 0.5
            else:
                label "Inventory" text_color ivory xalign 0.5

            null height 5

            use items_inv(char=ref, main_size=(268, 522), frame_size=(85, 85), return_value=["item", ref])

    screen r_lightbutton:
        default align = (0, 0)
        imagebutton:
            align align
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(0.15))
            action Return(return_value)

    screen rg_lightbutton:
        if entry.flag("_day_countdown_interactions_blowoff"):
            $ temp = "angry"
        elif entry.disposition >= 500:
            $ temp = "shy"
        elif entry.disposition >= 100:
            $ temp = "happy"
        else:
            $ temp = "indifferent"
        $ p_img = entry.show("portrait", temp, label_cache=True, resize=(90, 90), type="reduce")
        default align = (0, 0)
        vbox:
            frame:
                padding(2, 2)
                background Frame("content/gfx/frame/MC_bg3.png")
                imagebutton:
                    align align
                    idle (p_img)
                    hover (im.MatrixColor(p_img, im.matrix.brightness(0.15)))
                    action Return(return_value)
            frame:
                padding(2, 2)
                xsize 94
                background Frame("content/gfx/frame/gm_frame.png")
                label "Tier [entry.tier]" xalign 0.5 text_color "#DAA520"

    screen rtt_lightbutton:
        imagebutton yalign 0.5:
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
            action Return(return_value)
            hovered tt.action(u"%s"%tooltip)

    python:
        def get_screens(*args):
            """
            Simple checks for active screens.
            Returns True if at least one of the screens is shown and False if not.
            """
            for scr in args:
                if renpy.get_screen(scr):
                    return True
            return False

    screen quest_notifications(q, type, align=None, autohide=2.5):
        zorder 500

        fixed:
            at slide(so1=(0, -600), eo1=(0, 40), t1=.4,
                         so2=(0, 40), eo2=(0, -600), t2=.6)
            # else:
                # at slide(so1=(0, -600), eo1=(0, 0), t1=1.0,
                             # so2=(0, 0), eo2=(0, -600), t2=1.0)
            if align:
                align align
            else:
                xalign .5
            xysize (500, 200)
            frame:
                background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.65), 10, 10)
                style_group "dropdown_gm2"
                xysize (400, 150)
                align .5, .5
                text q align .5, .5 style "TisaOTM" size 25

                imagebutton:
                    align 1.005, -.03
                    idle "content/gfx/interface/buttons/close3.png"
                    hover "content/gfx/interface/buttons/close3_h.png"
                    action Hide("quest_notifications")

            add ProportionalScale(interfaceimages + "quest.png", 170, 120) pos (100, 0)
            frame:
                pos 400, 140 xanchor 1.0
                xpadding 15
                background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.45), 10, 10)
                text type style "content_text" size 40 color gold

        if autohide:
            timer autohide action Hide("quest_notifications")

    screen character_pick_screen: # screen to select someone from the MC team
        key "mousedown_3" action Return(False)
        frame:
            align (.5, .5)
            xsize 450
            ysize 310
            padding(2, 2)
            background Frame("content/gfx/frame/frame_dec_1.png")
            label "Select a character" align (0.5, 0.08) text_color "#DAA520" text_size 18
            hbox:
                spacing 45
                align (.5, .4)
                for l in hero.team:
                    $ char_profile_img = l.show('portrait', resize=(101, 101), cache=True)
                    $ img = "content/gfx/frame/ink_box.png"
                    vbox:
                        spacing 1
                        xsize 102
                        imagebutton:
                            xalign .5
                            background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                            idle (char_profile_img)
                            hover (im.MatrixColor(char_profile_img, im.matrix.brightness(0.15)))
                            action Return(l)
                            xysize (102, 102)
                        bar:
                            xalign .5
                            right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                            left_bar im.Scale("content/gfx/interface/bars/hp2.png", 102, 14)
                            value l.health
                            range l.get_max("health")
                            thumb None
                            left_gutter 0
                            right_gutter 0
                            xysize (102, 14)
                        bar:
                            xalign .5
                            right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                            left_bar im.Scale("content/gfx/interface/bars/mp2.png", 102, 14)
                            value l.mp
                            range l.get_max("mp")
                            thumb None
                            left_gutter 0
                            right_gutter 0
                            xysize (102, 14)
                        bar:
                            xalign .5
                            right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                            left_bar im.Scale("content/gfx/interface/bars/vitality2.png", 102, 14)
                            value l.vitality
                            range l.get_max("vitality")
                            thumb None
                            left_gutter 0
                            right_gutter 0
                            xysize (102, 14)
                        frame:
                            xalign .5
                            xsize 102
                            ysize 30
                            padding(2, 2)
                            background Frame("content/gfx/frame/gm_frame.png")
                            $ name = l.name[:8]
                            label "[name]" align (0.5, 0.5) text_color "#DAA520" text_size 16

            vbox:
                style_group "wood"
                align (.5, 0.9)
                button:
                    xysize (102, 40)
                    yalign 0.5
                    action Return(False)
                    text "Cancel" size 15 color goldenrod

    screen top_stripe(show_return_button=True, return_button_action=None, show_lead_away_buttons=True, show_team_status=False):
        default tt = Tooltip("")
        default return_action = Return(['control', 'return']) if return_button_action is None else return_button_action

        # Hotkeys:
        if show_return_button and not get_screens("girl_interactions",
                                                  "building_management_leftframe_businesses_mode",
                                                  "chars_list",
                                                  "char_profile"):
            key "mousedown_3" action return_action

        # Top Stripe Frame:
        add "content/gfx/frame/top_stripe.png"

        # Screen frame, always visible:
        if show_return_button:
            add "content/gfx/frame/h3.png"
        else:
            add "content/gfx/frame/h2.png"

        # All buttons:
        fixed:
            xysize(config.screen_width, 43)
            hbox:
                style_group "content"
                align .023, .5
                null width 10
                add "coin_top" yalign .5
                null width 5
                text "[hero.gold]" size 20 color gold yalign .5
                null width 15
                text u'Day [day]' size 20 color ivory yalign .5
                null width 15
                button:
                    style "sound_button"
                    xysize (37, 37)
                    action [SelectedIf(not (_preferences.mute["music"] or _preferences.mute["sfx"])),
                            If(_preferences.mute["music"] or _preferences.mute["sfx"],
                            true=[Preference("sound mute", "disable"), Preference("music mute", "disable")],
                            false=[Preference("sound mute", "enable"), Preference("music mute", "enable")])]
                    hovered tt.Action("Mute All")

            # Left HBox: ======================================================>>>>>>
            # Add to and remove from Team Button.
            hbox:
                align(0.3, 0.5)
                if renpy.get_screen("char_profile") and char not in pytfall.ra:
                    if char in hero.team:
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/RG.png" , 36, 40)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/RG.png", 36, 40), im.matrix.brightness(.15))
                            action Function(hero.team.remove, char)
                            hovered tt.Action("Remove [char.nickname] from player team")
                    else:
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/AG.png" , 36, 40)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/AG.png", 36, 40), im.matrix.brightness(.15))
                            action If(len(hero.team) < 3, true=Function(hero.team.add, char), false=Show("message_screen", msg="Team cannot have more than three members"))
                            hovered tt.Action("Add [char.nickname] to player team")

            # AP Frame/Next Day button:
            if any([renpy.current_screen().tag == "next_day", hero.AP == 0]) and renpy.current_screen().tag not in ["mainscreen", "girl_interactions"] and not show_team_status:
                button:
                    style_group "basic"
                    align (0.5, 0.6)
                    if renpy.current_screen().tag == "next_day":
                        action Return(['control', "next_day_local"])
                    else:
                        action (hs, Function(global_flags.set_flag, "nd_music_play"), Jump("next_day"))
                    text "Next Day"
            else:
                add ProportionalScale("content/gfx/frame/frame_ap.png", 170, 50) align (0.5, 0.7)
                label "[hero.AP]" align (0.53, 0.6) style "content_label"  text_size 23 text_color ivory text_bold True

            # Right HBox:
            hbox:
                align(0.8, 0.5)
                spacing 5
                if config.developer:
                    textbutton "{size=20}{color=[ivory]}{b}F":
                        yalign .5
                        action Jump("fonts")
                        hovered tt.Action("View available Fonts")

                if renpy.current_screen().tag not in ["quest_log"]:
                    imagebutton:
                        idle im.Scale("content/gfx/interface/buttons/journal1.png", 36, 40)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/journal1.png", 36, 40), im.matrix.brightness(0.25))
                        hovered tt.Action("Quest Journal")
                        action ShowMenu("quest_log")

                if renpy.current_screen().tag == "mainscreen":
                    imagebutton:
                        idle im.Scale("content/gfx/interface/buttons/preference.png", 39, 40)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/preference.png", 39, 40), im.matrix.brightness(0.25))
                        action Show("s_menu", transition=dissolve)
                        hovered tt.Action("Game Preferences")
                    key "mousedown_3" action Show("s_menu", transition=dissolve)

                if renpy.current_screen().tag not in ["mainscreen", "girl_interactions", "quest_log", "dungeon"] and show_lead_away_buttons:
                    imagebutton:
                        idle im.Scale("content/gfx/interface/buttons/MS.png" , 38, 37)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/MS.png" , 38, 37), im.matrix.brightness(0.25))
                        action (Hide(renpy.current_screen().tag), Function(global_flags.del_flag, "keep_playing_music"),  Jump("mainscreen"))
                        hovered tt.Action("Return to Main Screen")

                if renpy.current_screen().tag in ["char_profile", "char_equip"] and char.action != "Exploring":
                    imagebutton:
                        idle im.Scale("content/gfx/interface/buttons/IT2.png" , 34, 37)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/IT2.png" , 34, 37), im.matrix.brightness(0.25))
                        action Return(["jump", "item_transfer"])
                        hovered tt.Action("Transfer items between [hero.name] and and [char.nickname]")

                if renpy.current_screen().tag not in ["hero_profile", "girl_interactions", "quest_log"] and show_lead_away_buttons:
                    imagebutton:
                        idle im.Scale("content/gfx/interface/buttons/profile.png", 35, 40)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/profile.png", 35, 40), im.matrix.brightness(0.25))
                        action [SetField(pytfall.hp, "came_from", last_label), Hide(renpy.current_screen().tag), Jump("hero_profile")]
                        hovered tt.Action("View Hero Profile")

                null width 10

                imagebutton:
                        idle im.Scale("content/gfx/interface/buttons/save.png" , 40, 40)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/save.png" , 40, 40), im.matrix.brightness(0.25))
                        hovered tt.Action("QuickSave")
                        action QuickSave()

                imagebutton:
                    idle im.Scale("content/gfx/interface/buttons/load.png" , 38, 40)
                    hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/load.png" , 38, 40), im.matrix.brightness(0.25))
                    hovered tt.Action("QuickLoad")
                    action QuickLoad()

            if show_return_button:
                imagebutton:
                    align(0.993, 0.5)
                    idle im.Scale("content/gfx/interface/buttons/close.png", 35, 35)
                    hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/close.png", 35, 35), im.matrix.brightness(0.25))
                    action return_action
                    hovered tt.Action("Return to previous screen")

            if show_team_status:
                hbox:
                    spacing 25
                    pos (17, 50)
                    for l in hero.team:
                        $ char_profile_img = l.show('portrait', resize=(101, 101), cache=True)
                        $ img = "content/gfx/frame/ink_box.png"
                        vbox:
                            spacing 1
                            xsize 102
                            imagebutton:
                                background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                                idle (char_profile_img)
                                hover (im.MatrixColor(char_profile_img, im.matrix.brightness(0.15)))
                                action Return(l)
                                align 0, .5
                                xysize (102, 102)
                            bar:
                                right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                                left_bar im.Scale("content/gfx/interface/bars/hp2.png", 102, 14)
                                value l.health
                                range l.get_max("health")
                                thumb None
                                left_gutter 0
                                right_gutter 0
                                xysize (102, 14)
                            bar:
                                right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                                left_bar im.Scale("content/gfx/interface/bars/mp2.png", 102, 14)
                                value l.mp
                                range l.get_max("mp")
                                thumb None
                                left_gutter 0
                                right_gutter 0
                                xysize (102, 14)
                            bar:
                                right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                                left_bar im.Scale("content/gfx/interface/bars/vitality2.png", 102, 14)
                                value l.vitality
                                range l.get_max("vitality")
                                thumb None
                                left_gutter 0
                                right_gutter 0
                                xysize (102, 14)
        if renpy.current_screen().tag == "mainscreen":
            frame:
                background None
                align(0.5, 0.997)
                xysize (750, 100)
                text (u"{=content_text}{size=24}{color=[ivory]}%s" % tt.value) align(0.5, 0.5)
        elif renpy.current_screen().tag == "building_management":
            frame:
                pos (960, 300)
                background None
                xpadding 10
                xysize (310, 200)
                text (u"{=content_text}{size=20}{color=[goldenrod]}%s" % tt.value) yalign 0.02 size 14

        elif renpy.current_screen().tag == "char_profile":
            frame:
                background None
                pos 332, 622
                xpadding 10
                xysize (951, 100)
                has hbox spacing 1
                text (u"{=content_text}{color=[ivory]}%s" % tt.value)
        elif renpy.current_screen().tag == "chars_list":
            frame:
                background None
                align(0.1, 1.0)
                xysize (946, 65)
                text (u"{=content_text}{size=24}{color=[ivory]}%s" % tt.value) align(0.5, 0.5)

    screen message_screen(msg, size=(500, 300), use_return=False):
        modal True
        zorder 10

        fixed:
            align(0.5, 0.5)
            xysize(size[0], size[1])
            xfill True
            yfill True

            add im.Scale("content/gfx/frame/frame_bg.png", size[0], size[1])

            vbox:
                style_prefix "proper_stats"
                spacing 30
                align(0.5, 0.5)
                vbox:
                    xmaximum (size[0] - 50)
                    text msg xalign 0.5 color lightgoldenrodyellow size 20
                textbutton "Ok" action If(use_return, true=Return(), false=Hide("message_screen")) minimum(120, 30) xalign 0.5 style "yesno_button"
        key "K_RETURN" action If(use_return, true=Return(), false=Hide("message_screen"))
        key "K_ESCAPE" action If(use_return, true=Return(), false=Hide("message_screen"))

    screen display_disposition(tag, d, size, x, y, t):
        tag tag
        text "[d]" font "fonts/rubius.ttf" size size color crimson at found_cash(x, y, t)
        timer t+0.2 action Hide("display_disposition")

    screen pyt_input(default="", text="", length=20, size=(350, 150)):
        use keymap_override
        modal True
        zorder 10

        fixed:
            align(0.5, 0.5)
            minimum(size[0], size[1])
            maximum(size[0], size[1])
            xfill True
            yfill True

            add im.Scale("content/gfx/frame/frame_bg.png", size[0], size[1])

            vbox:
                spacing 10
                align(0.5, 0.5)
                text text xalign 0.5 style "TisaOTM" size 20 color goldenrod
                input:
                    id "text_input"
                    default default
                    length length
                    xalign 0.5
                    style "TisaOTM"
                    size 20
                    color white
                    changed dummy_interaction_restart
                button:
                    style_prefix "wood"
                    xysize (100, 50)
                    text "OK"  style "TisaOTM" size 15 color goldenrod align (.5, .5)
                    xalign .5
                    action Return(renpy.get_widget("pyt_input", "text_input").content)
        key "input_enter" action Return(renpy.get_widget("pyt_input", "text_input").content)
        key "mousedown_3" action Return (default)

    screen exit_button(size=(35, 35), align=(1.0, 0.0), action=Return(['control', 'return'])):
        $ img = im.Scale("content/gfx/interface/buttons/close.png" , size[0], size[1])
        imagebutton:
            align(align[0], align[1])
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(0.25))
            action action
        key "mousedown_3" action action
        key "K_ESCAPE" action action

    screen dropdown(pos):
        # Trying to create a drop down screen with choices of actions:
        zorder 3
        modal True

        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()

        # Get mouse coords:
        python:
            x, y = pos
            xval = 1.0 if x > config.screen_width/2 else .0
            yval = 1.0 if y > config.screen_height/2 else .0

        frame:
            style_prefix "dropdown_gm"
            pos (x, y)
            anchor (xval, yval)
            has vbox

            transclude # Doesn't work as expected, no style passing to other screens, no modal, bull shit of a statement basically at this stage :(  TODO: is it still true in modern renpy?

    screen set_action_dropdown(char, pos=()):
        # Trying to create a drop down screen with choices of actions:
        zorder 3
        modal True

        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()

        # Get mouse coords:
        python:
            x, y = pos
            xval = 1.0 if x > config.screen_width/2 else .0
            yval = 1.0 if y > config.screen_height/2 else .0

        frame:
            style_prefix "dropdown_gm"
            pos (x, y)
            anchor (xval, yval)
            has vbox

            if isinstance(char.location, UpgradableBuilding):
                # Jobs:
                $ jobs = char.location.get_valid_jobs(char)
                for i in jobs:
                    textbutton "[i.id]":
                        # Without Equipping for the job!
                        action [Function(set_char_to_work, char, char.location, i), Hide("set_action_dropdown")]

            # Other buildings
            elif hasattr(char.location, "actions"):
                for entry in char.location.actions:
                    if entry == "Guard":
                        if char.status not in ("slave", "various") and ("Warrior" in char.occupations or char.disposition <= 950):
                            textbutton "[entry]":
                                action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                    elif entry == "Take Course":
                        textbutton "[entry]":
                            action [Hide("set_action_dropdown"), Hide("charslist"), Hide("char_profile"), # Hide the dropdown screen, the chars list and char profile screens
                                    SetField(store, "char", char, True), # Ensure that the global var char is set to the current char
                                    Jump("char_training")] # Jump to the training screen
                    else:
                        textbutton "[entry]":
                                action [SetField(char, "action", entry), Function(equip_for, char, entry), If(char_is_training(char), true=Function(stop_training, char)), Hide("set_action_dropdown")]

            # Prevent none action in schools
            if not hasattr(char.location, "is_school") or not char.location.is_school:
                textbutton "None":
                    action [SetField(char, "action", None), If(char_is_training(char), true=Function(stop_training, char)), Hide("set_action_dropdown")]

            textbutton "Rest":
                # TODO: Temporary way to set action to Rest, this needs to be rewritten completely.
                action [SetField(char, "action", Rest()), Hide("set_action_dropdown")]

            textbutton "Close":
                action [Hide("set_action_dropdown")]
                
        key "K_ESCAPE" action [Hide("set_action_dropdown")]

    screen set_location_dropdown(char, pos=()):
        # Trying to create a drop down screen with choices of actions:
        zorder 3
        modal True

        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()

        # Get mouse coords:
        python:
            x, y = pos
            xval = 1.0 if x > config.screen_width/2 else .0
            yval = 1.0 if y > config.screen_height/2 else .0

        frame:
            style_prefix "dropdown_gm"
            pos (x, y)
            anchor (xval, yval)
            has vbox
            # Updating to new code: *Ugly code atm, TODO: Fix IT!
            for building in hero.buildings:
                if isinstance(building, UpgradableBuilding):
                    if char.action in building.jobs:
                        $ can_keep_action = True
                    else:
                        $ can_keep_action = False
                    if can_keep_action:
                        textbutton "[building.name]":
                            action [SelectedIf(char.location==building), If(char_is_training(char),
                                    true=Function(stop_training, char)), Function(change_location, char, building),
                                    Hide("set_location_dropdown")]
                    else:
                        textbutton "[building.name]":
                            action [SelectedIf(char.location==building), SetField(char, "action", None),
                                    If(char_is_training(char), true=Function(stop_training, char)),
                                    Function(change_location, char, building),
                                    Hide("set_location_dropdown")]

            textbutton "Home":
                action [If(char_is_training(char), true=Function(stop_training, char)), Function(change_location, char, char.home), Hide("set_location_dropdown")]

            textbutton "Close":
                action Hide("set_location_dropdown")
                
        key "K_ESCAPE" action Hide("set_location_dropdown")

    screen set_home_dropdown(char, pos=()):
        # Trying to create a drop down screen with choices of actions:
        zorder 3
        modal True

        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()

        # Get mouse coords:
        python:
            x, y = pos
            xval = 1.0 if x > config.screen_width/2 else .0
            yval = 1.0 if y > config.screen_height/2 else .0

        frame:
            style_prefix "dropdown_gm"
            pos (x, y)
            anchor (xval, yval)
            has vbox

            for building in hero.buildings:
                if isinstance(building, UpgradableBuilding) or building.habitable:
                    textbutton "[building.name]":
                        action SelectedIf(char.home==building), SetField(char, "home", building), Hide("set_home_dropdown")
            textbutton "Streets":
                action SetField(char, "home", locations["Streets"]), Hide("set_home_dropdown")
            textbutton "Close":
                action Hide("set_home_dropdown")
                
        key "K_ESCAPE" action Hide("set_home_dropdown")

    screen char_rename(char=None):
        modal True
        zorder 1
        frame:
            if isinstance(char, Player):
                background Frame("content/gfx/frame/post_battle.png", 500, 400)
                xysize(500, 400)
            elif char.status != "slave":
                background Frame("content/gfx/frame/post_battle.png", 500, 300)
                xysize(500, 300)
            else:
                background Frame("content/gfx/frame/post_battle.png", 500, 500)
                xysize(500, 500)
            align (0.5, 0.5)
            vbox:
                style_prefix "wood"
                at fade_in_out()
                align (0.5, 0.5)
                spacing 10
                if isinstance(char, Player) or char.status == "slave":
                    text "Name:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                    button:
                        xysize (340, 60)
                        xalign 1.0
                        yalign 0.5
                        text "[char.name]" size 16 color goldenrod
                        action Return(["rename", "name"])
                        padding (10, 10)
                if not(isinstance(char, Player)): # it's weird to give a nickname to yourself. should be handled by ingame events
                    text "Nickname:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                    button:
                        xysize (340, 60)
                        xalign 1.0
                        yalign 0.5
                        if char.nickname != char.name:
                            text "[char.nickname]" size 16 color goldenrod
                        else:
                            text "None" size 16 color goldenrod
                        action Return(["rename", "nick"])
                        padding (10, 10)
                if isinstance(char, Player) or char.status == "slave":
                    text "Full Name:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                    button:
                        xysize (340, 60)
                        xalign 1.0
                        yalign 0.5
                        text "[char.fullname]" size 16 color goldenrod
                        action Return(["rename", "full"])
                        padding (10, 10)

                null height 20
                button:
                    xysize (100, 50)
                    xalign 0.5
                    yalign 0.5
                    text "Back" size 16 color goldenrod
                    action Hide("char_rename")
                    padding (10, 10)
                    
        key "K_ESCAPE" action Hide("char_rename")

    screen poly_matrix(in_file, show_exit_button=False, cursor="content/gfx/interface/icons/zoom_glass.png", xoff=20, yoff=20, hidden=[]):
        # If a tuple with coordinates is provided instead of False for show_exit_button, exit button will be placed there.

        default tooltip = False

        on "hide":
            action SetField(config, "mouse", None), Hide("show_poly_matrix_tt")

        python:
            with open(renpy.loader.transfn(in_file)) as f:
                matrix = json.load(f)

        $ func = renpy.curry(point_in_poly)
        for i in matrix:
            if i["id"] not in hidden:
                if "tooltip" in i:
                    if "align" in i:
                        python:
                            align = tuple(i["align"])
                            pos = ()
                            anchor = ()
                    else:
                        python:
                            align = ()
                            # Get a proper placement:
                            allx, ally = list(), list()

                            for t in i["xy"]:
                                allx.append(t[0])
                                ally.append(t[1])

                            maxx = max(allx)
                            maxy = max(ally)
                            minx = min(allx)
                            miny = min(ally)

                            w, h = config.screen_width, config.screen_height

                            side = i.get("place", "left")

                            if side == "left":
                                pos = (minx - 10, sum(ally)/len(ally))
                                anchor = (1.0, 0.5)
                            elif side == "right":
                                pos = (maxx + 10, sum(ally)/len(ally))
                                anchor = (0.0, 0.5)
                            elif side == "bottom":
                                pos = (sum(allx)/len(allx), maxy + 10)
                                anchor = (0.5, 0.0)
                            elif side == "top":
                                pos = (sum(allx)/len(allx), miny - 10)
                                anchor = (0.5, 1.0)

                    button:
                        background Null()
                        focus_mask func(i["xy"])
                        action Return(i["id"])
                        hovered [SetField(config, "mouse", {"default": [(cursor, xoff, yoff)]}),
                                       Show("show_poly_matrix_tt", pos=pos, anchor=anchor, align=align, text=i["tooltip"]), With(dissolve)]
                        unhovered [SetField(config, "mouse", None),
                                           Hide("show_poly_matrix_tt"), With(dissolve)]
                else:
                    button:
                        background Null()
                        focus_mask func(i["xy"])
                        action Return(i["id"])
                        hovered SetField(config, "mouse", {"default": [(cursor, xoff, yoff)]})
                        unhovered SetField(config, "mouse", None)

        if show_exit_button:
            textbutton "Close":
                align show_exit_button
                action Return(False)

    screen show_poly_matrix_tt(pos=(), anchor=(), align=(), text=""):
        zorder 1
        frame:
            if align:
                align align
            if pos:
                pos pos
                anchor anchor
            text text

    screen hidden_area(items=()):
        on "hide":
            action SetField(config, "mouse", None)

        # randomly places a "hidden" rectangular area(s) on the screen. Areas are actually plain buttons with super low alpha...
        # Expects a list/tuple, like: (["hidden_cache_1", (100, 100), (.1, .5)], ["hidden_cache_2", (50, 50), (.54, .10)] If cache is found, screen (which should be called) will return: "hidden_cache_1" string. Tuple is the size in pixels.
        # Data is randomized outside of this screen!
        for item, size, align in items:
            button:
                align align
                background Transform(Solid("#000000", xysize=size), alpha=.01)
                xysize size
                focus_mask True
                action Return(item)
                hovered SetField(config, "mouse", {"default": [("content/gfx/interface/icons/net.png", 0, 0)]})
                unhovered SetField(config, "mouse", None)

                # $ raise Exception(args[1])

    screen fishing_area(items):
        on "hide":
            action SetField(config, "mouse", None)

        hbox:
            xsize 1280
            box_wrap True
            for i in xrange(15):
                add "water_texture__"

        # special screen for fishing based on screen hidden_area, uses visible animated imagebuttons instead of invisible areas:
        $ fishing_circles_webm = Transform(Movie(channel="main_gfx_attacks", play="content/gfx/animations/bubbles_webm/movie.webm", mask="content/gfx/animations/bubbles_webm/mask.webm"), zoom=0.4, alpha=0.4)
        $ fishing_circles_webm_alpha = Transform(Movie(channel="main_gfx_attacks", play="content/gfx/animations/bubbles_webm/movie.webm", mask="content/gfx/animations/bubbles_webm/mask.webm"), zoom=0.8, alpha=1.0)
        for item in items:
            imagebutton:
                at fish # Randomization is now done here.
                idle (fishing_circles_webm)
                hover (fishing_circles_webm_alpha)
                action Return(item)
                hovered SetField(config, "mouse", {"default": [("content/gfx/interface/icons/fishing_hook.png", 20, 20)]})
                unhovered SetField(config, "mouse", None)
        key "mousedown_3" action (Hide("fishing_area"), Return("Stop Fishing"))
    ##############################################################################
    screen notify:
        zorder 500

        vbox:
            at fade_in_out(t1=0.25, t2=0.25)
            style_group "notify_bubble"

            frame:
                text message

        timer 1.5 action Hide("notify")

init: # Settings:
    screen s_menu(s_menu="Settings"):
        default tt = Tooltip("Hover cursor over options buttons to see the description.")
        zorder 10**5 + 1
        modal True

        key "mousedown_3" action Hide("s_menu"), With(dissolve)

        # default s_menu = "Settings"

        add Transform("content/gfx/images/bg_gradient2.png", alpha=0.8)

        frame:
            # at fade_in_out(sv1=0.0, ev1=1.0, t1=0.7,
                                    # sv2=1.0, ev2=0.0, t2=0.5)
            background Frame (Transform("content/gfx/frame/framegp2.png", alpha=0.8), 10, 10)
            align (0.315, 0.5)
            xysize (690, 414)
            style_group "smenu"
            has hbox align (0.5, 0.5) xfill True

            if s_menu == "Settings":
                grid 3 1:
                    align (0.5, 0.5)
                    spacing 7
                    # Left column...
                    frame:
                        align (0.5, 0.5)
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.3), 10, 10)
                        xpadding 10
                        ypadding 10
                        has vbox spacing 5
                        # frame:
                            # background Frame(Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            # xsize 194
                            # ypadding 8
                            # style_group "dropdown_gm2"
                            # has vbox align (0.5, 0.5)

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Display -") style "TisaOTMolxm"
                            textbutton _("Window") action Preference("display", "window") xsize 150 xalign 0.5 text_size 16
                            textbutton _("Fullscreen") action Preference("display", "fullscreen") xsize 150 xalign 0.5 text_size 16

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Transitions -") style "TisaOTMolxm"
                            textbutton _("All") action Preference("transitions", "all") xsize 150 xalign 0.5 text_size 16
                            textbutton _("None") action Preference("transitions", "none") xsize 150 xalign 0.5 text_size 16

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Text Speed -") style "TisaOTMolxm"
                            null height 8
                            bar value Preference("text speed") align (0.5, 0.5)

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            textbutton _("Gamepad") action SensitiveIf(GamepadExists()), GamepadCalibrate() xsize 150 text_size 16


                    # Middle column...
                    frame:
                        align (0.5, 0.5)
                        background Frame (Transform("content/gfx/frame/ink_box.png", alpha=0.3), 10, 10)
                        xpadding 10
                        ypadding 10
                        has vbox spacing 5
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Skip -") style "TisaOTMolxm"
                            textbutton _("Seen Messages") action Preference("skip", "seen") xsize 150 xalign 0.5 text_size 16
                            textbutton _("All Messages") action Preference("skip", "all") xsize 150 xalign 0.5 text_size 16

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- After Choices -") style "TisaOTMolxm"
                            textbutton _("Stop Skipping") action Preference("after choices", "stop") xsize 150 xalign 0.5 text_size 16
                            textbutton _("Keep Skipping") action Preference("after choices", "skip") xsize 150 xalign 0.5 text_size 16

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- A-Forward Time -") style "TisaOTMolxm"
                            null height 8
                            bar value Preference("auto-forward time") align (0.5, 0.5)
                            if config.has_voice:
                                textbutton _("Wait for Voice") action Preference("wait for voice", "toggle") xsize 150 xalign 0.5 text_size 16

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            textbutton _("Begin Skipping") action Skip() xsize 150 text_size 16

                    # Right column...
                    frame:
                        align (0.5, 0.0)
                        background Frame (Transform("content/gfx/frame/ink_box.png", alpha=0.3), 10, 10)
                        xpadding 10
                        ypadding 10
                        has vbox spacing 5

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194

                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184

                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Mute -") style "TisaOTMolxm"
                            textbutton "Music" action Preference("music mute", "toggle") xsize 150 xalign 0.5 text_size 16
                            textbutton "Sound" action Preference("sound mute", "toggle") xsize 150 xalign 0.5 text_size 16

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Music Volume -") align (0.5, 0.0) style "TisaOTMolxm"
                            null height 8
                            bar value Preference("music volume") align (0.5, 0.5)

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Sound Volume -") style "TisaOTMolxm"
                            null height 8
                            bar value Preference("sound volume") align (0.5, 0.5)
                            if config.sample_sound:
                                textbutton _("Test"):
                                    action Play("sound", config.sample_sound)
                                    style "soundtest_button"
                        # frame:
                            # background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
                            # xsize 194
                            # ypadding 10
                            # style_group "smenu"
                            # has vbox align (0.5, 0.5)
                            # button:
                                # xsize 164
                                # yalign 0.5
                                # action Function(dev_mode_switch)
                                # text "Debug Mode" size 18 align (0.5, 0.5):
                                    # if config.developer:
                                        # color green
                                    # else:
                                        # color red


            elif s_menu == "Game":
                frame:
                    background Frame("content/gfx/frame/ink_box.png", 10, 10)
                    xysize (333, 130)
                    xpadding 10
                    align .5, .1
                    text (u"{=stats_text}{color=[goldenrod]}{size=15}%s" % tt.value) outlines [(1, "#3a3a3a", 0, 0)]
                grid 1 1:
                    align (0.5, 0.5)
                    spacing 7
                    # Left column...
                    frame:
                        align (0.5, 0.5)
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.3), 10, 10)
                        xpadding 10
                        ypadding 10
                        has vbox spacing 5
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Panic Screen -") style "TisaOTMolxm"
                            textbutton _("Enable") action SetField(persistent, "unsafe_mode", True) xsize 150 xalign 0.5 text_size 16 hovered tt.Action("If it's enabled, press Q to activate panic screen. It hides NSFW content and mutes all sounds. Press Q again to deactivate it.")
                            textbutton _("Disable") action SetField(persistent, "unsafe_mode", False) xsize 150 xalign 0.5 text_size 16 hovered tt.Action("If it's enabled, press Q to activate panic screen. It hides NSFW content and mutes all sounds. Press Q again to deactivate it.")

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Battle Results -") style "TisaOTMolxm"
                            textbutton _("Show") action SetField(persistent, "battle_results", True) xsize 150 xalign 0.5 text_size 16 hovered tt.Action("Enables/disables screen with gained experience and gold after combat.")
                            textbutton _("Don't") action SetField(persistent, "battle_results", False) xsize 150 xalign 0.5 text_size 16 hovered tt.Action("Enables/disables screen with gained experience and gold after combat.")

                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                                text _("- Autosave -") style "TisaOTMolxm"
                            textbutton _("Enable") action SetField(persistent, "auto_saves", True) xsize 150 xalign 0.5 text_size 16 hovered tt.Action("Creates autosave every time you leave the next day screen. Can be slow, disable if it bothers you.")
                            textbutton _("Disable") action SetField(persistent, "auto_saves", False) xsize 150 xalign 0.5 text_size 16 hovered tt.Action("Creates autosave every time you leave the next day screen. Can be slow, disable if it bothers you.")

            elif s_menu in ("Save", "Load"):
                vbox:
                    yfill True
                    xfill True
                    spacing 5
                    null height 5
                    hbox:
                        spacing 3
                        style_group "dropdown_gm2"
                        align (0.5, 0.5)
                        textbutton _("Previous") action FilePagePrevious(), With(dissolve) text_size 16
                        textbutton _("Auto") action FilePage("auto"), With(dissolve) text_size 16
                        textbutton _("Quick") action FilePage("quick"), With(dissolve) text_size 16
                        for i in range(1, 9):
                            textbutton str(i):
                                action FilePage(i), With(dissolve)
                        textbutton _("Next") action FilePageNext(), With(dissolve) text_size 16
                    $ columns = 2
                    $ rows = 3
                    grid columns rows:
                        transpose True
                        style_group "dropdown_gm2"
                        xfill True
                        yfill True
                        spacing -10
                        for i in range(1, columns * rows + 1):

                            $ file_name = FileSlotName(i, columns * rows)
                            $ file_time = FileTime(i, empty=_("Empty Slot"))
                            # $ file_time = "0"
                            $ json_info = FileJson(i, empty= _(""))
                            $ save_name = FileSaveName(i)

                            hbox:
                                align (0.5, 0.5)
                                if "portrait" in json_info:
                                    frame:
                                        background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                                        align (0.5, 0.5)
                                        add ProportionalScale(json_info["portrait"], 90, 90) align (0.5, 0.5)
                                else:
                                    frame:
                                        background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                                        align (0.5, 0.5)
                                        xysize (102, 102)
                                button:
                                    style "smenu2_button"
                                    align (0.5, 0.5)
                                    xysize (220, 100)
                                    if s_menu == "Save":
                                        action FileSave(i)
                                        text " - [file_name] -" align (1.0, 0) style "TisaOTMol" size 14 outlines [(3, "#3a3a3a", 0, 0), (2, "#458B00", 0, 0), (1, "#3a3a3a", 0, 0)]
                                        text "[file_time!t]\n[save_name!t]" style "TisaOTMol" size 12 align (1.05, 1.25)
                                    elif s_menu == "Load":
                                        action FileLoad(i)
                                        text " - [file_name] -" align (1.0, 0) style "TisaOTMol" size 14 outlines [(3, "#3a3a3a", 0, 0),(2, "#009ACD", 0, 0), (1, "#3a3a3a", 0, 0)]
                                        text "[file_time!t]\n[save_name!t]" style "TisaOTMol" size 12 align (1.05, 1.25)
                                    vbox:
                                        xpos 0
                                        yalign 0.5
                                        spacing -7
                                        if "name" in json_info:
                                            text "[json_info[name]]" style "TisaOTMol" color gold size 17
                                        if "level" in json_info:
                                            text "Level: [json_info[level]]" style "TisaOTMol" ypos 0
                                        if "chars" in json_info:
                                            text "Chars: [json_info[chars]]" style "TisaOTMol" ypos 0
                                        if "gold" in json_info:
                                            text "Gold: [json_info[gold]]" style "TisaOTMol" ypos 0
                                        if "buildings" in json_info:
                                            text "Buildings: [json_info[buildings]]" style "TisaOTMol" ypos 0

                                    key "save_delete" action FileDelete(i)
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
            align (0.765, 0.505)
            xysize (150, 409)
            style_group "smenu"
            xpadding 8
            has vbox spacing 5 align (0.5, 0.5)
            null height 3
            vbox:
                xfill True
                spacing -10
                align (0.5, 0.5)
                if s_menu == "Settings":
                    text "Settings" style "TisaOTMol" size 26 align (0.5, 0.5)
                if s_menu == "Game":
                    text "Game" style "TisaOTMol" size 26 align (0.5, 0.5)
                elif s_menu == "Save":
                    text "Save" style "TisaOTMol" size 26 align (0.5, 0.5)
                elif s_menu == "Load":
                    text "Load" style "TisaOTMol" size 26 align (0.5, 0.5)
            button:
                yalign 0.5
                action Hide("s_menu"), With(dissolve)
                text "Return" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action SelectedIf(s_menu == "Settings"), Hide("s_menu"), Show("s_menu", s_menu="Settings"), With(dissolve) # SetScreenVariable("s_menu", "Settings")
                text "Settings" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action SelectedIf(s_menu == "Game"), Hide("s_menu"), Show("s_menu", s_menu="Game"), With(dissolve)
                text "Game" size 18 align (0.5, 0.5)
            button:
                yalign 0.5
                action SensitiveIf(not main_menu), SelectedIf(s_menu == "Save"), Hide("s_menu"), Show("s_menu", s_menu="Save"), With(dissolve)#, SetScreenVariable("s_menu", "Save")
                text "Save" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action SelectedIf(s_menu == "Load"), Hide("s_menu"), Show("s_menu", s_menu="Load"), With(dissolve)#, SetScreenVariable("s_menu", "Load")
                text "Load" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action MainMenu()
                text "Main Menu" size 18 align (0.5, 0.5) #  style "mmenu_button_text"
            button:
                yalign 1.0
                action Quit()
                text "Quit" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            null height 3

screen keymap_override():
    on "show":
        action SetVariable("_skipping", False)
    on "hide":
        action SetVariable("_skipping", True)

    key "hide_windows" action NullAction()
    key "game_menu" action NullAction()
    key "help" action NullAction()
    key "rollback" action NullAction()
    key "rollforward" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "fast_skip" action NullAction()
    key "mouseup_3" action NullAction()

screen panic_screen:
    zorder 1000000000
    modal True
    add "content/gfx/bg/panic_screen.jpg" zoom 1.32
    default original_transitions_state = _preferences.transitions
    on "show":
        action [PauseAudio("events", True), PauseAudio("events2", True), PauseAudio("world", True), PauseAudio("gamemusic", True), PauseAudio("music", True), SetField(_preferences, "transitions", 0)]
    on "hide":
        action [SetField(config, "window_title", config.name), PauseAudio("events", False), PauseAudio("events2", False), PauseAudio("world", False), PauseAudio("gamemusic", False), PauseAudio("music", False), SetField(_preferences, "transitions", original_transitions_state), SetField(config, "window_icon", "content/gfx/interface/icons/win_icon.png"), renpy.game.interface.set_icon]
    use keymap_override
    key "q" action Hide("panic_screen")
    key "Q" action Hide("panic_screen")

screen give_exp_after_battle(group, exp = 0, money=0): # shows post-battle results; TODO after beta: make the animation to show exp gained post battle, not just the current one;
    modal True
    zorder 100
    frame:
        align (0.5, 0.5)
        background Frame("content/gfx/frame/post_battle.png", 75, 75)
        xpadding 75
        ypadding 75
        has vbox
        text ("You gained %d exp"%exp) size 20 align (0.5, 0.5) style "proper_stats_value_text" bold True outlines [(1, "#181818", 0, 0)] color "#DAA520"
        null height 15
        for l in group:
            $ char_profile_img = l.show('portrait', resize=(101, 101), cache=True)
            $ img = "content/gfx/frame/ink_box.png"
            hbox:
                imagebutton:
                    background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                    idle (char_profile_img)
                    hover (im.MatrixColor(char_profile_img, im.matrix.brightness(0.15)))
                    action None
                    align 0, .5
                    xysize (102, 102)
                null width 15
                text ("Level %d"%l.level) style "proper_stats_value_text" bold True outlines [(1, "#181818", 0, 0)] size 22 color "#DAA520" yalign 0.9
            bar:
                value AnimatedValue(value=l.stats.exp + l.stats.goal_increase - l.stats.goal, range=l.stats.goal_increase, delay=1.0, old_value=0)
                left_bar ("content/gfx/interface/bars/exp_full.png")
                right_bar ("content/gfx/interface/bars/exp_empty.png")
                thumb None
                maximum (324, 25)
            hbox:
                spacing 10
                pos (90, -23)
                xmaximum 160
                xfill True
                add "content/gfx/interface/images/exp_b.png" ypos 2 xalign 0.8
                text "[l.exp]/[l.goal]" style "proper_stats_value_text" bold True outlines [(1, "#181818", 0, 0)] color "#DAA520"
        if money > 0:
            hbox:
                xalign 0.5
                text ("You found %d"%money) size 20 align (0.5, 0.5) style "proper_stats_value_text" bold True outlines [(1, "#181818", 0, 0)] color "#DAA520"
                null width 5
                add "coin_top" align (0.5, 0.5)
        style_prefix "wood"
        null height 15
        button:
            xalign .5
            xysize (120, 40)
            yalign 0.5
            action [Hide("give_exp_after_battle")]
            text "OK" size 15
            
    key "K_ESCAPE" action [Hide("give_exp_after_battle")]
    key "K_RETURN" action [Hide("give_exp_after_battle")]