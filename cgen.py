import sys
import random

from io import parsefile, printfile


def applyRules(note, previous):
    pass


def main(infile, fpath, sp):
    header, footer, notes_on, notes_off = parsefile(infile)
    # print(header)
    # print(footer)
    # print(notes_on)

    printfile(fpath, notes_on, notes_off, header, footer)
    return

    new_notes_on = []
    new_notes_off = []
    previous = []
    for idx in range(0, len(notes_on)):
        pitch = notes_on[idx][1]
        options = applyRules(pitch, previous)  # pick new pitch
        r = random.randint(0, len(options))
        new_pitch = options[r]
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
