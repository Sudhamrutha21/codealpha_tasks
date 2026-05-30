from music21 import converter, note, stream
import numpy as np
from tensorflow.keras.models import load_model

midi = converter.parse("dataset/twinkle.mid")

notes = []

for element in midi.flat.notes:
    if isinstance(element, note.Note):
        notes.append(str(element.pitch))

unique_notes = sorted(set(notes))

note_to_int = dict((n, i) for i, n in enumerate(unique_notes))
int_to_note = dict((i, n) for i, n in enumerate(unique_notes))

sequence_length = 5

model = load_model("model/music_model.keras")

pattern = [note_to_int[n] for n in notes[:5]]

prediction_output = []

for _ in range(30):

    prediction_input = np.reshape(
        pattern,
        (1, sequence_length, 1)
    )

    prediction_input = prediction_input / float(len(unique_notes))

    prediction = model.predict(
        prediction_input,
        verbose=0
    )

    index = np.argmax(prediction)

    result = int_to_note[index]

    prediction_output.append(result)

    pattern.append(index)
    pattern = pattern[1:]

output_notes = []

offset = 0

for pattern in prediction_output:
    new_note = note.Note(pattern)
    new_note.offset = offset
    output_notes.append(new_note)

    offset += 0.5

midi_stream = stream.Stream(output_notes)

midi_stream.write(
    'midi',
    fp='output/generated.mid'
)

print("generated.mid created")