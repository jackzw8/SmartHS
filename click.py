"""
    模拟点击屏幕模块
"""

import win32gui
import win32api
import win32con
import pywintypes
import time
from pynput.mouse import Button, Controller
import random
import sys

from constants.constants import *
from print_info import *
from get_screen import *


def rand_sleep(interval):
    """休眠interval秒左右"""
    base_time = interval * 0.75
    rand_time = interval * 0.5 * random.random()  # avg = 0.25 * interval
    time.sleep(base_time + rand_time)


def click_button(x, y, button):
    """鼠标点击 但按SCALE比例放大或缩小  x,y 5内随机加减 """
    x = x * SCALE
    y = y * SCALE
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    mouse = Controller()
    rand_sleep(0.1)
    mouse.position = (x, y)
    # debug_print(mouse.position)
    rand_sleep(0.1)
    mouse.press(button)
    rand_sleep(0.1)
    mouse.release(button)


def click_button_old(x, y, button):
    """鼠标点击 x,y 5内随机加减 """
    x += random.randint(-5, 5)
    y += random.randint(-5, 5)
    mouse = Controller()
    rand_sleep(0.1)
    mouse.position = (x, y)
    rand_sleep(0.1)
    mouse.press(button)
    rand_sleep(0.1)
    mouse.release(button)


def left_click(x, y):
    click_button(x, y, Button.left)


def right_click(x, y):
    click_button(x, y, Button.right)


def choose_my_minion(mine_index, mine_num):
    """选择我方场上随从"""
    rand_sleep(OPERATE_INTERVAL)
    x = 960 - (mine_num - 1) * 70 + mine_index * 140
    y = 600
    left_click(x, y)


def choose_my_hero():
    """选择我方英雄"""
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 850)


def choose_opponent_minion(oppo_index, oppo_num):
    """选择对方场上随从"""
    rand_sleep(OPERATE_INTERVAL)
    x = 960 - (oppo_num - 1) * 70 + oppo_index * 140
    y = 400
    left_click(x, y)


def choose_oppo_hero():
    """选择对方英雄"""
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 200)


def cancel_click():
    """右键点击  取消一些操作"""
    rand_sleep(TINY_OPERATE_INTERVAL)
    right_click(50, 400)


def test_click():
    """测试左键点击  用到一些点击跳过的情况"""
    rand_sleep(TINY_OPERATE_INTERVAL)
    left_click(50, 400)


# 手牌位置
HAND_CARD_X = [
    [],  # 0
    [885],  # 1
    [820, 980],  # 2
    [750, 890, 1040],  # 3
    [690, 820, 970, 1130],  # 4
    [680, 780, 890, 1010, 1130],  # 5
    [660, 750, 840, 930, 1020, 1110],  # 6
    [660, 733, 810, 885, 965, 1040, 1120],  # 7
    [650, 720, 785, 855, 925, 995, 1060, 1130],  # 8
    [650, 710, 765, 825, 880, 950, 1010, 1070, 1140],  # 9
    [647, 700, 750, 800, 860, 910, 970, 1020, 1070, 1120]  # 10
]


def choose_card(card_index, card_num):
    """选中指定手牌"""
    rand_sleep(OPERATE_INTERVAL)

    assert 0 <= card_index < card_num <= 10
    # x = START[card_num] + 65 + STEP[card_num] * card_index
    x = HAND_CARD_X[card_num][card_index]

    y = 1000
    left_click(x, y)


# 对战开始的留换卡牌位置
STARTING_CARD_X = {
    3: [600, 960, 1320],
    5: [600, 850, 1100, 1350],
}


def replace_starting_card(card_index, hand_card_num):
    """选中要换掉的牌"""
    assert hand_card_num in STARTING_CARD_X
    assert card_index < len(STARTING_CARD_X[hand_card_num])

    rand_sleep(OPERATE_INTERVAL)
    left_click(STARTING_CARD_X[hand_card_num][card_index], 500)


def click_middle():
    """选中屏幕中央"""
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 500)


def click_setting():
    """选中'选项'按钮"""
    rand_sleep(OPERATE_INTERVAL)
    left_click(1880, 1050)


def choose_and_use_spell(card_index, card_num):
    """施放法术牌, 无指向性的"""
    choose_card(card_index, card_num)
    click_middle()


# 第[i]个随从左边那个空隙记为第[i]个gap
def put_minion(gap_index, minion_num):
    """选中一个场上的随从"""
    rand_sleep(OPERATE_INTERVAL)

    if minion_num >= 7:
        warn_print(f"Try to put a minion but there has already been {minion_num} minions")

    x = 960 - (minion_num - 1) * 70 + 140 * gap_index - 70
    y = 600
    left_click(x, y)


def match_opponent():
    """点击对战按钮"""
    # 一些奇怪的错误提示
    commit_error_report()
    rand_sleep(OPERATE_INTERVAL)
    left_click(1400, 900)


def enter_battle_mode():
    """点击传统对战按钮"""
    # 一些奇怪的错误提示
    commit_error_report()
    rand_sleep(OPERATE_INTERVAL)
    left_click(950, 320)


def commit_choose_card():
    """确定留换牌的选择"""
    rand_sleep(OPERATE_INTERVAL)
    left_click(960, 850)


def end_turn():
    """点击回合结束按钮"""
    rand_sleep(OPERATE_INTERVAL)
    left_click(1550, 500)


def commit_error_report():
    # 一些奇怪的错误提示
    left_click(1100, 820)
    # 如果已断线, 点这里时取消
    left_click(960, 650)


def emoj(target=None):
    """发表情"""
    emoj_list = [(800, 880), (800, 780), (800, 680), (1150, 680), (1150, 780)]
    right_click(960, 830)
    rand_sleep(OPERATE_INTERVAL)

    if target is None:
        x, y = emoj_list[random.randint(1, 4)]
    else:
        x, y = emoj_list[target]
    left_click(x, y)
    rand_sleep(OPERATE_INTERVAL)


def click_skill():
    """点击技能"""
    rand_sleep(OPERATE_INTERVAL)
    left_click(1150, 850)


def use_skill_no_point():
    """使用无指向性的技能"""
    click_skill()
    cancel_click()


def use_skill_point_oppo(op_index, op_num):
    """使用技能，指向对方英雄或随从"""
    click_skill()
    if op_index >= 0:
        choose_opponent_minion(op_index, op_num)
    else:
        choose_oppo_hero()

    cancel_click()

    '''
    def use_with_arg(cls, state, card_index, *args):
        if len(args) == 0:
            hand_card = state.my_hand_cards[card_index]
            warn_print(f"Receive 0 args in using SpellPointOppo card {hand_card.name}")
            return
        oppo_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(cls.wait_time)
    '''


def use_skill_point_mine(my_index, my_num):
    """使用技能，指向我方英雄或随从"""
    click_skill()

    if my_index < 0:
        choose_my_hero()
    else:
        choose_my_minion(my_index, my_num)

    cancel_click()


def minion_beat_minion(mine_index, mine_number, oppo_index, oppo_num):
    """我方随从攻击对方随从"""
    choose_my_minion(mine_index, mine_number)
    choose_opponent_minion(oppo_index, oppo_num)
    cancel_click()


def minion_beat_hero(mine_index, mine_number):
    """我方随从攻击对方英雄"""
    choose_my_minion(mine_index, mine_number)
    choose_oppo_hero()
    cancel_click()


def hero_beat_minion(oppo_index, oppo_num):
    """我方英雄攻击对方随从"""
    choose_my_hero()
    choose_opponent_minion(oppo_index, oppo_num)
    cancel_click()


def hero_beat_hero():
    """我方英雄攻击对方英雄"""
    choose_my_hero()
    choose_oppo_hero()
    cancel_click()


def enter_HS():
    """通过战网客户端进入炉石"""
    rand_sleep(1)

    if test_hs_available():
        move_window_foreground(get_HS_hwnd(), "炉石传说")
        return

    battlenet_hwnd = get_battlenet_hwnd()

    if battlenet_hwnd == 0:
        error_print("未找到应用战网")
        sys.exit()

    move_window_foreground(battlenet_hwnd, "战网")

    rand_sleep(1)

    left, top, right, bottom = win32gui.GetWindowRect(battlenet_hwnd)
    # left_click(left + 180, bottom - 110)
    click_button_old(left + 180, bottom - 110, Button.left)
