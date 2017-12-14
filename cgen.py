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

        for n in options:
            if abs((note + n) - previous[1]) > 7:
                options.remove(n)

    return options


def main(infile, fpath, species, b):
    header, footer, notes_on, notes_off = parsefile(infile)
    # print(header)
    # print(footer)
    # print(notes_on)

    half_bar = (notes_on[1][0] - notes_on[0][0]) / 2

    for b in range(1, batch + 1):
        new_notes_on = []
        new_notes_off = []
        previous = None
        for idx in range(0, len(notes_on) - 2):
            pitch = notes_on[idx][1]
            options = applyRules(pitch, previous)  # pick new pitch
            r = random.randint(0, len(options) - 1)
            new_pitch = options[r] + pitch
            previous = [pitch, new_pitch]

            new_on = [notes_on[idx][0], new_pitch]  # turn the note on with the original note
            if species == 1:  # first species
                new_off = [notes_off[idx][0], new_pitch]  # turn the note off next bar
            else:  # second species
                new_off = [notes_off[idx][0] - half_bar, new_pitch]  # half bar off instead
                options = applyRules(pitch, previous)  # pick new pitch using 1st again
                r = random.randint(0, len(options) - 1)
                new_pitch = options[r] + pitch
                previous = [pitch, new_pitch]

                new_on2 = [notes_on[idx][0] + half_bar, new_pitch]  # place half bar forward
                new_off2 = [notes_off[idx][0], new_pitch]  # turn off end of bar

            new_notes_on.append(notes_on[idx])
            new_notes_on.append(new_on)
            new_notes_off.append(new_off)
            if species > 1:
                new_notes_on.append(new_on2)
                new_notes_off.append(new_off2)
            new_notes_off.append(notes_off[idx])

        stl_on = notes_on[len(notes_on) - 2]  # last 6th
        stl_off = notes_off[len(notes_off) - 2]
        new_stl_on = [stl_on[0], stl_on[1] + 9]
        new_stl_off = [stl_off[0], stl_off[1] + 9]

        l_on = notes_on[len(notes_on) - 1]  # last 8th
        l_off = notes_off[len(notes_off) - 1]
        new_l_on = [l_on[0], l_on[1] + 12]
        new_l_off = [l_off[0], l_off[1] + 12]

        new_notes_on.append(stl_on)  # append stl
        new_notes_on.append(new_stl_on)
        new_notes_off.append(stl_off)
        new_notes_off.append(new_stl_off)

        new_notes_on.append(l_on)  # append l
        new_notes_on.append(new_l_on)
        new_notes_off.append(l_off)
        new_notes_off.append(new_l_off)

        for i in range(0, len(new_notes_on)):
            print(new_notes_on[i])
            print(new_notes_off[i])

        printfile(str(b) + "_" + fpath, new_notes_on, new_notes_off, header, footer, species)


if __name__ == "__main__":
    fpath = str(sys.argv[1])
    species = int(sys.argv[2])
    try:
        batch = int(sys.argv[3])
    except IndexError:
        batch = 1
    try:
        f = open(fpath, "r")
    except IOError:
        print("Invalid File")
        sys.exit(1)

    main(f, fpath, species, batch)
