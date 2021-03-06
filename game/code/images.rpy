# ANIMATION
init:
    image no_image = "content/gfx/interface/images/no_image.png"

    image bg_main = "content/gfx/bg/main.jpg"

    image eyes:
        zoom 0.7
        additive 1.0
        alpha 0.7
        "content/gfx/animations/main_menu/eyes/eyes1.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes2.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes3.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes4.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes5.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes6.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes7.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes8.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes9.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes10.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes11.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes12.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes13.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes14.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes15.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes16.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes17.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes18.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes19.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes20.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes21.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes22.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes23.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes24.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes25.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes26.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes27.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes28.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes29.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes30.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes31.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes32.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes33.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes34.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes35.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes36.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes37.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes38.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes39.png"
        pause 0.4
        "content/gfx/animations/main_menu/eyes/eyes40.png"
        pause 0.4
        repeat

    image logo:
        subpixel True
        additive 0.1
        alpha 0.95
        "content/gfx/animations/main_menu/logo/logo1.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo2.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo3.png"
        pause 0.4
        "content/gfx/animations/main_menu/logo/logo2.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo1.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo5.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo6.png"
        pause 0.4
        "content/gfx/animations/main_menu/logo/logo5.png"
        pause 0.3
        repeat

    image fog:
        "content/gfx/animations/main_menu/fog1.png"
        pos (15, 20)

    image mm_fire = "content/gfx/animations/main_menu/fire1.png"

    image mm_clouds = "content/gfx/animations/main_menu/cloud1.png"
    image mm_cloudstest = im.Scale("content/gfx/animations/main_menu/cloud1.png", 287, 263)

    image save:
        zoom 0.4
        additive 1.0
        alpha 0.7
        "content/gfx/animations/main_menu/settings/save1.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save2.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save3.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save4.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save5.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save6.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save7.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save8.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save9.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save10.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save11.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save12.png"
        pause 0.2
        repeat

    image slo:
        zoom 0.9
        additive 1.0
        #alpha 0.7
        "content/gfx/animations/main_menu/settings/slo1.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo2.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo3.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo4.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo5.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo6.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo7.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo8.png"
        pause 0.2
        repeat

    # Interactions module:
    # Portrait overlays (for enhancing emotions):
    image angry_pulse = "content/gfx/animations/interactions/angry.png"
    image sweat_drop = "content/gfx/animations/interactions/uncertain.png"
    image scared_lines = "content/gfx/animations/interactions/scared.png"
    image question_mark = "content/gfx/animations/interactions/puzzled.png"
    image exclamation_mark = "content/gfx/animations/interactions/exclamation.png"
    image music_note = "content/gfx/animations/interactions/note.png"
    image shy_blush = "content/gfx/animations/interactions/blush.png"
    image hearts_rise = FilmStrip('content/gfx/animations/interactions/hearts.png', (168, 157), (10, 3), 0.07, loop=True)

    image hearts_flow:
        subpixel True
        anchor (.5, 1.0)
        alpha .8
        additive .9
        "content/gfx/animations/interactions/hearts/heart1.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart2.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart3.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart4.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart5.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart6.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart7.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart8.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart9.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart10.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart11.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart12.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart13.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart14.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart15.png"
        pause 0.07
        repeat

    image fire_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_fire.png", 15, 15)
    image water_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_water.png", 15, 15)
    image earth_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_earth.png", 15, 15)
    image darkness_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_darkness.png", 15, 15)
    image ice_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_ice.png", 15, 15)
    image air_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_air.png", 15, 15)
    image ele_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_electricity.png", 15, 15)
    image light_element_be_viewport = ProportionalScale("content/gfx/interface/images/elements/small_light.png", 15, 15)
    image healing_be_viewport = ProportionalScale("content/gfx/interface/images/elements/healing.png", 13, 13)
    image poison_be_viewport = ProportionalScale("content/gfx/interface/images/elements/poison.png", 15, 15)
    image physical_be_viewport = ProportionalScale("content/gfx/interface/images/elements/physical.png", 15, 15)

    image fire_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_fire.png", 20, 20)
    image water_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_water.png", 20, 20)
    image earth_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_earth.png", 20, 20)
    image darkness_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_darkness.png", 20, 20)
    image ice_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_ice.png", 20, 20)
    image air_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_air.png", 20, 20)
    image ele_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_electricity.png", 20, 20)
    image light_element_be_size20 = ProportionalScale("content/gfx/interface/images/elements/small_light.png", 20, 20)
    image healing_be_size20 = ProportionalScale("content/gfx/interface/images/elements/healing.png", 18, 18)
    image poison_be_size20 = ProportionalScale("content/gfx/interface/images/elements/poison.png", 20, 20)
    image physical_be_size20 = ProportionalScale("content/gfx/interface/images/elements/physical.png", 20, 20)
