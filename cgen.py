import sys
import random

from io import parsefile, printfile


def applyRules(note, previous):
    options = [3, 4, 7, 8, 9, 12]  # all intervals allowed in counterpoint
    if previous is None:
        options = [7, 12]
    else:
        prev_int = previous[1] - previous[0]
        print(prev_int)
        print(options)
        if prev_int == 3 or prev_int == 4:  # no consecutive thirds
            options.remove(3)
            options.remove(4)
        elif prev_int == 8 or prev_int == 9:  # no consecutive sixths
            options.remove(8)
            options.remove(9)
        else:
            options.remove(prev_int)  # no consecutive 5ths or octaves

        # if we would approach 5th by parallel motion
        if (note + 7) - previous[1] > 0 and (note - previous[0]) > 0:
            if 7 in options:
                options.remove(7)
        elif (note + 7) - previous[1] < 0 and (note - previous[0]) < 0:
            if 7 in options:
                options.remove(7)

    return options

def main(infile, fpath, sp):
    header, footer, notes_on, notes_off = parsefile(infile)
    # print(header)
    # print(footer)
    # print(notes_on)

    new_notes_on = []
    new_notes_off = []
    previous = None
    for idx in range(0, len(notes_on)):
        pitch = notes_on[idx][1]
        options = applyRules(pitch, previous)  # pick new pitch
        r = random.randint(0, len(options) - 1)
        new_pitch = options[r] + pitch
        previous = [pitch, new_pitch]

        new_on = [notes_on[idx][0], new_pitch]  # turn the note on with the original note
        new_off = [notes_off[idx][0], new_pitch]  # turn the note off next bar

        new_notes_on.append(notes_on[idx])
        new_notes_on.append(new_on)
        new_notes_off.append(notes_off[idx])
        new_notes_off.append(new_off)

    print(new_notes_on)
    print(new_notes_off)

    printfile(fpath, new_notes_on, new_notes_off, header, footer)


if __name__ == "__main__":
    fpath = str(sys.argv[1])
    species = int(sys.argv[2])
    try:
        f = open(fpath, "r")
    except IOError:
        print("Invalid File")
        sys.exit(1)

    main(f, fpath, species)
