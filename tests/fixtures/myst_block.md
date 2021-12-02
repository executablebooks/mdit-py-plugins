
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
<div class="myst-target">target = <code>a</code></div>
.


Target terminates other blocks:
.
a
(a)=
- b
(a)=
> c
(a)=
.
<p>a</p>
<div class="myst-target">target = <code>a</code></div><ul>
<li>b</li>
</ul>
<div class="myst-target">target = <code>a</code></div><blockquote>
<p>c</p>
</blockquote>
<div class="myst-target">target = <code>a</code></div>
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
