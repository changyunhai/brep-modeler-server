import time, re, json
import argparse
import socketio
import sys

sio = socketio.Client()
isConnected: bool = False
EVENT_HANDLER_EXCLUDES: list[str] = ["documentLoadBrep"]


def eventHandler(data):
    print("------\nEVENT RESULT:\n", data)


def parseArguments(argv: list[str]):
    evt_type, *event_args = argv
    documentid, *cmd = event_args
    # print(f"event_type={evt_type}, document_id={documentid}, cmd={cmd}")
    if evt_type not in EVENT_HANDLER_EXCLUDES:
        sio.on(f"on_{evt_type}", eventHandler)
    sio.emit(evt_type, data=event_args)


@sio.event
def connect():
    global isConnected
    isConnected = True
    print(f"---- connected ----")


@sio.on('on_error')
def on_error(err):
    print(f"    !!! ERROR !!! \n {err}")


@sio.event
def disconnect():
    print("disconnected!")


# --------------------main------------------

if __name__ == '__main__':
    # command line arguments:
    parser = argparse.ArgumentParser(description="python modeler connector client")
    parser.add_argument('-d', '--documentid', default="document_001", type=str, help='set interactive documentid')
    parser.add_argument('--server', default='http://localhost:8810/', type=str, help="workstation socketio server")
    parser.add_argument('--max_connection_count', default=30, type=int, help='set max server connection count')
    args = parser.parse_args()

    server = args.server
    documentid: str = args.documentid

    sio.connect(server)
    connectTrying: int = 0

    while not isConnected:
        time.sleep(0.1)
        connectTrying += 1
        if connectTrying > args.max_connection_count:
            print('connect refuse, check socketio server:', server)
            sys.exit(0)

    while True:
        try:
            time.sleep(1)
            cmdStr: str = input("-----------------------------------------------\nEnter the command, 'help' to get all, 'exit' for quit:\n")
            cmdStr = cmdStr.strip()
            if cmdStr == 'exit':
                sio.disconnect()
                sys.exit(0)

            argStr: str = input("Enter command arguments, in 'str' or json array format:\n")
            argStr = argStr.strip()
            cmds = json.loads(argStr) if len(argStr) > 0 else []
            if not isinstance(cmds, list):
                cmds = [cmds]
            cmds.insert(0, documentid)
            cmds.insert(0, cmdStr)

            print(f"cmd={cmds}")
            parseArguments(cmds)
        except Exception as err:
            print("got exception:\t\t", str(err))
