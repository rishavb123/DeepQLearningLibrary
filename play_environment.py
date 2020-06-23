import sys

from pynput import keyboard
import gym
from multiprocessing import Process

from environments.gym import GymEnvironment
from environments.flappy_bird import FlappyBird
from environments.coin_collector import CoinCollector

# env = GymEnvironment(gym.make('LunarLander-v2'))
env = FlappyBird()
# env = CoinCollector()

default_action = 0
action = default_action

click_action = True
switch_back = False

def set_action(act):
    print('Setting action to', act)
    action = act

def on_key_press(key):
    # print('Pressed Key %s' % key)
    if str(key)[1:-1].isdigit() and int(str(key)[1:-1]) < env.num_of_actions():
        set_action(int(str(key)[1:-1]))
    switch_back = click_action

def on_key_release(key):
    # print('Released Key %s' % key)
    if not click_action and str(key)[1:-1].isdigit() and int(str(key)[1:-1]) < env.num_of_actions():
        set_action(default_action)

def key_listener():
    with keyboard.Listener(on_release=on_key_release, on_press=on_key_press) as listener:
        listener.join()

if __name__ == '__main__':

    p = Process(target=key_listener)
    p.start()

    done = False

    print(env.num_of_actions())

    while not done or input('Play again? (Y/n)').lower()[0] == 'y':

        done = False
        score = 0
        observation = env.reset()

        while not done:
            observation, reward, done, info = env.step(action)
            score += reward
            env.render()
            if switch_back: set_action(default_action)

    env.close()
    p.terminate()
    sys.exit()