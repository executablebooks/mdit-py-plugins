
Simple admonition
.
!!! note
    *content*
.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p><em>content</em></p>
</div>
.


Could contain block elements too
.
!!! note
    ### heading

    -----------

.
<div class="admonition note">
<p class="admonition-title">Note</p>
<h3>heading</h3>
<hr>
</div>
.


Shows custom title
.
!!! note Custom title

    Some text

.
<div class="admonition note">
<p class="admonition-title">Custom title</p>
<p>Some text</p>
</div>
.


Shows no title
.
!!! note ""
    Some text

.
<div class="admonition note">
<p>Some text</p>
</div>
.


Closes block after 2 empty lines
.
!!! note 
    Some text


    A code block
.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Some text</p>
</div>
<pre><code>A code block
</code></pre>
.


Nested blocks
.
!!! note
    !!! note
        Some text
            
            code block
.
<div class="admonition note">
<p class="admonition-title">Note</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Some text</p>
<pre><code>code block
</code></pre>
</div>
</div>
.


Consecutive admonitions
.
!!! note

!!! warning
.
<div class="admonition note">
<p class="admonition-title">Note</p>
</div>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
</div>
.


Marker may be indented up to 3 chars
.
   !!! note
       content
.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>content</p>
</div>
.


But that's a code block
.
    !!! note
        content
.
<pre><code>!!! note
    content
</code></pre>
.


Some more indent checks
.
  !!! note
   not a code block

    code block
.
<div class="admonition note">
<p class="admonition-title">Note</p>
</div>
<p>not a code block</p>
<pre><code>code block
</code></pre>
.


Type could be adjacent to marker 
.
!!!note
   xxx

.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>xxx</p>
</div>
.


Type could be adjacent to marker and content may be shifted up to 3 chars
.
!!!note
      xxx

.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>xxx</p>
</div>
.


Or several spaces apart
.
!!!     note
        xxx
.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>xxx</p>
</div>
.


Admonitions self-close at the end of the document
.
!!! note
    xxx
.
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>xxx</p>
</div>
.


They could be nested in lists
.
- !!! note
      - a
      - b
- !!! warning
      - c
      - d
.
<ul>
<li>
<div class="admonition note">
<p class="admonition-title">Note</p>
<ul>
<li>a</li>
<li>b</li>
</ul>
</div>
</li>
<li>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<ul>
<li>c</li>
<li>d</li>
</ul>
</div>
</li>
</ul>
.


Or in blockquotes
.
> !!! note
>     xxx
>     > yyy
>     zzz
>
.
<blockquote>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>xxx</p>
<blockquote>
<p>yyy
zzz</p>
</blockquote>
</div>
</blockquote>
.


Renders unknown admonition type 
.
!!! unknown title
    content
.
<div class="admonition unknown">
<p class="admonition-title">title</p>
<p>content</p>
</div>
.


Does not render
.
!!!
    content
.
<p>!!!
content</p>
.
