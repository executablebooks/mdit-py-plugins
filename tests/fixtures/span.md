simple
.
[a]{#id .b}c
.
<p><span id="id" class="b">a</span>c</p>
.

space between brace and attrs
.
[a] {.b}
.
<p>[a] {.b}</p>
.

escaped span start
.
\[a]{.b}
.
<p>[a]{.b}</p>
.

escaped span end
.
[a\]{.b}
.
<p>[a]{.b}</p>
.

escaped span attribute
.
[a]\{.b}
.
<p>[a]{.b}</p>
.

nested text syntax
.
[*a*]{.b}c
.
<p><span class="b"><em>a</em></span>c</p>
.

nested span
.
*[a]{.b}c*
.
<p><em><span class="b">a</span>c</em></p>
.

multi-line
.
x [a
b]{#id
b=c} y
.
<p>x <span id="id" b="c">a
b</span> y</p>
.

nested spans
.
[[a]{.b}]{.c}
.
<p><span class="c"><span class="b">a</span></span></p>
.

short link takes precedence over span
.
[a]{#id .b}

[a]: /url
.
<p><a href="/url">a</a>{#id .b}</p>
.

long link takes precedence over span
.
[a][a]{#id .b}

[a]: /url
.
<p><a href="/url">a</a>{#id .b}</p>
.

link inside span
.
[[a]]{#id .b}

[a]: /url
.
<p><span id="id" class="b"><a href="/url">a</a></span></p>
.
