import time
from gamer.prompts import get_system_prompt

from gamer.api import get_sm64_operation, get_poker_operation
from gamer.adapter import Adapter

adapters = Adapter()


from gamer.operating_system import OperatingSystem

operating_system = OperatingSystem()

debug = True


def main():
    #print("[poker-agent]")

    system_prompt = get_system_prompt()
    system_message = {"role": "system", "content": system_prompt}
    messages = [system_message]
    # wait for two seconds

    if debug:
        #print("[poker-agent] starting")

    loop_count = 0

    loop_max = 20

    while True:
        time.sleep(2)

        if len(messages) > 5:
            #print("[poker-agent] truncating earlier message")
            messages = [system_message] + messages[-4:]

        operation = get_poker_operation(
                messages
            )  # at https://www.247freepoker.com/
            
        #print("[poker-agent] operation", operation)

        operate(operation)

        loop_count += 1
        if loop_count > loop_max:
            break


def operate(preprocessed_operation):
    if debug:
        #print("[poker-agent] operate")

    # print("[poker-agent] action", action)
    # print("[poker-agent] thought", thought)
    # print("[poker-agent] duration", thought)
    operations = adapters.poker(preprocessed_operation)

    if debug:
        #print("[poker-agent] operations", operations)

    for operation in operations:
        # if debug:
        #     print("[poker-agent] operation", operation)
        operate_type = operation.get("operation")

        if operate_type == "press":
            if debug:
                #print("[poker-agent] press operation!")
            key = operation.get("key")
            duration = operation.get("duration", 0.5)
            operating_system.press(key, duration)
        elif operate_type == "write":
            if debug:
                #print("[poker-agent] write operation!")
            content = operation.get("content")
            operate_detail = content
            # operating_system.write(content)
        elif operate_type == "click":
            if debug:
                #print("[poker-agent] click operation!")
            x = operation.get("x")
            y = operation.get("y")
            click_detail = {"x": x, "y": y}

            operating_system.mouse(click_detail)
        else:
            #print("[poker-agent] operation not mapped, no problem!")
            return


if __name__ == "__main__":
    main()
