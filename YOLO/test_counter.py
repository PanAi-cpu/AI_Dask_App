# 校验计数器
from counter_reader import read_counter_value

while True:
    value = read_counter_value()
    print("计米器:", value)