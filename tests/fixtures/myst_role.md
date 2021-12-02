
Basic:
.
{abc}`xyz`
.
<p><code class="myst role">{abc}[xyz]</code></p>
.

Multiple:
.
{abc}`xyz`{def}`uvw`
.
<p><code class="myst role">{abc}[xyz]</code><code class="myst role">{def}[uvw]</code></p>
.

Surrounding Text:
.
a {abc}`xyz` b
.
<p>a <code class="myst role">{abc}[xyz]</code> b</p>
.

New lines:
.
{abc}`xy
z` `d
e`
.
<p><code class="myst role">{abc}[xy z]</code> <code>d e</code></p>
.

In Code:
.
`` {abc}`xyz` ``
.
<p><code>{abc}`xyz`</code></p>
.

Empty content:
.
{name}`` a
.
<p>{name}`` a</p>
.

Surrounding Code:
.
`a` {abc}`xyz` `b`
.
<p><code>a</code> <code class="myst role">{abc}[xyz]</code> <code>b</code></p>
.

In list:
.
- {abc}`xyz`
.
<ul>
<li><code class="myst role">{abc}[xyz]</code></li>
</ul>
.

In Quote:
.
> {abc}`xyz` b
.
<blockquote>
<p><code class="myst role">{abc}[xyz]</code> b</p>
</blockquote>
.

Multiple ticks:
.
{abc}``xyz``
.
<p><code class="myst role">{abc}[xyz]</code></p>
.

Inner tick:
.
{abc}``x`yz``
.
<p><code class="myst role">{abc}[x`yz]</code></p>
.

Unbalanced ticks:
.
{abc}``xyz`
.
<p>{abc}``xyz`</p>
.

Space in name:
.
{ab c}`xyz`
.
<p>{ab c}<code>xyz</code></p>
.

Escaped:
.
\{abc}`xyz`
.
<p>{abc}<code>xyz</code></p>
.
