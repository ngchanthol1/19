# !usr/bin/env python
# -*- coding:utf-8 -*-
# Author:LiuQian,time:2018/5/18

import numpy as np

import pandas as pd

import json


class RL(object):

    def __init__(self, action_space, learning_rate=0.01, reward_decay=1, e_greedy=0.9):

        self.actions = action_space  # a list

        self.lr = learning_rate

        self.gamma = reward_decay

        self.epsilon = e_greedy

        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):

        if state not in self.q_table.index:

            # append new state to q table

            self.q_table = self.q_table.append(

                pd.Series(

                    [0]*len(self.actions),

                    index=self.q_table.columns,

                    name=state,

                )

            )
        else:
            self.q_table = self.q_table

        return self.q_table

    def choose_action(self, observation):

        self.check_state_exist(observation)

        # action selection

        if np.random.rand() < self.epsilon:

            # choose best action

            state_action = self.q_table.loc[observation, :]

            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value

            action = state_action.idxmax()

        else:

            # choose random action

            action = np.random.choice(self.actions)

        return action

    def learn(self, *args):

        pass


class NTDTable(RL):

    def __init__(self, actions, learning_rate=0.01, reward_decay=1, e_greedy=0.9):

        super(NTDTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

    def check_state_exist(self, state):

        if state not in self.q_table.index:

            # append new state to q table

            to_be_append = pd.Series(

                    [0] * len(self.actions),

                    index=self.q_table.columns,

                    name=state,

                )

            self.q_table = self.q_table.append(to_be_append)

        return self.q_table

    def choose_action(self, observation):

        self.check_state_exist(observation)

        # action selection

        if np.random.rand() < self.epsilon:

            # choose best action

            state_action = self.q_table.loc[observation, :]

            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value

            action = state_action.idxmax()

        else:

            # choose random action

            action = np.random.choice(self.actions)

        return action

    # ????????????

    def learn(self, s, a, r, n):

        # global c

        c = 0

        l = self.q_table.shape[0]  # ??????Q????????????

        name = np.array(self.q_table.index)  # ??????Q?????????????????????list

        for k in range(0, n):

            stateToUpdate = s[k]  # ?????????????????????

            actionToUpdate = a[k]  # ?????????????????????

            G = 0  # ????????????????????????0,int

            for t in range(k, n):

                G += pow(self.gamma, t) * r[t]  # ????????????????????????G= R[] + R[] + R[]

            for i in range(l):  # ???????????????????????????Q[S(n-1), A(n-1)]???Q?????????,???????????????

                # global q_predict

                if json.loads(name[i]) == s[n - 1]:

                    # ?????????, q_predict = G + Q[S(n-1), A(n-1)]

                    q_predict = G + pow(self.gamma, n) * int(self.q_table.iloc[i, [a[n - 1]]])

                    for j in range(l):

                        if json.loads(name[j]) == stateToUpdate:

                            # ???????????????????????????Q[S(UT), A(UT)]????????????

                            q_target = int(self.q_table.iloc[j, [actionToUpdate]])

                            error = q_predict - q_target  # ??????

                            # ??????Q???

                            self.q_table.iloc[j, [actionToUpdate]] = q_target + self.lr * error  # * eligibility_trace

                            c += error

        return self.q_table, c