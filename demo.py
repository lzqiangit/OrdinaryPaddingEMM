from client import Client
from Crypto.Random import get_random_bytes


def show_menu(): 
    print("""
    m: menu     x: exit     s: setup server     r: rebuild server
    i: insert   d: delete   u: update           q: query
    qd: query and get details
    """)

if __name__ == '__main__':
    key = get_random_bytes(16)
    my_client = Client(key)
    show_menu()
    while True: 
        # 输入一个字符
        cmd = input(">>> ")
        if cmd == 'm':
            show_menu()
        elif cmd == 'x':
            break
        elif cmd == 's':
            my_client.setup_server()
        elif cmd == 'r':
            my_client.rebuild_server()
        elif cmd == 'i':
            key = input("key: ")
            values = input("values: ")
            for value in values.split(' '):
                my_client.insert(key, value)
        elif cmd == 'd':
            key = input("key: ")
            value =input("value: ")
            my_client.delete(key, value)
        elif cmd == 'u':
            key = input("key: ")
            old_value = input("old_value: ")
            new_value = input("new_value: ")
            my_client.update(key, old_value, new_value)
        elif cmd == 'q':
            key = input("key: ")
            res,t1,t2 = my_client.query(key)
            print('*' * 60)
            print(res)
            print('*' * 60)
        elif cmd == 'qd':
            key = input("key: ")
            res, all, up = my_client.query(key)
            print('*' * 60)
            print("查询结果: " + str(res))
            print("所有数据: " + str(all))
            print("updata表中数据: " + str(up))
            print("是否构建服务器: " + str(my_client.isSetup))
            print('*' * 60)
        else: 
            print("unknown command")