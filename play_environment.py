import sys

from pynput import keyboard
from pynput.keyboard import Key
import gym
from multiprocessing import Process, Value
import time

from environments.gym import GymEnvironment
from environments.flappy_bird import FlappyBird
from environments.coin_collector import CoinCollector
from environments.snake import SnakeGame

# env = GymEnvironment(gym.make('LunarLander-v2'))
# env = FlappyBird()
# env = CoinCollector()
env = SnakeGame()

# # Default Empty Mappings:
# mappings = {}

# # Flappy Bird Mappings:
# mappings = {
#     Key.space: 1
# }

# # Snake Game Mappings:
mappings = {
    Key.left: 0,
    Key.up: 1,
    Key.right: 2,
    Key.down: 3
}

default_action = 0
action = default_action

click_action = True
use_switch_back = True

switch_back = False

v = Value('i', 0)
def key_listener(v):

    def set_action(act):
        v.value = act
        

    def on_key_press(key):
        # print('Pressed Key %s' % key)
        if key in mappings:
            key = "'" + str(mappings[key]) + "'"
        if str(key)[1:-1].isdigit() and int(str(key)[1:-1]) < env.num_of_actions():
            set_action(int(str(key)[1:-1]))
            switch_back = click_action

    def on_key_release(key):
        # print('Released Key %s' % key)
        if not click_action and str(key)[1:-1].isdigit() and int(str(key)[1:-1]) < env.num_of_actions():
            set_action(default_action)

    with keyboard.Listener(on_release=on_key_release, on_press=on_key_press) as listener:
        listener.join()

if __name__ == '__main__':

    p = Process(target=key_listener, args=(v, ))
    p.start()

    done = False

    while not done or input('Play again? (Y/n)').lower()[0] == 'y':

        done = False
        score = 0
        observation = env.reset()
        action = default_action

        while not done:
            action = v.value
            observation, reward, done, info = env.step(action)
            print(len(observation), env.len_of_state())
            score += reward
            env.render()
            if switch_back and use_switch_back: 
                v.value = default_action
                switch_back = False
            time.sleep(0.1)

        env.close()
    p.terminate()
    sys.exit()