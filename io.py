def parsefile(f):
    header_string = ""
    footer_string = ""
    notes_on = []
    notes_off = []

    seen_mid = False
    for line in f:
        lsplit = line.replace(" ", "").split(",")
        print(lsplit)
        if lsplit[2] == "Note_on_c" or lsplit[2] == "Note_off_c":
            # if this is a note we care about
            seen_mid = True
            time = int(lsplit[1])
            pitch = int(lsplit[4])
            if lsplit[2] == "Note_on_c":
                nvec = [time, pitch]
                notes_on.append(nvec)
            else:
                nvec = [time, pitch]
                notes_off.append(nvec)
        else:
            # it's preamble/postamble
            if seen_mid:
                footer_string += line
            else:
                header_string += line

    return header_string, footer_string, notes_on, notes_off


def printfile(fpath, new_notes_on, new_notes_off, header, footer):
    nfp = fpath.split(".")[0] + "_counterpoint.csv"
    f = open(nfp, "w")
    f.write(header)
    for idx in range(0, len(new_notes_on)):
        on = new_notes_on[idx]
        note_on_line = "2, " + str(on[0]) + ", Note_on_c, 0, " + str(on[1]) + ", 100\n"
        off = new_notes_off[idx]
        note_off_line = "2, " + str(off[0]) + ", Note_off_c, 0, " + str(off[1]) + ", 0\n"

        f.write(note_on_line)
        f.write(note_off_line)

    f.write(footer)
