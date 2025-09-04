import music21
def note_to_abc(note_input):
    """
    Converts a music note into its ABC notation pitch representation.

    Args:
        note_input (str or music21.note.Note): The note to convert.
            Can be a string like "C#4" or "Bb5", or a music21.note.Note object.

    Returns:
        str: The note's pitch represented in ABC notation (e.g., "^C", "b'", "_G,").
        Returns an empty string if the input is invalid.
    """
    try:
        # Step 1: Ensure we have a music21 Pitch object
        if isinstance(note_input, str):
            p = music21.pitch.Pitch(note_input)
        elif isinstance(note_input, music21.note.Note):
            p = note_input.pitch
        elif isinstance(note_input, music21.pitch.Pitch):
            p = note_input
        else:
            raise ValueError("Input must be a string, music21.note.Note, or music21.pitch.Pitch")

    except (music21.pitch.PitchException, ValueError) as e:
        print(f"Error processing input: {e}")
        return ""

    # Step 2: Convert the accidental
    abc_accidental = ""
    if p.accidental:
        accidental_map = {
            'sharp': '^',
            'double-sharp': '^^',
            'flat': '_',
            'double-flat': '__',
            'natural': '='
        }
        # Get the ABC symbol from the map, defaulting to empty string if not found
        abc_accidental = accidental_map.get(p.accidental.name, "")

    # Step 3: Determine the base note and octave modifier
    octave = p.octave
    base_note = ""
    octave_modifier = ""

    # Octave 4 (e.g., C4) and above use lowercase letters
    if octave >= 4:
        base_note = p.step.lower()
        # Octave 5 and higher add apostrophes
        if octave > 4:
            octave_modifier = "'" * (octave - 4)
    # Octave 3 (e.g., C3) and below use uppercase letters
    else:  # octave < 4
        base_note = p.step.upper()
        # Octave 2 and lower add commas
        if octave < 3:
            octave_modifier = "," * (3 - octave)
            
    # Step 4: Assemble the final ABC string
    return f"{abc_accidental}{base_note}{octave_modifier}"