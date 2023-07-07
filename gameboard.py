import execjs


# Notes:
# We need to create the bag which the pieces comes out with. This we can match with a seed which needs to
# determine in what order the pieces are placed into the queue. The queue is 5 long.
# https://harddrop.com/forums/index.php?showtopic=7087&st=135&p=92057&#entry92057
# On this blog post, we get the script which chooses the piece in the queue.
# Since Alea does not exist on python we need to run the script using PyExecJS module.
# or
#
# We need to make a board represented using either numpy or a list inside a list.
# https://tetris.fandom.com/wiki/Tetris_Guideline according to this, the board needs to have the dimensions 10x40
# with pieces spawning at 20 for I piece and 21/20 for all other pieces. E.g. for the z piece, we want
# the lower half to start at 20 and the upper half starts at 21.
#
# We need to implement hold piece.
#

def get_queue(seed):
    with open('queue.js', 'r') as file:
        javascript_code = file.read()
    # It just looks at the code as a still picture. So we just run 110 getBlocks in queue.js
    # and return that to this file
    #
    context = execjs.compile(javascript_code)
    queue = context.call('getQueue', str(seed))
    return queue


class Board:
    def __int__(self, seed: str):
        self.dimensions = [['-' for _ in range(10)] for _ in range(40)]
        self.hold_piece = None
        self.pieces = get_queue(seed)
        self.queue = Queue()

    def print_board(self):
        # TODO: prints board
        pass

    def __start_queue(self):
        # There are 5 pieces in the queue.
        for i in range(5):
            self.queue.put(self.pieces.pop(0))

    def __remove_lines(self, lines: int):
        # TODO: removes 1-4 lines depending on
        pass

    def hold_cur_piece(self):
        # TODO: remove piece in queue and insert to hold block.
        #       If there already exists a piece, we swap.
        pass

    def board_height(self):
        pass


if __name__ == '__main__':
    print(get_queue("q9te4k"))
