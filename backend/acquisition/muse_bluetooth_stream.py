from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

class MuseEEG:

    def __init__(self):

        params = BrainFlowInputParams()

        self.board = BoardShim(BoardIds.MUSE_S_BOARD.value, params)

    def start(self):

        self.board.prepare_session()
        self.board.start_stream()

    def get_data(self):

        return self.board.get_current_board_data(256)