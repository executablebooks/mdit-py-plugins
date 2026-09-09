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

block: attrs last in a blockquote
.
> {.a}

para
.
<blockquote></blockquote>
<p>para</p>
.

block: attrs last in a list item
.
- {.a}
.
<ul>
<li></li>
</ul>
.

block: attrs last in an ordered list item
.
1. {.a}
.
<ol>
<li></li>
</ol>
.

block: two attrs blocks last in a blockquote
.
> {.a}
> {.b}
.
<blockquote></blockquote>
.

block: attrs before a blockquote containing only attrs
.
{.a}
{.b}
> {.c}
.
<blockquote class="a b"></blockquote>
.

block: attrs followed by a paragraph in a blockquote
.
> {.a}
> para
.
<blockquote>
<p class="a">para</p>
</blockquote>
.

block after paragraph
.
a
{#a .a c=1}
.
<p>a
{#a .a c=1}</p>
.

unterminated: block group is not an attribute block
.
{.a
para
.
<p>{.a
para</p>
.

comment: block
.
{%x}
para
.
<p>para</p>
.

comment: block after a class
.
{.a %c}
para
.
<p class="a">para</p>
.

comment: block closed by a percent
.
{% just a comment %}
para
.
<p>para</p>
.

comment: block with a brace inside the comment
.
{% x } y %}
para
.
<p>para</p>
.

comment: block, attributes after a brace inside the comment
.
{% c } % .b}
para
.
<p class="b">para</p>
.

comment: block, a brace inside the comment does not terminate the group
.
{% see } below %{x}
para
.
<p>{% see } below %{x}
para</p>
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

quoted value keeps a backslash escape
.
`a`{k="a\"b"}
.
<p><code k="a\&quot;b">a</code></p>
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

unterminated: inline code
.
`a`{
.
<p><code>a</code>{</p>
.

unterminated: inline code with a class
.
`a`{.a
.
<p><code>a</code>{.a</p>
.

unterminated: link
.
[a](u){
.
<p><a href="u">a</a>{</p>
.

unterminated: image
.
![a](u){.x
.
<p><img src="u" alt="a">{.x</p>
.

unterminated: following text is not consumed
.
`a`{.a
more
.
<p><code>a</code>{.a
more</p>
.

unterminated: group after a terminated group
.
`a`{.a}{
.
<p><code class="a">a</code>{</p>
.

unterminated: partially scanned attributes are not applied
.
`a`{ .a b
.
<p><code>a</code>{ .a b</p>
.

unterminated: escaped brace inside a quoted value
.
`a`{k="a\}
.
<p><code>a</code>{k=&quot;a}</p>
.

unterminated: inside a link label
.
[x `a`{.a](u)
.
<p><a href="u">x <code>a</code>{.a</a></p>
.

comment: inline code
.
`a`{%c}
.
<p><code>a</code></p>
.

comment: after a class
.
`a`{.a %c}
.
<p><code class="a">a</code></p>
.

comment: link
.
[a](u){%c}
.
<p><a href="u">a</a></p>
.

comment: closed by a brace, following text is kept
.
`a`{%a}b
.
<p><code>a</code>b</p>
.

comment: a brace inside a comment closed by a percent
.
`a`{% x } y %}
.
<p><code>a</code></p>
.

comment: attributes after a brace inside the comment
.
`a`{.a % c } % #i}
.
<p><code id="i" class="a">a</code></p>
.

comment: an empty comment containing a brace
.
`a`{% } %}
.
<p><code>a</code></p>
.

comment: text after a brace-closed comment is kept
.
`a`{.a %c} and {more}
.
<p><code class="a">a</code> and {more}</p>
.

comment: a later percent keeps a brace-closed comment open
.
`a`{.a %c} and 100% sure
.
<p><code>a</code>{.a %c} and 100% sure</p>
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

spans: unterminated attributes are not a span
.
[a]{
.
<p>[a]{</p>
.

spans: unterminated attributes with a class are not a span
.
[a]{.x
.
<p>[a]{.x</p>
.

spans: comment
.
[a]{%c}
.
<p><span>a</span></p>
.

spans: a brace inside an unterminated comment is not a span
.
[a]{% a } %{b}
.
<p>[a]{% a } %{b}</p>
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
<p><span id="b" class="a a b" other="d">a</span></p>
.

spans: merge classes from two groups
.
[a]{.x}{.y}
.
<p><span class="x y">a</span></p>
.

spans: merge classes from three groups
.
[a]{.x}{.y}{.z}
.
<p><span class="x y z">a</span></p>
.

spans: merge classes with an id in each group
.
[a]{.x #p}{.y #q}
.
<p><span id="q" class="x y">a</span></p>
.

spans: merge classes on the outer of nested spans
.
[[a]{.i}]{.x}{.y}
.
<p><span class="x y"><span class="i">a</span></span></p>
.

links: merge classes from two groups
.
[a](u){.x}{.y}
.
<p><a href="u" class="x y">a</a></p>
.

links: merge classes from three groups
.
[a](u){.x}{.y}{.z}
.
<p><a href="u" class="x y z">a</a></p>
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
