init python:
    if config.debug:
        register_event("angelica_meet", locations=["mages_tower"], priority=1000, start_day=1, jump=True, dice=100, max_runs=1)
    else:
        register_event("angelica_meet", locations=["mages_tower"], simple_conditions=["global_flags.flag('mt_counter') > 3"], priority=100, start_day=1, jump=True, dice=80, max_runs=1)

label angelica_meet:
    $ a = npcs["Angelica_mage_tower"].say

    hide screen mages_tower
    show expression npcs["Angelica_mage_tower"].get_vnsprite() as angelica
    with dissolve

    if not global_flags.flag("met_angelica"):
        $ global_flags.set_flag("met_angelica")

        a "Hi! I am Angelica!"
        a "I noticed you've been hanging around the Tower."
        menu:
            a "Are you interested in magic?"
            "Yes":
                a "Great! You cannot join us in the tower at the moment, but there are things I can help you with!"
                a "I for once am one of the very few people in this part of the world who can unlock add and remove elemental alignments from a person."
                a "It is not an easy task so don't think that you will be able to get away with being a cheapskate!"
                a "It takes a lot out of me, so I expect to be very well compensated. If you believe that you can find a better deal elsewhere... I do dare you to try."
                $ global_flags.set_flag("angelica_free_alignment")
                a "You look like you have some potential... so I'll give you one freebie. "
                extend "Do not expect that to happen again!"
                a "I charge 10 000 Gold for the first element if you do not have any alignment at all and 10 000 and 5 000 more for every one that you already have!"
                a "If you want to lose one, it is a lot trickier... elements are not shoes you can put on and off. That will cost you 50 000 per elements."
                a "And feel free to bring your teammates, I can do it for pretty much anyone."

                a "I can also teach you basics of {color=[lightyellow]}Light{/color} and {color=[darkviolet]}Darkness{/color} magic."
            "Not really":
                a "Oh? Well, never mind then..."
                a "I'll be around if you change your mind."
                jump mages_tower
    a "How can I be of assistance?"

label angelica_menu:
    show screen angelica_menu
    with dissolve
    while 1:
        $ result = ui.interact()

label angelica_spells:
    a "Magic is knowledge and knowledge is power!"
    python:
        angelica_shop = ItemShop("Angelica Shop", 18, ["Angelica Shop"], gold=5000, sells=["scroll"], sell_margin=1, buy_margin=5.0)
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.angelica_shop
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)

    with dissolve
    call shop_control

    $ global_flags.del_flag("keep_playing_music")
    hide screen shopping
    with dissolve
    a "Use your magic responsibly."
    jump angelica_menu

label angelica_add_alignment:
    a "Let's take a look."
    if len(hero.team) > 1:
        a "Who is it going to be?"
        call screen character_pick_screen
        $ character = _return
    else:
        $ character = hero
    if not character:
        a "Ok then."
        jump angelica_menu

    $ elements = list(el for el in traits.values() if el.elemental and el != traits["Neutral"] and el not in character.traits)
    if len(elements) <= 0:
        a "Oh. It looks like you already have them all. It's not wise. Maybe you should remove a few?"
    else:
        call screen alignment_choice(character)
        $ alignment = _return

        if alignment:
            if "Neutral" in character.traits:
                $ price = 10000
            else:
                $ price = 10000 + len([e for e in character.traits if e.elemental])*5000
            if global_flags.flag("angelica_free_alignment") or hero.take_money(price, reason="Element Purchase"):
                a "There! All done!"
                a "Don't let these new powers go into your head and use them responsibly!"
                python:
                    global_flags.del_flag("angelica_free_alignment")
                    character.apply_trait(alignment)
            else:
                a "You don't have enough money. It will be [price] gold."
    jump angelica_menu

label angelica_remove_alignment:
    a "Let's take a look."
    if len(hero.team) > 1:
        call screen character_pick_screen
        $ character = _return
    else:
        $ character = hero
    if not character:
        a "Ok then."
        jump angelica_menu

    if not "Neutral" in character.traits:
        call screen alignment_removal_choice(character)
        $ alignment = _return
        if alignment:
            if alignment == "clear_all":
                $ price = 50000 * len(list(el for el in character.traits if el.elemental))
                if hero.take_money(price, reason="Element Purchase"):
                    a "There! All elements were removed."
                    python:
                        for el in list(el for el in character.traits if el.elemental):
                            character.remove_trait(el)
                else:
                    a "You don't have enough money. It will be [price] gold."
            else:
                $ price = 50000
                if hero.take_money(price, reason="Element Purchase"):
                    a "There! I removed it."
                    $ character.remove_trait(alignment)
                else:
                    a "You don't have enough money. It will be [price] gold."
    else:
        a "I can't remove an element if you don't have any."
    jump angelica_menu

screen alignment_choice(character):
    default tt = Tooltip("Cancel")
    key "mousedown_3" action Return("")

    vbox:
        style_group "wood"
        xalign .5
        button:
            xysize (250, 40)
            yalign 0.5
            action Return("")
            text "[tt.value]" size 15

    python:
        elements = list(el for el in traits.values() if el.elemental and el != traits["Neutral"] and el not in character.traits)
        step = 360 / len(elements)
        var = 0

    for el in elements:
        python:
            img = ProportionalScale(el.icon, 120, 120)
            angle = var
            var = var + step
        imagebutton at circle_around(t=10, angle=angle, radius=250):
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(0.25))
            action Return(el)
            hovered tt.Action("Add "+el.id)

screen alignment_removal_choice(character):
    default tt = Tooltip("Cancel")
    key "mousedown_3" action Return("")

    vbox:
        style_group "wood"
        xalign .5
        button:
            xysize (250, 40)
            yalign 0.5
            action Return("")
            text "[tt.value]" size 15

    python:
        elements = list(el for el in character.traits if el.elemental)
        step = 360 / len(elements)
        var = 0

    for el in elements:
        python:
            img = ProportionalScale(el.icon, 120, 120)
            angle = var
            var = var + step
        imagebutton at circle_around(t=10, angle=angle, radius=250):
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(0.25))
            action Return(el)
            hovered tt.Action("Remove " + el.id)

    $ img = ProportionalScale(traits["Neutral"].icon, 120, 120)
    imagebutton:
        align (.5, .5)
        idle img
        hover Transform(im.MatrixColor(img, im.matrix.brightness(0.25)), zoom=1.2)
        action Return("clear_all")
        hovered tt.Action("Remove all elements")

screen angelica_menu:
    frame:
        xalign 0.95
        ypos 20
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (200, 40)
                yalign 0.5
                action [Hide("angelica_menu"), Jump("angelica_spells")]
                text "Spells" size 15
            button:
                xysize (200, 40)
                yalign 0.5
                action [Hide("angelica_menu"), Jump("angelica_add_alignment")]
                text "Add Alignment" size 15
            button:
                xysize (200, 40)
                yalign 0.5
                action [Hide("angelica_menu"), Jump("angelica_remove_alignment")]
                text "Remove Alignment" size 15
            button:
                xysize (200, 40)
                yalign 0.5
                action [Hide("angelica_menu"), Jump("mages_tower")]
                text "Leave" size 15
