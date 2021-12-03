Body alignment:
.
:no body:

:single line: content
:paragraph: content
  running onto new line
:body inline: paragraph 1

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
      code
:name: body

           code
.
<dl class="field-list">
<dt>name</dt>
<dd>
<pre><code>code
</code></pre>
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
.
<blockquote>
<dl class="field-list">
<dt>name</dt>
<dd>
<p>body</p>
</dd>
</dl>
</blockquote>
.
