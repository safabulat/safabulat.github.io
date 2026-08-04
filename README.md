# safabulat.github.io

The hub page that sits above every product site — <https://safabulat.github.io/>

One HTML file, one stylesheet, three app icons. No framework, no build step, no external
requests, so it renders straight off a disk. Push to `main` and GitHub Pages publishes it.

    index.html    the whole page
    style.css     dark first, light supported; both are real designs
    img/          app icons, copied from each product's own site repo

## House rules

- **No external requests.** No CDN, no web fonts, no analytics, no embeds. If something needs a
  network call to render, it does not belong here.
- **Colour comes from the icons.** The page itself is near-monochrome with one muted blue for
  links. Deskestra is brass and Kick Kick is pitch green — an umbrella page that picks its own loud
  colour starts competing with the things underneath it.
- **`<meta name="darkreader-lock">` stays.** Without it the Dark Reader extension repaints the
  page and the light design never gets seen.
- **Icons are copies, not the source of truth.** Each product site owns its own `img/appicon.png`;
  when one changes, re-copy it here.

## Product sites

- Deskestra — <https://safabulat.github.io/deskestra-site/>
- Kick Kick — <https://safabulat.github.io/kickkick-site/>
