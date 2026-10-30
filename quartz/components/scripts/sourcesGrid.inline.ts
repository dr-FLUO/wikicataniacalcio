function setupSourcesAndLinksGrid() {
  const article = document.querySelector('article')
  if (!article) return
  if (article.querySelector('.nfc-sources-and-links-grid')) return

  const headings = Array.from(article.querySelectorAll('h2, h3'))
  let linksHeading: Element | null = null
  let sourcesHeading: Element | null = null

  for (const h of headings) {
    const text = h.textContent?.toLowerCase() || ''
    if (!linksHeading && (text.includes('collegament') || text.includes('voci correlat'))) {
      linksHeading = h
    } else if (!sourcesHeading && (text.includes('fonti') || text.includes('bibliografia'))) {
      sourcesHeading = h
    }
  }

  if (!linksHeading && !sourcesHeading) return

  function collectSectionNodes(heading: Element) {
    const nodes: Element[] = []
    let curr = heading.nextElementSibling
    while (curr && !['H1', 'H2', 'H3'].includes(curr.tagName) && !curr.classList.contains('rossazzurri-footer')) {
      const next = curr.nextElementSibling
      if (curr.tagName === 'HR') {
        curr.remove()
      } else {
        nodes.push(curr)
      }
      curr = next
    }
    return nodes
  }

  const linksNodes = linksHeading ? collectSectionNodes(linksHeading) : []
  const sourcesNodes = sourcesHeading ? collectSectionNodes(sourcesHeading) : []

  const referenceNode = linksHeading || sourcesHeading
  if (!referenceNode) return
  const parent = referenceNode.parentNode
  if (!parent) return

  const grid = document.createElement('div')
  grid.className = 'nfc-sources-and-links-grid'
  parent.insertBefore(grid, referenceNode)

  if (linksHeading) {
    const colLinks = document.createElement('div')
    colLinks.className = 'nfc-grid-column nfc-column-links'
    colLinks.appendChild(linksHeading)
    for (const node of linksNodes) {
      colLinks.appendChild(node)
    }
    grid.appendChild(colLinks)
  }

  if (sourcesHeading) {
    const colSources = document.createElement('div')
    colSources.className = 'nfc-grid-column nfc-column-sources'
    colSources.appendChild(sourcesHeading)
    for (const node of sourcesNodes) {
      colSources.appendChild(node)
    }
    grid.appendChild(colSources)
  }
}

document.addEventListener('nav', setupSourcesAndLinksGrid)
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupSourcesAndLinksGrid)
} else {
  setupSourcesAndLinksGrid()
}
