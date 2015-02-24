Whyqd
=====

Whyqd is an extensible object-based wiki bringing revision control, content presentation, branching and embedding to any type of digital object. The current simplified implementation was developed to present and distribute my science-fiction novel, [Tartarus Falls](https://tartarusfalls.com).

Features:

- HTML-based presentation of complete novel;;
- Import novel source DOCX and convert to individual HTML pages for each chapter;
- Price and set permissions for each chapter (as open, login or own);
- Structure the Contents page;
- Manage currency conversion, sales and distribution of the novel, including refunds;
- Create one-time / time-limited download tokens for distribution;
- Manage marketing and distribution of free review copies by author;

In the future, Whyqd will allow:

- Online creation and editing of a novel;
- Online conversion of HTML pages into epub, mobi and pdf ebooks;
- Readers can fork, change and re-release books they buy;

Whyqd allows content creators to publish and sell via a personal demand pricing model (e.g. the further a user reads into your novel, the higher the final price will be), and allow users to remix and republish the content after they've bought it.

Remixing means that users could translate a novel, write their own fan-fiction, or expand on existing work all without having to do more than start editing.

Whyqd is written in Python and Django, with Jquery for the client side.

Roadmap
-------

##### Current version (0.1):

- The following wiqi objects are supported: Text, Images (not live), Maps (not live, handlers still to be written)
- [Facebook auth system](https://github.com/tschellenbach/Django-facebook) along with per-object permissions;
- A "book" model so that individual texts can be arranged as a single work;
- Book management system (shuffling order of chapters);
- Integration of python-docx for upload of Docx files;
- [Stripe](https://stripe.com/gb) integration to support author sales of books;
- [AWS Boto](https://github.com/boto/boto) integration for S3 time-limited download of books;
- [Open Exchange Rates](https://openexchangerates.org/) for currency conversion;
- [Mandrill](https://mandrill.com/) integration for distributed mail;

##### Next steps:

While maintaining the ability to publish only a single book, the next version should include a minimalist wiqi interface influenced by blog sites like [Medium](http://medium.com) and [WriteBox](http://writeboxapps.com/). [Guardian Scribe](https://github.com/guardian/scribe) is still extremely ugly, but the underlying approach to managing `contenteditable` is the best I've seen. The objective is that readers can remix and republish the novel to create new versions:

- WYSIWIG writing interface: no separation of view vs editing pages;
- Minimal interface: there is an assumption you know what you're doing, no queries regarding branching, new versions, etc.
- Permissions-based: if you own a document, you can do what you like, if you don't, you branch it if you want to change it;
- Merge-changes: if you want to merge two docs, view the diff, edit and commit;
- D3.js simple tree view to present wiqi stack, as well as branched changes;

##### Long-term roadmap:

Once the basic system is up and stable, then adding in new wiqi objects to support a much richer environment of book creation, including technical textbooks. I would also like the software to handle multiple books (requiring a search interface and a completely different approach to presenting the content).

There's a long way to go and I would be grateful for code review and forks.

Acknowledgements
----------------

See the requirements.txt file for all the Python libraries included. The snippets folder includes code from all over and the comments in the code give links to various sources I used. The included Javascript libraries are also sourced from their various creators.

My thanks to everyone, too numerous across the community of coders, are offered with deep gratitude.

License
-------

Whyqd is copyright Gavin Chait and [Whythawk](http://www.whythawk.com). The software is released under the [GNU Affero General Public License](http://www.gnu.org/licenses/agpl-3.0.html). All visual and design elements are copyright Gavin Chait. The Red Maple image is copyright [Rodd Halstead](http://www.gettyimages.co.uk/detail/photo/red-maple-fruit-samara-royalty-free-image/89736283).

The **personal demand pricing** approach adopted here is similar to that in use by airlines, congestion charging in cities, and is documented extensively (cf. peak pricing, demand pricing, Pareto efficiency, etc.). It is not patented and this implementation serves as prior art for anyone wanting to implement such a system in their own publication platform.