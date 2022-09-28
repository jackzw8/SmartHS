import keyboard

import constants.constants as cons
import constants.global_var as gl
from print_info import *
from FSM_action import init
from FSM_action import system_exit, SmartHS_go


def check_name():
    """检查是否设置了用户名.   这里能自动检查当前玩家的用户名就好了,多账号玩家要注意了."""
    my_name = YOUR_NAME
    if my_name == "ChangeThis#54321":
        my_name = input("请输入你的炉石用户名, 例子: \"为所欲为、异灵术#54321\" (不用输入引号!)\n").strip()
    gl.set_value("MY_NAME",my_name)

    sys_print(HEARTHSTONE_POWER_LOG_PATH)
    sys_print("@" + my_name + "@")


if __name__ == "__main__":
    print_info_init()
    check_name()
    init()
    keyboard.add_hotkey("ctrl+q", system_exit)

    # SmartHS_go()
    # 如果因分辨率,屏幕检查等从正式入口有问题,可直接手动从选卡组界面开始.
    # 但还是要在constants中设置好分辨率及相对1920*1080的缩放比例.
    if FIRST_STATE:
        gl.set_value("state",FIRST_STATE)
    SmartHS_go(FIRST_STATE)
