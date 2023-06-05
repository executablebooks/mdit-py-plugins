Docutils example
.
:Date: 2001-08-16
:Version: 1
:Authors: - Me
          - Myself
          - I
:Indentation: Since the field marker may be quite long, the second
   and subsequent lines of the field body do not have to line up
   with the first line, but they must be indented relative to the
   field name marker, and they must line up with each other.
:Parameter i: integer
.
<dl class="field-list">
<dt>Date</dt>
<dd>
<p>2001-08-16</p>
</dd>
<dt>Version</dt>
<dd>
<p>1</p>
</dd>
<dt>Authors</dt>
<dd>
<ul>
<li>Me</li>
<li>Myself</li>
<li>I</li>
</ul>
</dd>
<dt>Indentation</dt>
<dd>
<p>Since the field marker may be quite long, the second
and subsequent lines of the field body do not have to line up
with the first line, but they must be indented relative to the
field name marker, and they must line up with each other.</p>
</dd>
<dt>Parameter i</dt>
<dd>
<p>integer</p>
</dd>
</dl>
.

Body alignment:
.
:no body:

:single line: content
:paragraph: content
  running onto new line
:body inline: paragraph 1

              paragraph 2
                
              paragraph 3

:body less: paragraph 1

    paragraph 2
                
    paragraph 3

:body on 2nd line:
  paragraph 1

  paragraph 2

:body on 3rd line:

  paragraph 1

  paragraph 2
.
<dl class="field-list">
<dt>no body</dt>
<dd></dd>
<dt>single line</dt>
<dd>
<p>content</p>
</dd>
<dt>paragraph</dt>
<dd>
<p>content
running onto new line</p>
</dd>
<dt>body inline</dt>
<dd>
<p>paragraph 1</p>
<p>paragraph 2</p>
<p>paragraph 3</p>
</dd>
<dt>body less</dt>
<dd>
<p>paragraph 1</p>
<p>paragraph 2</p>
<p>paragraph 3</p>
</dd>
<dt>body on 2nd line</dt>
<dd>
<p>paragraph 1</p>
<p>paragraph 2</p>
</dd>
<dt>body on 3rd line</dt>
<dd>
<p>paragraph 1</p>
<p>paragraph 2</p>
</dd>
</dl>
.

choose smallest indent
.
:name: a

     b

   c
.
<dl class="field-list">
<dt>name</dt>
<dd>
<p>a</p>
<p>b</p>
<p>c</p>
</dd>
</dl>
.

Empty name:
.
::
.
<p>::</p>
.

Whitespace only name:
.
: :
.
<p>: :</p>
.

Name markup:
.
:inline *markup*:
.
<dl class="field-list">
<dt>inline <em>markup</em></dt>
<dd></dd>
</dl>
.

Content paragraph markup:
.
:name: body *markup*
.
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body <em>markup</em></p>
</dd>
</dl>
.

Body list:
.
:name:
  - item 1
  - item 2
:name: - item 1
       - item 2
.
<dl class="field-list">
<dt>name</dt>
<dd>
<ul>
<li>item 1</li>
<li>item 2</li>
</ul>
</dd>
<dt>name</dt>
<dd>
<ul>
<li>item 1</li>
<li>item 2</li>
</ul>
</dd>
</dl>
.

Body code block
.
:name:
      not code
:name: body

           code
.
<dl class="field-list">
<dt>name</dt>
<dd>
<p>not code</p>
</dd>
<dt>name</dt>
<dd>
<p>body</p>
<pre><code>code
</code></pre>
</dd>
</dl>
.

Body blockquote:
.
:name:
  > item 1
  > item 2
:name: > item 1
       > item 2
.
<dl class="field-list">
<dt>name</dt>
<dd>
<blockquote>
<p>item 1
item 2</p>
</blockquote>
</dd>
<dt>name</dt>
<dd>
<blockquote>
<p>item 1
item 2</p>
</blockquote>
</dd>
</dl>
.

Body fence:
.
:name:
  ```python
  code
  ```
.
<dl class="field-list">
<dt>name</dt>
<dd>
<pre><code class="language-python">code
</code></pre>
</dd>
</dl>
.

Following blocks:
.
:name: body
- item 1
:name: body
> block quote
:name: body
```python
code
```
:name: body
    more

   more
trailing

other
.
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body</p>
</dd>
</dl>
<ul>
<li>item 1</li>
</ul>
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body</p>
</dd>
</dl>
<blockquote>
<p>block quote</p>
</blockquote>
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body</p>
</dd>
</dl>
<pre><code class="language-python">code
</code></pre>
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body
more</p>
<p>more
trailing</p>
</dd>
</dl>
<p>other</p>
.

In list:
.
- :name: body
- item 2
.
<ul>
<li>
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body</p>
</dd>
</dl>
</li>
<li>item 2</li>
</ul>
.

In blockquote:
.
> :name: body
> :name: body
>   other
> :name: body
>
>     other
> :name: body
>
>          other
.
<blockquote>
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body</p>
</dd>
<dt>name</dt>
<dd>
<p>body
other</p>
</dd>
<dt>name</dt>
<dd>
<p>body</p>
<p>other</p>
</dd>
<dt>name</dt>
<dd>
<p>body</p>
<p>other</p>
</dd>
</dl>
</blockquote>
.


Indented by 4 spaces
.
    :name: text
        indented
.
<pre><code>:name: text
    indented
</code></pre>
.

Indented by 4 spaces, DISABLE-CODEBLOCKS
.
    :name: text
        indented
.
<dl class="field-list">
<dt>name</dt>
<dd>
<p>text
indented</p>
</dd>
</dl>
.
