basic
.
::name This is the content
.
<div class="name">
<p>This is the content</p>
</div>
.

multiline
.
::name This is the content
it can run onto multiple lines

But is interrupted by a blank line
.
<div class="name">
<p>This is the content
it can run onto multiple lines</p>
</div>
<p>But is interrupted by a blank line</p>
.

must have two :
.
:name This is the content
.
<p>:name This is the content</p>
.

but not three :
.
:::name This is the content
.
<p>:::name This is the content</p>
.

must be proceeded by a non-whitespace charater
.
::

:: This is the content
.
<p>::</p>
<p>:: This is the content</p>
.

Just a name
.
::name
.
<div class="name"></div>
.

Just a name with a space
.
::name 
.
<div class="name"></div>
.

It does not interrupt paragraphs or other blocks
.
Paragraph

::name This is the content

Paragraph
::name This is the content

- list
::name This is the content
.
<p>Paragraph</p>
<div class="name">
<p>This is the content</p>
</div>
<p>Paragraph
::name This is the content</p>
<ul>
<li>list
::name This is the content</li>
</ul>
.
