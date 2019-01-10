import vlc

Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new('data/test2.mkv')

player.set_media(Media)
player.play()