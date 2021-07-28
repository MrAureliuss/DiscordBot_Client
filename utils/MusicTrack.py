class MusicTrack:
    def __init__(self, player, ctx):
        self.player = player
        self.ctx = ctx

    def get_music_player(self):
        return self.player

    def get_ctx(self):
        return self.ctx
