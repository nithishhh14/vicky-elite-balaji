// Local search landing pages ("Floor Tiles in Coimbatore", "Granite
// Countertops in Coimbatore"...). Competitors rank for these phrases with
// pages that carry no products at all; every page here is backed by the real
// catalogue, real sizes and an honest note when we have to source something.
//
// Rules: no invented stock, no prices, no "No. 1 / largest / best" claims.
// `match` selects from the real product collection; if it returns nothing the
// page still explains the material and says we source it on request.

export interface Guide {
  slug: string; // always ends -coimbatore: keeps the root namespace predictable
  h1: string;
  title: string;
  description: string;
  eyebrow: string;
  intro: string[];
  /** Which real products belong on this page. */
  match: { rx: RegExp; halls?: string[]; kind?: "tile" | "material" };
  choose: { title: string; detail: string }[];
  faq: { q: string; a: string }[];
  related: string[];
  enquiry: string;
}

export const guides: Guide[] = [
  {
    slug: "floor-tiles-coimbatore",
    h1: "Floor tiles in Coimbatore",
    title: "Floor Tiles in Coimbatore | Elite Balaji",
    description:
      "Vitrified, ceramic, heritage and large-format floor tiles from our Karamadai showroom, with sizes, finishes and laying by our own crews across Coimbatore.",
    eyebrow: "Tiles · Floors",
    intro: [
      "Floor tiles carry the whole house: they take the traffic, the water and the cleaning. What we stock ranges from 600 × 1200 mm vitrified tiles for a seamless hall floor to handmade Athangudi tiles for a veranda or pooja room.",
      "Everything below is in our catalogue with its real size and finish. We also lay what we supply, so the tile, the adhesive and the crew come from one team.",
    ],
    match: { rx: /floor|flooring/i },
    choose: [
      { title: "Room first, tile second", detail: "Living and dining floors suit large-format vitrified tiles; bathrooms and wash areas need an anti-skid surface; verandas take patterned or stone floors." },
      { title: "Fewer joints looks calmer", detail: "A 600 × 1200 mm tile halves the grout lines of a 600 × 600 mm floor in the same room." },
      { title: "Match the adhesive to the tile", detail: "Large and vitrified tiles need the right adhesive class, not river sand and cement, or they hollow and lift later." },
    ],
    faq: [
      { q: "What is the best tile size for a hall in Coimbatore?", a: "For most halls we suggest 600 × 1200 mm vitrified tiles: fewer joints, easier cleaning and a more spacious look. Smaller rooms often look better with 600 × 600 mm." },
      { q: "Do you lay the tiles as well?", a: "Yes. Our own crews measure, lay and finish across Coimbatore, Mettupalayam, Karamadai and the surrounding areas. Supply-only is fine too." },
      { q: "How do I get a rate?", a: "Rates move with stock, so we quote on WhatsApp or by phone once we know the tile, the area in square feet and where the job is." },
    ],
    related: ["bathroom-tiles-coimbatore", "vitrified-tiles-coimbatore", "athangudi-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm looking for floor tiles. Room: ___, area: ___ sq ft, location: ___.",
  },
  {
    slug: "wall-tiles-coimbatore",
    h1: "Wall tiles in Coimbatore",
    title: "Wall Tiles in Coimbatore | Elite Balaji",
    description:
      "Ceramic and vitrified wall tiles, marble-look large formats and stone cladding for bathrooms, kitchens and feature walls, from our Karamadai showroom.",
    eyebrow: "Tiles · Walls",
    intro: [
      "Wall tiles are lighter and more decorative than floor tiles, and they are where a bathroom or kitchen gets its character. We stock glazed ceramic wall tiles, marble-look large formats for feature walls, and natural stone cladding when you want real material on the wall.",
      "Tell us the wall size and the look you are after and we will show you what is in the showroom this week.",
    ],
    match: { rx: /wall|cladding|backsplash/i },
    choose: [
      { title: "Wall tiles are not floor tiles", detail: "Wall tiles are thinner and glazed for looks, not for foot traffic. Ask us before using a wall tile on a floor." },
      { title: "One feature wall, one plain", detail: "A patterned or marble-look wall works best when the other walls stay quiet." },
      { title: "Check the batch", detail: "Shade varies between production batches, so buy the full wall in one lot with a little extra." },
    ],
    faq: [
      { q: "Can I use the same tile on the wall and the floor?", a: "Some vitrified tiles work on both; glazed ceramic wall tiles do not belong on a floor. We will tell you which is which for the tile you like." },
      { q: "Do you supply marble-look tiles for feature walls?", a: "Yes, the Mozzato Endless 600 × 1200 mm range is marble-look and works well on walls, along with real marble and granite cladding." },
    ],
    related: ["bathroom-tiles-coimbatore", "elevation-tiles-coimbatore", "vitrified-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm looking for wall tiles. Room: ___, wall size: ___, location: ___.",
  },
  {
    slug: "bathroom-tiles-coimbatore",
    h1: "Bathroom tiles in Coimbatore",
    title: "Bathroom Tiles in Coimbatore | Elite Balaji",
    description:
      "Anti-skid floor tiles, wall tiles, wash basins and fittings for bathrooms, supplied and laid from our Karamadai showroom across Coimbatore.",
    eyebrow: "Tiles · Bathrooms",
    intro: [
      "A bathroom needs three decisions together: a floor tile with grip, a wall tile that suits it, and the basin and fittings. We keep all three, so the shades and sizes are chosen in one visit instead of three shops.",
      "Wet areas are also where bad laying shows fastest, which is why we prefer to supply the adhesive and grout with the tile.",
    ],
    match: { rx: /bath|basin|wash|sanitary/i },
    choose: [
      { title: "Grip on the floor", detail: "Choose a matt or anti-skid floor tile for the wet area. Polished tiles belong outside the shower." },
      { title: "Plan the basin early", detail: "The counter cut-out depends on the basin. Choosing the basin with the counter stone avoids re-cutting." },
      { title: "Grout matters", detail: "Epoxy grout resists staining in wet areas much better than cement grout." },
    ],
    faq: [
      { q: "Which tile is best for a bathroom floor?", a: "A matt or anti-skid vitrified tile in 300 × 300 mm or 600 × 600 mm. We can show you the texture in the showroom so you can feel the grip." },
      { q: "Do you supply wash basins too?", a: "Yes. We carry art basins and marble-finish basin collections in many shapes and sizes, plus quartz and steel kitchen sinks." },
    ],
    related: ["wash-basins-coimbatore", "wall-tiles-coimbatore", "floor-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm doing a bathroom. Floor area: ___, wall height: ___, location: ___.",
  },
  {
    slug: "vitrified-tiles-coimbatore",
    h1: "Vitrified tiles: GVT, PGVT & double charge",
    title: "Vitrified Tiles (GVT & PGVT) in Coimbatore | Elite Balaji",
    description:
      "GVT, PGVT and double-charge vitrified tiles explained, with the sizes and finishes we stock in Karamadai and supply across Coimbatore.",
    eyebrow: "Tiles · Vitrified",
    intro: [
      "Vitrified tiles are pressed and fired hard enough to absorb very little water, which is why they suit Indian floors. The confusing part is the labels, so here they are in plain words.",
      "GVT is a vitrified tile with a printed glaze, so it can look like marble, wood or stone. PGVT is the same thing polished to a mirror finish. Double charge presses two layers of pigment deep into the body, so the pattern survives heavy traffic but comes in plainer designs.",
    ],
    match: { rx: /vitrified|gvt|pgvt|double charge/i },
    choose: [
      { title: "GVT for looks", detail: "The best marble, wood and stone reproductions are GVT, because the design is printed rather than pressed." },
      { title: "PGVT for shine", detail: "Polished glazed tiles reflect light and make a room feel larger, but show scratches and footprints sooner." },
      { title: "Double charge for traffic", detail: "Showrooms, offices and busy homes: the design goes deep into the tile, so wear does not erase it." },
    ],
    faq: [
      { q: "What is the difference between GVT and PGVT?", a: "Both are glazed vitrified tiles. PGVT has a polished, glossy surface; plain GVT is usually matt or satin. The body underneath is the same." },
      { q: "Is double charge better than GVT?", a: "It is tougher, not prettier. Choose double charge for heavy traffic and GVT when you want a marble, wood or stone look." },
      { q: "Which sizes do you stock?", a: "Commonly 600 × 600 mm and 600 × 1200 mm, with larger formats on request. Ask us what is in the showroom this week." },
    ],
    related: ["large-format-tiles-coimbatore", "floor-tiles-coimbatore", "wall-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm comparing GVT, PGVT and double charge tiles for: ___.",
  },
  {
    slug: "large-format-tiles-coimbatore",
    h1: "Large format tiles (600 × 1200 and up)",
    title: "Large Format Tiles in Coimbatore | Elite Balaji",
    description:
      "600 × 1200 mm and larger tiles for seamless floors and feature walls, with the laying care big formats need, from Elite Balaji, Karamadai.",
    eyebrow: "Tiles · Large format",
    intro: [
      "Large format means fewer joints: a calmer floor, less grout to clean and a room that reads bigger. The trade-off is that big tiles are less forgiving to lay, so the floor has to be level and the adhesive right.",
      "We stock 600 × 1200 mm as standard and can source larger slabs on request.",
    ],
    match: { rx: /1200|1600|2400|large format/i },
    choose: [
      { title: "Level the floor first", detail: "A large tile telegraphs every dip in the base. Levelling before laying is not an extra, it is the job." },
      { title: "Use the right adhesive", detail: "Large formats need a C2-class adhesive with full back coverage, not spot fixing." },
      { title: "Plan the layout", detail: "Set the first row against the main sightline so cut tiles land where nobody looks." },
    ],
    faq: [
      { q: "Do large tiles work in small rooms?", a: "Often yes: fewer joints make a small room look larger. We can lay out the tile sizes against your room dimensions." },
      { q: "Can you supply tiles bigger than 600 × 1200 mm?", a: "We can source 800 × 1600 mm and 1200 × 2400 mm formats. Ask us for the current options and lead time." },
    ],
    related: ["vitrified-tiles-coimbatore", "floor-tiles-coimbatore", "marble-look-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm interested in large format tiles for: ___ (area ___ sq ft).",
  },
  {
    slug: "marble-look-tiles-coimbatore",
    h1: "Marble-look tiles in Coimbatore",
    title: "Marble-look Tiles in Coimbatore | Elite Balaji",
    description:
      "Marble-look vitrified tiles in 600 × 1200 mm from the Mozzato Endless collection, plus real marble slabs, compared honestly by Elite Balaji, Karamadai.",
    eyebrow: "Tiles · Marble look",
    intro: [
      "Marble veining without marble's upkeep: printed vitrified tiles have become good enough that most visitors cannot tell from standing height. They do not etch with lemon or stain with turmeric, and they cost less to lay.",
      "We stock both, so you can put a real marble slab beside the tile that imitates it and decide with your own eyes.",
    ],
    match: { rx: /marble/i },
    choose: [
      { title: "Tile for floors, marble for moments", detail: "Large floors in marble-look tile, real marble where it is touched and seen: a tulsi madam, a temple step, a feature wall." },
      { title: "Repeat patterns", detail: "Printed tiles repeat every few faces. Lay a few boxes out before fixing to spread the repeats." },
      { title: "Sealing", detail: "Real marble needs sealing and quick spill wiping; the tile does not." },
    ],
    faq: [
      { q: "Is marble-look tile cheaper than marble?", a: "Usually, and the laying is simpler too. We will quote both for your area so you can compare properly." },
      { q: "Will it look fake?", a: "Not in 600 × 1200 mm formats with a matt carving finish, which is what we stock. Come and see the Mozzato Endless range in the showroom." },
    ],
    related: ["large-format-tiles-coimbatore", "floor-tiles-coimbatore", "granite-countertops-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm choosing between marble and marble-look tiles for: ___.",
  },
  {
    slug: "athangudi-tiles-coimbatore",
    h1: "Athangudi & heritage tiles",
    title: "Athangudi & Heritage Tiles in Coimbatore | Elite Balaji",
    description:
      "Handmade Athangudi and patterned heritage tiles for verandas, pooja rooms and accent floors, supplied from Elite Balaji, Karamadai, Coimbatore.",
    eyebrow: "Tiles · Heritage",
    intro: [
      "Athangudi tiles are made by hand in Chettinad: coloured cement poured over a glass plate, one tile at a time. No two are identical, and that is the point.",
      "They suit verandas, pooja rooms, courtyards and any floor that should feel made rather than bought. They need a little care: a cement-based tile is softer than vitrified, so it prefers gentle cleaning.",
    ],
    match: { rx: /athangudi|moroccan|heritage|pattern|kolam/i },
    choose: [
      { title: "Give them a border", detail: "A plain border around a patterned field stops the floor looking restless." },
      { title: "Expect variation", detail: "Handmade means shade and edge differences. Mixing boxes while laying spreads the variation evenly." },
      { title: "Seal after laying", detail: "A wax or sealer brings out the colour and keeps stains out of the cement surface." },
    ],
    faq: [
      { q: "Are Athangudi tiles suitable for a bathroom?", a: "We suggest them for dry areas: verandas, pooja rooms, living floors. For wet areas a vitrified anti-skid tile is safer." },
      { q: "Can I get a custom pattern?", a: "Patterns and colour combinations can be made to order with lead time, and we also print custom designs onto vitrified tiles." },
    ],
    related: ["floor-tiles-coimbatore", "custom-printed-tiles-coimbatore", "wall-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'd like Athangudi or heritage tiles for: ___ (area ___ sq ft).",
  },
  {
    slug: "parking-tiles-coimbatore",
    h1: "Car parking & anti-skid tiles",
    title: "Car Parking & Anti-skid Tiles in Coimbatore | Elite Balaji",
    description:
      "Heavy-duty parking tiles, anti-skid outdoor surfaces and Kota stone for driveways, porticos and wash areas, from Elite Balaji, Karamadai.",
    eyebrow: "Tiles · Parking & outdoor",
    intro: [
      "A parking floor takes vehicle weight, turning tyres, rain and sun. It needs a thicker, textured surface, and the base under it matters as much as the tile.",
      "Alongside heavy-duty parking tiles we supply Kota stone, which many Coimbatore homes still prefer for driveways and open areas because it is hard, cool underfoot and repairable piece by piece.",
    ],
    match: { rx: /parking|anti.?skid|driveway|outdoor|pathway|veranda|courtyard/i },
    choose: [
      { title: "Texture over polish", detail: "Anything polished becomes a skating rink when wet. Parking and open areas want a rough or structured face." },
      { title: "The base carries the car", detail: "Tiles do not take the load, the bed under them does. Skimping there cracks the best tile." },
      { title: "Think about repairs", detail: "Kota and stone can be lifted and replaced piece by piece; a printed tile has to match a batch that may be gone." },
    ],
    faq: [
      { q: "Which is better for parking: tiles or Kota stone?", a: "Both work. Kota is hard, repairable and cool; parking tiles offer more patterns and a flatter finish. We will quote both for your area." },
      { q: "Do you supply paver blocks?", a: "We can source paver blocks and outdoor stone on request. Tell us the area and the vehicle load and we will suggest the option." },
    ],
    related: ["kota-stone-coimbatore", "elevation-tiles-coimbatore", "floor-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I need parking or outdoor flooring. Area: ___ sq ft, location: ___.",
  },
  {
    slug: "elevation-tiles-coimbatore",
    h1: "Elevation tiles & stone cladding",
    title: "Elevation Tiles & Stone Cladding in Coimbatore | Elite Balaji",
    description:
      "Exterior elevation tiles and granite cladding for front walls, compound walls and porticos, supplied and fixed from Karamadai, Coimbatore.",
    eyebrow: "Exterior · Elevation",
    intro: [
      "The front elevation is the part of the house everybody sees and the part the weather attacks hardest. Sun, monsoon and dust decide how a facade ages, not the showroom lighting.",
      "We supply weather-resistant elevation tiles and natural granite cladding, and our crews fix both. Granite costs more up front and needs almost nothing afterwards.",
    ],
    match: { rx: /elevation|cladding|facade|exterior/i },
    choose: [
      { title: "Darker stone hides weather", detail: "Rain marks and dust show far less on a dark granite or a textured tile than on a pale gloss face." },
      { title: "Fix it properly", detail: "Exterior cladding needs mechanical fixing or a proper exterior adhesive; interior adhesive fails outdoors." },
      { title: "Mind the joints", detail: "Water gets in at the joints. Sealed, well-planned joints are what make a facade last." },
    ],
    faq: [
      { q: "Granite or tiles for the front elevation?", a: "Granite lasts longer and needs no maintenance; elevation tiles offer more texture and pattern for less money. Many houses use granite at the base and tiles above." },
      { q: "Do you fix elevation cladding?", a: "Yes, our own crews do supply and fixing across Coimbatore and the surrounding areas." },
    ],
    related: ["granite-countertops-coimbatore", "parking-tiles-coimbatore", "wall-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm planning a front elevation. Area: ___ sq ft, location: ___.",
  },
  {
    slug: "granite-countertops-coimbatore",
    h1: "Granite countertops in Coimbatore",
    title: "Granite Countertops in Coimbatore | Elite Balaji",
    description:
      "Black Galaxy, Absolute Black, Tan Brown and leathered granite kitchen countertops, cut and fitted from our own slab yard in Karamadai.",
    eyebrow: "Granite · Countertops",
    intro: [
      "A kitchen countertop is the hardest-working surface in the house. Granite handles heat, knives and turmeric better than almost anything else, and we photograph our slabs in our own yard so you see the actual stone.",
      "We cut, edge and fit, including the sink cut-out, so the counter, the sink and the fitting are one job.",
    ],
    match: { rx: /counter|worktop|kitchen/i, halls: ["granite-marbles", "quartz", "kadappa"] },
    choose: [
      { title: "Leathered hides everything", detail: "A leathered black granite hides fingerprints and water marks that polished black shows all day." },
      { title: "Check the actual slab", detail: "Granite changes from block to block. Photos narrow it down; the slab in the yard decides it." },
      { title: "Plan the sink with the stone", detail: "An undermount quartz or steel sink needs its cut-out planned before the counter is cut." },
    ],
    faq: [
      { q: "Which granite is best for a kitchen platform?", a: "Black Galaxy and Absolute Black are the usual choices in Coimbatore for their hardness and looks. Tan Brown suits warmer kitchens. Leathered finishes hide marks best." },
      { q: "Do you make the sink cut-out?", a: "Yes. Bring the sink or buy it with the counter, and we cut, polish the edge and fit on site." },
      { q: "Granite or quartz?", a: "Granite is natural, heat-proof and unique per slab. Quartz is engineered, non-porous and perfectly consistent. We stock both and will show you the difference side by side." },
    ],
    related: ["kitchen-sinks-coimbatore", "marble-look-tiles-coimbatore", "elevation-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I need a granite kitchen countertop. Running feet: ___, location: ___.",
  },
  {
    slug: "wash-basins-coimbatore",
    h1: "Wash basins in Coimbatore",
    title: "Wash Basins in Coimbatore | Elite Balaji",
    description:
      "Table-top art basins, marble-finish basins and ceramic wash basins in many shapes and sizes, from Elite Balaji, Karamadai, Coimbatore.",
    eyebrow: "Sanitaryware · Basins",
    intro: [
      "Table-top basins changed bathrooms: the basin sits on the counter as an object rather than disappearing into it. We carry two full collections, one patterned and gold-detailed, one in marble finishes, in sizes from 14 to 25 inches.",
      "Because we also supply the counter stone, the basin and the cut-out get planned together.",
    ],
    match: { rx: /basin/i },
    choose: [
      { title: "Size to the counter", detail: "Measure the counter depth first. A 22-inch basin needs a deeper counter than a 16-inch one." },
      { title: "Tap height matters", detail: "Table-top basins sit high, so they need a tall basin mixer or a wall-mounted spout." },
      { title: "Shape follows cleaning", detail: "Rounded interiors wipe clean faster than sharp-cornered rectangles." },
    ],
    faq: [
      { q: "What sizes do the basins come in?", a: "From about 14 × 14 inches up to 25 × 17 inches across the collections. Each range page on this site lists its size." },
      { q: "Are the marble basins real stone?", a: "The collection is catalogued as “Marble”. Ask us to confirm the exact material of a specific model before you order — we will not guess on your behalf." },
      { q: "Do you supply the tap and waste too?", a: "We supply basins and can arrange the fittings with them. Tell us the model you like and we will put a set together." },
    ],
    related: ["bathroom-tiles-coimbatore", "kitchen-sinks-coimbatore", "granite-countertops-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm looking for a wash basin. Counter size: ___, style: ___, location: ___.",
  },
  {
    slug: "kitchen-sinks-coimbatore",
    h1: "Quartz & steel kitchen sinks",
    title: "Quartz & Steel Kitchen Sinks in Coimbatore | Elite Balaji",
    description:
      "Quartz composite and stainless steel kitchen sinks in single bowl, double bowl and drainboard versions, supplied with your counter from Karamadai.",
    eyebrow: "Sanitaryware · Sinks",
    intro: [
      "Quartz composite sinks have taken over Coimbatore kitchens: matt finish, quieter than steel, and they hide water marks. Stainless steel still wins on price and on taking abuse.",
      "We supply both, and because the counter comes from our own yard the cut-out is planned with the stone rather than after it.",
    ],
    match: { rx: /sink/i, halls: ["sanitaryware"] },
    choose: [
      { title: "Single, double or drainboard", detail: "A single large bowl suits big vessels; a drainboard keeps water off the counter; double bowls suit washing and rinsing apart." },
      { title: "Undermount needs planning", detail: "Undermounting looks cleaner and wipes straight into the bowl, but the cut-out must be made before the counter is polished." },
      { title: "Quartz colour", detail: "Black and grey hide marks best; lighter shades show them but keep a small kitchen brighter." },
    ],
    faq: [
      { q: "Is a quartz sink better than stainless steel?", a: "It is quieter, hides scratches and looks more finished. Steel is cheaper, lighter and handles rough use. Both are stocked, so come and feel the difference." },
      { q: "Can you fit the sink into my existing counter?", a: "Often yes, depending on the current cut-out size and the counter material. Send us a photo and the measurements on WhatsApp." },
    ],
    related: ["granite-countertops-coimbatore", "wash-basins-coimbatore", "bathroom-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm looking for a kitchen sink. Counter: ___, single/double bowl: ___, location: ___.",
  },
  {
    slug: "kota-stone-coimbatore",
    h1: "Kota stone in Coimbatore",
    title: "Kota Stone in Coimbatore | Elite Balaji",
    description:
      "Kota stone flooring in blue, green and beige shades for homes, parking, corridors and temples, supplied and laid from Karamadai, Coimbatore.",
    eyebrow: "Natural stone · Kota",
    intro: [
      "Kota is a fine-grained limestone from Rajasthan that has floored South Indian homes for generations: hard, cool underfoot, cheap to maintain and repairable one piece at a time.",
      "It comes rough and is polished on site, which is why the same stone can look rustic or glassy depending on the finish you ask for.",
    ],
    match: { rx: /kota|kadappa|limestone/i },
    choose: [
      { title: "Honed for grip, polished for shine", detail: "Honed or natural finishes suit parking, corridors and wet areas; mirror polish suits interior floors." },
      { title: "Shade varies", detail: "Blue, green and beige lots differ. See the actual lot before ordering a large area." },
      { title: "It ages well", detail: "Kota can be re-polished years later instead of being replaced." },
    ],
    faq: [
      { q: "Is Kota stone good for parking areas?", a: "Yes, it is one of the most common choices in Coimbatore for driveways and open areas because it is hard and repairable." },
      { q: "How is Kota different from Kadappa?", a: "Kadappa is a darker, almost black limestone from Andhra, usually used for kitchen platforms, steps and borders. Kota is lighter, in blue, green and beige shades, and used mainly for floors." },
    ],
    related: ["parking-tiles-coimbatore", "floor-tiles-coimbatore", "granite-countertops-coimbatore"],
    enquiry: "Hi Elite Balaji, I'm looking for Kota stone. Area: ___ sq ft, finish: ___, location: ___.",
  },
  {
    slug: "custom-printed-tiles-coimbatore",
    h1: "Custom printed tiles",
    title: "Custom Printed Tiles in Coimbatore | Elite Balaji",
    description:
      "Your image printed on vitrified tile: pooja room murals, kitchen backsplashes and feature walls, made to order and delivered across India.",
    eyebrow: "Custom · Printed tiles",
    intro: [
      "Send us an image and a wall size, and it can be printed across vitrified or ceramic tiles: deity art for a pooja room, a landscape behind the kitchen counter, a heritage pattern recreated, or a shop's own artwork.",
      "We confirm the tile, the size and the layout with you before anything is printed, and we deliver across India.",
    ],
    match: { rx: /athangudi|moroccan|pattern|print/i, kind: "tile" },
    choose: [
      { title: "Resolution decides the size", detail: "A phone photo prints well up to a certain wall size. Send the image first and we will tell you honestly how large it can go." },
      { title: "Plan around the joints", detail: "The design is split across tiles, so we place the joints away from faces and focal points." },
      { title: "Approve the layout", detail: "You see the tile layout before printing starts. Nothing is printed on a guess." },
    ],
    faq: [
      { q: "Can you print a family photo on tiles?", a: "Yes, as long as the image is sharp enough for the wall size. Send it on WhatsApp and we will check it before quoting." },
      { q: "How long does it take?", a: "It depends on the size and the tile. We confirm the timeline when we confirm the layout." },
      { q: "Do you deliver outside Coimbatore?", a: "Yes, custom art products including printed tiles are delivered across India." },
    ],
    related: ["athangudi-tiles-coimbatore", "wall-tiles-coimbatore", "floor-tiles-coimbatore"],
    enquiry: "Hi Elite Balaji, I'd like custom printed tiles. Image: (attached). Wall size: ___. Room: ___.",
  },
];

export const guideBySlug = (slug: string) => guides.find((g) => g.slug === slug);
