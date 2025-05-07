import time
from pgzero import clock
from game.constants import GameState
from game.gameplay.presets import (init_actors_from_preset, reset_actors_from_preset, handle_collisions_from_preset, handle_movement_from_preset)


def speedrun_level_easy(context):
    if context.clock.action == 0:
        init_actors_from_preset(context, 'speedrun_easy')
        context.clock.countup()
        context.audio.enable_music_restore()
        reset_actors_from_preset(context, 'speedrun_easy')

    context.clock.action = 1
    context.clock.show_count = True
    ts = time.time()

    if context.screens['game'].transition_manager.powerup_message_active:
        return context.current_screen

    if context.clock.count >= context.clock.count_max:
        context.current_screen = GameState.GAMEOVER_SPEED
        context.audio.disable_music_restore()
        context.clock.level_elapsed_time = context.clock.get_elapsed_time()
    if not context.animation.not_hit: clock.schedule(context.animation.stop_swimmer_hit_animation, 3)

    handle_collisions_from_preset(context, 'speedrun_easy', ts)
    handle_movement_from_preset(context, 'speedrun_easy')

    #Actors animation
    context.animation.moving_update_animations()
    return context.current_screen

def points_level_easy(context):
    if context.clock.action == 0:
        init_actors_from_preset(context, 'points_easy')
        context.clock.countdown()
        reset_actors_from_preset(context, 'points_easy')

    context.clock.action = 1
    context.clock.show_count = True
    ts = time.time()

    if context.screens['game'].transition_manager.powerup_message_active:
        return context.current_screen

    if context.clock.count_down_max == 0: context.current_screen = GameState.GAMEOVER_POINTS
    if not context.animation.not_hit: clock.schedule(context.animation.stop_swimmer_hit_animation, 3)

    handle_collisions_from_preset(context, 'points_easy', ts)
    handle_movement_from_preset(context, 'points_easy')

    #Actors animation
    context.animation.moving_update_animations()
    return context.current_screen

def speedrun_level_medium(context, dt):
    if context.clock.action == 0:
        init_actors_from_preset(context, 'speedrun_medium')
        context.clock.countup()
        context.audio.enable_music_restore()
        reset_actors_from_preset(context, 'speedrun_medium')

    context.clock.action = 1
    context.clock.show_count = True
    ts = time.time()

    if context.screens['game'].transition_manager.powerup_message_active:
        return context.current_screen

    if context.clock.count >= context.clock.count_max:
        context.current_screen = GameState.GAMEOVER_SPEED
        context.audio.disable_music_restore()
        context.clock.level_elapsed_time = context.clock.get_elapsed_time()
    if not context.animation.not_hit: clock.schedule(context.animation.stop_swimmer_hit_animation, 3)

    handle_collisions_from_preset(context, 'speedrun_medium', ts)
    handle_movement_from_preset(context, 'speedrun_medium', dt)

    # Actors animation
    context.animation.moving_update_animations()
    return context.current_screen

def points_level_medium(context, dt):
    if context.clock.action == 0:
        init_actors_from_preset(context, 'points_medium')
        context.clock.countdown()
        reset_actors_from_preset(context, 'points_medium')

    context.clock.action = 1
    context.clock.show_count = True
    ts = time.time()

    if context.screens['game'].transition_manager.powerup_message_active:
        return context.current_screen

    if context.clock.count_down_max == 0: context.current_screen = GameState.GAMEOVER_POINTS
    if not context.animation.not_hit: clock.schedule(context.animation.stop_swimmer_hit_animation, 3)

    handle_collisions_from_preset(context, 'points_medium', ts, dt=dt)
    handle_movement_from_preset(context, 'points_medium', dt)
    # Actors animation
    context.animation.moving_update_animations()
    return context.current_screen








