import random
from random import randint
from game.constants import GameState, QuestionStates
from pgzero.animation import animate


LEVEL_PRESETS = {
    'speedrun_easy': {
        'actors': {
            'obstacles': ['logs'],
            'collectibles': ['glasses'],
            'powerups': ['speed_powerup'],
            'special': ['q_block', 'inversion_portal']
        },
        'config': {
            'log_count': 3,
            'powerup_count': 1,
            'speed': {'normal': 2, 'fast': 3}
        }

    },
    'points_easy': {
        'actors': {
            'obstacles': ['logs'],
            'collectibles': ['coins', 'glasses'],
            'powerups': ['score_powerup', 'magnet_powerup'],
            'special': ['q_block', 'inversion_portal']
        },
        'config': {
            'log_count': 3,
            'coin_count': 20,
            'speed': {'normal': 2}
        }
    },
    'speedrun_medium':{
        'actors':{
            'obstacles': ['logs', 'shark'],
            'collectibles': ['glasses', 'swimmer_cap'],
            'powerups': ['speed_powerup', 'push_powerup'],
            'special': ['q_block', 'inversion_portal']
        },
        'config': {
            'log_count': 3,
            'powerup_count': 1,
            'speed': {'normal': 3, 'fast': 5}
        },
        'bird_attack': 'Yes'
    },
    'points_medium':{
        'actors':{
            'obstacles': ['logs', 'bear', 'poop'],
            'collectibles': ['coins', 'glasses', 'swimmer_cap'],
            'powerups': ['score_powerup', 'push_powerup', 'magnet_powerup'],
            'special': ['q_block', 'inversion_portal']
        },
        'config': {
            'log_count': 3,
            'powerup_count': 1,
            'speed': {'normal': 3, 'fast': 3}

        },
        'bird_attack': 'Yes'

    }

}


def init_actors_from_preset(context, preset_name):
    preset = LEVEL_PRESETS[preset_name]

    # Clear existing actors
    context.actors.reset_all_actors()

    # Initialize logs
    if 'logs' in preset['actors'].get('obstacles', []):
        for i, x in enumerate([250, 400, 550]):  # Explicit positions for left, middle, right
            new_log = context.actors.actor_storage.new_actor(
                image_name="log",
                position=(x, randint(-800, -300)),
                special_x=x,  # Explicit lane positioning
                first=-800,  # Min Y position
                last=-300,  # Max Y position
                x_positions=[x],  # Lock to this lane
                x_locked=False  # Disable random x-position changes
            )
            context.actors.logs.append(new_log)
            print(f"Initialized log {i} at x={x}")  # Debug print

    # Initialize powerups
    if 'powerups' in preset['actors']:
        for powerup_type in preset['actors']['powerups']:
            for _ in range(preset['config'].get('powerup_count', 1)):
                powerup = context.actors.actor_storage.new_actor(
                    image_name=powerup_type,
                    position=(random.choice(context.movement.config["default_positions"]),
                              randint(-1600, -800)),
                    actor_list=context.actors.powerups["powerups"],
                    first=-1600,
                    last=-800
                )
                # Also add to specific powerup list
                context.actors.powerups[powerup_type].append(powerup)

    # Initialize coins
    if 'coins' in preset['actors'].get('collectibles', []):
        for _ in range(preset['config'].get('coin_count', 20)):
            context.actors.actor_storage.new_actor(
                image_name="coin",
                position=(randint(175, 625), randint(-800, -100)),
            actor_list = context.actors.coins,
            first = -800,
            last = -100
        )

    # Initialize other collectibles
    if 'glasses' in preset['actors'].get('collectibles', []):
        glasses = context.actors.actor_storage.new_actor(
    image_name = "glasses",
    position = (random.choice([250, 550]), randint(-1000, -800)),
    actor_list = None,
    first = -1000,
    last = -800
    )
        context.actors.collectibles["glasses"] = glasses

    # Initialize special actors
    if 'inversion_portal' in preset['actors'].get('special', []):
        portal = context.actors.actor_storage.new_actor(
            image_name="inversion_portal",
            position=(random.choice([250, 400, 550]), randint(-3000, -2500)),
        actor_list = None,
        first = -3000,
        last = -2500
    )
        context.actors.special["inversion_portal"] = portal


def reset_actors_from_preset(context, preset_name):
    preset = LEVEL_PRESETS[preset_name]
    actors_to_reset = []

    # Handle special actors first
    q_block = context.actors.category_map.get('special', {}).get('q_block')
    if q_block:
        actors_to_reset.append(q_block)
    if 'inversion_portal' in preset['actors'].get('special', []):
        actors_to_reset.append(context.actors.category_map['special']['inversion_portal'])

    # Handle obstacle lists
    if 'logs' in preset['actors'].get('obstacles', []):
        actors_to_reset.extend(context.actors.category_map['obstacles']['logs'])

    # Handle collectible lists
    if 'coins' in preset['actors'].get('collectibles', []):
        actors_to_reset.extend(context.actors.category_map['collectibles']['coins'])
    if 'glasses' in preset['actors'].get('collectibles', []):
        actors_to_reset.append(context.actors.category_map['collectibles']['glasses'])

    # Handle powerups
    if 'powerups' in preset['actors']:
        for powerup_type in preset['actors']['powerups']:
            actors_to_reset.extend(context.actors.powerups.get(powerup_type, []))

    context.movement.reset_actors_position(context, *actors_to_reset)


def handle_collisions_from_preset(context, preset_name, ts, dt=None):
    preset = LEVEL_PRESETS[preset_name]

    if 'logs' in preset['actors'].get('obstacles', []):
        context.movement.log_collision(context, ts)
    if 'coins' in preset['actors'].get('collectibles', []):
        context.movement.coin_collision(context)
    if 'q_block' in preset['actors'].get('special', []):
        question_state_map = {
            'speedrun_easy': QuestionStates.SPEED_EASY,
            'points_easy': QuestionStates.POINTS_EASY,
            'speedrun_medium': QuestionStates.SPEED_MEDIUM,
            'points_medium': QuestionStates.POINTS_MEDIUM
        }
        q_screen = question_state_map.get(preset_name, QuestionStates.SPEED_EASY)

        context.current_screen = context.movement.q_block_collision(context, q_screen=q_screen)

    if 'inversion_portal' in preset['actors'].get('special', []):
        context.movement.inversion_portal_collision(context, context.actors.special['q_block'], context.actors.logs, context.actors.powerups["powerups"])

    if 'speed_powerup' in preset['actors'].get('powerups', []):
        context.movement.speed_powerup_collision(context, "stasis", 5, "strength")

    if 'score_powerup' in preset['actors'].get('powerups', []):
        context.movement.score_powerup_collision(context)

    if 'push_powerup' in preset['actors'].get('powerups', []):
        context.movement.push_powerup_collision(context)

    if 'glasses' in preset['actors'].get('collectibles', []):
        context.movement.glasses_collision(context)

    if 'shark' in preset['actors'].get('obstacles', []):
        context.movement.shark_collision(context)

    if 'poop' in preset['actors'].get('obstacles', []):
        context.movement.poop_collision(context)

    if 'swimmer_cap' in preset['actors'].get('collectibles', []):
        context.movement.swimmer_cap_collision(context)

    if 'bear' in preset['actors'].get('obstacles', []) or 'poop' in preset['actors'].get('obstacles', []):
        context.comp_actors.bear_actions(context)

    if 'magnet_powerup' in preset['actors'].get('powerups', []):
        context.movement.magnet_collision(context)
        context.movement.update_magnet_effect(context, dt)

    if 'bird_attack' in preset and 'Yes' in preset['bird_attack']:
        context.movement.handle_bird_attack_collisions(context)

    context.movement.handle_between_collisions(excluded_actor="swimmer")


def handle_movement_from_preset(context, preset_name, dt=None):
    preset = LEVEL_PRESETS[preset_name]
    speed = preset['config']['speed']

    moving_actors = []
    if hasattr(context.actors, 'logs') and context.actors.logs:
        moving_actors.append(context.actors.logs)

    for category, subcategories in preset['actors'].items():
        for subcategory in subcategories:
            # Get the actor or actor list from the category map
            actors = context.actors.category_map.get(category, {}).get(subcategory, [])

            if isinstance(actors, list):
                moving_actors.extend(actors)
            else:
                moving_actors.append(actors)

    context.movement.reposition_actors(
        context,
        *moving_actors,
        quantity=2,
        special_effect=context.actors.speed_powerup_collision,
        alt_quantity=3
    )

    context.movement.move_swimmer(
        context,
        context.actors.speed_powerup_collision,
        normal_speed=speed['normal'],
        fast_speed=speed.get('fast', speed['normal'],),
    )


    if 'bird_attack' in preset and 'Yes' in preset['bird_attack']:
        if random.random() < 0.001 and not context.comp_actors.bird_attack_active and not context.animation.inversion_active:
            all_actors = []
            for actor in moving_actors:
                if isinstance(actor, list):
                    all_actors.extend(actor)
                else:
                    all_actors.append(actor)
            for actor in all_actors:
                animate(actor, tween='accelerate', duration=1.0, pos=(actor.x, -1000))
            context.comp_actors.start_bird_attack()
        context.comp_actors.update_bird_attack(dt)
