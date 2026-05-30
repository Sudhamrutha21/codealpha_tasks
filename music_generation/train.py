from music21 import converter, note
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

midi = converter.parse("dataset/twinkle.mid")

notes = []

for element in midi.flat.notes:
    if isinstance(element, note.Note):
        notes.append(str(element.pitch))

unique_notes = sorted(set(notes))

note_to_int = dict((n, i) for i, n in enumerate(unique_notes))

sequence_length = 5

X = []
y = []

for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i+sequence_length]
    seq_out = notes[i+sequence_length]

    X.append([note_to_int[n] for n in seq_in])
    y.append(note_to_int[seq_out])

X = np.reshape(X, (len(X), sequence_length, 1))
X = X / float(len(unique_notes))

y = np.array(y)

model = Sequential()
model.add(LSTM(64, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(len(unique_notes), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam')

model.fit(X, y, epochs=20, batch_size=8)

model.save("model/music_model.keras")

print("Training completed")