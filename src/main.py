"""
Bowl
====

Simulation of bowling like games
"""

def sum_next_move(frames: list, index: int, n=2):
    """
    Compute {n} next move

    Args:
        frames (list): Frames liste
        index (int): Index of one frame that contain ("STRIKE" or "SPARE)
        n (int, optional): number of next move. Defaults to 2.

    Returns:
        int: Sum of {n} next move
    """

    frame = frames[index]
    result = []

    if "STRIKE" in frame:
        start_index = frame.index("STRIKE") + 1
    if "SPARE" in frame:
        start_index = frame.index("SPARE") + 1

    while len(result) < n:
        while True:
            if frame is None:
                result.append(0)
                break

            try:
                launch = frame[start_index]  # can produce IndexError
                if launch is not None:
                    result.append(launch)
            except IndexError:  # Jump to next frame
                start_index = 0
                index += 1

                try:
                    frame = frames[index]
                except IndexError:  # No next frame
                    result.append(0)

            else:
                start_index += 1
                break

    result = map(
        lambda score: 15 if score in ["STRIKE", "SPARE"] else score,
        result
    )
    return sum(result)


class Game:
    def __init__(self, launchs: list = [None]*3, keels: int = 15):
        self.default_launchs = launchs
        self.default_keels = keels

        self.frames = [None] * 5
        self.launchs = self.default_launchs.copy()
        self.keels = self.default_keels

        self.last_extended = False  # Used when last frame should be extended
        self.finished = False

    def get_touched_keels(self) -> int:
        while True:
            # Loop until receive a valid input
            try:
                return int(input("Nombre de quilles touchées: "))
            except ValueError:
                pass

    def touch_keels(self, number: int):
        if number > self.keels:
            raise ValueError("Number can't be greater than self.keels")

        self.keels -= number

        if self.keels == 0:
            return "STRIKE" if (self.launch_num == 1) else "SPARE"
        else:
            return number

    def write_score(self, score):
        # -1 because array start at 0
        self.launchs[self.launch_num - 1] = score

        if (score in ("STRIKE", "SPARE")) and (not self.last_extended):
            while True:  # remove all None
                try:
                    self.launchs.remove(None)
                except ValueError:
                    break

    def check_frame(self):
        """
        Check and jump to next frame when needed
        """

        if self.launch_left == 0:
            if (
                (self.frame_left == 1) and
                (("STRIKE" in self.launchs) or ("SPARE" in self.launchs)) and
                (self.frame_num == 5) and
                (not self.last_extended)
            ):
                self.last_extended = True

                if "STRIKE" in self.launchs:
                    self.launchs.extend([None] * 3)
                if "SPARE" in self.launchs:
                    self.launchs.extend([None] * 2)
            else:
                # Append finised launchs to self.frames
                self.frames[self.frame_num - 1] = self.launchs.copy()

                # reset (self.launchs and self.keels)
                self.launchs = self.default_launchs.copy()
                self.keels = self.default_keels

        if self.last_extended and (self.keels == 0):
            self.keels = self.default_keels

        self.finished = (self.frame_left == 0)

    @property
    def frame_left(self) -> int:
        return self.frames.count(None)

    @property
    def launch_left(self) -> int:
        return self.launchs.count(None)

    @property
    def frame_num(self) -> int:
        return (len(self.frames) + 1) - self.frame_left

    @property
    def launch_num(self) -> int:
        return (len(self.launchs) + 1) - self.launch_left

    @property
    def current_score(self) -> int:
        result = 0
        for index, launchs in enumerate(self.frames):
            if launchs is None:
                continue

            elif "STRIKE" in launchs:
                next_3move = sum_next_move(
                    self.frames,
                    index=index,
                    n=3, )

                result += (15 + next_3move)

            elif "SPARE" in launchs:
                next_2move = sum_next_move(
                    self.frames,
                    index=index,
                    n=2, )

                result += (15 + next_2move)

            else:
                for score in launchs:
                    result += score

        return result

    def launch(self, value=-1) -> bool:
        """
        Launch Bowl and receive touched keels in {value}

        Args:
            value (int, optional):
                Touched keels.
                -1 Mean get value from input
                Defaults to -1.
        """

        if self.finished:
            print("Game is finished")
            return True

        print(f"Frame Numéro: {self.frame_num}")
        print(f"Lancer Numéro: {self.launch_num}")

        if value == -1:
            touched_keels = self.get_touched_keels()
        else:
            touched_keels = value

        try:
            scored = self.touch_keels(touched_keels)
        except ValueError as e:
            print(e)
            return False

        self.write_score(scored)
        self.check_frame()

        print(f"Score: {self.current_score}")
        print("-------")

        return self.finished

    def loop(self):
        while True:
            finished = self.launch()

            if finished:
                break


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
