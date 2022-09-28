"""
逻辑处理主要模块，主要是界面的一些交互等。
FSM 含义?
"""

import random
import sys
import time
import keyboard

import click
import get_screen
from strategy import StrategyState
from log_state import *

# 全局变量
FSM_state = ""
time_begin = 0.0
game_count = 0
win_count = 0
quitting_flag = False

log_state = LogState()
log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
choose_hero_count = 0


def init():
    """初始化，读取日志文件Power.log（炉石日志）"""
    global log_state, log_iter, choose_hero_count

    # 有时候炉石退出时python握着Power.log的读锁, 因而炉石无法
    # 删除Power.log. 而当炉石重启时, 炉石会从头开始写Power.log,
    # 但此时python会读入完整的Power.log, 并在原来的末尾等待新的写入. 那
    # 样的话python就一直读不到新的log. 状态机进而卡死在匹配状态(不
    # 知道对战已经开始)
    # 这里是试图在每次初始化文件句柄的时候删除已有的炉石日志. 如果要清空的
    # 日志是关于当前打开的炉石的, 那么炉石会持有此文件的写锁, 使脚本无法
    # 清空日志. 这使得脚本不会清空有意义的日志
    if os.path.exists(HEARTHSTONE_POWER_LOG_PATH):
        try:
            file_handle = open(HEARTHSTONE_POWER_LOG_PATH, "w")
            file_handle.seek(0)
            file_handle.truncate()
            info_print("Success to truncate Power.log")
        except OSError:
            warn_print("Fail to truncate Power.log, maybe someone is using it")
    else:
        info_print("Power.log does not exist")

    log_state = LogState()
    log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
    choose_hero_count = 0


def update_log_state():
    """获取炉石日志最新数据"""
    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        return False

    for log_line_container in log_container.message_list:
        ok = update_state(log_state, log_line_container)
        # if not ok:
        #     return False

    if DEBUG_FILE_WRITE:  # 记录当前状态快照
        with open("./log/game_state_snapshot.txt", "w", encoding="utf8") as f:
            f.write(str(log_state))

    # 注意如果Power.log没有更新, 这个函数依然会返回. 应该考虑到game_state只是被初始化
    # 过而没有进一步更新的可能
    if log_state.game_entity_id == 0:
        return False

    return True


def system_exit():
    """系统退出。把退出状态quitting_flag设为True"""
    global quitting_flag

    sys_print(f"一共完成了{game_count}场对战, 赢了{win_count}场!")
    print_info_close()

    quitting_flag = True

    sys.exit(0)


def print_out():
    """根据不同状态打印相关日志"""
    global FSM_state
    global time_begin
    global game_count

    debug_print("-- 进入状态 " + str(FSM_state) + " --")

    if FSM_state == FSM_LEAVE_HS:
        warn_print("HearthStone not found! Try to go back to HS")

    if FSM_state == FSM_CHOOSING_CARD:
        game_count += 1
        sys_print("-" * 25 + "第 " + str(game_count) + " 场开始" + "-" * 25)
        time_begin = time.time()

    if FSM_state == FSM_QUITTING_BATTLE:
        time_now = time.time()
        if time_begin > 0:
            sys_print("本场耗时 : {} 分 {} 秒"
                      .format(int((time_now - time_begin) // 60),
                              int(time_now - time_begin) % 60))
        sys_print("-" * 25 + "第 " + str(game_count) + " 场结束" + "-" * 25)

    return


def ChoosingHeroAction():
    """选择卡组界面处理，实际只是点击对战按钮"""
    global choose_hero_count

    print_out()

    # 有时脚本会卡在某个地方, 从而在FSM_Matching
    # 和FSM_CHOOSING_HERO之间反复横跳. 这时候要
    # 重启炉石
    # choose_hero_count会在每一次开始留牌时重置
    choose_hero_count += 1
    if choose_hero_count >= 20:
        return FSM_ERROR

    time.sleep(2)
    click.match_opponent()
    time.sleep(1)
    return FSM_MATCHING


def MatchingAction():
    """对手匹配界面处理"""
    print_out()
    loop_count = 0

    while not quitting_flag:
        # if quitting_flag:
        #     sys.exit(0)

        time.sleep(STATE_CHECK_INTERVAL)

        click.commit_error_report()

        ok = update_log_state()
        if ok:
            if not log_state.is_end:
                return FSM_CHOOSING_CARD

        curr_state = get_screen.get_state()
        if curr_state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO

        loop_count += 1
        if loop_count >= 60:
            warn_print("Time out in Matching Opponent")
            return FSM_ERROR


def ChoosingCardAction():
    """留换牌处理"""
    global choose_hero_count
    choose_hero_count = 0

    print_out()
    time.sleep(21)
    loop_count = 0
    has_print = 0

    while not quitting_flag:
        ok = update_log_state()

        if not ok:
            return FSM_ERROR
        if log_state.game_num_turns_in_play > 0:
            return FSM_BATTLING
        if log_state.is_end:
            return FSM_QUITTING_BATTLE

        strategy_state = StrategyState(log_state)
        hand_card_num = strategy_state.my_hand_card_num

        # 等待被替换的卡牌 ZONE=HAND
        # 注意后手时幸运币会作为第五张卡牌算在手牌里, 故只取前四张手牌
        # 但是后手时 hand_card_num 仍然是 5
        for my_hand_index, my_hand_card in \
                enumerate(strategy_state.my_hand_cards[:4]):
            detail_card = my_hand_card.detail_card

            if detail_card is None:
                should_keep_in_hand = \
                    my_hand_card.current_cost <= REPLACE_COST_BAR
            else:
                should_keep_in_hand = \
                    detail_card.keep_in_hand(strategy_state, my_hand_index)

            if not has_print:
                debug_print(f"手牌-[{my_hand_index}]({my_hand_card.name})"
                            f"是否保留: {should_keep_in_hand}")

            if not should_keep_in_hand:
                click.replace_starting_card(my_hand_index, hand_card_num)

        has_print = 1

        click.commit_choose_card()

        loop_count += 1
        if loop_count >= 60:
            warn_print("Time out in Choosing Opponent")
            return FSM_ERROR
        time.sleep(STATE_CHECK_INTERVAL)


def Battling():
    """对战界面处理。本模块主要功能点！"""
    global win_count
    global log_state

    print_out()

    not_mine_count = 0
    mine_count = 0
    last_controller_is_me = False

    while not quitting_flag:
        # if quitting_flag:
        #     sys.exit(0)

        ok = update_log_state()
        if not ok:
            return FSM_ERROR

        # 对战结束后记录相关信息
        if log_state.is_end:
            my_hero = log_state.entity_dict[ \
                log_state.my_entity.query_tag("HERO_ENTITY")]
            oppo_hero = log_state.entity_dict[ \
                log_state.oppo_entity.query_tag("HERO_ENTITY")]
            sys_print(log_state.my_name + " vs. " + log_state.oppo_name)
            sys_print("我方英雄：" + my_hero.name + "(" + my_hero.query_tag('HEALTH') + ")")
            sys_print("对方英雄：" + oppo_hero.name + "(" + oppo_hero.query_tag('HEALTH') + ")")
            if log_state.my_entity.query_tag("PLAYSTATE") == "WON":
                win_count += 1
                sys_print("---恭喜，你赢了！共赢了 " + str(win_count) + " 盘！---")
            else:
                sys_print("---遗憾，你输了！---")
            sys_print("本人第 " + log_state.my_entity.query_tag("TURN") + " 回合")
            return FSM_QUITTING_BATTLE

        # 对方回合，等就行了
        if not log_state.is_my_turn:
            last_controller_is_me = False
            mine_count = 0

            not_mine_count += 1
            if not_mine_count >= 400:
                warn_print("Time out in Opponent's turn")
                return FSM_ERROR

            continue

        # 接下来考虑在我的回合的出牌逻辑。重点！！！

        # 如果是这个我的回合的第一次操作。 发表情
        if not last_controller_is_me:
            time.sleep(4)
            # 在游戏的第一个我的回合, 发一个你好
            # game_num_turns_in_play在每一个回合开始时都会加一, 即
            # 后手放第一个回合这个数是2
            if log_state.game_num_turns_in_play <= 2:
                click.emoj(0)
            else:
                # 在之后每个回合开始时有概率发表情
                if random.random() < EMOJ_RATIO:
                    click.emoj()

        last_controller_is_me = True
        not_mine_count = 0
        mine_count += 1

        if mine_count >= 20:
            if mine_count >= 40:
                return FSM_ERROR
            click.end_turn()
            click.commit_error_report()
            click.cancel_click()
            time.sleep(STATE_CHECK_INTERVAL)

        debug_print("-" * 60)
        strategy_state = StrategyState(log_state)
        strategy_state.debug_print_out()  # 打印双方信息

        # 1.考虑要不要出牌。  策略的重点，智能点所在！！！
        index, args = strategy_state.best_h_index_arg()

        # index == -1 代表使用技能, -2 代表不出牌
        if index != -2:
            strategy_state.use_best_entity(index, args)
            continue

        # 2.如果不出牌, 考虑随从怎么对战。  策略的重点，智能点所在！！！
        my_index, oppo_index = strategy_state.get_best_attack_target()

        # my_index == -1代表英雄攻击, -2 代表不攻击
        if my_index != -2:
            strategy_state.my_entity_attack_oppo(my_index, oppo_index)
        else:
            click.end_turn()
            time.sleep(STATE_CHECK_INTERVAL)

        # 3. TODO 出牌和对战的配合策略？
        # 打脸的收益和解场的收益比较，这个是做了比较的，配置里也有参数配置。
        # ？多个小随从解一个大随从，单个随从收益不高，但合作收益高。
        # ？手牌和场从随从合作解一个大随从，也是同上理。


def QuittingBattle():
    """对战结束后处理"""
    print_out()

    time.sleep(5)

    loop_count = 0
    while not quitting_flag:
        # if quitting_flag:
        #     sys.exit(0)

        state = get_screen.get_state()
        if state in [FSM_CHOOSING_HERO, FSM_LEAVE_HS]:
            return state
        click.cancel_click()
        click.test_click()
        click.commit_error_report()

        loop_count += 1
        if loop_count >= 15:
            return FSM_ERROR

        time.sleep(STATE_CHECK_INTERVAL)


def GoBackHSAction():
    """通过战网客户端点开始按钮进入炉石"""
    global FSM_state

    print_out()
    time.sleep(3)

    while not get_screen.test_hs_available():
        if quitting_flag:
            sys.exit(0)
        click.enter_HS()
        time.sleep(10)

    # 有时候炉石进程会直接重写Power.log, 这时应该重新创建文件操作句柄
    init()

    return FSM_WAIT_MAIN_MENU


def MainMenuAction():
    """炉石主界面处理. 主是点击进入传统对战."""
    print_out()

    time.sleep(3)

    while not quitting_flag:
        # if quitting_flag:
        #     sys.exit(0)

        click.enter_battle_mode()
        time.sleep(5)

        state = get_screen.get_state()

        # 重新连接对战之类的
        if state == FSM_BATTLING:
            ok = update_log_state()
            if ok and log_state.available:
                return FSM_BATTLING
        if state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO


def WaitMainMenu():
    """等待进入炉石主界面.  有可能卡在这个方法里,一直等?"""
    print_out()
    while get_screen.get_state() != FSM_MAIN_MENU:
        if quitting_flag:
            sys.exit(0)
        # click.click_middle()  # middle有可能点了中间别的窗口之类
        click.test_click()
        time.sleep(5)
    return FSM_MAIN_MENU


def HandleErrorAction():
    """出错处理"""
    print_out()

    if not get_screen.test_hs_available():
        return FSM_LEAVE_HS
    else:
        click.commit_error_report()
        click.click_setting()
        time.sleep(0.5)
        # 先尝试点认输
        click.left_click(960, 380)
        time.sleep(2)

        get_screen.terminate_HS()
        time.sleep(STATE_CHECK_INTERVAL)

        return FSM_LEAVE_HS


def FSM_dispatch(next_state):
    """分发状态处理器"""
    dispatch_dict = {
        FSM_LEAVE_HS: GoBackHSAction,
        FSM_MAIN_MENU: MainMenuAction,
        FSM_CHOOSING_HERO: ChoosingHeroAction,
        FSM_MATCHING: MatchingAction,
        FSM_CHOOSING_CARD: ChoosingCardAction,
        FSM_BATTLING: Battling,
        FSM_ERROR: HandleErrorAction,
        FSM_QUITTING_BATTLE: QuittingBattle,
        FSM_WAIT_MAIN_MENU: WaitMainMenu,
    }

    if next_state not in dispatch_dict:
        error_print("Unknown state!")
        sys.exit()
    else:
        return dispatch_dict[next_state]()


def SmartHS_go():
    """脚本执行入口. 前置炉石窗口,检查界面状态,分发处理器."""
    global FSM_state

    if get_screen.test_hs_available():
        hs_hwnd = get_screen.get_HS_hwnd()
        get_screen.move_window_foreground(hs_hwnd)
        time.sleep(0.5)

    while not quitting_flag:
        # if quitting_flag:
        #     sys.exit(0)
        if FSM_state == "":
            FSM_state = get_screen.get_state()
        FSM_state = FSM_dispatch(FSM_state)


#        FSM_state = get_screen.get_state()
#        debug_print(FSM_state)
#        time.sleep(1)


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+q", system_exit)

    init()
