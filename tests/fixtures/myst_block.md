
Block Break:
.
+++
.
<hr class="myst-block">
.

Block Break Split Markers:
.
 + +   + + xfsdfsdf
.
<hr class="myst-block">
.

Block Break Too Few Markers:
.
++
.
<p>++</p>
.

Block Break terminates other blocks:
.
a
+++
- b
+++
> c
+++
.
<p>a</p>
<hr class="myst-block">
<ul>
<li>b</li>
</ul>
<hr class="myst-block">
<blockquote>
<p>c</p>
</blockquote>
<hr class="myst-block">
.

Target:
.
(a)=
.
<div class="myst-target"><a href="#a">(a)=</a></div>
.

Target characters:
.
(a bc   |@<>*./_-+:)=
.
<div class="myst-target"><a href="#a bc   |@<>*./_-+:">(a bc   |@<>*./_-+:)=</a></div>
.

Empty target:
.
()=
.
<p>()=</p>
.

Escaped target:
.
\(a)=
.
<p>(a)=</p>
.

Indented target:
.
  (a)= 
.
<div class="myst-target"><a href="#a">(a)=</a></div>
.

Target terminates other blocks:
.
a
(a-b)=
- b
(a b)=
> c
(a)=
.
<p>a</p>
<div class="myst-target"><a href="#a-b">(a-b)=</a></div><ul>
<li>b</li>
</ul>
<div class="myst-target"><a href="#a b">(a b)=</a></div><blockquote>
<p>c</p>
</blockquote>
<div class="myst-target"><a href="#a">(a)=</a></div>
.

Comment:
.
% abc
.
<!-- abc -->
.

Comment terminates other blocks:
.
a
% abc
- b
% abc
> c
% abc
.
<p>a</p>
<!-- abc --><ul>
<li>b</li>
</ul>
<!-- abc --><blockquote>
<p>c</p>
</blockquote>
<!-- abc -->
.

Multiline comment:
.
a
% abc
%   def
- b
%  abc
%def
> c
%abc
%
%def
.
<p>a</p>
<!-- abc
def --><ul>
<li>b</li>
</ul>
<!-- abc
def --><blockquote>
<p>c</p>
</blockquote>
<!-- abc

def -->
.


Indented by 4 spaces
.
    +++

    % abc

    (a)=
.
<pre><code>+++

% abc

(a)=
</code></pre>
.

Indented by 4 spaces, DISABLE-CODEBLOCKS
.
    +++

    % abc

    (a)=
.
<hr class="myst-block">
<!-- abc --><div class="myst-target"><a href="#a">(a)=</a></div>
.
