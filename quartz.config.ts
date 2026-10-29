import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Configurazione Ufficiale Wiki Catania Calcio (1929–Oggi)
 * - Design System Magazine Editoriale (ispirato a No Football Colors & Sincro)
 * - Tipografia Self-Hosted: Big Shoulders Display (Condensed Display) + Plus Jakarta Sans
 * - Palette: #d11317 (Rosso), #0cb2d9 (Azzurro), Light #191919 su #f7f7f7, Dark #f7f7f7 su #191919, Oro #d29933
 * - Conformità UE: GDPR Cookie-less (analytics: null, fontOrigin: "local"), WCAG 2.1 AA / EAA
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Wiki Catania Calcio",
    pageTitleSuffix: " — Magazine & Archivio Storico (1929–Oggi)",
    enableSPA: true,
    enablePopovers: false,
    analytics: null, // 100% Cookie-less & Zero-Tracking (Conforme GDPR Reg. UE 2016/679)
    locale: "it-IT",
    baseUrl: "wikicataniacalcio.com",
    ignorePatterns: ["private", "templates", ".obsidian", "SCHEMA.md"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "local", // Self-hosted WOFF2 in /static/fonts/: zero trasferimento IP a Google Fonts (GDPR compliant)
      cdnCaching: false,
      typography: {
        header: "Big Shoulders Display",
        body: "Plus Jakarta Sans",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#f7f7f7", // Sfondo primario Light (Carta magazine off-white)
          lightgray: "#dcdcdc", // Bordi hair-line (1px) architettonici
          gray: "#666666", // Metadati secondari, didascalie (WCAG AA)
          darkgray: "#222222", // Corpo del testo editoriale ad altissima leggibilità
          dark: "#191919", // Inchiostro primario: titoli, bordi strutturali e icone (Contrasto 15.8:1 AAA)
          secondary: "#d11317", // Principale 1: Rosso Catania
          tertiary: "#0cb2d9", // Principale 2: Azzurro Catania
          highlight: "rgba(12, 178, 217, 0.10)", // Sfondo pillole [[wikilinks]] e tag
          textHighlight: "rgba(210, 153, 51, 0.28)", // Evidenziazione basata sul dettaglio #d29933
        },
        darkMode: {
          light: "#191919", // Sfondo primario Dark (Antracite profondo)
          lightgray: "#2e2e2e", // Bordi hair-line (1px) su sfondo scuro
          gray: "#a0a0a0", // Metadati secondari in Dark Mode (WCAG AA)
          darkgray: "#e4e4e4", // Corpo del testo corrente in Dark Mode
          dark: "#f7f7f7", // Titoli H1-H4, testo forte e bordi editoriali (Contrasto 15.8:1 AAA)
          secondary: "#d11317", // Principale 1: Rosso Catania
          tertiary: "#0cb2d9", // Principale 2: Azzurro Catania
          highlight: "rgba(12, 178, 217, 0.15)", // Sfondo pillole [[wikilinks]] in Dark Mode
          textHighlight: "rgba(210, 153, 51, 0.35)", // Evidenziazione basata sul dettaglio #d29933
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents({ maxDepth: 3 }),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      Plugin.CNAME(),
    ],
  },
}

export default config
