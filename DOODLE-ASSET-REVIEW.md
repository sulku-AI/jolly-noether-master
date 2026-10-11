# Doodle Asset Review

## Result

20 distinct cutouts are active in the site. Their original JPEG/JFIF files are unchanged under `assets/doodle-elements/`; the site uses transparent PNGs under `assets/doodles-transparent/`. The processor reports transparent-pixel coverage after alpha trimming. Every active PNG was checked in a contact sheet against plum, lime, and paper surfaces; the star, flower, checkerboard, and paper-edge samples were also reviewed at larger size.

| Transparent asset | Original source | Placement | Transparent pixels | Review |
| --- | --- | --- | ---: | --- |
| `asset-2.png` | `asset-2.jpg` | Hero, star field | 70.0% | Pass: distinct stars; enclosed fills preserved |
| `asset-3.png` | `asset-3.jpg` | Hero, floral mark | 58.3% | Pass: flower centers and fine outlines intact |
| `asset-4.png` | `asset-4.jpg` | Hero, small corner sticker | 69.2% | Pass: clean silhouette |
| `asset-5.png` | `asset-5.jpg` | Leadership letters, upper edge | 30.3% | Pass: torn-paper edge retained |
| `asset-6.png` | `asset-6.jpg` | Leadership letters, opposite edge | 13.0% | Pass: texture remains; low transparency is expected for a mostly solid paper piece |
| `asset-8.png` | `asset-8.jpg` | Leadership letters, lower edge | 46.7% | Pass: diagonal torn edge retained |
| `asset-9.png` | `asset-9.jpg` | Purpose section, left edge | 38.8% | Pass: lavender strip remains distinct |
| `asset-10.png` | `asset-10.jpg` | Purpose section, upper edge | 49.9% | Pass: paper silhouette retained |
| `asset-11.png` | `asset-11.jpg` | Purpose section, lower edge | 52.3% | Pass: kraft-paper texture retained |
| `asset-12.png` | `indir (16).jfif` | Conference, upper edge | 35.0% | Pass: purple paper fragment retained |
| `asset-13.png` | `asset-13.jpg` | Conference, side accent | 31.6% | Pass: baked checkerboard removed with a source-specific neutral key |
| `asset-14.png` | `indir (2).jfif` | Conference, ribbon accent | 80.0% | Pass: thin dotted ribbon retained |
| `asset-15.png` | `indir (3).jfif` | Programme, angled bow | 67.2% | Pass: ribbon outline retained |
| `asset-16.png` | `paper texture.jfif` | Programme, green cutout | 37.7% | Pass: irregular shape retained |
| `00e9a30753f9f708bf24201267dcfeb3.png` | `00e9a30753f9f708bf24201267dcfeb3.jpg` | Giving section, flowers | 59.0% | Pass: petals and centers retained |
| `38ce4829bf95691a5f696226fd7dd676.png` | `38ce4829bf95691a5f696226fd7dd676.jpg` | Giving section, gingham strip | 18.6% | Pass: transparent gaps between checks; strip remains readable |
| `4cb7532834cf0687a8b0a966b59b43f4.png` | `4cb7532834cf0687a8b0a966b59b43f4.jpg` | Applications, sticker sheet | 56.1% | Pass: individual stickers remain visible without the white sheet |
| `39a23bc6c616fff3f98acad14698f82c.png` | `39a23bc6c616fff3f98acad14698f82c.jpg` | Applications, small house doodle | 37.8% | Pass at small decorative scale |
| `6e4a6b406249ba3c1917fcdc52319204.png` | `6e4a6b406249ba3c1917fcdc52319204.jpg` | Applications, secondary illustration | 36.7% | Pass: colored line art retained |
| `f7ca03040f481342660a330dcf514f70.png` | `f7ca03040f481342660a330dcf514f70.jpg` | Applications, flower accent | 58.5% | Pass: petals and stem retained |

## Excluded

- `asset-7.jpg`: the cutout contained only about 2% visible artwork, so it was too faint to justify a placement.
- `9e4615fb29cf8e396f12d6e7c81dd9d5.jpg`: a stock-site watermark is baked into the lower edge; it is not used.
- The previously used turtle-like icon was removed from the team-note heading at the user's request.

## User-Eye Pass

- The first viewport still leads with HopeMUN identity, mission, and the action button.
- Doodles are distributed around distinct edges and orientations instead of collecting in one repeated corner.
- Decorative images remain behind text, use empty alt text, and do not block calls to action.
- Desktop and 390px mobile checks report no horizontal overflow; all active doodle PNGs load.
- Applications navigation still reaches its section and closes the mobile menu.