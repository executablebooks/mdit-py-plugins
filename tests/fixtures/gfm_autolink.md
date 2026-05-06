GFM autolink: www basic (spec 622)
.
www.commonmark.org
.
<p><a href="http://www.commonmark.org">www.commonmark.org</a></p>
.

GFM autolink: www with path (spec 623)
.
Visit www.commonmark.org/help for more information.
.
<p>Visit <a href="http://www.commonmark.org/help">www.commonmark.org/help</a> for more information.</p>
.

GFM autolink: trailing punctuation (spec 624)
.
Visit www.commonmark.org.

Visit www.commonmark.org/a.b.
.
<p>Visit <a href="http://www.commonmark.org">www.commonmark.org</a>.</p>
<p>Visit <a href="http://www.commonmark.org/a.b">www.commonmark.org/a.b</a>.</p>
.

GFM autolink: parentheses balancing (spec 625)
.
www.google.com/search?q=Markup+(business)

www.google.com/search?q=Markup+(business)))

(www.google.com/search?q=Markup+(business))

(www.google.com/search?q=Markup+(business)
.
<p><a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a></p>
<p><a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a>))</p>
<p>(<a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a>)</p>
<p>(<a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a></p>
.

GFM autolink: interior parens only (spec 626)
.
www.google.com/search?q=(business))+ok
.
<p><a href="http://www.google.com/search?q=(business))+ok">www.google.com/search?q=(business))+ok</a></p>
.

GFM autolink: entity reference exclusion (spec 627)
.
www.google.com/search?q=commonmark&hl=en

www.google.com/search?q=commonmark&hl;
.
<p><a href="http://www.google.com/search?q=commonmark&amp;hl=en">www.google.com/search?q=commonmark&amp;hl=en</a></p>
<p><a href="http://www.google.com/search?q=commonmark">www.google.com/search?q=commonmark</a>&amp;hl;</p>
.

GFM autolink: less-than ends autolink (spec 628)
.
www.commonmark.org/he<lp
.
<p><a href="http://www.commonmark.org/he">www.commonmark.org/he</a>&lt;lp</p>
.

GFM autolink: http/https (spec 629)
.
http://commonmark.org

(Visit https://encrypted.google.com/search?q=Markup+(business))
.
<p><a href="http://commonmark.org">http://commonmark.org</a></p>
<p>(Visit <a href="https://encrypted.google.com/search?q=Markup+(business)">https://encrypted.google.com/search?q=Markup+(business)</a>)</p>
.

GFM autolink: bare email (spec 630)
.
foo@bar.baz
.
<p><a href="mailto:foo@bar.baz">foo@bar.baz</a></p>
.

GFM autolink: email local part (spec 632 modified)
.
a.b-c-d@a.b

a.b-c-d@a.b.

a.b-c-d@a.b-

a.b-c-d@a.b_
.
<p><a href="mailto:a.b-c-d@a.b">a.b-c-d@a.b</a></p>
<p><a href="mailto:a.b-c-d@a.b">a.b-c-d@a.b</a>.</p>
<p>a.b-c-d@a.b-</p>
<p>a.b-c-d@a.b_</p>
.

GFM autolink: mailto/xmpp protocol (spec 633)
.
mailto:foo@bar.baz

mailto:a.b-c_d@a.b

mailto:a.b-c_d@a.b.

mailto:a.b-c_d@a.b/

mailto:a.b-c_d@a.b-

mailto:a.b-c_d@a.b_

xmpp:foo@bar.baz

xmpp:foo@bar.baz.
.
<p><a href="mailto:foo@bar.baz">mailto:foo@bar.baz</a></p>
<p><a href="mailto:a.b-c_d@a.b">mailto:a.b-c_d@a.b</a></p>
<p><a href="mailto:a.b-c_d@a.b">mailto:a.b-c_d@a.b</a>.</p>
<p><a href="mailto:a.b-c_d@a.b">mailto:a.b-c_d@a.b</a>/</p>
<p>mailto:a.b-c_d@a.b-</p>
<p>mailto:a.b-c_d@a.b_</p>
<p><a href="xmpp:foo@bar.baz">xmpp:foo@bar.baz</a></p>
<p><a href="xmpp:foo@bar.baz">xmpp:foo@bar.baz</a>.</p>
.

GFM autolink: xmpp resource (spec 634)
.
xmpp:foo@bar.baz/txt

xmpp:foo@bar.baz/txt@bin

xmpp:foo@bar.baz/txt@bin.com
.
<p><a href="xmpp:foo@bar.baz/txt">xmpp:foo@bar.baz/txt</a></p>
<p><a href="xmpp:foo@bar.baz/txt@bin">xmpp:foo@bar.baz/txt@bin</a></p>
<p><a href="xmpp:foo@bar.baz/txt@bin.com">xmpp:foo@bar.baz/txt@bin.com</a></p>
.

GFM autolink: trailing delimiters
.
http://google.com/he<lp
mailto:bob@google.co<m
bob@google.co<m

http://google.com/(business)
http://google.com/(business))

http://google.com/other_
.
<p><a href="http://google.com/he">http://google.com/he</a>&lt;lp
<a href="mailto:bob@google.co">mailto:bob@google.co</a>&lt;m
<a href="mailto:bob@google.co">bob@google.co</a>&lt;m</p>
<p><a href="http://google.com/(business)">http://google.com/(business)</a>
<a href="http://google.com/(business)">http://google.com/(business)</a>)</p>
<p><a href="http://google.com/other">http://google.com/other</a>_</p>
.

GFM autolink: integration with other syntax
.
**www.example.com**

*https://example.com*
.
<p><strong><a href="http://www.example.com">www.example.com</a></strong></p>
<p><em><a href="https://example.com">https://example.com</a></em></p>
.

GFM autolink: not inside links
.
[http://example.com](http://example.com)
[mailto:bob@example.com](https://example.com)
[bob@example.com](https://example.com)
.
<p><a href="http://example.com">http://example.com</a>
<a href="https://example.com">mailto:bob@example.com</a>
<a href="https://example.com">bob@example.com</a></p>
.

GFM autolink: preceded by letter (no match)
.
awww.example.com
ahttps://example.com
amailto:bob@example.com
.
<p>awww.example.com
ahttps://example.com
amailto:bob@example.com</p>
.

GFM autolink: email plus in local part
.
hello@mail+xyz.example

hello+xyz@mail.example
.
<p>hello@mail+xyz.example</p>
<p><a href="mailto:hello+xyz@mail.example">hello+xyz@mail.example</a></p>
.

GFM autolink: angle bracket autolink still works
.
<http://www.example.com>www.example.com
.
<p><a href="http://www.example.com">http://www.example.com</a>www.example.com</p>
.

GFM autolink: non-match cases
.
example.com

www.

@example.com
.
<p>example.com</p>
<p>www.</p>
<p>@example.com</p>
.

GFM autolink: xmpp no second slash
.
xmpp:foo@bar.baz/txt/bin
.
<p><a href="xmpp:foo@bar.baz/txt">xmpp:foo@bar.baz/txt</a>/bin</p>
.
