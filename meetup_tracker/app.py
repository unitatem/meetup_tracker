from .meetup import Meetup


def main():
    print("App is running...")

    meetup = Meetup()
    meetup.track()

    input("Press Enter to continue...")
