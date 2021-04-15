# Enigma

A simple Python implementation of an Enigma Machine. It's not 1:1, I mostly just
read the basics of how they work and created a model based on that.

This model works with N rotors where N >= 1, so it should be virtually
uncrackable given enough rotors. Rotor configurations are also very easy to
share since you can create a rotor from any hashable object (notably strings).
If you wanted to discretely share a rotor configuration you could have a code
question where each word in the response is a separate rotor and the last word
is the reflector seed. For example:

> Have any plans for the weekend?

> Just going to play some Kerbal Space Program.

Then we can load a machine based on that.

``` python3
>>> enigma = Enigma(rotor_seeds='Just going to play some Kerbal Space'.split(), reflector_seed='Program.')
```

Easy. Now we'll encode a secret message using that machine configuration.

``` python3
>>> enigma('The surprise party will be at eight on Sunday')
'ROK IXJFUUPM SUGWK QWIA RS SF SLWMW IH XZDJYD'
```

Now if the receiver of the coded message creates a machine the same way, they
can run it back through and see the original secret message.

``` python3
>>> enigma = Enigma(rotor_seeds='Just going to play some Kerbal Space'.split(), reflector_seed='Program.')
>>> enigma('ROK IXJFUUPM SUGWK QWIA RS SF SLWMW IH XZDJYD')
'THE SURPRISE PARTY WILL BE AT EIGHT ON SUNDAY'
```

It's important to note that rotors are called as such for a reason, and that
each character passed through the machine alters the machine's state. This means
that if you pass the same message through multiple times you'll get different
results.


``` python3
>>> enigma = Enigma(['cat', 'dog'], 'sheep')
>>> enigma('example')
'FJPAVIS'
>>> enigma('example')
'NNYEVPP'
>>> enigma('example')
'YDXYRPQ'
>>> enigma('example')
'YDEAXVM'
```

So it's important to encode and decode messages in the exact same order to avoid
de-synchronizing and ending up with a pile of garbage. If you mess up in either
step, I've added a handy method that resets your machine to its original state
so you can start over.

``` python3
>>> enigma('Part one of the message')
'KWXL IHS YI ISS YPMUXKW'
>>> enigma('Part two has a ttypo')
'LRXH QNR UHC P SMOQP'
>>> enigma.reset()
>>> enigma('Part one of the message')
'KWXL IHS YI ISS YPMUXKW'
>>> enigma('Part two has no typos')
'LRXH QNR UHC GZ MOQPZ'
```
