if goback.collidepoint(pos) and (speedscreen or pointscreen or game_over_speed or game_over_coin):
    sounds.goback.play()
    speedscreen = False
    pointscreen = False
    game_over_speed = False
    game_over_coin = False
    reset_variables()
    screen2 = True
    music.play("loadscreen")
if easy.collidepoint(pos):
    speed_easy_screen = speed_screen(sounds, music)
    points_easy_screen = points_screen(sounds, music)