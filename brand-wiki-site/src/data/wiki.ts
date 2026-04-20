import type { CollectionEntry } from 'astro:content';
import type { ImageMetadata } from 'astro';

import brandKitImage from '../images/brand-kit/brand-kit-bento-grid.webp';
import coverAnamnesis from '../images/covers/book-cover-1-anamnesis-engine.webp';
import coverChorus from '../images/covers/book-cover-2-myocardial-chorus.webp';
import coverRipening from '../images/covers/book-cover-3-the-ripening.webp';
import logoGlassClassic from '../images/logos/logo-glass-classic.webp';
import logoGlassGradient from '../images/logos/logo-glass-gradient.webp';
import logoWaxSealBroken from '../images/logos/logo-wax-seal-broken.webp';
import logoWaxSealTriple from '../images/logos/logo-wax-seal-triple.webp';
import anatomyHeartBrain from '../images/anatomy/anatomy-heart-brain-axis.webp';
import anatomyTriangulation from '../images/anatomy/anatomy-triangulation-engine.webp';
import anatomyVagal from '../images/anatomy/anatomy-vagal-nerve.webp';
import anatomyField from '../images/anatomy/anatomy-khaloree-field-architecture.webp';
import anatomySeverance from '../images/anatomy/anatomy-severance-pathways.webp';
import anatomySomaticMapping from '../images/anatomy/anatomy-somatic-mapping.webp';
import anatomyNeural from '../images/anatomy/anatomy-neural-dendrites.webp';
import arcanaFool from '../images/arcana/00-fool-stem-cell.webp';
import arcanaHighPriestess from '../images/arcana/02-high-priestess-pineal.webp';
import arcanaChariot from '../images/arcana/07-chariot-cardiac-coherence.webp';
import arcanaTower from '../images/arcana/16-tower-severance.webp';
import arcanaWorld from '../images/arcana/21-world-homeostasis.webp';

export type DocEntry = CollectionEntry<'docs'>;

export interface CategoryMeta {
  id: string;
  label: string;
  kicker: string;
  description: string;
  featureImage: ImageMetadata;
  featureAlt: string;
}

export interface AssetFamilyMeta {
  id: string;
  label: string;
  kicker: string;
  description: string;
  count: number;
  href: string;
  featureImage: ImageMetadata;
  featureAlt: string;
  relatedDocs: string[];
}

export interface DocVisualMeta {
  eyebrow: string;
  summary: string;
  heroImage: ImageMetadata;
  heroAlt: string;
  highlights: string[];
  assetFamilies: string[];
  gallery: Array<{
    image: ImageMetadata;
    alt: string;
    label: string;
  }>;
}

export const archiveStats = [
  { label: 'Core dossiers', value: '9' },
  { label: 'Mapped visuals', value: '42' },
  { label: 'Asset families', value: '5' },
] as const;

export const categoryOrder = ['overview', 'product', 'brand', 'audience', 'market'] as const;

export const assetFamilyOrder = ['brand-kit', 'covers', 'logos', 'anatomy', 'arcana'] as const;

export const categoryMeta: Record<string, CategoryMeta> = {
  overview: {
    id: 'overview',
    label: 'Getting Started',
    kicker: 'Foundational brief',
    description: 'The complete brand identity, archive orientation, and key concepts that frame the trilogy.',
    featureImage: brandKitImage,
    featureAlt: 'Somatic Canticles brand kit board composed of covers, logos, and palette studies.',
  },
  product: {
    id: 'product',
    label: 'Trilogy Design',
    kicker: 'System architecture',
    description: 'Product overview, feature stack, and market positioning for the three-book Somatic Canticles arc.',
    featureImage: coverAnamnesis,
    featureAlt: 'Book one cover for Anamnesis Engine.',
  },
  brand: {
    id: 'brand',
    label: 'Brand System',
    kicker: 'Clinical mysticism',
    description: 'Voice, tone, visual identity, and the symbolic systems that make the archive feel authored rather than templated.',
    featureImage: logoGlassGradient,
    featureAlt: 'Glass sigil logo for Somatic Canticles.',
  },
  audience: {
    id: 'audience',
    label: 'Reader Archetype',
    kicker: 'Who this work serves',
    description: 'The Philosopher-Healer profile, their worldview, their habits, and why this trilogy is calibrated for them.',
    featureImage: arcanaHighPriestess,
    featureAlt: 'Tarot-biological illustration for the High Priestess and the pineal system.',
  },
  market: {
    id: 'market',
    label: 'Market Thesis',
    kicker: 'Proof and positioning',
    description: 'Niche validation, competitor gaps, and the strategic logic for how Somatic Canticles enters the market.',
    featureImage: anatomyHeartBrain,
    featureAlt: 'Anatomical diagram of the heart-brain axis.',
  },
};

export const assetFamilyMeta: Record<string, AssetFamilyMeta> = {
  'brand-kit': {
    id: 'brand-kit',
    label: 'Brand Board',
    kicker: 'System overview',
    description: 'The single board that compresses covers, logos, palette, anatomy, and arcana into one inspectable operating sheet.',
    count: 1,
    href: '/visual-atlas#brand-kit',
    featureImage: brandKitImage,
    featureAlt: 'Somatic Canticles brand board composed of covers, logos, anatomy, and arcana studies.',
    relatedDocs: ['index', 'brand/visual-identity'],
  },
  covers: {
    id: 'covers',
    label: 'Book Covers',
    kicker: 'Trilogy arc',
    description: 'Three title-specific cover treatments that track the narrative movement from anamnesis to myocardial chorus to ripening.',
    count: 3,
    href: '/visual-atlas#covers',
    featureImage: coverRipening,
    featureAlt: 'The Ripening cover artwork for Somatic Canticles.',
    relatedDocs: ['product/overview', 'product/positioning'],
  },
  logos: {
    id: 'logos',
    label: 'Logo System',
    kicker: 'Identity marks',
    description: 'Glass sigils and wax seals that hold the project between sacred object, clinical artifact, and archival stamp.',
    count: 8,
    href: '/visual-atlas#logos',
    featureImage: logoGlassClassic,
    featureAlt: 'Somatic Canticles glass sigil logo treatment.',
    relatedDocs: ['brand/visual-identity', 'brand/voice-tone'],
  },
  anatomy: {
    id: 'anatomy',
    label: 'Anatomy Diagrams',
    kicker: 'Embodied rigor',
    description: 'Somatic and neuroscientific diagrams that keep the trilogy grounded in felt biology instead of untethered metaphor.',
    count: 8,
    href: '/visual-atlas#anatomy',
    featureImage: anatomyHeartBrain,
    featureAlt: 'Heart-brain axis diagram used in the Somatic Canticles archive.',
    relatedDocs: ['product/features', 'market/niche-validation'],
  },
  arcana: {
    id: 'arcana',
    label: 'Arcana Studies',
    kicker: 'Mythic-biological deck',
    description: 'Twenty-two tarot-biological correspondences that translate symbolic states into concrete physiological and psychological imagery.',
    count: 22,
    href: '/visual-atlas#arcana',
    featureImage: arcanaChariot,
    featureAlt: 'Chariot arcana illustration paired with cardiac coherence symbolism.',
    relatedDocs: ['audience/primary-persona', 'market/competitive-landscape'],
  },
};

export const docMeta: Record<string, DocVisualMeta> = {
  index: {
    eyebrow: 'Master archive brief',
    summary: 'The shortest path into the world: what Somatic Canticles is, who it serves, and which dossier to read next.',
    heroImage: brandKitImage,
    heroAlt: 'Brand identity board for Somatic Canticles showing the trilogy system.',
    highlights: [
      'Maps the trilogy arc across diagnosis, integration, and mastery.',
      'Explains the Philosopher-Healer reader identity and why the brand exists.',
      'Links the most important product, audience, brand, and market dossiers.',
    ],
    assetFamilies: ['brand-kit', 'covers', 'logos'],
    gallery: [
      { image: coverAnamnesis, alt: 'Cover for book one, Anamnesis Engine.', label: 'Book one cover' },
      { image: logoGlassClassic, alt: 'Classic glass sigil logo.', label: 'Glass sigil' },
      { image: arcanaWorld, alt: 'World arcana biological illustration.', label: 'Arcana endpoint' },
    ],
  },
  'product/overview': {
    eyebrow: 'Trilogy chassis',
    summary: 'A product-level look at the trilogy promise, structure, use cases, and emotional trajectory.',
    heroImage: coverAnamnesis,
    heroAlt: 'Anamnesis Engine cover artwork.',
    highlights: [
      'Frames the trilogy as a three-phase healing journey.',
      'Clarifies the core value propositions for readers and practitioners.',
      'Captures the intended emotional progression from curiosity to integration.',
    ],
    assetFamilies: ['covers', 'brand-kit', 'anatomy'],
    gallery: [
      { image: coverChorus, alt: 'The Myocardial Chorus cover artwork.', label: 'Book two cover' },
      { image: coverRipening, alt: 'The Ripening cover artwork.', label: 'Book three cover' },
      { image: anatomyTriangulation, alt: 'Triangulation engine anatomy diagram.', label: 'Triangulation engine' },
    ],
  },
  'product/features': {
    eyebrow: 'Feature stack',
    summary: 'The mechanisms, reader benefits, and concrete differentiators that make the trilogy feel engineered instead of merely atmospheric.',
    heroImage: anatomyTriangulation,
    heroAlt: 'Triangulation engine diagram from the Somatic Canticles visual system.',
    highlights: [
      'Breaks the narrative system into functional, emotional, and symbolic value.',
      'Connects story mechanics to concrete neuroscience and somatic concepts.',
      'Positions the trilogy as a designed experience rather than a generic lore deck.',
    ],
    assetFamilies: ['anatomy', 'arcana', 'covers'],
    gallery: [
      { image: anatomySomaticMapping, alt: 'Somatic mapping system diagram.', label: 'Somatic mapping' },
      { image: anatomyVagal, alt: 'Vagal nerve anatomy diagram.', label: 'Vagal system' },
      { image: arcanaChariot, alt: 'Chariot arcana biological illustration.', label: 'Cardiac coherence arcana' },
    ],
  },
  'product/positioning': {
    eyebrow: 'Market angle',
    summary: 'The exact wedge Somatic Canticles occupies between hard SF, trauma literature, and visionary mysticism.',
    heroImage: coverChorus,
    heroAlt: 'The Myocardial Chorus cover artwork.',
    highlights: [
      'Explains the high-rigor, high-embodiment, transformational-arc quadrant.',
      'Benchmarks the trilogy against Watts, Egan, Chiang, and van der Kolk.',
      'Provides the clearest one-sentence articulation of the project’s market position.',
    ],
    assetFamilies: ['covers', 'logos', 'brand-kit'],
    gallery: [
      { image: coverRipening, alt: 'The Ripening cover artwork.', label: 'Final arc cover' },
      { image: logoWaxSealTriple, alt: 'Triple wax seal logo variant.', label: 'Wax seal system' },
      { image: brandKitImage, alt: 'Brand kit composition board.', label: 'Brand board' },
    ],
  },
  'brand/voice-tone': {
    eyebrow: 'Voice system',
    summary: 'How Somatic Canticles speaks: rigorous, embodied, and symbolically exact without drifting into generic mystic copy.',
    heroImage: logoWaxSealTriple,
    heroAlt: 'Triple wax seal logo treatment.',
    highlights: [
      'Defines voice traits, banned language, and preferred rhetorical patterns.',
      'Keeps the brand from slipping into startup filler or vague spirituality.',
      'Turns the archive into a coherent authored voice rather than disconnected docs.',
    ],
    assetFamilies: ['logos', 'arcana', 'brand-kit'],
    gallery: [
      { image: logoGlassGradient, alt: 'Gradient glass sigil logo.', label: 'Glass sigil' },
      { image: logoWaxSealBroken, alt: 'Broken wax seal logo.', label: 'Broken seal' },
      { image: arcanaFool, alt: 'Fool arcana stem cell illustration.', label: 'Origin image' },
    ],
  },
  'brand/visual-identity': {
    eyebrow: 'Visual doctrine',
    summary: 'The palette, typography, symbolism, and image rules that define Somatic Canticles as clinical mysticism.',
    heroImage: brandKitImage,
    heroAlt: 'Somatic Canticles visual identity board.',
    highlights: [
      'Codifies the trilogy’s clinical mysticism look and feel.',
      'Documents palette, typography, logo usage, and graphic system rules.',
      'Provides the visual bridge between neuroscience precision and sacred imagery.',
    ],
    assetFamilies: ['brand-kit', 'logos', 'covers'],
    gallery: [
      { image: logoGlassClassic, alt: 'Classic glass sigil logo.', label: 'Primary logo' },
      { image: coverAnamnesis, alt: 'Anamnesis Engine cover.', label: 'Cover application' },
      { image: anatomyField, alt: 'Khaloree field architecture diagram.', label: 'System visual' },
    ],
  },
  'audience/primary-persona': {
    eyebrow: 'Primary reader',
    summary: 'The Philosopher-Healer archetype, their media diet, frustrations, decision criteria, and the language that resonates with them.',
    heroImage: arcanaHighPriestess,
    heroAlt: 'High Priestess arcana illustration associated with pineal symbolism.',
    highlights: [
      'Describes the hybrid reader who wants both neuroscience and mysticism handled seriously.',
      'Captures purchase triggers, pain points, and social proof requirements.',
      'Turns audience strategy into a concrete operator brief for brand and launch decisions.',
    ],
    assetFamilies: ['arcana', 'anatomy', 'covers'],
    gallery: [
      { image: coverAnamnesis, alt: 'Anamnesis Engine cover artwork.', label: 'Reader-facing cover' },
      { image: anatomyNeural, alt: 'Neural dendrites anatomy image.', label: 'Embodied cognition' },
      { image: arcanaChariot, alt: 'Chariot arcana cardiac coherence artwork.', label: 'Embodiment cue' },
    ],
  },
  'market/competitive-landscape': {
    eyebrow: 'Competitive field',
    summary: 'Where the trilogy sits relative to adjacent authors, adjacent categories, and the narrative gap it intends to occupy.',
    heroImage: anatomySeverance,
    heroAlt: 'Severance pathways anatomy illustration.',
    highlights: [
      'Maps comparable works and clarifies what Somatic Canticles uniquely combines.',
      'Turns competition into a strategic framing tool instead of a generic comparison list.',
      'Helps the archive explain why the project matters now.',
    ],
    assetFamilies: ['anatomy', 'arcana', 'logos'],
    gallery: [
      { image: coverRipening, alt: 'The Ripening cover artwork.', label: 'Endgame cover' },
      { image: logoWaxSealBroken, alt: 'Broken wax seal logo variant.', label: 'Fracture motif' },
      { image: anatomyHeartBrain, alt: 'Heart-brain axis anatomy image.', label: 'Somatic proof' },
    ],
  },
  'market/niche-validation': {
    eyebrow: 'Viability scorecard',
    summary: 'The practical readout of pain intensity, purchasing power, competition gap, and go-to-market confidence.',
    heroImage: anatomyHeartBrain,
    heroAlt: 'Heart-brain axis diagram used as a market proof visual.',
    highlights: [
      'Quantifies the niche case with an 85 percent viability score.',
      'Names the specific market tensions the trilogy resolves better than adjacent works.',
      'Provides a concrete launch thesis rather than abstract optimism.',
    ],
    assetFamilies: ['brand-kit', 'anatomy', 'arcana'],
    gallery: [
      { image: brandKitImage, alt: 'Brand board collage.', label: 'Brand evidence' },
      { image: anatomyVagal, alt: 'Vagal nerve anatomy image.', label: 'Biology cue' },
      { image: arcanaTower, alt: 'Tower arcana severance illustration.', label: 'Disruption motif' },
    ],
  },
};

export const primaryReadingPath = [
  'index',
  'product/overview',
  'brand/visual-identity',
  'audience/primary-persona',
  'market/niche-validation',
] as const;

export function getCategoryMeta(category?: string) {
  return category ? categoryMeta[category] : undefined;
}

export function getAssetFamilyMeta(family?: string) {
  return family ? assetFamilyMeta[family] : undefined;
}

export function getDocMeta(slug: string) {
  return docMeta[slug] ?? docMeta.index;
}

export function getDocAssetFamilies(slug: string) {
  return getDocMeta(slug).assetFamilies
    .map((family) => assetFamilyMeta[family])
    .filter(Boolean);
}

export function orderDocs(docs: DocEntry[]) {
  return [...docs].sort((a, b) => {
    const categoryRank = categoryOrder.indexOf((a.data.category ?? 'overview') as (typeof categoryOrder)[number])
      - categoryOrder.indexOf((b.data.category ?? 'overview') as (typeof categoryOrder)[number]);

    if (categoryRank !== 0) return categoryRank;

    const orderA = a.data.order ?? 999;
    const orderB = b.data.order ?? 999;
    if (orderA !== orderB) return orderA - orderB;

    return a.data.title.localeCompare(b.data.title);
  });
}

export function categoryLabel(category?: string) {
  return category ? (categoryMeta[category]?.label ?? category) : 'Archive';
}
