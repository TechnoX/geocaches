import pygame as pg 
import time


pg.mixer.init()
pg.init()

screen = pg.display.set_mode((1184,624));#, pg.FULLSCREEN)
# Initialing RGB Color 
white = (255,255,255)



all_notes = ['F3','F3#', 'G3', 'G3#', 'A3', 'A3#', 'B3', 'C4', 'C4#', 'D4', 'D4#', 'E4', 'F4']
currently_playing = [False]*len(all_notes)
pg.mixer.set_num_channels(len(all_notes))

song = ["F3", "G3", "A3", "A3#", "C4", "F4", "E4", "D4", "A3#", "D4", "C4", "A3"]
pos = 0
positions = [p-207 for p in [207, 280,340,397,452,513,602,683,745,801,870,951,1043]]

#images = []
notes = []
for note in all_notes:
    n = note.lower()
    if note[-1] == "#":
        soundfile = "tedagame__" + n[0] + "-" + n[1] + ".ogg"
        #imagefile = "piano_" + n[:2] + "s.png"
    else:
        soundfile = "tedagame__" + n + ".ogg"
        #imagefile = "piano_" + n[:2] + ".png"
    print("Loading: " + soundfile)
    notes.append(pg.mixer.Sound(soundfile))

print(notes)
melody = pg.image.load("melody3.png")
melody.convert()
#piano = pg.image.load("piano.png")
#piano.convert()
well_played = pg.image.load("well-played2.png")
well_played.convert()



def play_note(noteIndex,duration):
    #time.sleep(duration) # make a pause 
    pg.mixer.Channel(noteIndex).play(notes[noteIndex])
    time.sleep(duration) # Let the sound play
    pg.mixer.Channel(noteIndex).stop()
	
#for i in range(len(notes)):
#    play_note(i, 3)

#play_note()

#play_note(2, 0)
#play_note(5, 0)
#play_note(9, 3)
clock = pg.time.Clock()
run = True
klar = True
keys = ["up", "down", "left", "right", "w", "a", "s", "d", "f", "g", "space"]
buttons = [1, 3]
while run:
    #clock.tick(60)
    for event in pg.event.get():
        #print(event)
        t = 750
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            #print(pg.key.name(event.key))
            if klar == True:
                pos = 0
                klar = False
            for index, key in enumerate(keys):
                if pg.key.name(event.key) == key:
                    #pg.mixer.Channel(index).play(notes[index])
                    currently_playing[index] = True
                    notes[index].play()
                    if all_notes[index] == song[pos]:
                        pos += 1
                        if pos >= len(song):
                            klar = True
                    else:
                        pos = 0
            if pg.key.name(event.key) == "escape":
                pg.quit()
                exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            for index, button in enumerate(buttons):
                if event.button == button:
                    currently_playing[11+index] = True
                    notes[11+index].play()
                    if all_notes[11+index] == song[pos]:
                        pos += 1
                        if pos >= len(song):
                            klar = True
                    else:
                        pos = 0
        if event.type == pg.KEYUP:
            for index, key in enumerate(keys):
                if pg.key.name(event.key) == key:
                    #pg.mixer.Channel(index).fadeout(t)
                    currently_playing[index] = False
                    notes[index].fadeout(t)
        if event.type == pg.MOUSEBUTTONUP:
            for index, button in enumerate(buttons):
                if event.button == button:
                    currently_playing[11+index] = False
                    notes[11+index].fadeout(t)


    screen.fill(white)
    mx = 0
    my = 0
    pg.draw.rect(screen, (11, 218, 81), (mx+277,my+31,positions[pos], 100))
    screen.blit(melody, (mx,my))
    if klar:
        screen.blit(well_played, (0, 0))
    #else:
    #    screen.blit(piano, (400,500))
    
    coords = [43,81,129,170,214,263,300,385,422,471,514,556,641]
    for i in range(len(notes)):
        if currently_playing[i]:
            print("Not " + str(i) + " is playing")
            if all_notes[i][-1] == "#":
                pg.draw.circle(screen, (95, 133, 117), (200+coords[i], 460), 12)
            else:
                pg.draw.circle(screen, (193, 225, 193), (200+coords[i], 520), 25)
    
    pg.display.flip()
    clock.tick(60)
            
pg.quit()
exit()

