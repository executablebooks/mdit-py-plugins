simple reference link
.
[text *emphasis*](a){#id .a}
.
<p><a href="a" id="id" class="a">text <em>emphasis</em></a></p>
.

simple definition link
.
[a][]{#id .b}

[a]: /url
.
<p><a href="/url" id="id" class="b">a</a></p>
.

simple image
.
![a](b){#id .a b=c}
.
<p><img src="b" alt="a" id="id" b="c" class="a"></p>
.

simple inline code
.
`a`{#id .a b=c}
.
<p><code id="id" b="c" class="a">a</code></p>
.

ignore if space
.
![a](b) {#id key="*"}
.
<p><img src="b" alt="a"> {#id key=&quot;*&quot;}</p>
.

ignore if text
.
![a](b)b{#id key="*"}
.
<p><img src="b" alt="a">b{#id key=&quot;*&quot;}</p>
.

multi-line
.
![a](b){
    #id .a
    b=c
    }
more
.
<p><img src="b" alt="a" id="id" b="c" class="a">
more</p>
.

combined
.
![a](b){#a .a}{.b class=x other=h}{#x class="x g" other=a}
.
<p><img src="b" alt="a" id="x" class="a b x x g" other="a"></p>
.
