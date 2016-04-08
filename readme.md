Whyqd
=====

Whyqd is an extensible object-based wiki bringing revision control, content presentation, branching and embedding to any type of digital object. The current simplified implementation was developed to present and distribute my science-fiction novel, [Lament for the Fallen](https://lamentforthefallen.com).

Features:

- Fully-implemented a text wiki, with a base wiqi for developing other types of wiki;
- Wiki can be branched, as well as the usual tools for version control;

Whyqd is written in Python and Django, with Jquery for the client side.

Quick start
-----------

1. Add "whyqd" to your INSTALLED_APPS setting like this::

    `INSTALLED_APPS = [
        ...
        'whyqd',
    ]`

2. Include the whyqd URLconf in your project urls.py like this::

    `url(r'^wiqi/', include('whyqd.urls')),`

3. Run `python manage.py migrate` to create the whyqd models.

4. Start the development server and visit http://127.0.0.1:8000/create/
   to create your first Text wiqi.

5. Visit http://127.0.0.1:8000/ to view the list of wiqis.

Roadmap
-------

##### Current version (0.2):

- Updated libraries to latest (Django 1.9);
- Text pages can have custom class defined in div;

##### Previous version (0.1):

- The following wiqi objects are supported: Text, Images (not live), Maps (not live, handlers still to be written);
- [Facebook auth system](https://github.com/tschellenbach/Django-facebook) along with per-object permissions;

##### Next steps:

While maintaining the ability to publish only a single book, the next version should include a minimalist wiqi interface influenced by blog sites like [Medium](http://medium.com) and [WriteBox](http://writeboxapps.com/). [Guardian Scribe](https://github.com/guardian/scribe) is still extremely ugly, but the underlying approach to managing `contenteditable` is the best I've seen. The objective is that readers can remix and republish the novel to create new versions:

- WYSIWIG writing interface: no separation of view vs editing pages;
- Minimal interface: there is an assumption you know what you're doing, no queries regarding branching, new versions, etc.
- Permissions-based: if you own a document, you can do what you like, if you don't, you branch it if you want to change it;
- Merge-changes: if you want to merge two docs, view the diff, edit and commit;
- D3.js simple tree view to present wiqi stack, as well as branched changes;

##### Long-term roadmap:

Once the basic system is up and stable, then adding in new wiqi objects to support a much richer environment of book creation, including technical textbooks.

There's a long way to go and I would be grateful for code review and forks.

Acknowledgements
----------------

See the requirements.txt file for all the Python libraries included. The snippets folder includes code from all over and the comments in the code give links to various sources I used. The included Javascript libraries are also sourced from their various creators.

My thanks to everyone, too numerous across the community of coders, are offered with deep gratitude.

License
-------

Whyqd is copyright Gavin Chait and [Whythawk](http://www.whythawk.com). The software is released under the [GNU Affero General Public License](http://www.gnu.org/licenses/agpl-3.0.html). All visual and design elements are copyright Gavin Chait.

The **personal demand pricing** approach adopted here is similar to that in use by airlines, congestion charging in cities, and is documented extensively (cf. peak pricing, demand pricing, Pareto efficiency, etc.). It is not patented and this implementation serves as prior art for anyone wanting to implement such a system in their own publication platform.