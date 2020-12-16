Basic (space):
.
{{ block }}

a {{ inline }} b
.
<div class="substitution" text="block" />
<p>a <span class="substitution" text="inline" /> b</p>
.

Basic (no space):
.
{{block}}

a {{inline}} b
.
<div class="substitution" text="block" />
<p>a <span class="substitution" text="inline" /> b</p>
.

New line:
.
{{a}}
{{b}}
.
<div class="substitution" text="a" />
<div class="substitution" text="b" />
.

Blocks:
.
- {{a}}

> {{b}}

1. {{c}}
.
<ul>
<li>
<div class="substitution" text="a" />
</li>
</ul>
<blockquote>
<div class="substitution" text="b" />
</blockquote>
<ol>
<li>
<div class="substitution" text="c" />
</li>
</ol>
.

Inline:
.
- {{a}} x

> {{b}} y

1. {{c}} z
.
<ul>
<li><span class="substitution" text="a" /> x</li>
</ul>
<blockquote>
<p><span class="substitution" text="b" /> y</p>
</blockquote>
<ol>
<li><span class="substitution" text="c" /> z</li>
</ol>
.

Tables:
.
| | |
|-|-|
|{{a}}|{{b}} c|
.
<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><span class="substitution" text="a" /></td>
<td><span class="substitution" text="b" /> c</td>
</tr>
</tbody>
</table>
.
