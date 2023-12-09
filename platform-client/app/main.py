from core import Controller


def main() -> None:
    controller : Controller = Controller()
    try:
        controller.initialize()
        controller.work()
    
    except KeyboardInterrupt:
        print('[*] Stop.')

if __name__ == '__main__':
    main()
