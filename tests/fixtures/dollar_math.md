single dollar
.
$
.
<p>$</p>
.

double-dollar
.
$$
.
<p>$$</p>
.

single character inline equation. (valid=True)
.
$a$
.
<p><span class="math inline">a</span></p>
.

inline equation with single greek character (valid=True)
.
$\\varphi$
.
<p><span class="math inline">\\varphi</span></p>
.

simple equation starting and ending with numbers. (valid=True)
.
$1+1=2$
.
<p><span class="math inline">1+1=2</span></p>
.

simple equation including special html character. (valid=True)
.
$1+1<3$
.
<p><span class="math inline">1+1&lt;3</span></p>
.

equation including backslashes. (valid=True)
.
$a \\backslash$
.
<p><span class="math inline">a \\backslash</span></p>
.

use of currency symbol, i.e. digits before/after opening/closing (valid=True)
.
3$1+2$ $1+2$3
.
<p>3$1+2$ $1+2$3</p>
.

use of currency symbol (valid=True)
.
If you solve $1+2$ you get $3
.
<p>If you solve <span class="math inline">1+2</span> you get $3</p>
.

inline fraction (valid=True)
.
$\\frac{1}{2}$
.
<p><span class="math inline">\\frac{1}{2}</span></p>
.

inline column vector (valid=True)
.
$\\begin{pmatrix}x\\\\y\\end{pmatrix}$
.
<p><span class="math inline">\\begin{pmatrix}x\\\\y\\end{pmatrix}</span></p>
.

inline bold vector notation (valid=True)
.
${\\tilde\\bold e}_\\alpha$
.
<p><span class="math inline">{\\tilde\\bold e}_\\alpha</span></p>
.

exponentiation (valid=True)
.
$a^{b}$
.
<p><span class="math inline">a^{b}</span></p>
.

conjugate complex (valid=True)
.
$a^\*b$ with $a^\*$
.
<p><span class="math inline">a^\*b</span> with <span class="math inline">a^\*</span></p>
.

Inline multi-line (valid=True)
.
a $a
\not=1$ b
.
<p>a <span class="math inline">a
\not=1</span> b</p>
.

Inline multi-line with newline (valid=False)
.
a $a

\not=1$ b
.
<p>a $a</p>
<p>\not=1$ b</p>
.

single block equation, greek index (valid=True)
.
$$e_\\alpha$$
.
<div class="math block">
e_\\alpha
</div>
.

display equation on its own single line. (valid=True)
.
$$1+1=2$$
.
<div class="math block">
1+1=2
</div>
.

display equation with number on its own single line. (valid=True)
.
$$1+1=2$$ (2)
.
<div id="2" class="math block">
<a href="#2" class="mathlabel" title="Permalink to this equation">¶</a>
1+1=2
</div>
.

inline equation followed by block equation. (valid=True)
.
${e}_x$

$$e_\\alpha$$
.
<p><span class="math inline">{e}_x</span></p>
<div class="math block">
e_\\alpha
</div>
.

underline tests (valid=True)
.
$$c{\\bold e}_x = a{\\bold e}_\\alpha - b\\tilde{\\bold e}_\\alpha$$
.
<div class="math block">
c{\\bold e}_x = a{\\bold e}_\\alpha - b\\tilde{\\bold e}_\\alpha
</div>
.

non-numeric character before opening $ or
after closing $ or both is allowed. (valid=True)
.
a$1+1=2$
$1+1=2$b
c$x$d
.
<p>a<span class="math inline">1+1=2</span>
<span class="math inline">1+1=2</span>b
c<span class="math inline">x</span>d</p>
.

following dollar character '$' is allowed. (valid=True)
.
$x$ $
.
<p><span class="math inline">x</span> $</p>
.

consecutive inline equations. (valid=True)
.
$x$ $y$
.
<p><span class="math inline">x</span> <span class="math inline">y</span></p>
.

inline equation after '-' sign in text. (valid=True)
.
so-what is $x$
.
<p>so-what is <span class="math inline">x</span></p>
.

display equation with line breaks. (valid=True)
.
$$
1+1=2
$$
.
<div class="math block">
1+1=2
</div>
.

multiple equations (valid=True)
.
$$
a = 1
$$

$$
b = 2
$$
.
<div class="math block">
a = 1
</div>
<div class="math block">
b = 2
</div>
.

display equation with blank lines. (valid=False)
.
$$
1+1=2

$$
.
<p>$$
1+1=2</p>
<p>$$</p>
.

equation followed by a labelled equation (valid=True)
.
$$
a = 1
$$

$$
b = 2
$$ (1)
.
<div class="math block">
a = 1
</div>
<div id="1" class="math block">
<a href="#1" class="mathlabel" title="Permalink to this equation">¶</a>
b = 2
</div>
.

multiline equation. (valid=True)
.
$$\\begin{matrix}
 f & = & 2 + x + 3 \\
 & = & 5 + x
\\end{matrix}$$
.
<div class="math block">
\\begin{matrix}
 f &amp; = &amp; 2 + x + 3 \\
 &amp; = &amp; 5 + x
\\end{matrix}
</div>
.

vector equation. (valid=True)
.
$$\\begin{pmatrix}x_2 \\\\ y_2 \\end{pmatrix} =
\\begin{pmatrix} A & B \\\\ C & D \\end{pmatrix}\\cdot
\\begin{pmatrix} x_1 \\\\ y_1 \\end{pmatrix}$$
.
<div class="math block">
\\begin{pmatrix}x_2 \\\\ y_2 \\end{pmatrix} =
\\begin{pmatrix} A &amp; B \\\\ C &amp; D \\end{pmatrix}\\cdot
\\begin{pmatrix} x_1 \\\\ y_1 \\end{pmatrix}
</div>
.

display equation with equation number. (valid=True)
.
$$f(x) = x^2 - 1$$ (1)
.
<div id="1" class="math block">
<a href="#1" class="mathlabel" title="Permalink to this equation">¶</a>
f(x) = x^2 - 1
</div>
.

inline equation following code section. (valid=True)
.
`code`$a-b$
.
<p><code>code</code><span class="math inline">a-b</span></p>
.

equation following code block. (valid=True)
.
```
code
```
$$a+b$$
.
<pre><code>code
</code></pre>
<div class="math block">
a+b
</div>
.

numbered equation following code block. (valid=True)
.
```
code
```
$$a+b$$(1)
.
<pre><code>code
</code></pre>
<div id="1" class="math block">
<a href="#1" class="mathlabel" title="Permalink to this equation">¶</a>
a+b
</div>
.

Equations in list. (valid=True)
.
1. $1+2$
2. $2+3$
    1. $3+4$
.
<ol>
<li><span class="math inline">1+2</span></li>
<li><span class="math inline">2+3</span>
<ol>
<li><span class="math inline">3+4</span></li>
</ol>
</li>
</ol>
.

Inline sum. (valid=True)
.
$\\sum\_{i=1}^n$
.
<p><span class="math inline">\\sum\_{i=1}^n</span></p>
.

Sum without equation number. (valid=True)
.
$$\\sum\_{i=1}^n$$
.
<div class="math block">
\\sum\_{i=1}^n
</div>
.

Sum with equation number. (valid=True)
.
$$\\sum\_{i=1}\^n$$ (2)
.
<div id="2" class="math block">
<a href="#2" class="mathlabel" title="Permalink to this equation">¶</a>
\\sum\_{i=1}\^n
</div>
.

equation number always vertically aligned. (valid=True)
.
$${\\bold e}(\\varphi) = \\begin{pmatrix}
\\cos\\varphi\\\\\\sin\\varphi
\\end{pmatrix}$$ (3)
.
<div id="3" class="math block">
<a href="#3" class="mathlabel" title="Permalink to this equation">¶</a>
{\\bold e}(\\varphi) = \\begin{pmatrix}
\\cos\\varphi\\\\\\sin\\varphi
\\end{pmatrix}
</div>
.

inline equations in blockquote. (valid=True)
.
> see $a = b + c$
> $c^2=a^2+b^2$ (2)
> $c^2=a^2+b^2$
.
<blockquote>
<p>see <span class="math inline">a = b + c</span>
<span class="math inline">c^2=a^2+b^2</span> (2)
<span class="math inline">c^2=a^2+b^2</span></p>
</blockquote>
.

display equation in blockquote. (valid=True)
.
> formula
>
> $$ a+b=c$$ (2)
>
> in blockquote.
.
<blockquote>
<p>formula</p>
<div id="2" class="math block">
<a href="#2" class="mathlabel" title="Permalink to this equation">¶</a>
a+b=c
</div>
<p>in blockquote.</p>
</blockquote>
.

mixed syntax:
.
$$
a=1 \\
b=2
$$ (abc)

- ab $c=1$ d
.
<div id="abc" class="math block">
<a href="#abc" class="mathlabel" title="Permalink to this equation">¶</a>
a=1 \\
b=2
</div>
<ul>
<li>ab <span class="math inline">c=1</span> d</li>
</ul>
.

escaped dollars '\\$' are interpreted as
dollar '$' characters. (valid=True)
.
\\$1+1=2$
$1+1=2\\$
.
<p>\<span class="math inline">1+1=2</span>
<span class="math inline">1+1=2\\</span></p>
.

empty line between text and display formula is required. (valid=False)
.
some text
 \$\\$a+b=c\$\$
.
<p>some text
$\$a+b=c$$</p>
.

whitespace character after opening $
or before closing $ is not allowed. (valid=False)
.
$ $
$ x$
$x $
.
<p>$ $
$ x$
$x $</p>
.

new line in blockquote block (valid=False):
.
> \$\$ a+b\n=c\$\$
.
<blockquote>
<p>$$ a+b\n=c$$</p>
</blockquote>
.

math-escaping: escaped start $:
.
\$p_2 = $a
.
<p>$p_2 = $a</p>
.

math-escaping: escaped end $:
.
$p_2 = \$a
.
<p>$p_2 = $a</p>
.

math-escaping: internal escaped $:
.
$p_2 = \$1$
.
<p><span class="math inline">p_2 = \$1</span></p>
.

math-escaping: double-escaped start $:
.
\\$p_2 = 1$
.
<p>\<span class="math inline">p_2 = 1</span></p>
.

math-escaping: double-escaped end $:
.
$p_2 = \\$a
.
<p><span class="math inline">p_2 = \\</span>a</p>
.

Inline double-dollar start:
.
$$a=1$$ b
.
<p><div class="math inline">a=1</div> b</p>
.

Inline double-dollar end:
.
a $$a=1$$
.
<p>a <div class="math inline">a=1</div></p>
.

Inline double-dollar enclosed:
.
a $$a=1$$ (1) b
.
<p>a <div class="math inline">a=1</div> (1) b</p>
.

Inline double-dollar, escaped:
.
a \$$a=1$$ b
.
<p>a $<span class="math inline">a=1</span>$ b</p>
.

Inline mixed single/double dollars:
.
Hence, for $\alpha \in (0, 1)$,
$$
  \mathbb P (\alpha \bar{X} \ge \mu) \le \alpha;
$$
i.e., $[\alpha \bar{X}, \infty)$ is a lower 1-sided $1-\alpha$ confidence bound for $\mu$.
.
<p>Hence, for <span class="math inline">\alpha \in (0, 1)</span>,
<div class="math inline">\mathbb P (\alpha \bar{X} \ge \mu) \le \alpha;</div>
i.e., <span class="math inline">[\alpha \bar{X}, \infty)</span> is a lower 1-sided <span class="math inline">1-\alpha</span> confidence bound for <span class="math inline">\mu</span>.</p>
.

display equation with label containing whitespace. (valid=True)
.
$$1+1=2$$ (a b)
.
<div id="a-b" class="math block">
<a href="#a-b" class="mathlabel" title="Permalink to this equation">¶</a>
1+1=2
</div>
.


Indented by 4 spaces
.
    $$a$$
.
<pre><code>$$a$$
</code></pre>
.

Indented by 4 spaces, DISABLE-CODEBLOCKS
.
    $$a$$
.
<div class="math block">
a
</div>
.
