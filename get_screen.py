"""
    窗口操作及屏幕截图判断
"""

import win32gui
import win32ui
import win32con
import win32com.client
import win32api
import win32process
import numpy

from print_info import *
from constants.constants import *


def get_HS_hwnd():
    """获得炉石窗口"""
    hwnd = win32gui.FindWindow(None, "炉石传说")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "《爐石戰記》")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "Hearthstone")
    return hwnd


def get_battlenet_hwnd():
    """获得战网窗口"""
    hwnd = win32gui.FindWindow(None, "战网")
    if hwnd != 0:
        return hwnd

    hwnd = win32gui.FindWindow(None, "Battle.net")
    return hwnd


def test_hs_available():
    """是否获得炉石窗口"""
    return get_HS_hwnd() != 0


def move_window_foreground(hwnd, name=""):
    """把窗口移动到前台"""
    try:
        win32gui.BringWindowToTop(hwnd)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        if name != "":
            warn_print(f"Open {name}: {e}")
        else:
            warn_print(e)

    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)


def max_diff(img, pixel_list):
    ans = 0
    for pair in pixel_list:
        diff = abs(int(img[pair[0]][pair[1]][1]) -
                   int(img[pair[0]][pair[1]][0]))
        ans = max(ans, diff)
        # print(img[pair[0]][pair[1]])

    return ans


def catch_screen(name=None):
    """屏幕截图"""
    # 第一个参数是类名，第二个参数是窗口名字
    # hwnd -> Handle to a Window !
    # 如果找不到对应名字的窗口，返回0
    if name is not None:
        hwnd = win32gui.FindWindow(None, name)
    else:
        hwnd = get_HS_hwnd()

    if hwnd == 0:
        return

    width = WIDTH
    height = HEIGHT
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框 DC device context
    hwin = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hwin)
    # hwndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)

    return im_opencv


def pixel_very_similar(im_opencv, y, x, expected_val):
    """比较点位像素的值"""
    img_val = im_opencv[y][x][:3]

    diff = abs(img_val[0] - expected_val[0]) + \
           abs(img_val[1] - expected_val[1]) + \
           abs(img_val[2] - expected_val[2])

    if diff <= 3:
        return True

    return False


def get_state():
    """根据预先设置的像素点位值来判断是那个界面"""
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return FSM_LEAVE_HS

    im_opencv = catch_screen()
    # debug_print(im_opencv[100][100][:3])
    state = ""
    if pixel_very_similar(im_opencv, 100, 100, [21, 25, 53]) or \
            pixel_very_similar(im_opencv, 305, 705, [21, 43, 95]):  # ？ 万圣节主界面会变
        state = FSM_MAIN_MENU
    elif pixel_very_similar(im_opencv, 100, 100, [8, 17, 24]):
        state = FSM_CHOOSING_HERO
    elif pixel_very_similar(im_opencv, 100, 100, [16, 17, 18]):
        state = FSM_MATCHING
    elif pixel_very_similar(im_opencv, 100, 100, [8, 9, 13]):
        state = FSM_CHOOSING_CARD
    else:
        state = FSM_BATTLING
    # debug_print(state)
    return state

# def image_hash(img):
#     img = Image.fromarray(img)
#     return imagehash.phash(img)
#
#
# def hash_diff(str1, str2):
#     return bin(int(str1, 16) ^ int(str2, 16))[2:].count("1")


def terminate_HS():
    """结束炉石窗口"""
    hwnd = get_HS_hwnd()
    if hwnd == 0:
        return
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, process_id)
    win32api.TerminateProcess(handle, 0)
    win32api.CloseHandle(handle)
