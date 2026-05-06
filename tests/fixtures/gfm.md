GFM: table
.
| foo | bar |
| --- | --- |
| baz | bim |
.
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
.

GFM: strikethrough (double tilde)
.
~~hello~~
.
<p><s>hello</s></p>
.

GFM: strikethrough (single tilde)
.
~hello~
.
<p><s>hello</s></p>
.

GFM: autolink www
.
www.example.com
.
<p><a href="http://www.example.com">www.example.com</a></p>
.

GFM: autolink protocol
.
https://example.com
.
<p><a href="https://example.com">https://example.com</a></p>
.

GFM: autolink email
.
user@example.com
.
<p><a href="mailto:user@example.com">user@example.com</a></p>
.

GFM: task list
.
- [x] done
- [ ] todo
.
<ul class="contains-task-list">
<li class="task-list-item"><input class="task-list-item-checkbox" disabled="" type="checkbox" checked=""> done</li>
<li class="task-list-item"><input class="task-list-item-checkbox" disabled="" type="checkbox"> todo</li>
</ul>
.

GFM: alert
.
> [!NOTE]
> This is a note.
.
<div class="markdown-alert markdown-alert-note">
<p class="markdown-alert-title">Note</p>
<p>This is a note.</p>
</div>
.

GFM: combined features
.
Check out https://example.com for more info.

~~old~~ and ~also old~

- [x] visited www.example.com
- [ ] email user@example.com
.
<p>Check out <a href="https://example.com">https://example.com</a> for more info.</p>
<p><s>old</s> and <s>also old</s></p>
<ul class="contains-task-list">
<li class="task-list-item"><input class="task-list-item-checkbox" disabled="" type="checkbox" checked=""> visited <a href="http://www.example.com">www.example.com</a></li>
<li class="task-list-item"><input class="task-list-item-checkbox" disabled="" type="checkbox"> email <a href="mailto:user@example.com">user@example.com</a></li>
</ul>
.

GFM: footnotes
.
Here is a footnote[^1].

[^1]: Footnote content.
.
<p>Here is a footnote<sup class="footnote-ref"><a href="#fn1" id="fnref1">[1]</a></sup>.</p>
<hr class="footnotes-sep">
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1" class="footnote-item"><p>Footnote content. <a href="#fnref1" class="footnote-backref">↩︎</a></p>
</li>
</ol>
</section>
.

GFM: dollar math inline
.
Euler's formula: $e^{i\pi} + 1 = 0$
.
<p>Euler's formula: <span class="math inline">e^{i\pi} + 1 = 0</span></p>
.

GFM: dollar math block
.
$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
.
<div class="math block">
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
</div>
.
