label hero_profile:
    scene bg h_profile

    $ global_flags.set_flag("keep_playing_music")

    # $ pytfall.world_quests.run_quests("auto") Goes against squelching policy?
    $ pytfall.world_events.run_events("auto")
    $ renpy.retain_after_load()

    show screen hero_profile
    with dissolve

    $ hero.inventory.set_page_size(18)

    while 1:
        $ result = ui.interact()

        # To kill input error during team renaming:
        if not result:
            pass
        elif result[0] == "item":
            if result[1] == "transfer":
                hide screen hero_profile
                $ items_transfer([hero, hero.location])
                show screen hero_profile
        elif result[0] == 'control':
            if result[1] == 'return':
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False
                hide screen hero_profile

                # Reset filters (prevents crap from happening in shops):
                $ hero.inventory.male_filter = False
                $ hero.inventory.apply_filter('all')

                jump expression pytfall.hp.came_from
        elif result[0] == "dropdown":
            if result[1] == "loc":
                $ renpy.show_screen("set_location_dropdown", hero, pos=renpy.get_mouse_pos())
            elif result[1] == "home":
                $ renpy.show_screen("set_home_dropdown", hero, pos=renpy.get_mouse_pos())
        elif result[0] == 'hero':
            if result[1] == 'equip':
                $ came_to_equip_from = "hero_profile"
                $ eqtarget = hero
                jump char_equip
        elif result[0] == "remove_from_team":
            $ hero.team.remove(result[1])
        elif result[0] == "rename_team":
            if result[1] == "set_name":
                $ hero.team.name = renpy.call_screen("pyt_input", hero.team.name, "Enter Team Name", 20, (350, 200))

init:
    screen hero_profile():
        on "hide":
            action Hide("show_trait_info")

        default tt = Tooltip("")
        default lframe_display = "status"
        default rframe_display = "skills"

        key "mousedown_3" action Return(['control', 'return'])

        # HERO SPRITE ====================================>
        add Transform(hero.show("profile", resize=(550, 550)), alpha=.97) align .65, .9

        # BASE FRAME 2 "bottom layer" and portrait ====================================>
        add "content/gfx/frame/h_profile.png"
        add hero.show("everyday", resize=(100, 100)) pos (64, 8) # portrait should be between "Base Frame 2" and "Base Frame 1" :Gismo

        # BATTLE STATS ====================================>
        fixed:
            xysize (270, 270)
            pos (300, 413)
            add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                                  (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 112, 126, 148, blue), alpha=0.4) align (0.5, 0.5)
            add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                                  (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 65, 126, 148, blueviolet), alpha=0.3) align (0.5, 0.5)
            add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                                  (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 33, 126, 148, aquamarine), alpha=0.2) align (0.5, 0.5)
            add ProportionalScale("content/gfx/interface/images/pentagon1.png", 250, 250) align (0.01, 0.5)

        fixed:
            frame:
                pos (375, 402)
                background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                has hbox
                add ProportionalScale("content/gfx/interface/images/atk.png", 24, 24)
                text("{size=-5}{font=fonts/Rubius.ttf}{color=[red]}[hero.attack]|%d"%(hero.get_max("attack"))) outlines [(1, "#0d0d0d", 0, 0)]
            frame:
                pos (223, 483)
                background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                has hbox
                add ProportionalScale("content/gfx/interface/images/def.png", 24, 24)
                text("{size=-5}{font=fonts/Rubius.ttf}{color=#dc762c}[hero.defence]|%d"%(hero.get_max("defence"))) outlines [(1, "#0d0d0d", 0, 0)]
            frame:
                pos (255, 643)
                background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                has hbox
                add ProportionalScale("content/gfx/interface/images/agi.png", 24, 24)
                text("{size=-5}{font=fonts/Rubius.ttf}{color=#1E90FF} [hero.agility]|%d"%(hero.get_max("agility"))) outlines [(1, "#0d0d0d", 0, 0)]
            frame:
                pos (495, 643)
                background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                has hbox
                add ProportionalScale("content/gfx/interface/images/luck.png", 24, 24)
                text("{size=-5}{font=fonts/Rubius.ttf}{color=#00FA9A}[hero.luck]|%d"%(hero.get_max("luck"))) outlines [(1, "#0d0d0d", 0, 0)]
            frame:
                pos (526, 483)
                background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=0.9), 10, 10)
                has hbox
                add ProportionalScale("content/gfx/interface/images/mag.png", 24, 24)
                text("{size=-5}{font=fonts/Rubius.ttf}{color=#8470FF}[hero.magic]|%d"%(hero.get_max("magic"))) outlines [(1, "#0d0d0d", 0, 0)]

        # LEFT FRAME (Stats/Friends/Etc) ====================================>
        vbox:
            xsize 217
            pos (8, 110)

            # NAME^   LVL   (ok for 1m lvls) ====================================>
            text (u"[hero.name]") style "TisaOTMol" size 28  xalign 0.492 ypos 5
            hbox:
                spacing 1
                if (hero.level) < 10:
                    pos (89, 11)
                elif (hero.level) < 100:
                    pos (86, 11)
                elif (hero.level) < 10000:
                    pos (77, 11)
                else:
                    pos (73, 11)
                label "{color=#CDAD00}Lvl" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
                label "{color=#CDAD00}[hero.level]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
            hbox:
                pos (84, 21)
                label "{color=#CDAD00}Tier " text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
                label "{color=#CDAD00}[hero.tier]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]

            if lframe_display == "status":
                # STATS ====================================>
                null height 20
                $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation"]
                vbox:
                    style_group "proper_stats"
                    spacing 1
                    xsize 212
                    frame:
                        xysize (212, 27)
                        xalign 0.5
                        text "Health:" xalign 0.02 color "#CD4F39"
                        if hero.health <= hero.get_max("health")*0.3:
                            text (u"{color=[red]}%s/%s"%(hero.health, hero.get_max("health"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                        else:
                            text (u"{color=#F5F5DC}%s/%s"%(hero.health, hero.get_max("health"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                    frame:
                        xysize (212, 27)
                        xalign 0.5
                        text "MP:" xalign 0.02 color "#009ACD"
                        if hero.mp <= hero.get_max("mp")*0.3:
                            text (u"{color=[red]}%s/%s"%(hero.mp, hero.get_max("mp"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                        else:
                            text (u"{color=#F5F5DC}%s/%s"%(hero.mp, hero.get_max("mp"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                    frame:
                        xysize (212, 27)
                        xalign 0.5
                        text "{color=#43CD80}Vitality:" xalign (0.02)
                        if hero.vitality <= hero.get_max("vitality")*0.3:
                            text (u"{color=[red]}%s/%s"%(hero.vitality, hero.get_max("vitality"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                        else:
                            text (u"{color=#F5F5DC}%s/%s"%(hero.vitality, hero.get_max("vitality"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                    for stat in stats:
                        frame:
                            xysize (212, 27)
                            xalign 0.5
                            text '{}'.format(stat.capitalize()) xalign 0.02 color "#79CDCD"
                            text ('%d/%d'%(getattr(hero, stat), hero.get_max(stat))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4

                null height 5

                # LOCATION ====================================>
                button:
                    style_group "ddlist"
                    action Return(["dropdown", "loc"])
                    alternate Return(["dropdown", "home"])
                    text "{image=content/gfx/interface/icons/move15.png}Location:\n       [hero.location]":
                        if len(str(hero.location)) > 18:
                            size 15
                        else:
                            size 16
                    hovered tt.Action("Left click to change [hero.name]'s current location. Right click to select his home location to rest at night.")

                null height 3

                # ELEMENTAL ALIGNMENT ====================================>
                $ els = [Transform(e.icon, size=(90, 90)) for e in hero.elements]
                $ els_a = [Transform(im.MatrixColor(e.icon, im.matrix.brightness(0.10)), size=(90, 90)) for e in hero.elements]
                frame:
                    xalign 0.5
                    yfill True
                    background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                    xysize (100, 30)
                    text (u"{color=#CDAD00} Element") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.7)
                fixed:
                    xalign 0.5
                    xysize (100, 100)
                    frame:
                        xysize (100, 100)
                        background Frame (Transform("content/gfx/frame/frame_it1.png", alpha=0.6, size=(100, 100)), 10, 10)
                        $ x = 0
                        $ els = [Transform(i, crop=(90/len(els)*els.index(i), 0, 90/len(els), 90), subpixel=True, xpos=(x + 90/len(els)*els.index(i))) for i in els]
                        $ els_a = [Transform(i, crop=(90/len(els_a)*els_a.index(i), 0, 90/len(els_a), 90), subpixel=True, xpos=(x + 90/len(els_a)*els_a.index(i))) for i in els_a]
                        $ f = Fixed(*els, xysize=(90, 90))
                        $ f_a = Fixed(*els_a, xysize=(90, 90))
                    add ProportionalScale("content/gfx/interface/images/elements/hover.png", 98, 98) align (.5, .5)
                    button:
                        xysize (90, 90)
                        align (.5, .5)
                        if len(hero.elements) > 1:
                            $ ele = ""
                            for e in hero.elements:
                                $ ele += e.id + ", "
                            $ ele = ele[:-2]
                        else:
                            $ ele = hero.elements[0].id
                        action Show("show_trait_info", trait=hero, elemental_mode=True, place="hero_element")
                        background f
                        hover_background f_a
                        hovered tt.action("[ele]")

                    # viewport:
                        # draggable True
                        # edgescroll (15, 10)
                        # xysize (200, 110)
                        # align (0, 0.5)
                        # has vbox spacing -4
                        # for e in hero.elements:
                            # textbutton "{=TisaOTM}{size=14}[e.id]":
                                # background None
                                # action NullAction()
                                # hovered tt.Action("%s" % e.desc)
                    # add ProportionalScale("content/gfx/interface/images/elements/hover.png", 90, 90) pos (105, 10)
            elif lframe_display == "skills":
                null height 26
                viewport:
                    scrollbars "vertical"
                    xysize(200, 500)
                    mousewheel True
                    has vbox spacing 4 xfill True

                    for skill in hero.stats.skills:
                        $ skill_val = int(hero.get_skill(skill))
                        $ skill_limit = int(hero.get_max_skill(skill))
                        # We don't care about the skill if it's less than 10% of limit:
                        if skill_val/float(skill_limit) > .1:
                            hbox:
                                align .0, .9
                                xsize 180
                                text "{}:".format(skill.capitalize()) style_suffix "value_text" color gold xalign .0 size 12 yoffset 2
                                hbox:
                                    xalign 1.0
                                    $ step = skill_limit/10.0
                                    for i in range(5):
                                        if (2*step) <= skill_val:
                                            add Transform("content/gfx/interface/icons/stars/star2.png", size=(18, 18))
                                            $ skill_val -= 2*step
                                        elif step <= skill_val:
                                            add Transform("content/gfx/interface/icons/stars/star3.png", size=(18, 18))
                                            $ skill_val -= step
                                        else:
                                            add Transform("content/gfx/interface/icons/stars/star1.png", size=(18, 18))

            elif lframe_display == "friends":
                # FRIEND LIST ====================================>
                null height 26
                viewport:
                    xysize (200, 500)
                    scrollbars "vertical"
                    draggable True
                    mousewheel True
                    xalign 0.5
                    has vbox spacing 4 xfill True
                    $ temp = sorted(list(hero.friends | hero.lovers), key=attrgetter("name"))
                    $ temp = list(i for i in temp if i not in hero.chars)
                    for char in temp:
                        $ not_escaped = char not in pytfall.ra
                        frame:
                            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.6), 5, 5)
                            top_padding 10
                            bottom_padding 3
                            xpadding 5
                            xmargin 0
                            ymargin 0
                            xminimum 180
                            align (0.5, 0.5)
                            has vbox spacing 1 xalign 0.5
                            button:
                                ypadding 1
                                xpadding 1
                                xmargin 0
                                ymargin 0
                                align (0.5, 0.5)
                                style "basic_choice2_button"
                                add char.show("portrait", resize=(120, 120), cache=True) align (0.5, 0.5)
                                action [Hide("hero_profile"), With(dissolve), Function(friends_list_gms, char)]
                                hovered tt.Action("Click to meet [char.name] in the city")

                            text "{=TisaOTMolxm}[char.nickname]" align (0.5, 1.0) yoffset 5 xmaximum 190
                            if char in hero.lovers:
                                add ProportionalScale("content/gfx/interface/images/love.png", 35, 35) xalign 0.5
                            else:
                                add ProportionalScale("content/gfx/interface/images/friendship.png", 35, 35) xalign 0.5

        # BUTTONS on the "bottom layer" ------------------------------------>
        hbox:
            style_group "pb"
            spacing 1
            pos (1142, 156)
            button:
                action Hide("show_trait_info"), SetScreenVariable("rframe_display", "skills"), With(dissolve)
                text "Skills" style "pb_button_text"
            button:
                action SetScreenVariable("rframe_display", "traits"), With(dissolve)
                text "Traits" style "pb_button_text"

        # RIGHT FRAME ====================================>
        vbox:
            pos (1124, 60)
            xsize 153
            frame:
                xalign 0.5
                yfill True
                background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                xysize (153, 60)
                text (u"{color=#CDAD00} Day [day]") font "fonts/Rubius.ttf" size 26 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.6)
            null height 2
            frame:
                xalign 0.5
                xysize 142, 22
                style_prefix "proper_stats"
                text "Gold:" size 16  outlines [(1, "#3a3a3a", 0, 0)] color gold xalign .1
                text "[hero.gold]" size 14 outlines [(1, "#3a3a3a", 0, 0)] style_suffix "value_text" color gold xalign .9 yoffset 2

        # ATTACKS/MAGIC SKILLS ====================================>
        if rframe_display == "skills":
            vbox:
                pos (1125, 205)
                style_group "proper_stats"

                frame:
                    background Frame("content/gfx/frame/hp_1.png", 5, 5)
                    xysize (160, 192)
                    has vbox
                    label (u"Attack:") text_size 20 text_color ivory text_bold True xalign .45 text_outlines [(3, "#3a3a3a", 0, 0), (2, "#8B0000", 0, 0), (1, "#3a3a3a", 0, 0)]
                    viewport:
                        xysize (160, 155)
                        scrollbars "vertical"
                        draggable True
                        mousewheel True
                        has vbox spacing 1
                        for entry in hero.attack_skills:
                            frame:
                                xysize (147, 25)
                                button:
                                    background Null()
                                    xysize (147, 25)
                                    action NullAction()
                                    text "[entry.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(entry.name))))
                                    hovered tt.action(entry.desc)
                                    hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)

                frame:
                    background Frame("content/gfx/frame/hp_1.png", 5, 5)
                    xysize (160, 192)
                    has vbox
                    label (u"Magic:") text_size 20 text_color ivory text_bold True xalign .45 text_outlines [(3, "#3a3a3a", 0, 0), (2, "#104E8B", 0, 0), (1, "#3a3a3a", 0, 0)]
                    viewport:
                        xysize (160, 155)
                        scrollbars "vertical"
                        draggable True
                        mousewheel True
                        has vbox spacing 1
                        for entry in hero.magic_skills:
                            frame:
                                xysize (147, 25)
                                button:
                                    background Null()
                                    xysize (147, 25)
                                    action NullAction()
                                    text "[entry.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(entry.name))))
                                    hovered tt.action(entry.desc)
                                    hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)

        # TRAITS ====================================>
        elif rframe_display == "traits":
            frame:
                pos (1125, 205)
                background Frame("content/gfx/frame/hp_1long.png", 5, 5)
                xysize (160, 389)
                style_group "proper_stats"
                has vbox
                label (u"Traits:") text_size 20 text_color ivory text_bold True xalign .45
                viewport:
                    xysize (160, 150)
                    draggable True
                    mousewheel True
                    has vbox spacing 1
                    # for i in range(200):
                        # add Solid("#F00", xysize=(100, 20))
                    for trait in list(t for t in hero.traits if not any([t.personality, t.race, t.elemental])):
                        if not trait.hidden:
                            frame:
                                xsize 147
                                button:
                                    background Null()
                                    xsize 147
                                    action Show("show_trait_info", trait=trait.id, place="mc_trait")
                                    text trait.id idle_color ivory size 15 align .5, .5 hover_color crimson text_align .5
                                    hovered tt.Action(u"%s"%trait.desc)
                                    hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)

                null height 10

                label (u"Effects:") text_size 20 text_color ivory text_bold True xalign .45
                viewport:
                    xysize (160, 150)
                    draggable True
                    mousewheel True
                    has vbox spacing 1
                    for effect, val in hero.effects.iteritems():
                        if val['active']:
                            frame:
                                xysize (147, 25)
                                button:
                                    background Null()
                                    xysize (147, 25)
                                    action NullAction()
                                    text "[effect]" idle_color ivory size 15 align .5, .5 hover_color crimson
                                    hovered tt.Action(u"%s"%val.get("desc", "No Description availible."))
                                    hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)

        # TOOLTIP TEXT ====================================>
        hbox:
            spacing 1
            pos (621, 602)
            xysize (657, 114)
            yfill True
            if isinstance(tt.value, BE_Action):
                $ element = tt.value.get_element()
                if element:
                    fixed:
                        xysize (100, 100)
                        yalign 0.5
                        if element.icon:
                            $ img = ProportionalScale(element.icon, 90, 90)
                            add img align (0.5, 0.5)
                text tt.value.desc style "content_text" size 18 color "#ecc88a" yalign 0.1
            else:
                text (u"{=content_text}{color=#ecc88a}%s" % tt.value) size 18

        # BASE FRAME 1 "top layer" ====================================>
        add "content/gfx/frame/h_profile2.png"

        # BUTTONS and UI elements on the "top layer" ====================================>
        hbox:
            style_group "pb"
            spacing 2
            pos (472, 9)
            button:
                action SetScreenVariable("lframe_display", "status"), With(dissolve)
                text "Stats" style "pb_button_text"
                hovered tt.Action("Show Hero Stats")
            button:
                action SetScreenVariable("lframe_display", "skills"), With(dissolve)
                text "Skills" style "pb_button_text"
                hovered tt.Action("Show Hero Skills")
            button:
                action Hide("show_trait_info"), Show("hero_team", transition=dissolve)#, With(dissolve)
                text "Team" style "pb_button_text"
                hovered tt.Action("Show [hero.team.name]")#, With(dissolve)
            button:
                action Hide("show_trait_info"), Return(['hero', 'equip'])#, With(dissolve)
                text "Equipment" style "pb_button_text"
                hovered tt.Action("Take a look at your inventory")
            button:
                action Hide("show_trait_info"), Show("finances", None, hero, mode="main")#, With(dissolve)
                text "Finance" style "pb_button_text"
                hovered tt.Action("Show finances log")
            button:
                action Hide("show_trait_info"), [SetScreenVariable("lframe_display", "friends"), With(dissolve)]
                text "Friends" style "pb_button_text"
                hovered tt.Action("Show the list friends and lovers who don't work for [hero.name], allowing to find them immediately when needed")
            # Items Transfer to Home Location Inventory:
            if hasattr(hero.location, "inventory"):
                button:
                    action Return(["item", "transfer"])
                    text "Storage" style "pb_button_text"
                    hovered tt.Action("Open the location storage to leave or take items")

        # AP ====================================>
        frame:
            xalign .45
            ypos 50
            background ProportionalScale("content/gfx/frame/frame_ap2.png", 190, 80)
            label "[hero.AP]":
                pos (130, -2)
                style "content_label"
                text_color ivory
                text_size 22

        imagebutton:
            pos (900, 7) # (178, 70)
            idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
            hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
            action Hide("show_trait_info"), Return(['control', 'return'])
            hovered tt.Action("Return to previous screen!")

        # EXP BAR ====================================>
        fixed:
            pos (259, 697)
            bar:
                value hero.stats.exp + hero.stats.goal_increase - hero.stats.goal
                range hero.stats.goal_increase
                left_bar ("content/gfx/interface/bars/exp_full.png")
                right_bar ("content/gfx/interface/bars/exp_empty.png")
                thumb None
                maximum (324, 18)
            hbox:
                spacing 10
                pos (90, -17)
                xmaximum 160
                xfill True
                add "content/gfx/interface/images/exp_b.png" ypos 2 xalign 0.8
                text "[hero.exp]/[hero.goal]" style "proper_stats_value_text" bold True outlines [(1, "#181818", 0, 0)] color "#DAA520"

    screen hero_team():
        zorder 1
        modal True

        key "mousedown_3" action Hide("hero_team"), With(dissolve)

        default tt = Tooltip("")
        add Transform("content/gfx/images/bg_gradient2.png", alpha=0.3)

        # Hero team ====================================>
        frame:
            style_prefix "proper_stats"
            align .54, .4
            background Frame(Transform(im.Twocolor("content/gfx/frame/ink_box.png", white, black), alpha=0.7), 5, 5)
            padding 10, 5
            has vbox spacing 10

            hbox:
                spacing 2
                xalign .5
                label "[hero.team.name]" text_color "#CDAD00" text_size 30
                imagebutton:
                    idle im.Scale("content/gfx/interface/buttons/edit.png", 24, 30)
                    hover im.Scale("content/gfx/interface/buttons/edit_h.png", 24, 30)
                    action Return(["rename_team", "set_name"]), With(dissolve)
                    hovered tt.Action("Rename the team")

            for member in hero.team:
                $ img = member.show("portrait", resize=(120, 120), cache=True)
                hbox:
                    spacing 7
                    # Portrait/Button:
                    fixed:
                        align .5, .5
                        xysize 120, 120
                        imagebutton:
                            padding 1, 1
                            align .5, .5
                            style "basic_choice2_button"
                            idle img
                            hover img
                            selected_idle Transform(img, alpha=1.05)
                            action None

                        python:
                            if member.front_row:
                                img = ProportionalScale("content/gfx/interface/buttons/row_switch.png", 40, 20)
                            else:
                                img = im.Flip(ProportionalScale("content/gfx/interface/buttons/row_switch.png", 40, 20), horizontal=True)

                        imagebutton:
                            align (0, 1.0)
                            idle Transform(img, alpha=0.9)
                            hover Transform(img, alpha=1.05)
                            insensitive im.Sepia(img)
                            action If(hasattr(member, "front_row"), true=[ToggleField(member, "front_row"), tt.Action("Row has been changed!")])
                            if member.front_row:
                                hovered tt.Action("Toggle between rows in battle, currently selected front row")
                            else:
                                hovered tt.Action("Toggle between rows in battle, currently selected back row")

                    # Name/Status:
                    frame:
                        xsize 162
                        padding 10, 5
                        background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 5, 5)
                        has vbox spacing 4 xfill True
                        fixed:
                            xysize 158, 25
                            xalign .5
                            text "{=TisaOTMolxm}[member.name]" xalign .06
                            if not member == hero:
                                imagebutton:
                                    xalign .92
                                    idle ProportionalScale("content/gfx/interface/buttons/close4.png", 24, 30)
                                    hover ProportionalScale("content/gfx/interface/buttons/close4_h.png", 24, 30)
                                    action Return(["remove_from_team", member])
                                    hovered tt.Action("Remove %s from %s"%(member.nickname, hero.team.name))

                        # HP:
                        fixed:
                            ysize 25
                            bar:
                                left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                                right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                value member.health
                                range member.get_max("health")
                                thumb None
                                xysize (150, 20)
                            text "HP" size 14 color "#F5F5DC" bold True xpos 8
                            $ tmb = red if member.health <= member.get_max("health")*0.3 else "#F5F5DC"
                            text "[member.health]" size 14 color tmb bold True style_suffix "value_text" xpos 125 yoffset -8

                        # MP:
                        fixed:
                            ysize 25
                            bar:
                                left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                                right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                value member.mp
                                range member.get_max("mp")
                                thumb None
                                xysize (150, 20)
                            text "{color=#F5F5DC}MP" size 14 bold True xpos 8
                            $ tmb = red if member.mp <= member.get_max("mp")*0.3 else "#F5F5DC"
                            text "[member.mp]" size 14 color tmb bold True style_suffix "value_text" xpos 125 yoffset -8

                        # VP
                        fixed:
                            ysize 25
                            bar:
                                left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                                right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                value member.vitality
                                range member.get_max("vitality")
                                thumb None
                                xysize (150, 20)
                            text "{color=#F5F5DC}VP" size 14 bold True xpos 8
                            $ tmb = red if member.vitality <= member.get_max("vitality")*0.3 else "#F5F5DC"
                            text "[member.vitality]" size 14 color tmb bold True style_suffix "value_text" xpos 125 yoffset -8

            button:
                style_group "pb"
                xalign 0.5
                xsize 120
                action Hide("hero_team"), With(dissolve)
                text "Close" style "pb_button_text"
                hovered tt.Action("Close team screen")
        hbox:
            spacing 1
            pos (621, 602)
            xysize (657, 114)
            yfill True
            text (u"{=content_text}{color=#ecc88a}%s" % tt.value) size 18

    screen hero_finances():
        modal True
        zorder 1

        key "mousedown_3" action Hide("hero_finances"), With(dissolve)

        add Transform("content/gfx/images/bg_gradient2.png", alpha=0.3)
        frame:
            background Frame (Transform("content/gfx/frame/ink_box.png", alpha=0.65), 10, 10)
            style_group "content"
            align (0.5, 0.5)
            xysize (1120, 600)
            # side "c r":
                # area (20, 43, 1110, 495)
            viewport id "herofin_vp":
                style_group "stats"
                draggable True
                mousewheel True
                if day > 1:
                    $ fin_inc = hero.fin.game_main_income_log[day-1]
                    $ fin_exp = hero.fin.game_main_expense_log[day-1]

                    if pytfall.hp.finance_filter == 'day':
                        label (u"Fin Report (Yesterday)") xalign 0.4 ypos 30 text_size 30
                        # Income:
                        vbox:
                            pos (50, 100)
                            label "Income:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True
                                    for key in fin_inc:
                                        text "[key]"
                                vbox:
                                    null height 1
                                    spacing 4
                                    for key in fin_inc:
                                        $ val = fin_inc[key]
                                        text "[val]" style_suffix "value_text"

                        # Expense:
                        vbox:
                            pos (450, 100)
                            label "Expense:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True
                                    for key in fin_exp:
                                        text ("[key]")
                                vbox:
                                    null height 1
                                    spacing 4
                                    for key in fin_exp:
                                        $ val = fin_exp[key]
                                        text ("[val]") style_suffix "value_text"

                        python:
                            total_income = 0
                            total_expenses = 0
                            for key in fin_inc:
                                total_income += fin_inc[key]
                            for key in fin_exp:
                                total_expenses += fin_exp[key]
                            total = total_income - total_expenses

                        vbox:
                            align (0.80, 0.60)
                            text "----------------------------------------"
                            text ("Revenue: [total]"):
                                size 20
                                xpos 15
                                if total > 0:
                                    color lawngreen style_suffix "value_text"
                                else:
                                    color red style_suffix "value_text"

                        hbox:
                            style_group "basic"
                            align (0.5, 0.9)
                            textbutton "Show Total" action SetField(pytfall.hp, "finance_filter", "total")

                    elif pytfall.hp.finance_filter == 'total':
                        label (u"Fin Report (Game)") xalign 0.4 ypos 30 text_size 30
                        python:
                            income = dict()
                            for d in hero.fin.game_main_income_log:
                                for key, value in hero.fin.game_main_income_log[d].iteritems():
                                    income[key] = income.get(key, 0) + value
                        # Income:
                        vbox:
                            pos (50, 100)
                            label "Income:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True
                                    for key in income:
                                        text ("[key]")
                                vbox:
                                    null height 1
                                    spacing 4
                                    for key in income:
                                        $ val = income[key]
                                        text ("[val]") style_suffix "value_text"

                        python:
                            expenses = dict()
                            for d in hero.fin.game_main_expense_log:
                                for key, value in hero.fin.game_main_expense_log[d].iteritems():
                                    expenses[key] = expenses.get(key, 0) + value
                        # Expense:
                        vbox:
                            pos (450, 100)
                            label "Expense:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True
                                    for key in expenses:
                                        text ("[key]")
                                vbox:
                                    null height 1
                                    spacing 4
                                    for key in expenses:
                                        $ val = expenses[key]
                                        text ("[val]") style_suffix "value_text"

                        python:
                            game_total = 0
                            total_income = sum(income.values())
                            total_expenses = sum(expenses.values())
                            game_total = total_income - total_expenses

                        vbox:
                            align (0.80, 0.60)
                            text "----------------------------------------"
                            text ("Revenue: [game_total]"):
                                size 20
                                xpos 15
                                if game_total > 0:
                                    color lawngreen style_suffix "value_text"
                                else:
                                    color red style_suffix "value_text"

                        hbox:
                            style_group "basic"
                            align (0.5, 0.9)
                            textbutton "{size=-3}Show Daily" action SetField(pytfall.hp, "finance_filter", "day")

                    hbox:
                        pos (750, 100)
                        vbox:
                            xmaximum 140
                            xfill True
                            if hero.fin.property_tax_debt:
                                text ("Property:\n(Tax Debt") color red size 20 outlines [(2, "#424242", 0, 0)]
                            if hero.fin.income_tax_debt:
                                text ("Income:\n(Tax Debt)") color crimson size 20 outlines [(2, "#424242", 0, 0)]
                            if day != 1:
                                text "Taxes:\n(This week)" size 20 outlines [(2, "#424242", 0, 0)]
                        vbox:
                            if hero.fin.property_tax_debt:
                                null height 4
                                spacing 4
                                text ("[hero.fin.property_tax_debt]\n ") color red style_suffix "value_text"
                            if hero.fin.income_tax_debt:
                                null height 4
                                spacing 4
                                text ("[hero.fin.income_tax_debt]\n ") color crimson style_suffix "value_text"
                            if day != 1:
                                python:
                                    days = calendar.days.index(calendar.weekday())
                                    taxes = hero.fin.get_total_taxes(days)
                                null height 4
                                spacing 4
                                text ("[taxes]\n ") style_suffix "value_text"

                # vbar value YScrollValue("herofin_vp")
            button:
                style_group "basic"
                action Hide('hero_finances')
                minimum (250, 30)
                align (0.5, 0.96)
                text "OK"
