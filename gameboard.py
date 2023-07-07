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



if __name__ == '__main__':
    print(get_queue("q9te4k"))
