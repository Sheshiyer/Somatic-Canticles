import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import type { CollectionEntry } from 'astro:content';
import type { ImageMetadata } from 'astro';

export type DocEntry = CollectionEntry<'docs'>;
export type AssetFamilyId = 'brand-kit' | 'covers' | 'logos' | 'anatomy' | 'arcana';

interface GenerationManifestAsset {
  id: string;
  name: string;
  model: string;
  seeds: number;
  calls: number;
  est_cost: number;
}

interface GenerationManifest {
  total_assets: number;
  total_api_calls: number;
  estimated_cost_usd: number;
  assets: GenerationManifestAsset[];
}

interface MediaManifest {
  categories: Record<AssetFamilyId, string[]>;
  counts: Record<AssetFamilyId, number>;
  total: number;
}

interface AssetFamilyConfig {
  label: string;
  kicker: string;
  description: string;
  relatedDocs: string[];
  featureFile: string;
  featureAlt: string;
  assetFilter: (asset: GenerationManifestAsset) => boolean;
}

export interface CategoryMeta {
  id: string;
  label: string;
  kicker: string;
  description: string;
  featureImage: ImageMetadata;
  featureAlt: string;
}

export interface AssetFamilyMeta {
  id: AssetFamilyId;
  label: string;
  kicker: string;
  description: string;
  count: number;
  href: string;
  featureImage: ImageMetadata;
  featureAlt: string;
  relatedDocs: string[];
}

export interface VisualAssetRecord {
  id: string;
  title: string;
  subtitle: string;
  alt: string;
  family: AssetFamilyId;
  familyLabel: string;
  fileName: string;
  image: ImageMetadata;
  orientation: 'portrait' | 'landscape' | 'square';
  model: string;
  variants: number;
  estCostUsd: string;
}

export interface DocVisualMeta {
  eyebrow: string;
  summary: string;
  heroImage: ImageMetadata;
  heroAlt: string;
  highlights: string[];
  assetFamilies: AssetFamilyId[];
  gallery: Array<{
    image: ImageMetadata;
    alt: string;
    label: string;
  }>;
}

export interface BrandmintRunStats {
  totalAssets: number;
  totalApiCalls: number;
  estimatedCostUsd: string;
}

export const categoryOrder = ['overview', 'product', 'brand', 'audience', 'market'] as const;

export const assetFamilyOrder: AssetFamilyId[] = ['brand-kit', 'covers', 'logos', 'anatomy', 'arcana'];

const imageModules = import.meta.glob<{ default: ImageMetadata }>(
  '../images/**/*.{webp,png,jpg,jpeg,avif}',
  { eager: true }
);

const imageByKey = new Map(
  Object.entries(imageModules).map(([path, module]) => {
    const parts = path.split('/');
    const family = parts.at(-2);
    const fileName = parts.at(-1);
    return [`${family}/${fileName}`, module.default];
  })
);

function readJson<T>(relativePath: string): T {
  return JSON.parse(readFileSync(resolve(process.cwd(), relativePath), 'utf-8')) as T;
}

function resolveImage(family: AssetFamilyId, fileName: string): ImageMetadata {
  const image = imageByKey.get(`${family}/${fileName}`);

  if (!image) {
    throw new Error(`Missing synced wiki image for ${family}/${fileName}`);
  }

  return image;
}

function orientationFor(image: ImageMetadata): VisualAssetRecord['orientation'] {
  const ratio = image.width / image.height;

  if (ratio < 0.95) return 'portrait';
  if (ratio > 1.15) return 'landscape';
  return 'square';
}

function formatMoney(value: number): string {
  return value.toFixed(2);
}

function titleForAsset(asset: GenerationManifestAsset): string {
  if (asset.id === '2A') return asset.name;
  if (asset.id.startsWith('COVER-')) return asset.name.replace(/^Book Cover - /, '');
  if (asset.id.startsWith('LOGO-')) return asset.name.replace(/^Logo Variant - /, '');
  if (asset.id.startsWith('ANATOMY-')) return asset.name.replace(/^Anatomy Plate - /, '');
  if (asset.id.startsWith('ARCANA-')) return asset.name.replace(/^Arcana \d+ - /, '');
  return asset.name;
}

function subtitleForAsset(asset: GenerationManifestAsset, family: AssetFamilyId): string {
  if (family === 'arcana' && asset.name.includes(' / ')) {
    return asset.name.split(' / ').slice(1).join(' / ');
  }

  if (family === 'covers') return 'Hardcover series artwork';
  if (family === 'logos') return 'Identity mark variant';
  if (family === 'anatomy') return 'Sacred anatomy plate';
  if (family === 'brand-kit') return 'Current-run system board';

  return asset.model;
}

function galleryItem(family: AssetFamilyId, fileName: string, alt: string, label: string) {
  return {
    image: resolveImage(family, fileName),
    alt,
    label,
  };
}

const mediaManifest = readJson<MediaManifest>('src/images/media-manifest.json');
const generationManifest = readJson<GenerationManifest>(
  '../brandmint-input/somatic-canticles/generation-manifest.json'
);

const assetFamilyConfig: Record<AssetFamilyId, AssetFamilyConfig> = {
  'brand-kit': {
    label: 'Brand Board',
    kicker: 'System overview',
    description:
      'The single board that compresses covers, logos, palette, anatomy, and arcana into one inspectable operating sheet.',
    relatedDocs: ['index', 'brand/visual-identity'],
    featureFile: 'brand-kit-bento-grid.webp',
    featureAlt: 'Somatic Canticles brand board composed of covers, logos, anatomy, and arcana studies.',
    assetFilter: (asset) => asset.id === '2A',
  },
  covers: {
    label: 'Book Covers',
    kicker: 'Trilogy arc',
    description:
      'Three title-specific cover treatments that track the narrative movement from anamnesis to myocardial chorus to ripening.',
    relatedDocs: ['product/overview', 'product/positioning'],
    featureFile: 'book-cover-3-the-ripening.webp',
    featureAlt: 'The Ripening cover artwork for Somatic Canticles.',
    assetFilter: (asset) => asset.id.startsWith('COVER-'),
  },
  logos: {
    label: 'Logo System',
    kicker: 'Identity marks',
    description:
      'Glass sigils and wax seals that hold the project between sacred object, clinical artifact, and archival stamp.',
    relatedDocs: ['brand/visual-identity', 'brand/voice-tone'],
    featureFile: 'logo-glass-classic.webp',
    featureAlt: 'Somatic Canticles glass sigil logo treatment.',
    assetFilter: (asset) => asset.id.startsWith('LOGO-'),
  },
  anatomy: {
    label: 'Anatomy Diagrams',
    kicker: 'Embodied rigor',
    description:
      'Somatic and neuroscientific diagrams that keep the trilogy grounded in felt biology instead of untethered metaphor.',
    relatedDocs: ['product/features', 'market/niche-validation'],
    featureFile: 'anatomy-heart-brain-axis.webp',
    featureAlt: 'Heart-brain axis diagram used in the Somatic Canticles archive.',
    assetFilter: (asset) => asset.id.startsWith('ANATOMY-'),
  },
  arcana: {
    label: 'Arcana Studies',
    kicker: 'Mythic-biological deck',
    description:
      'Twenty-two tarot-biological correspondences that translate symbolic states into concrete physiological and psychological imagery.',
    relatedDocs: ['audience/primary-persona', 'market/competitive-landscape'],
    featureFile: '07-chariot-cardiac-coherence.webp',
    featureAlt: 'Chariot arcana illustration paired with cardiac coherence symbolism.',
    assetFilter: (asset) => asset.id.startsWith('ARCANA-'),
  },
};

const visualAssetsByFamily = Object.fromEntries(
  assetFamilyOrder.map((family) => {
    const familyFiles = mediaManifest.categories[family] ?? [];
    const pipelineAssets = generationManifest.assets.filter(assetFamilyConfig[family].assetFilter);

    if (familyFiles.length !== pipelineAssets.length) {
      throw new Error(
        `Brandmint/media manifest mismatch for ${family}: ${pipelineAssets.length} assets in generation-manifest.json, ${familyFiles.length} synced files in media-manifest.json`
      );
    }

    const assets: VisualAssetRecord[] = familyFiles.map((fileName, index) => {
      const pipelineAsset = pipelineAssets[index];
      const image = resolveImage(family, fileName);

      return {
        id: pipelineAsset.id,
        title: titleForAsset(pipelineAsset),
        subtitle: subtitleForAsset(pipelineAsset, family),
        alt: `${pipelineAsset.name} for Somatic Canticles`,
        family,
        familyLabel: assetFamilyConfig[family].label,
        fileName,
        image,
        orientation: orientationFor(image),
        model: pipelineAsset.model,
        variants: pipelineAsset.seeds,
        estCostUsd: formatMoney(pipelineAsset.est_cost),
      };
    });

    return [family, assets];
  })
) as Record<AssetFamilyId, VisualAssetRecord[]>;

export const brandmintRunStats: BrandmintRunStats = {
  totalAssets: generationManifest.total_assets,
  totalApiCalls: generationManifest.total_api_calls,
  estimatedCostUsd: formatMoney(generationManifest.estimated_cost_usd),
};

export const categoryMeta: Record<string, CategoryMeta> = {
  overview: {
    id: 'overview',
    label: 'Getting Started',
    kicker: 'Foundational brief',
    description: 'The complete brand identity, archive orientation, and key concepts that frame the trilogy.',
    featureImage: resolveImage('brand-kit', 'brand-kit-bento-grid.webp'),
    featureAlt: 'Somatic Canticles brand kit board composed of covers, logos, and palette studies.',
  },
  product: {
    id: 'product',
    label: 'Trilogy Design',
    kicker: 'System architecture',
    description:
      'Product overview, feature stack, and market positioning for the three-book Somatic Canticles arc.',
    featureImage: resolveImage('covers', 'book-cover-1-anamnesis-engine.webp'),
    featureAlt: 'Book one cover for Anamnesis Engine.',
  },
  brand: {
    id: 'brand',
    label: 'Brand System',
    kicker: 'Clinical mysticism',
    description:
      'Voice, tone, visual identity, and the symbolic systems that make the archive feel authored rather than templated.',
    featureImage: resolveImage('logos', 'logo-glass-gradient.webp'),
    featureAlt: 'Glass sigil logo for Somatic Canticles.',
  },
  audience: {
    id: 'audience',
    label: 'Reader Archetype',
    kicker: 'Who this work serves',
    description:
      'The Philosopher-Healer profile, their worldview, their habits, and why this trilogy is calibrated for them.',
    featureImage: resolveImage('arcana', '02-high-priestess-pineal.webp'),
    featureAlt: 'Tarot-biological illustration for the High Priestess and the pineal system.',
  },
  market: {
    id: 'market',
    label: 'Market Thesis',
    kicker: 'Proof and positioning',
    description:
      'Niche validation, competitor gaps, and the strategic logic for how Somatic Canticles enters the market.',
    featureImage: resolveImage('anatomy', 'anatomy-heart-brain-axis.webp'),
    featureAlt: 'Anatomical diagram of the heart-brain axis.',
  },
};

export const assetFamilyMeta = Object.fromEntries(
  assetFamilyOrder.map((family) => {
    const config = assetFamilyConfig[family];

    return [
      family,
      {
        id: family,
        label: config.label,
        kicker: config.kicker,
        description: config.description,
        count: visualAssetsByFamily[family].length,
        href: `/visual-atlas#${family}`,
        featureImage: resolveImage(family, config.featureFile),
        featureAlt: config.featureAlt,
        relatedDocs: config.relatedDocs,
      },
    ];
  })
) as Record<AssetFamilyId, AssetFamilyMeta>;

export const docMeta: Record<string, DocVisualMeta> = {
  index: {
    eyebrow: 'Master archive brief',
    summary: 'The shortest path into the world: what Somatic Canticles is, who it serves, and which dossier to read next.',
    heroImage: resolveImage('brand-kit', 'brand-kit-bento-grid.webp'),
    heroAlt: 'Brand identity board for Somatic Canticles showing the trilogy system.',
    highlights: [
      'Maps the trilogy arc across diagnosis, integration, and mastery.',
      'Explains the Philosopher-Healer reader identity and why the brand exists.',
      'Links the most important product, audience, brand, and market dossiers.',
    ],
    assetFamilies: ['brand-kit', 'covers', 'logos'],
    gallery: [
      galleryItem('covers', 'book-cover-1-anamnesis-engine.webp', 'Cover for book one, Anamnesis Engine.', 'Book one cover'),
      galleryItem('logos', 'logo-glass-classic.webp', 'Classic glass sigil logo.', 'Glass sigil'),
      galleryItem('arcana', '21-world-homeostasis.webp', 'World arcana biological illustration.', 'Arcana endpoint'),
    ],
  },
  'product/overview': {
    eyebrow: 'Trilogy chassis',
    summary: 'A product-level look at the trilogy promise, structure, use cases, and emotional trajectory.',
    heroImage: resolveImage('covers', 'book-cover-1-anamnesis-engine.webp'),
    heroAlt: 'Anamnesis Engine cover artwork.',
    highlights: [
      'Frames the trilogy as a three-phase healing journey.',
      'Clarifies the core value propositions for readers and practitioners.',
      'Captures the intended emotional progression from curiosity to integration.',
    ],
    assetFamilies: ['covers', 'brand-kit', 'anatomy'],
    gallery: [
      galleryItem('covers', 'book-cover-2-myocardial-chorus.webp', 'The Myocardial Chorus cover artwork.', 'Book two cover'),
      galleryItem('covers', 'book-cover-3-the-ripening.webp', 'The Ripening cover artwork.', 'Book three cover'),
      galleryItem('anatomy', 'anatomy-triangulation-engine.webp', 'Triangulation engine anatomy diagram.', 'Triangulation engine'),
    ],
  },
  'product/features': {
    eyebrow: 'Feature stack',
    summary:
      'The mechanisms, reader benefits, and concrete differentiators that make the trilogy feel engineered instead of merely atmospheric.',
    heroImage: resolveImage('anatomy', 'anatomy-triangulation-engine.webp'),
    heroAlt: 'Triangulation engine diagram from the Somatic Canticles visual system.',
    highlights: [
      'Breaks the narrative system into functional, emotional, and symbolic value.',
      'Connects story mechanics to concrete neuroscience and somatic concepts.',
      'Positions the trilogy as a designed experience rather than a generic lore deck.',
    ],
    assetFamilies: ['anatomy', 'arcana', 'covers'],
    gallery: [
      galleryItem('anatomy', 'anatomy-somatic-mapping.webp', 'Somatic mapping system diagram.', 'Somatic mapping'),
      galleryItem('anatomy', 'anatomy-vagal-nerve.webp', 'Vagal nerve anatomy diagram.', 'Vagal system'),
      galleryItem('arcana', '07-chariot-cardiac-coherence.webp', 'Chariot arcana biological illustration.', 'Cardiac coherence arcana'),
    ],
  },
  'product/positioning': {
    eyebrow: 'Market angle',
    summary:
      'The exact wedge Somatic Canticles occupies between hard SF, trauma literature, and visionary mysticism.',
    heroImage: resolveImage('covers', 'book-cover-2-myocardial-chorus.webp'),
    heroAlt: 'The Myocardial Chorus cover artwork.',
    highlights: [
      'Explains the high-rigor, high-embodiment, transformational-arc quadrant.',
      'Benchmarks the trilogy against Watts, Egan, Chiang, and van der Kolk.',
      'Provides the clearest one-sentence articulation of the project’s market position.',
    ],
    assetFamilies: ['covers', 'logos', 'brand-kit'],
    gallery: [
      galleryItem('covers', 'book-cover-3-the-ripening.webp', 'The Ripening cover artwork.', 'Final arc cover'),
      galleryItem('logos', 'logo-wax-seal-triple.webp', 'Triple wax seal logo variant.', 'Wax seal system'),
      galleryItem('brand-kit', 'brand-kit-bento-grid.webp', 'Brand kit composition board.', 'Brand board'),
    ],
  },
  'brand/voice-tone': {
    eyebrow: 'Voice system',
    summary:
      'How Somatic Canticles speaks: rigorous, embodied, and symbolically exact without drifting into generic mystic copy.',
    heroImage: resolveImage('logos', 'logo-wax-seal-triple.webp'),
    heroAlt: 'Triple wax seal logo treatment.',
    highlights: [
      'Defines voice traits, banned language, and preferred rhetorical patterns.',
      'Keeps the brand from slipping into startup filler or vague spirituality.',
      'Turns the archive into a coherent authored voice rather than disconnected docs.',
    ],
    assetFamilies: ['logos', 'arcana', 'brand-kit'],
    gallery: [
      galleryItem('logos', 'logo-glass-gradient.webp', 'Gradient glass sigil logo.', 'Glass sigil'),
      galleryItem('logos', 'logo-wax-seal-broken.webp', 'Broken wax seal logo.', 'Broken seal'),
      galleryItem('arcana', '00-fool-stem-cell.webp', 'Fool arcana stem cell illustration.', 'Origin image'),
    ],
  },
  'brand/visual-identity': {
    eyebrow: 'Visual doctrine',
    summary:
      'The palette, typography, symbolism, and image rules that define Somatic Canticles as clinical mysticism.',
    heroImage: resolveImage('brand-kit', 'brand-kit-bento-grid.webp'),
    heroAlt: 'Somatic Canticles visual identity board.',
    highlights: [
      'Codifies the trilogy’s clinical mysticism look and feel.',
      'Documents palette, typography, logo usage, and graphic system rules.',
      'Provides the visual bridge between neuroscience precision and sacred imagery.',
    ],
    assetFamilies: ['brand-kit', 'logos', 'covers'],
    gallery: [
      galleryItem('logos', 'logo-glass-classic.webp', 'Classic glass sigil logo.', 'Primary logo'),
      galleryItem('covers', 'book-cover-1-anamnesis-engine.webp', 'Anamnesis Engine cover.', 'Cover application'),
      galleryItem('anatomy', 'anatomy-khaloree-field-architecture.webp', 'Khaloree field architecture diagram.', 'System visual'),
    ],
  },
  'audience/primary-persona': {
    eyebrow: 'Primary reader',
    summary:
      'The Philosopher-Healer archetype, their media diet, frustrations, decision criteria, and the language that resonates with them.',
    heroImage: resolveImage('arcana', '02-high-priestess-pineal.webp'),
    heroAlt: 'High Priestess arcana illustration associated with pineal symbolism.',
    highlights: [
      'Describes the hybrid reader who wants both neuroscience and mysticism handled seriously.',
      'Captures purchase triggers, pain points, and social proof requirements.',
      'Turns audience strategy into a concrete operator brief for brand and launch decisions.',
    ],
    assetFamilies: ['arcana', 'anatomy', 'covers'],
    gallery: [
      galleryItem('covers', 'book-cover-1-anamnesis-engine.webp', 'Anamnesis Engine cover artwork.', 'Reader-facing cover'),
      galleryItem('anatomy', 'anatomy-neural-dendrites.webp', 'Neural dendrites anatomy image.', 'Embodied cognition'),
      galleryItem('arcana', '07-chariot-cardiac-coherence.webp', 'Chariot arcana cardiac coherence artwork.', 'Embodiment cue'),
    ],
  },
  'market/competitive-landscape': {
    eyebrow: 'Competitive field',
    summary:
      'Where the trilogy sits relative to adjacent authors, adjacent categories, and the narrative gap it intends to occupy.',
    heroImage: resolveImage('anatomy', 'anatomy-severance-pathways.webp'),
    heroAlt: 'Severance pathways anatomy illustration.',
    highlights: [
      'Maps comparable works and clarifies what Somatic Canticles uniquely combines.',
      'Turns competition into a strategic framing tool instead of a generic comparison list.',
      'Helps the archive explain why the project matters now.',
    ],
    assetFamilies: ['anatomy', 'arcana', 'logos'],
    gallery: [
      galleryItem('covers', 'book-cover-3-the-ripening.webp', 'The Ripening cover artwork.', 'Endgame cover'),
      galleryItem('logos', 'logo-wax-seal-broken.webp', 'Broken wax seal logo variant.', 'Fracture motif'),
      galleryItem('anatomy', 'anatomy-heart-brain-axis.webp', 'Heart-brain axis anatomy image.', 'Somatic proof'),
    ],
  },
  'market/niche-validation': {
    eyebrow: 'Viability scorecard',
    summary:
      'The practical readout of pain intensity, purchasing power, competition gap, and go-to-market confidence.',
    heroImage: resolveImage('anatomy', 'anatomy-heart-brain-axis.webp'),
    heroAlt: 'Heart-brain axis diagram used as a market proof visual.',
    highlights: [
      'Quantifies the niche case with an 85 percent viability score.',
      'Names the specific market tensions the trilogy resolves better than adjacent works.',
      'Provides a concrete launch thesis rather than abstract optimism.',
    ],
    assetFamilies: ['brand-kit', 'anatomy', 'arcana'],
    gallery: [
      galleryItem('brand-kit', 'brand-kit-bento-grid.webp', 'Brand board collage.', 'Brand evidence'),
      galleryItem('anatomy', 'anatomy-vagal-nerve.webp', 'Vagal nerve anatomy image.', 'Biology cue'),
      galleryItem('arcana', '16-tower-severance.webp', 'Tower arcana severance illustration.', 'Disruption motif'),
    ],
  },
};

const totalMappedAssets = assetFamilyOrder.reduce((sum, family) => sum + visualAssetsByFamily[family].length, 0);

export const archiveStats = [
  { label: 'Core dossiers', value: String(Object.keys(docMeta).length) },
  { label: 'Brandmint assets', value: String(totalMappedAssets) },
  { label: 'API calls', value: String(brandmintRunStats.totalApiCalls) },
] as const;

export const primaryReadingPath = [
  'index',
  'product/overview',
  'brand/visual-identity',
  'audience/primary-persona',
  'market/niche-validation',
] as const;

export const visualAssetCatalog = assetFamilyOrder.flatMap((family) => visualAssetsByFamily[family]);

export function getCategoryMeta(category?: string) {
  return category ? categoryMeta[category] : undefined;
}

export function getAssetFamilyMeta(family?: string) {
  return family ? assetFamilyMeta[family as AssetFamilyId] : undefined;
}

export function getAssetFamilyAssets(family?: string) {
  return family ? visualAssetsByFamily[family as AssetFamilyId] ?? [] : [];
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
    const categoryRank =
      categoryOrder.indexOf((a.data.category ?? 'overview') as (typeof categoryOrder)[number]) -
      categoryOrder.indexOf((b.data.category ?? 'overview') as (typeof categoryOrder)[number]);

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
