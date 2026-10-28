import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative, FullSlug } from "../util/path"

function cleanWikilink(val: unknown): string {
  if (val === null || val === undefined) return ""
  if (Array.isArray(val)) {
    return val.map((item) => cleanWikilink(item)).join(", ")
  }
  const str = String(val)
  return str.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, "$2").replace(/\[\[([^\]]+)\]\]/g, "$1")
}

const ENTITY_LABELS: Record<string, string> = {
  home_portal: "Copertina Magazine",
  era_societaria: "Dossier Societario",
  corporate_era: "Era Societaria",
  dirigente: "Profilo Dirigenziale",
  president: "Profilo Presidenziale",
  stagione_agonistica: "Annale Stagione",
  season: "Annale Stagione",
  tabellino_gara: "Tabellino Storico",
  match: "Tabellino Storico",
  archivio_precedenti: "Bilancio Precedenti",
  head_to_head: "Bilancio Precedenti",
  calciatore: "Monografia Calciatore",
  player: "Monografia Calciatore",
  allenatore: "Monografia Allenatore",
  coach: "Monografia Allenatore",
  impianto_sportivo: "Architettura & Stadi",
  stadium: "Architettura & Stadi",
  kit_storico: "Estetica & Araldica",
  heraldry_kits: "Estetica & Araldica",
  vicenda_legale: "Dossier Giurisprudenziale",
  legal_dossier: "Dossier Giurisprudenziale",
  gruppo_ultras: "Etnografia Ultras",
  ultras_group: "Etnografia Ultras",
  relazione_tifo: "Diplomazia Tifoseria",
  ultras_twinnings: "Gemellaggio Storico",
  ultras_rivalry: "Rivalità Storica",
  evento_tifo: "Evento Storico Tifoseria",
  ultras_event: "Evento Storico Tifoseria",
  biografia_tifo: "Biografia Curva",
  ultras_biography: "Biografia Curva",
  legal_compliance: "Conformità Normativa UE",
  feedback_portal: "Redazione & Fact-Checking",
}

export default (() => {
  const RossazzurriInfobox: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const fm = fileData.frontmatter
    if (!fm || fm.slug === "index" || fileData.slug === "index") {
      return null
    }

    const entityType = String(fm.entity_type ?? "voce_wiki")
    const entityLabel = ENTITY_LABELS[entityType] ?? "Scheda Redazionale"
    const isVerified = fm.status === "verified"

    const rows: Array<{ label: string; value: string }> = []

    const addRow = (label: string, rawVal: unknown) => {
      if (rawVal !== undefined && rawVal !== null && rawVal !== "") {
        const cleaned = cleanWikilink(rawVal)
        if (cleaned.trim().length > 0) {
          rows.push({ label, value: cleaned })
        }
      }
    }

    // Campi biografici, stagionali, societari, giudiziari e ultras
    addRow("Nome Completo", fm.full_name)
    addRow("Ruolo", fm.role)
    addRow("Militanza Catania", fm.catania_period ?? fm.period ?? fm.years_active)
    if (fm.catania_appearances !== undefined) {
      addRow(
        "Presenze Catania",
        fm.catania_goals !== undefined
          ? `${fm.catania_appearances} gare (${fm.catania_goals} reti)`
          : `${fm.catania_appearances} gare`,
      )
    }
    addRow("Stagione", fm.season_label ?? fm.season ?? fm.season_ref)
    addRow(
      "Data / Periodo",
      fm.match_date ??
        fm.date ??
        (fm.date_start && fm.date_end ? `${fm.date_start} → ${fm.date_end}` : fm.date_start),
    )
    addRow("Fondazione", fm.foundation_year ?? fm.founded_year)
    addRow("Ragione Sociale", fm.club_entity ?? fm.official_name)
    addRow("Matricola FIGC", fm.figc_matricola)
    addRow("Competizione", fm.division ?? fm.competition)
    addRow("Turno", fm.matchday)
    addRow(
      "Piazzamento",
      fm.final_position
        ? String(fm.final_position).includes("º") || String(fm.final_position).includes("°")
          ? String(fm.final_position)
          : `${fm.final_position}º posto`
        : undefined,
    )
    if (fm.matches_played !== undefined) {
      addRow("Bilancio Gare", `${fm.matches_played} G (${fm.wins}V · ${fm.draws}N · ${fm.losses}P)`)
    }
    if (fm.goals_for !== undefined && fm.goals_against !== undefined) {
      addRow("Reti (GF / GS)", `${fm.goals_for} fatte / ${fm.goals_against} subite`)
    }
    if (fm.points_final !== undefined || fm.points !== undefined) {
      const pts = fm.points_final ?? fm.points
      const pen = Number(fm.points_penalty ?? fm.penalty_points ?? 0)
      addRow(
        "Punti Ufficiali",
        pen > 0 ? `${pts} pt (-${pen} pen.)` : `${pts} pt`,
      )
    }
    if (fm.score_home !== undefined && fm.score_away !== undefined) {
      addRow("Risultato", `${fm.score_home} - ${fm.score_away}`)
    } else if (fm.score !== undefined) {
      addRow("Risultato", fm.score)
    }
    addRow("Presidente", fm.president_ref ?? fm.president)
    addRow("Allenatore", fm.coach_refs ?? fm.coaches ?? fm.home_coach)
    addRow(
      "Capocannoniere",
      fm.top_scorer_ref
        ? `${cleanWikilink(fm.top_scorer_ref)} (${fm.top_scorer_goals} reti)`
        : fm.top_scorer,
    )
    addRow("Impianto", fm.stadium_ref ?? fm.venue ?? fm.stadium)
    addRow(
      "Spettatori",
      fm.attendance
        ? typeof fm.attendance === "number"
          ? fm.attendance.toLocaleString("it-IT")
          : String(fm.attendance)
        : undefined,
    )
    addRow("Arbitro", fm.referee)
    addRow("Fondatore", fm.founder)
    addRow("Settore / Curva", fm.stadium_sector ?? fm.sector)
    addRow("Organi Giudicanti", fm.court_bodies)
    addRow("Esito Giuridico", fm.legal_outcome ?? fm.verdict_summary)

    const sourcesCount = Array.isArray(fm.sources) ? fm.sources.length : 0
    if (sourcesCount > 0) {
      addRow(
        "Fonti Certificate",
        `${sourcesCount} ${sourcesCount === 1 ? "fonte bibliografica" : "fonti bibliografiche"}`,
      )
    }

    const currentSlug = (fileData.slug ?? "index") as FullSlug
    const reportHref = resolveRelative(currentSlug, "segnala-correzione" as FullSlug)

    return (
      <aside
        class="rossazzurri-infobox"
        role="region"
        aria-label="Scheda tecnica della voce"
      >
        <div class="infobox-header">
          <span class="infobox-category">{entityLabel}</span>
          {isVerified && (
            <span class="verified-badge" title="Dati e fonti verificati dalla redazione">
              ✓ VERIFICATO
            </span>
          )}
        </div>
        <div class="infobox-title">{fm.title}</div>
        {rows.length > 0 && (
          <dl class="infobox-list">
            {rows.map((r) => (
              <div class="infobox-row">
                <dt class="label">{r.label}</dt>
                <dd class="value">{r.value}</dd>
              </div>
            ))}
          </dl>
        )}
        <div class="infobox-footer">
          <a
            href={`${reportHref}?voce=${encodeURIComponent(String(fm.slug ?? fileData.slug ?? ""))}`}
            class="report-correction-btn"
            aria-label={`Segnala un errore o proponi un aggiornamento con fonte per ${fm.title}`}
          >
            ✎ SEGNALA CORREZIONE O FONTE
          </a>
        </div>
      </aside>
    )
  }

  return RossazzurriInfobox
}) satisfies QuartzComponentConstructor
