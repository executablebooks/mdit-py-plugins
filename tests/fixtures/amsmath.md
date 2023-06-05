equation environment:
.
\begin{equation}
a = 1
\end{equation}
.
<div class="math amsmath">
\begin{equation}
a = 1
\end{equation}
</div>
.

equation* environment:
.
\begin{equation*}
a = 1
\end{equation*}
.
<div class="math amsmath">
\begin{equation*}
a = 1
\end{equation*}
</div>
.

multline environment:
.
\begin{multline}
a = 1
\end{multline}
.
<div class="math amsmath">
\begin{multline}
a = 1
\end{multline}
</div>
.

multline* environment:
.
\begin{multline*}
a = 1
\end{multline*}
.
<div class="math amsmath">
\begin{multline*}
a = 1
\end{multline*}
</div>
.

gather environment:
.
\begin{gather}
a = 1
\end{gather}
.
<div class="math amsmath">
\begin{gather}
a = 1
\end{gather}
</div>
.

gather* environment:
.
\begin{gather*}
a = 1
\end{gather*}
.
<div class="math amsmath">
\begin{gather*}
a = 1
\end{gather*}
</div>
.

align environment:
.
\begin{align}
a = 1
\end{align}
.
<div class="math amsmath">
\begin{align}
a = 1
\end{align}
</div>
.

align* environment:
.
\begin{align*}
a = 1
\end{align*}
.
<div class="math amsmath">
\begin{align*}
a = 1
\end{align*}
</div>
.

alignat environment:
.
\begin{alignat}
a = 1
\end{alignat}
.
<div class="math amsmath">
\begin{alignat}
a = 1
\end{alignat}
</div>
.

alignat* environment:
.
\begin{alignat*}
a = 1
\end{alignat*}
.
<div class="math amsmath">
\begin{alignat*}
a = 1
\end{alignat*}
</div>
.

flalign environment:
.
\begin{flalign}
a = 1
\end{flalign}
.
<div class="math amsmath">
\begin{flalign}
a = 1
\end{flalign}
</div>
.

flalign* environment:
.
\begin{flalign*}
a = 1
\end{flalign*}
.
<div class="math amsmath">
\begin{flalign*}
a = 1
\end{flalign*}
</div>
.

equation environment, with before/after paragraphs:
.
before
\begin{equation}
a = 1
\end{equation}
after
.
<p>before</p>
<div class="math amsmath">
\begin{equation}
a = 1
\end{equation}
</div>
<p>after</p>
.

equation environment, in list:
.
- \begin{equation}
  a = 1
  \end{equation}
.
<ul>
<li>
<div class="math amsmath">
\begin{equation}
  a = 1
  \end{equation}
</div>
</li>
</ul>
.

`alignat` environment and HTML escaping
.
\begin{alignat}{3}
    & d   = \frac{1}{1 + 0.2316419x}  \quad && a_1  = 0.31938153   \quad && a_2 = -0.356563782 \\
    & a_3 = 1.781477937               \quad && a_4  = -1.821255978 \quad && a_5 = 1.330274429
\end{alignat}
.
<div class="math amsmath">
\begin{alignat}{3}
    &amp; d   = \frac{1}{1 + 0.2316419x}  \quad &amp;&amp; a_1  = 0.31938153   \quad &amp;&amp; a_2 = -0.356563782 \\
    &amp; a_3 = 1.781477937               \quad &amp;&amp; a_4  = -1.821255978 \quad &amp;&amp; a_5 = 1.330274429
\end{alignat}
</div>
.

`alignat*` environment and HTML escaping
.
\begin{alignat*}{3}
& m   \quad && \text{módulo}            \quad && m>0\\
& a   \quad && \text{multiplicador}     \quad && 0<a<m\\
& c   \quad && \text{constante aditiva} \quad && 0\leq c<m\\
& x_0 \quad && \text{valor inicial}     \quad && 0\leq x_0 <m
\end{alignat*}
.
<div class="math amsmath">
\begin{alignat*}{3}
&amp; m   \quad &amp;&amp; \text{módulo}            \quad &amp;&amp; m&gt;0\\
&amp; a   \quad &amp;&amp; \text{multiplicador}     \quad &amp;&amp; 0&lt;a&lt;m\\
&amp; c   \quad &amp;&amp; \text{constante aditiva} \quad &amp;&amp; 0\leq c&lt;m\\
&amp; x_0 \quad &amp;&amp; \text{valor inicial}     \quad &amp;&amp; 0\leq x_0 &lt;m
\end{alignat*}
</div>
.

Indented by 4 spaces
.
    \begin{equation}
    a = 1
    \end{equation}
.
<pre><code>\begin{equation}
a = 1
\end{equation}
</code></pre>
.

Indented by 4 spaces, DISABLE-CODEBLOCKS
.
    \begin{equation}
    a = 1
    \end{equation}
.
<div class="math amsmath">
\begin{equation}
    a = 1
    \end{equation}
</div>
.
