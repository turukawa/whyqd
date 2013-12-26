Whyqd
=====

Whyqd is an extensible object-based wiki bringing revision control, content presentation, forking and embedding to any type of digital object.

Whyqd is written in Python and Django, with Jquery for the client side.

The current implementation permits the following wiqi objects:

 - Text
 - Images
 - Maps (handlers still to be written)

While you can write your own views and templates, I have included a minimalist wiqi interface influenced by blog sites like [Medium](http://medium.com) and [WriteBox](http://writeboxapps.com/). Note a few permutations of this wiqi:

 - WYSIWIG writing interface: no separation of view vs editing pages;
 - Minimal interface: there is an assumption you know what you're doing, no queries regarding forking, new versions, etc.
 - Permissions-based: if you own a document, you can do what you like, if you don't, you fork it if you want to change it;
 - Merge-changes: if you want to merge two docs, view the diff, edit and commit;

I will put a demo up at some point so you can see this in action.

Roadmap
-------

 - Complete the auth system along with per-object permissions;
 - A "book" model so that individual texts can be arranged as a single work;
 - D3.js simple tree view to present wiqi stack, as well as forked changes;
 - Book management system (shuffling order of chapters);
 - Integration of html2docx and python-docx for upload of Docx files, as well as download of work;
 - Integration of [EbookGlue](https://ebookglue.com/) API so books can be saved as .epub and .mobi files;
 - eCommerce system to support author sales of books;

Long-term roadmap:

Once the basic system is up and stable, then adding in new wiqi objects to support a much richer environment of book creation, including technical textbooks.

There's a long way to go and I would be grateful for code review and forks.

Acknowledgements
----------------

See the requirements.txt file for all the list of Python libraries included. The snippets folder includes code from all over and the comments in the code gives links to various sources I used. The included Javascript libraries are also sourced from their various creators.

My thanks to everyone, too numerous across the community of coders, are offered with deep gratitude.

License
-------

Whyqd is released under the [GNU Affero General Public License](http://www.gnu.org/licenses/agpl-3.0.html).

Attribution: Gavin Chait, http://www.whythawk.com/