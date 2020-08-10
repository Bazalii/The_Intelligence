from Gripper_suspension.Gripper_suspension_resiver import GripSuspension

val = GripSuspension("/dev/ttyACM5", 115200, graph=True, sleep_time=0.0001)
while True:
    dat = input()
    if dat == "exit":
        val.terminate_thread()
        val.join()
        break
    elif dat == "zero":
        val.set_zero()
    elif dat == "no zero":
        val.no_zero()
    else:
        try:
            dat = int(dat)
            for i in range(dat):
                while len(val.buffer) <= 0:
                    pass
                buffer = val.latest_val()
                print(str(buffer[0]), str(buffer[1]))
                first = buffer[0].length()
                second = buffer[1]['-x'] + buffer[1]['+x'] + buffer[1]['-y'] + buffer[1]['+y']
                print(f"{first} == {second},  {first == second}")
        except:
            pass