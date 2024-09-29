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

Strikethrough versus subscript:
.
~~strikethrough~~ versus ~subscript~
.
<p><s>strikethrough</s> versus <sub>subscript</sub></p>
.

Subscript in strikethrough (beginning):
.
~~~subscript~ in the beginning within a strikethrough is perceived as first line of a code block and hence ignored~~
.
<pre><code class="language-subscript~"></code></pre>
.

Strikethrough in subscript (beginning):
.
~~~strikethrough~ in the beginning within a subscript is perceived as first line of a code block and hence ignored~~
.
<pre><code class="language-strikethrough~"></code></pre>
.

Subscript in strikethrough (end):
.
~~strikethrough contains ~subscript~~~
.
<p><s>strikethrough contains <sub>subscript</sub></s></p>
.

Strikethrough in subscript (end):
.
~subscript contains ~~strikethrough~~~
TODO: This is not rendered correctly in markdown-it either, but can be fixed
.
<p>~subscript contains <s>strikethrough</s>~
TODO: This is not rendered correctly in markdown-it either, but can be fixed</p>
.

Subscript in strikethrough:
.
~~strikethrough with ~subscript~ text~~
.
<p><s>strikethrough with <sub>subscript</sub> text</s></p>
.

Strikethrough in subscript:
.
~subscript contains ~~strikethrough~~ text~
TODO: This is not rendered correctly in markdown-it either, but can be fixed
.
<p>~subscript contains <s>strikethrough</s> text~
TODO: This is not rendered correctly in markdown-it either, but can be fixed</p>
.