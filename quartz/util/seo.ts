import { Root, RootContent } from "hast"

const RUBRIC_LABELS: Record<string, string> = {
  "01-societa": "Società",
  "02-cronistoria": "Cronistoria",
  "03-tesserati": "Tesserati",
  "04-strutture": "Strutture",
  "05-identita-e-simboli": "Identità e Simboli",
  "06-tifoseria-e-cultura": "Tifoseria e Cultura",
  "07-media-e-comunicazione": "Media e Comunicazione",
  "08-settori-paralleli": "Vivaio e Women",
}

const PERSON_ENTITY_TYPES = new Set([
  "calciatore",
  "allenatore",
  "dirigente",
  "presidente",
  "biografia_giornalista",
  "giornalista",
  "biografia_ultras",
  "ultras_biography",
])

export function isNoIndexPage(slug?: string, fm?: Record<string, any>): boolean {
  if (!slug) return false
  if (
    slug === "404" ||
    slug === "tags" ||
    slug.startsWith("tags/") ||
    slug === "segnala-correzione"
  ) {
    return true
  }
  if (fm?.noindex === true) {
    return true
  }
  if (
    fm?.entity_type === "calciatore" &&
    fm?.current_squad !== true &&
    !slug.includes("/rosa-attuale/")
  ) {
    const apps = fm.total_appearances ?? fm.catania_appearances ?? fm.league_appearances
    if (apps !== undefined && apps !== null && apps !== "" && Number(apps) === 0) {
      return true
    }
  }
  return false
}

export function stripRedundantBodyH1(tree: Root): Root {
  let seenFirstElement = false
  const newChildren: RootContent[] = []

  for (const child of tree.children) {
    if (child.type === "element") {
      if (!seenFirstElement) {
        seenFirstElement = true
        if (child.tagName === "h1") {
          continue
        }
        newChildren.push(child)
      } else if (child.tagName === "h1") {
        newChildren.push({ ...child, tagName: "h2" })
      } else {
        newChildren.push(child)
      }
    } else {
      newChildren.push(child)
    }
  }

  return { ...tree, children: newChildren }
}

export function buildPageJsonLd(opts: {
  slug: string
  baseUrl: string
  title: string
  description: string
  socialUrl: string
  imageUrl: string
  fm?: Record<string, any>
  modifiedIso?: string
}): Record<string, any> {
  const { slug, baseUrl, title, description, socialUrl, imageUrl, fm, modifiedIso } = opts
  const siteRoot = `https://${baseUrl}/`
  const websiteId = `https://${baseUrl}/#website`
  const orgId = `https://${baseUrl}/#organization`

  if (slug === "index") {
    return {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "WebSite",
          "@id": websiteId,
          url: siteRoot,
          name: "Wiki Catania Calcio",
          alternateName: ["Wiki Calcio Catania", "Enciclopedia Storica Calcio Catania"],
          description,
          inLanguage: "it-IT",
          publisher: { "@id": orgId },
        },
        {
          "@type": "Organization",
          "@id": orgId,
          name: "Wiki Catania Calcio",
          url: siteRoot,
          logo: {
            "@type": "ImageObject",
            url: `https://${baseUrl}/static/icon.png`,
            width: 512,
            height: 512,
          },
        },
      ],
    }
  }

  const segs = slug.split("/").filter(Boolean)
  const seg0 = segs[0] ?? ""
  const rubricLabel = RUBRIC_LABELS[seg0]
  const cleanName =
    String(fm?.title ?? title)
      .split(" — ")[0]
      .split(" | ")[0]
      .trim() || title

  const itemListElement: Record<string, any>[] = [
    {
      "@type": "ListItem",
      position: 1,
      name: "Home",
      item: siteRoot,
    },
  ]

  if (rubricLabel) {
    if (slug === `${seg0}/index`) {
      itemListElement.push({
        "@type": "ListItem",
        position: 2,
        name: cleanName,
        item: socialUrl,
      })
    } else {
      itemListElement.push({
        "@type": "ListItem",
        position: 2,
        name: rubricLabel,
        item: `https://${baseUrl}/${seg0}/`,
      })
      itemListElement.push({
        "@type": "ListItem",
        position: 3,
        name: cleanName,
        item: socialUrl,
      })
    }
  } else {
    itemListElement.push({
      "@type": "ListItem",
      position: 2,
      name: cleanName,
      item: socialUrl,
    })
  }

  const breadcrumbNode: Record<string, any> = {
    "@type": "BreadcrumbList",
    itemListElement,
  }

  let mainEntity: Record<string, any>
  if (slug.endsWith("/index")) {
    mainEntity = {
      "@type": "CollectionPage",
      name: title,
      description,
      url: socialUrl,
      inLanguage: "it-IT",
      isPartOf: { "@id": websiteId },
    }
  } else {
    mainEntity = {
      "@type": "Article",
      headline: title.slice(0, 110),
      description,
      url: socialUrl,
      mainEntityOfPage: {
        "@type": "WebPage",
        "@id": socialUrl,
      },
      image: [imageUrl],
      inLanguage: "it-IT",
      author: {
        "@type": "Organization",
        name: "Redazione Wiki Catania Calcio",
        url: siteRoot,
      },
      publisher: {
        "@type": "Organization",
        name: "Wiki Catania Calcio",
        logo: {
          "@type": "ImageObject",
          url: `https://${baseUrl}/static/icon.png`,
        },
      },
      ...(modifiedIso ? { dateModified: modifiedIso } : {}),
    }

    const entityType = fm?.entity_type ? String(fm.entity_type) : ""
    if (entityType && PERSON_ENTITY_TYPES.has(entityType)) {
      const personName = String(
        fm?.full_name ?? title.split(" — ")[0].split(" | ")[0],
      ).trim()
      mainEntity.about = {
        "@type": "Person",
        name: personName,
        ...(fm?.role ? { jobTitle: String(fm.role) } : {}),
      }
    }
  }

  return {
    "@context": "https://schema.org",
    "@graph": [breadcrumbNode, mainEntity],
  }
}
