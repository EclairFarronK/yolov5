# pyautogui是用来操作鼠标和键盘，也可以用来截图
import pyautogui

# pyautogui.dragTo(200, 200, duration=2, button='left')
# pyautogui.dragTo(200, 200, duration=2, button='right')
# 绝对坐标
pyautogui.moveTo(956, 534, duration=2)
# pyautogui.moveTo(100, 100, duration=2)
# # 相对坐标
# pyautogui.drag(100, 100, duration=2)
# pyautogui.dragTo(200, 200, duration=2)
# pyautogui.dragTo(200, 200, duration=2, button='right')
# pyautogui.click()
# pyautogui.write('hello', interval=0.25)
screenshot = pyautogui.screenshot()
