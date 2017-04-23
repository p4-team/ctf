Alice and Bob are communicating with their fancy new QKD devices. Their protocol is fairly standard, but we've
learned enough details to be worth reporting.

Alice generates 600 qubits, each with a random (Y or Z) basis and (-1 or 1) value. Alice sends each of these
qubits to Bob, who acknowledges their receipt with a 1 in the Z basis.

As soon as Bob receives the 600th qubit, he begins to transmit his guessed bases to Alice. He sends these via the
Z basis, with -1 corresponding to a Z, and a 1 corresponding to a Y. After each guess, Alice will tell Bob if the guess
was in the correct basis or not (a 1 in the Z basis means correct, a -1 means wrong).

As soon as Bob finishes these transmissions, Alice and Bob make sure no one was listening to their exchange. Bob
takes every other measurement he made where Alice verified the basis as correct (so he takes the 0th agreed value, the
2nd agreed value, 4th, and so on). He sends the values he measured on these positions to Alice using the Z basis.
If Alice disagrees with any of the value sent, this means an eavesdropper was on the line, and she immediately aborts.
Otherwise, she sends Bob an ACK in the form of a 1 in the Z basis.

After this phase has completed, Alice and Bob trust that there was not an eavesdropper present on the line. They use
the first 128 agreed measurements which were not already spent (so the 1st, 3rd, 5th, and so on agreed values) to 
establish a shared AES key (the 128 values are treated as as 128bit binary key, -1 corresponding to 0, and 1 to 1)
If there are not 128 unused values on which Alice and Bob agree on the bases, then the connection is aborted.

Finally, Alice and Bob each send their 200% secure AES128-ECB encrypted message!
