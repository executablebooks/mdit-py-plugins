
Basic single-level:
.
See §1 for details.
.
<p>See <span class="section-ref">§1</span> for details.</p>
.

Nested number:
.
See §1.2.3 for details.
.
<p>See <span class="section-ref">§1.2.3</span> for details.</p>
.

At start and end of a paragraph:
.
§1 opens and closes §2
.
<p><span class="section-ref">§1</span> opens and closes <span class="section-ref">§2</span></p>
.

Multiple refs and a range:
.
Compare §1.1-§1.4 and also §2
.
<p>Compare <span class="section-ref">§1.1</span>-<span class="section-ref">§1.4</span> and also <span class="section-ref">§2</span></p>
.

Adjacent refs:
.
§1§2
.
<p><span class="section-ref">§1</span><span class="section-ref">§2</span></p>
.

Trailing period:
.
See §1.
.
<p>See <span class="section-ref">§1</span>.</p>
.

Parenthesised:
.
(§2)
.
<p>(<span class="section-ref">§2</span>)</p>
.

Trailing comma:
.
§3, and more
.
<p><span class="section-ref">§3</span>, and more</p>
.

Trailing possessive apostrophe:
.
§4.3's rules
.
<p><span class="section-ref">§4.3</span>'s rules</p>
.

Inside emphasis:
.
*important: §2.1*
.
<p><em>important: <span class="section-ref">§2.1</span></em></p>
.

Inside link text:
.
[see §1](https://example.com)
.
<p><a href="https://example.com">see <span class="section-ref">§1</span></a></p>
.

Inside inline code (not captured):
.
`§1`
.
<p><code>§1</code></p>
.

Inside fenced code block (not captured):
.
```
§1
```
.
<pre><code>§1
</code></pre>
.

Bare section sign (not captured):
.
just a § here
.
<p>just a § here</p>
.

Space between sign and number (not captured):
.
§ 1
.
<p>§ 1</p>
.

Followed by ASCII letter, single level (not captured):
.
§1a
.
<p>§1a</p>
.

Followed by ASCII letter, nested (not captured):
.
§1.2b
.
<p>§1.2b</p>
.

Backslash-escaped (not captured):
.
\§1
.
<p>\§1</p>
.

Escaped backslash before ref (captured):
.
\\§1
.
<p>\<span class="section-ref">§1</span></p>
.

Followed by non-digit, non-space char (not captured):
.
§x and §.5
.
<p>§x and §.5</p>
.

Leading zeros preserved in content (meta numbers are normalized):
.
§01.02
.
<p><span class="section-ref">§01.02</span></p>
.

In a heading:
.
## About §2
.
<h2>About <span class="section-ref">§2</span></h2>
.

Non-ASCII letter after ref does not block match:
.
见§3章
.
<p>见<span class="section-ref">§3</span>章</p>
.
