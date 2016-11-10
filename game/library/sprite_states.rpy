init -8 python:
    # collect positions and transitions DON'T EDIT BY HAND (unless you know the result is still parseable)
    # deep nested composition strings are converted to respective indices during initialization
    #body.modus['state']['defaultr'] = {'right/body/chest/neck': 'shirt_g_tie', 'head/right': 'default', 'right/body/shirts': 'vest_g_lvl4', 'head/right/face/eyes': 'default', 'right/leftarm': 'dl', 'right/body': 'h', 'head/right/hair/right': 'brown', 'right/leftleg': 'l', 'right/rightarm': 'hand1dr', 'right/body/skirts': 'high_long', 'head/right/face/mouth': 'default', 'right/body/chest': 'pressed', 'head/right/hair': 'brown', 'right/rightleg': 'r', 'right/body/chest/bras': 'white', 'right/body/pubis': 'x0'}
    body.modus['state']['default'] = {'body/chest/neck': 'shirt_g_tie', 'head': 'default', 'body/shirts': 'vest_g_lvl4', 'head/face/eyes': 'default', 'leftarm': 'dl', 'body': 'h', 'head/hair/right': 'brown', 'leftleg': 'l', 'rightarm': 'hand1dr', 'body/skirts': 'high_long', 'head/face/mouth': 'default', 'body/chest': 'pressed', 'head/hair': 'brown', 'rightleg': 'r', 'body/chest/bras': 'white', 'body/pubis': 'x0'}
    body.modus['transition']['low_right_arm_to_hair'] = Transition(bp = 'rightarm', item = [['upper/rbd', 100], ['hand1dr', 100], ['rsd2', 100], ['rstr', 100], ['rup', 100], ['rus', 100], ['rub', 100]])
    body.modus['transition']['blink'] = Transition(bp = 'head/face/eyes', item = [['glance', 10], ['shut_closed', [20, 90]], ['glance', 10], ['soft', [500,5000]]])
    body.modus['transition']['mouth'] = Transition(bp = 'head/face/mouth', item = [['default', [40, 200]], ['soft', [40, 100]]])
    body.modus['transition']['leftleg'] = Transition(bp = 'leftleg', item = [['l3', 100], ['l2', 100], ['lb', 100], ['l', 100]])
    body.modus['transition']['rightleg'] = Transition(bp = 'rightleg', item = [['rf', 100], ['r', 100], ['rb', 100], ['rm', 100]])
    body.modus['transition']['rightarm'] = Transition(bp = 'rightarm', item = [[('upper/rb',), [100, 300]], ['hand1dr', [100, 300]]])
    body.modus['transition']['leftarm'] = Transition(bp = 'leftarm', item = [['dl', [180, 220]], ['ld1', [100, 300]]])
    body.modus['transition']['40_left'] = Transition(item = [[[-10, 0], 80], [[-5, 2], [10, 30]], [[-10, 0], [10, 30]], [[-5, -2], [10, 30]]])
    body.modus['transition']['40_right'] = Transition(item = [[[20, 0], 80], [[5, 2], [10, 30]], [[10, 0], [10, 30]], [[5, -2], [10, 30]]])
    body.modus['activity']['walk_left'] = {'state': 'default', 'transition': {'leftleg': 0, 'rightleg': 20, 'rightarm': 0, 'leftarm': 20, 'blink': [0, 40], '40_left': 0}}
    body.modus['activity']['dance'] = {'state': 'default', 'transition': {'leftleg': 0, 'rightleg': 100, 'rightarm': 0, 'leftarm': 100, 'blink': [0, 20], '40_left': 0, '40_right': 0}}

