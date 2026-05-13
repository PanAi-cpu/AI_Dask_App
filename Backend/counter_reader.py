import serial
import time
import struct


def read_counter_value(port='COM5', baudrate=9600, timeout=1):
    """
    从 CY7 计数器读取实时计数值

    参数:
        port: 串口号，默认 'COM7'
        baudrate: 波特率，默认 9600
        timeout: 超时时间（秒），默认 1

    返回:
        成功: 计数值 (整数)
        失败: None
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        cmd = bytes.fromhex('01 03 00 0B 00 04 35 CB')

        ser.write(cmd)
        response = ser.read(100)
        ser.close()

        if len(response) < 9 or response[0] != 0x01 or response[2] != 8:
            return None

        # 提取 0EH 寄存器的值（计数值低位）
        count_low = struct.unpack('>H', response[9:11])[0]
        return count_low

    except Exception as e:
        print(f"读取失败: {e}")
        return None


def continuous_read(port='COM6', baudrate=9600, interval=1, callback=None):
    """
    持续读取计数值

    参数:
        port: 串口号
        baudrate: 波特率
        interval: 读取间隔（秒）
        callback: 回调函数，每次读到值时调用
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    cmd = bytes.fromhex('01 03 00 0B 00 04 35 CB')

    try:
        while True:
            ser.write(cmd)
            response = ser.read(100)

            if len(response) >= 11 and response[0] == 0x01:
                count = struct.unpack('>H', response[9:11])[0]
                if callback:
                    callback(count)
                else:
                    print(count)

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n停止读取")
    finally:
        ser.close()