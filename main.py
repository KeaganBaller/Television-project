from logic import *
import sys
def main():
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running program: {e}")
        sys.exit(0)