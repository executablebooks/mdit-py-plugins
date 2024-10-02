Strikethrough versus subscript:
.
~~strikethrough~~versus~subscript~
.
<p><s>strikethrough</s>versus<sub>subscript</sub></p>
.

Subscript in strikethrough (beginning):
.
~~~subscript~strikethrough~~
This ends up being rendered as a code block, but that's expected.
Hence, it has to be closed with `~~~`
~~~
Only then will the following text be rendered as it is intended.
We cannot use `~~~subscript~strikethrough~~` at the beginning of a line.
.
<pre><code class="language-subscript~strikethrough~~">This ends up being rendered as a code block, but that's expected.
Hence, it has to be closed with `~~~`
</code></pre>
<p>Only then will the following text be rendered as it is intended.
We cannot use <code>~~~subscript~strikethrough~~</code> at the beginning of a line.</p>
.

Strikethrough in subscript (beginning):
.
~~~strikethrough~~subscript~
This ends up being rendered as a code block, but that's expected.
Hence, it has to be closed with `~~~`
~~~
Only then will the following text be rendered as it is intended.
We cannot use `~~~strikethrough~~subscript~` at the beginning of a line.
.
<pre><code class="language-strikethrough~~subscript~">This ends up being rendered as a code block, but that's expected.
Hence, it has to be closed with `~~~`
</code></pre>
<p>Only then will the following text be rendered as it is intended.
We cannot use <code>~~~strikethrough~~subscript~</code> at the beginning of a line.</p>
.

Subscript in strikethrough (end):
.
~~strikethrough~subscript~~~
.
<p><s>strikethrough<sub>subscript</sub></s></p>
.

Strikethrough in subscript (end):
.
TODO: ~subscript~~strikethrough~~~
.
<p>TODO: <sub>subscript</sub><sub>strikethrough</sub>~~</p>
.

Subscript in strikethrough:
.
~~strikethrough~subscript~strikethrough~~
.
<p><s>strikethrough<sub>subscript</sub>strikethrough</s></p>
.

Strikethrough in subscript:
.
TODO: ~subscript~~strikethrough~~subscript~
This should have beeen similar to *emphasised**strong**emphasised*.
.
<p>TODO: <sub>subscript</sub><sub>strikethrough</sub><sub>subscript</sub>
This should have beeen similar to <em>emphasised<strong>strong</strong>emphasised</em>.</p>
.