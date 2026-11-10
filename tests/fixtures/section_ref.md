
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

Inside an autolink (not captured):
.
<https://example.com/§1>
.
<p><a href="https://example.com/%C2%A71">https://example.com/§1</a></p>
.

Inside raw HTML (not captured), but captured in its content:
.
<span title="§1">§2</span>
.
<p><span title="§1"><span class="section-ref">§2</span></span></p>
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

Entity section signs give a literal sign (not captured):
.
&sect;1 and &#167;2
.
<p>§1 and §2</p>
.

Followed by non-digit, non-space char (not captured):
.
§x and §.5
.
<p>§x and §.5</p>
.

Non-ASCII digits (not captured):
.
§١ and §３
.
<p>§١ and §３</p>
.

Leading zeros preserved in content (meta numbers are normalized):
.
§01.02
.
<p><span class="section-ref">§01.02</span></p>
.

Level at the nine-digit bound (captured):
.
§123456789 and §1.999999999
.
<p><span class="section-ref">§123456789</span> and <span class="section-ref">§1.999999999</span></p>
.

Level one past the nine-digit bound (not captured):
.
§1234567890 and §1.1234567890
.
<p>§1234567890 and §1.1234567890</p>
.

Over-long middle level (not captured, no partial prefix):
.
§1.1234567890.2 then §3
.
<p>§1.1234567890.2 then <span class="section-ref">§3</span></p>
.

Leading zeros count towards the bound (not captured):
.
§0000000001
.
<p>§0000000001</p>
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
