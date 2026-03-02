block with preceding text is not a block
.
{#a .a b=c} a
.
<p>{#a .a b=c} a</p>
.

block no preceding
.
{#a .a c=1}
.

.

block basic
.
{#a .a c=1}
a
.
<p id="a" c="1" class="a">a</p>
.

multiple blocks
.
{#a .a c=1} 

 {#b .b c=2}
a
.
<p id="b" c="2" class="a b">a</p>
.

block list
.
{#a .a c=1}
- a
.
<ul id="a" c="1" class="a">
<li>a</li>
</ul>
.

block quote
.
{#a .a c=1}
> a
.
<blockquote id="a" c="1" class="a">
<p>a</p>
</blockquote>
.

block fence
.
{#a .b c=1}
```python
a = 1
```
.
<pre><code id="a" c="1" class="b language-python">a = 1
</code></pre>
.

block after paragraph
.
a
{#a .a c=1}
.
<p>a
{#a .a c=1}</p>
.


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

merging attributes
.
![a](b){#a .a}{.b class=x other=h}{#x class="x g" other=a}
.
<p><img src="b" alt="a" id="x" class="a b x x g" other="a"></p>
.

spans: simple
.
[a]{#id .b}c
.
<p><span id="id" class="b">a</span>c</p>
.

spans: end of inline before attrs
.
[a]
.
<p>[a]</p>
.

spans: space between brace and attrs
.
[a] {.b}
.
<p>[a] {.b}</p>
.

spans: escaped span start
.
\[a]{.b}
.
<p>[a]{.b}</p>
.

spans: escaped span end
.
[a\]{.b}
.
<p>[a]{.b}</p>
.

spans: escaped span attribute
.
[a]\{.b}
.
<p>[a]{.b}</p>
.

spans: nested text syntax
.
[*a*]{.b}c
.
<p><span class="b"><em>a</em></span>c</p>
.

spans: nested span
.
*[a]{.b}c*
.
<p><em><span class="b">a</span>c</em></p>
.

spans: multi-line
.
x [a
b]{#id
b=c} y
.
<p>x <span id="id" b="c">a
b</span> y</p>
.

spans: nested spans
.
[[a]{.b}]{.c}
.
<p><span class="c"><span class="b">a</span></span></p>
.

spans: short link takes precedence over span
.
[a]{#id .b}

[a]: /url
.
<p><a href="/url" id="id" class="b">a</a></p>
.

spans: long link takes precedence over span
.
[a][a]{#id .b}

[a]: /url
.
<p><a href="/url" id="id" class="b">a</a></p>
.

spans: link inside span
.
[[a]]{#id .b}

[a]: /url
.
<p><span id="id" class="b"><a href="/url">a</a></span></p>
.

spans: merge attributes
.
[a]{#a .a}{#b .a .b other=c}{other=d}
.
<p><span id="b" class="a b" other="d">a</span></p>
.

Indented by 4 spaces
.
    {#a .a b=c}
    # head
.
<pre><code>{#a .a b=c}
# head
</code></pre>
.

Indented by 4 spaces, DISABLE-CODEBLOCKS
.
    {#a .a b=c}
    # head
.
<h1 id="a" b="c" class="a">head</h1>
.
