does not alter ordinary unordered list syntax:
.
* foo
* bar
- baz
.
<ul>
<li>foo</li>
<li>bar</li>
</ul>
<ul>
<li>baz</li>
</ul>
.

does not alter ordinary ordered list syntax:
.
1. foo
2. bar
3) baz
.
<ol>
<li>foo</li>
<li>bar</li>
</ol>
<ol start="3">
<li>baz</li>
</ol>
.

does not alter ordinary nested ordered list syntax:
.
1. foo
   1. first
   2. second
2. bar
3) baz
.
<ol>
<li>foo
<ol>
<li>first</li>
<li>second</li>
</ol>
</li>
<li>bar</li>
</ol>
<ol start="3">
<li>baz</li>
</ol>
.

supports lowercase alphabetical numbering:
.
a. foo
b. bar
c. baz
.
<ol type="a">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports offsets for lowercase alphabetical numbering:
.
b. foo
c. bar
d. baz
.
<ol type="a" start="2">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports uppercase alphabetical numbering:
.
A) foo
B) bar
C) baz
.
<ol type="A">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports offsets for uppercase alphabetical numbering:
.
B) foo
C) bar
D) baz
.
<ol type="A" start="2">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

test supports lowercase roman numbering:
.
i. foo
ii. bar
iii. baz
.
<ol type="i">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports offsets for lowercase roman numbering:
.
iv. foo
v. bar
vi. baz
.
<ol type="i" start="4">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports uppercase roman numbering:
.
I) foo
II) bar
III) baz
.
<ol type="I">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports offsets for uppercase roman numbering:
.
XII. foo
XIII. bar
XIV. baz
.
<ol type="I" start="12">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

ignores invalid roman numerals as list marker:
.
VV. foo
VVI. bar
VVII. baz
.
<p>VV. foo
VVI. bar
VVII. baz</p>
.

supports hash as list marker for subsequent items:
.
1. foo
#. bar
#. baz
.
<ol>
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports hash as list marker for subsequent roman numeric marker:
.
i. foo
#. bar
#. baz
.
<ol type="i">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports hash as list marker for subsequent alphanumeric marker:
.
a. foo
#. bar
#. baz
.
<ol type="a">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

supports hash as list marker for initial item:
.
#. foo
#. bar
#. baz
.
<ol>
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

allows first numbers to interrupt paragraphs:
.
I need to buy
a. new shoes
b. a coat
c. a plane ticket

I also need to buy
i. new shoes
ii. a coat
iii. a plane ticket
.
<p>I need to buy</p>
<ol type="a">
<li>new shoes</li>
<li>a coat</li>
<li>a plane ticket</li>
</ol>
<p>I also need to buy</p>
<ol type="i">
<li>new shoes</li>
<li>a coat</li>
<li>a plane ticket</li>
</ol>
.

does not allow subsequent numbers to interrupt paragraphs:
.
I need to buy
b. new shoes
c. a coat
d. a plane ticket

I also need to buy
ii. new shoes
iii. a coat
iv. a plane ticket
.
<p>I need to buy
b. new shoes
c. a coat
d. a plane ticket</p>
<p>I also need to buy
ii. new shoes
iii. a coat
iv. a plane ticket</p>
.

supports nested lists:
.
 9)  Ninth
10)  Tenth
11)  Eleventh
       i. subone
      ii. subtwo
     iii. subthree
.
<ol start="9">
<li>Ninth</li>
<li>Tenth</li>
<li>Eleventh
<ol type="i">
<li>subone</li>
<li>subtwo</li>
<li>subthree</li>
</ol>
</li>
</ol>
.

supports nested lists with start:
.
c. charlie
#. delta
   iv) subfour
   #) subfive
   #) subsix
#. echo
.
<ol type="a" start="3">
<li>charlie</li>
<li>delta
<ol type="i" start="4">
<li>subfour</li>
<li>subfive</li>
<li>subsix</li>
</ol>
</li>
<li>echo</li>
</ol>
.

supports nested lists with extra newline:
.
c. charlie
#. delta

   sigma
   iv) subfour
   #) subfive
   #) subsix
#. echo
.
<ol type="a" start="3">
<li>
<p>charlie</p>
</li>
<li>
<p>delta</p>
<p>sigma</p>
<ol type="i" start="4">
<li>subfour</li>
<li>subfive</li>
<li>subsix</li>
</ol>
</li>
<li>
<p>echo</p>
</li>
</ol>
.

starts a new list when a different type of numbering is used:
.
1) First
A) First again
i) Another first
ii) Second
.
<ol>
<li>First</li>
</ol>
<ol type="A">
<li>First again</li>
</ol>
<ol type="i">
<li>Another first</li>
<li>Second</li>
</ol>
.

starts a new list when a sequence of letters is not a valid roman numeral:
.
I) First
A) First again
.
<ol type="I">
<li>First</li>
</ol>
<ol type="A">
<li>First again</li>
</ol>
.

Nested capital inside lower roman:
.
i. First
   A.  First again
ii. Second
    A.  First again again
        I.  First
.
<ol type="i">
<li>First
<ol type="A">
<li>First again</li>
</ol>
</li>
<li>Second
<ol type="A">
<li>First again again
<ol type="I">
<li>First</li>
</ol>
</li>
</ol>
</li>
</ol>
.

marker is considered to be alphabetical when part of an alphabetical list:
.
A) First
I) Second
II) First of new list

a) First
i) Second
ii) First of new list
.
<ol type="A">
<li>First</li>
<li>Second</li>
</ol>
<ol type="I" start="2">
<li>First of new list</li>
</ol>
<ol type="a">
<li>First</li>
<li>Second</li>
</ol>
<ol type="i" start="2">
<li>First of new list</li>
</ol>
.

single letter roman numerals other than I are considered alphabetical without context:
.
v. foo

X) foo

l. foo

C) foo

d. foo

M) foo
.
<ol type="a" start="22">
<li>foo</li>
</ol>
<ol type="A" start="24">
<li>foo</li>
</ol>
<ol type="a" start="12">
<li>foo</li>
</ol>
<ol type="A" start="3">
<li>foo</li>
</ol>
<ol type="a" start="4">
<li>foo</li>
</ol>
<ol type="A" start="13">
<li>foo</li>
</ol>
.

requires two spaces after a capital letter and a period:
.
B. Russell was an English philosopher.

I. Elba is an English actor.

I.  foo
II. bar

B.  foo
C.  bar
.
<p>B. Russell was an English philosopher.</p>
<p>I. Elba is an English actor.</p>
<ol type="I">
<li>foo</li>
<li>bar</li>
</ol>
<ol type="A" start="2">
<li>foo</li>
<li>bar</li>
</ol>
.

does not support an ordinal indicator by default:
.
1º. foo
2º. bar
3º. baz
.
<p>1º. foo
2º. bar
3º. baz</p>
.

supports an ordinal indicator if enabled in options (ordinal):
.
1º. foo
2º. bar
3º. baz
.
<ol class="ordinal">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

allows ordinal indicators with Roman numerals (ordinal):
.
IIº. foo
IIIº. bar
IVº. baz
.
<ol type="I" start="2" class="ordinal">
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>
.

starts a new list when ordinal indicators are introduced or omitted (ordinal):
.
1) First
1º) First again
2º) Second
1) Another first
.
<ol>
<li>First</li>
</ol>
<ol class="ordinal">
<li>First again</li>
<li>Second</li>
</ol>
<ol>
<li>Another first</li>
</ol>
.

tolerates characters commonly mistaken for ordinal indicators (ordinal):
.
1°. degree sign
2˚. ring above
3ᵒ. modifier letter small o
4º. ordinal indicator
.
<ol class="ordinal">
<li>degree sign</li>
<li>ring above</li>
<li>modifier letter small o</li>
<li>ordinal indicator</li>
</ol>
.
