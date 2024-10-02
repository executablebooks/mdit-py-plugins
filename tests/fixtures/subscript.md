.
~foo\~
.
<p>~foo~</p>
.

.
~foo bar~
.
<p>~foo bar~</p>
.

.
~foo\ bar\ baz~
.
<p><sub>foo bar baz</sub></p>
.

.
~\ foo\ ~
.
<p><sub> foo </sub></p>
.

.
~foo\\\\\\\ bar~
.
<p><sub>foo\\\ bar</sub></p>
.

.
~foo\\\\\\ bar~
.
<p>~foo\\\ bar~</p>
.

.
**~foo~ bar**
.
<p><strong><sub>foo</sub> bar</strong></p>
.


coverage
.
*~f
.
<p>*~f</p>
.

Basic:
.
H~2~O
.
<p>H<sub>2</sub>O</p>
.

Spaces:
.
H~2 O~2
.
<p>H~2 O~2</p>
.

Escaped:
.
H\~2\~O
.
<p>H~2~O</p>
.

Nested:
.
a~b~c~d~e
.
<p>a<sub>b</sub>c<sub>d</sub>e</p>
.