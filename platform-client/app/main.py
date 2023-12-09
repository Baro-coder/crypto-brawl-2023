from core import Controller


def main() -> None:
    controller : Controller = Controller(
        load_strategies_data_from_files=True
    )
    try:
        controller.initialize()
        controller.work()
    
    except KeyboardInterrupt:
        print('[*] Stop.')

if __name__ == '__main__':
    main()
