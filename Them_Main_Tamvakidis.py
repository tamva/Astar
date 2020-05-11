from Them_Grid_Tamvakidis import Grid
import Them_Astar_Tamvakidis as AS
from collections import defaultdict


def get_move(world, dimension, state, actions, noise, gamma):
    v_a_pairs = []
    for action in actions:
        is_end, n_state = world.move_given_action(state, action)
        if is_end:
          v = n_state
        else:
            lr_states = world.given_action(state, action)
            v_n_state = (1. - noise) * (-0.04 + dimension[n_state] * gamma)
            v_l_state = (noise / 2) * (-0.04 + dimension[lr_states[0]] * gamma)
            v_r_state = (noise / 2) * (-0.04 + dimension[lr_states[1]] * gamma)
            v = v_n_state + v_l_state + v_r_state

        v_a_pairs.append((v, action))
    return max(v_a_pairs)


def value_iter(world,
               noise=0.2,
               h=100,
               verbose=5
               ):
    gam = [0.9,0.6,0.2]

    dimension = defaultdict(lambda: 0.)
    pi_star = {}
    for state in world.pos_reward_states:
        pi_star[state] = world.EXIT
    for state in world.neg_reward_states:
        pi_star[state] = world.EXIT
    for gs in gam:
        print("<==><==><==><==> GAMMA {} <==><==><==><==>".format(gs))
        for k in range(1, h+1):
                for state in world.states:
                    possible_actions = world.actions_available(state)
                    dimension[state], pi_star[state] = get_move(world,
                         dimension, state, possible_actions, noise, gs)
                if k % verbose == 0:
                    print(' {}/{}'.format(k, h))
                    world.look_world(dimension)
                    print('\n')

    return dimension, pi_star,type(dimension)


def run():

    world = Grid()

    v, p, typ = value_iter(
        world,
        noise=0.2,
        h=100,
        verbose=10
    )
    return v, p, typ, world

if __name__ == '__main__':

    v, p, typ, world = run()
    print("Values", v)
    print('Last Values: ')
    world.look_world(v)
    keys = v.keys()
    rows, cols = (3, 4)
    map_world = [[0 for i in range(cols)] for j in range(rows)]
    U = [[0 for i in range(cols)] for j in range(rows)]
    gi= [1,2,3]
    si = [1,2,3,4]
    for s in si:
        for g in gi:

            tup = (s, g)
            for vk in keys:
                if vk == tup:
                    dato = v.get(tup)
                    g = g - 1
                    s = s - 1
                    U[g][s] = dato
                    g = g + 1
                    s = s + 1
    print(U)
    map_world[1][1] = 1
    start = [0, 0]  # starting position
    end = [2, 3]  # ending position
    path = AS.search(map_world, U, start, end)
    print("\n")
    print('======> A_ASTAR RESULTS <======')
    print('\n'.join(map(str, path)))

