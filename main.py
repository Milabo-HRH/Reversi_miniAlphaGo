import copy
from copy import deepcopy

import random

from board import Board

import math

# 棋盘初始化
board = Board()

# 打印初始化棋盘
board.display()


class RandomPlayer:
    """
    随机玩家, 随机返回一个合法落子位置
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color

    def random_choice(self, board):
        """
        从合法落子位置中随机选一个落子位置
        :param board: 棋盘
        :return: 随机合法落子位置, e.g. 'A1'
        """
        # 用 list() 方法获取所有合法落子位置坐标列表
        action_list = list(board.get_legal_actions(self.color))

        # 如果 action_list 为空，则返回 None,否则从中选取一个随机元素，即合法的落子坐标
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        action = self.random_choice(board)
        return action


class HumanPlayer:
    """
    人类玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color

    def get_move(self, board):
        """
        根据当前棋盘输入人类合法落子位置
        :param board: 棋盘
        :return: 人类下棋落子位置
        """
        # 如果 self.color 是黑棋 "X",则 player 是 "黑棋"，否则是 "白棋"
        if self.color == "X":
            player = "黑棋"
        else:
            player = "白棋"

        # 人类玩家输入落子位置，如果输入 'Q', 则返回 'Q'并结束比赛。
        # 如果人类玩家输入棋盘位置，e.g. 'A1'，
        # 首先判断输入是否正确，然后再判断是否符合黑白棋规则的落子位置
        while True:
            action = input(
                "请'{}-{}'方输入一个合法的坐标(e.g. 'D3'，若不想进行，请务必输入'Q'结束游戏。): ".format(player,
                                                                             self.color))

            # 如果人类玩家输入 Q 则表示想结束比赛
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                # 检查人类输入是否正确
                if row in '12345678' and col in 'ABCDEFGH':
                    # 检查人类输入是否为符合规则的可落子位置
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")


import time


class Node:
    def __init__(self, state, color='X', parent=None, action=None):
        self.state = state
        self.color = color
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.reward = 0.0

    def AddChild(self, state_c, color, action):
        child = Node(state_c, color, self, action)
        self.children.append(child)
        return child


c = pow(2, 0.5) / 2


def nextColor(color):
    if color == 'X':
        new_color = 'O'
    else:
        new_color = 'X'
    return new_color


def eqBoard(board1: Board, board2: Board):
    for i in range(8):
        if board1.__getitem__(i) != board2.__getitem__(i):
            return False
    return True


priority = [[1, 5, 3, 3, 3, 3, 5, 1],
            [5, 5, 4, 4, 4, 4, 5, 5],
            [3, 4, 2, 2, 2, 2, 4, 3],
            [3, 4, 2, 2, 2, 2, 4, 3],
            [3, 4, 2, 2, 2, 2, 4, 3],
            [3, 4, 2, 2, 2, 2, 4, 3],
            [5, 5, 4, 4, 4, 4, 5, 5],
            [1, 5, 3, 3, 3, 3, 5, 1]]


class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color, max_times=8000):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color
        self.max_times = max_times
        board_now = Board()
        self.node = Node(state=board_now, color=self.color)

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------
        root = None
        for node in self.node.children:
            if eqBoard(node.state, board):
                root = node
                break
        if root is None:
            board_now = deepcopy(board)
            root = Node(state=board_now, color=self.color)
        self.node = root
        action = self.UCTSearch(max_times=self.max_times, node=root)
        # ------------------------------------------------------------------------

        return action

    def UCTSearch(self, max_times, node):
        """
        通过蒙特卡洛搜索返回此时的最佳动作
        :param max_times: 允许的最大搜索次数
        :param node: 蒙特卡洛树上当前访问的节点,表示当前状态
        :return action: 玩家MAX行动下最优动作a*
        """
        time_s = time.time()
        for i in range(max_times):
            leave = self.SelectPolicy(node)
            self.BackPropagate(leave)
            time_n = time.time()
            if time_n-time_s > 50:
                break
        m = -1
        best_action = None
        for a in node.children:
            if a.reward > m:
                m = a.reward
                best_action = a.action
                self.node = a
        return best_action

    def SelectPolicy(self, node):
        """
        选择将要被拓展的节点
        :param node: 蒙特卡洛树上当前访问的节点
        :return node: 将要被拓展的节点
        """
        while len(list(node.state.get_legal_actions(node.color))):
            node.visits += 1
            if len(node.children) < len(list(node.state.get_legal_actions(node.color))):
                temp = self.Expand(node)
                return temp
            else:
                stack = []
                max_node = None
                max_value = float(-1.0)
                for i in range(len(node.children)):
                    val = node.children[i].reward / node.children[i].visits + c * pow(
                        2 * math.log(node.visits) / node.children[i].visits, 0.5)
                    if val > max_value:
                        max_value = val
                        max_node = node.children[i]
                node = max_node
        return node

    def Expand(self, node):
        """
        完成节点的拓展
        :param node: 待拓展的节点
        :return node: 该拓展对应的随机叶子节点
        """
        actions = list(node.state.get_legal_actions(node.color))
        tried = [temp.action for temp in node.children]
        to_expand = None
        val = 6
        for a in actions:
            if a in tried:
                continue
            row, col = Board.board_num(node.state, a)
            if priority[row][col] < val:
                val = priority[row][col]
                to_expand = a
        new_state = copy.deepcopy(node.state)
        new_state._move(to_expand, node.color)

        if node.color == 'X':
            new_color = 'O'
        else:
            new_color = 'X'
        return self.SimulatePolicy(node.AddChild(state_c=new_state, action=to_expand, color=new_color))

    def SimulatePolicy(self, node):
        """
        模拟当前状态终局的结果
        :param node: 节点 表示当前状态
        :return state: 模拟棋局得到的终局节点
        """
        board = copy.deepcopy(node.state)
        actions = list(board.get_legal_actions(node.color))
        if len(actions):
            optimal = None
            val = 6
            for a in actions:
                row, col = Board.board_num(node.state, a)
                if priority[row][col] < val:
                    val = priority[row][col]
                    optimal = a
            new_state = copy.deepcopy(node.state)
            new_state._move(optimal, node.color)
            return self.SimulatePolicy(node.AddChild(state_c=new_state, action=optimal, color=nextColor(node.color)))
        else:
            if len(list(board.get_legal_actions(nextColor(node.color)))):
                node.AddChild(state_c=node.state, action=None, color=nextColor(node.color))
                return self.SimulatePolicy(node.children[0])
            else:
                return node

    def BackPropagate(self, node):
        """
        反向传播
        :param node: 反向传播更新的起始节点
        :return: NONE
        """
        res = node.state.get_winner
        while node:
            node.visits += 1
            if res == 2:
                if node.color == self.color:
                    node.reward += -0.5
                else:
                    node.reward += 0.5
            elif res == 0:
                if self.color == 'X':
                    if node.color == self.color:
                        node.reward += -1
                    else:
                        node.reward += 1
            elif res == 1:
                if self.color == 'O':
                    if node.color == self.color:
                        node.reward += -1
                    else:
                        node.reward += 1
            node = node.parent


from game import Game

# 人类玩家黑棋初始化
black_player = AIPlayer("X", 8000)

# AI 玩家 白棋初始化
white_player = AIPlayer("O", 8000)

# 游戏初始化，第一个玩家是黑棋，第二个玩家是白棋
game = Game(black_player, white_player)

# 开始下棋
game.run()
